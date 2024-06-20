from flask import render_template, redirect, session, current_app, request, flash, url_for
from app.authorization.forms import *
from app.models import *
from flask_mail import Message
from .. import mail
from .. authorization import authorization
from flask_login import login_user, logout_user, current_user, login_required


@login_required
@authorization.route('/signout')
def sign_out():
    '''
    Выход из системы и очистка сессии
    '''
    logout_user()
    session['name'] = None
    return redirect('/')


@authorization.route('/signin', methods=['GET', 'POST'])
def sign_in():
    '''
    Авторизация
    Метод будет работать для неавторизированных пользователей.
    Ищет пользователя в бд и сверяет пароли.
    В next запоминает следующую страницу.
    :return: либо темплейт авторизации, либо главную страницу.
    '''
    if not current_user.is_authenticated:
        form = AuthorizationForm()
        formTittle = "Sign In"
        if form.validate_on_submit():
            user = User.query.filter_by(email=form.email.data).first()
            if user is not None and user.password_verify(form.password.data):
                login_user(user)
                next = request.args.get('next')
                session['name'] = user.email
                if next is None or not next.startswith('/'):
                    next = url_for('main.index')
                return redirect(next)
            flash('Invalid username or password')
        return render_template('formTemplates/baseFormTemplate.html', form=form, formTittle=formTittle)
    return redirect('/')


@authorization.route('/signup', methods=['GET', 'POST'])
def sign_up():
    '''
    Регистрация
    Метод будет работать для неавторизированных пользователей.
    Создает пользователя, с дефолтным значением роли - работник.
    Отправляет письмо с подтверждением.
    '''
    if not current_user.is_authenticated:
        form = RegistrationForm()
        formTittle = "Sign Up"
        if form.validate_on_submit():
            user = User()
            user.name = form.name.data
            user.email = form.email.data
            user.password = form.password.data
            user.city = form.city.data
            user.experience = form.experience.data
            if form.is_employer.data:
                user.role = Role.Employer
            db.session.add(user)
            db.session.commit()
            token = user.generate_confirmation_token()
            confirm(form.name.data, form.email.data, token.decode('utf-8'))
            return redirect('/')
        return render_template('formTemplates/baseFormTemplate.html', form=form, formTittle=formTittle)
    return redirect('/')


def confirm(name, email, token):
    '''
    :param name: Имя получателя
    :param email: Почта получателя
    :param token: Токен подтверждения
    Вызывает метод send_mail
    '''
    send_mail(email, 'Congratz', 'mailTemplates/welcomeMailTemplate', name=name, token=token)


def send_mail(to, subject, template, **kwargs):
    '''
    :param to: Кому письмо
    :param subject: Тема письма
    :param template: Тело письма
    :param kwargs: Переменные в письмо
    Отправляет письмо
    '''
    msg = Message(subject, sender=current_app.config['MAIL_USERNAME'],
                  recipients=[to])
    msg.body = render_template(template+'.txt', **kwargs)
    mail.send(msg)


@authorization.route('/check/<token>')
@login_required
def check_token(token):
    '''
    :param token: уникальный токен для каждого пользователя, чтобы подтвердить аккаунт
    Метод Вызывается после тапа по ссылке на почте, изменяет подтвержденность аккаунта в бд.
    '''
    if current_user.confirmed:
        return redirect('/')
    if current_user.confirm(token):
        db.session.commit()
        flash('Подтверждение прошло успешно!')
    else:
        flash('Подтверждение не удалось')
    return redirect(url_for('main.index'))
