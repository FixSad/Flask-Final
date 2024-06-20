from flask import render_template, session, redirect
from . import main
from flask_login import login_required, current_user
from app.models import *
import random
from app.main.forms import *
from app.decorators import role_required


@main.route('/')
def index():
    '''
    Главная страница сайта
    Ищет авторизированного пользователя
    передает рандомное число от 1 до 6 для генерации аватарки
    '''
    user = User.query.filter_by(email=session.get('name')).first()
    return render_template('agonyTemplates/main.html', username=session.get('name'),
                           user=user, rand=random.randint(1, 6))


@main.route('/403error')
@main.errorhandler(403)
def error():
    '''
    Обработчик ошибки 403
    '''
    return render_template('errorTemplates/403.html'), 403


@main.route('/projects')
@login_required
def projects():
    '''
    Для пользователей в системе (login_required)
    Передает все проекты пользователя и проверяет подтвержден ли у него аккаунт
    '''
    user = User.query.filter_by(email=session.get('name')).first()
    print(user.confirmed)
    return render_template('agonyTemplates/projects.html', projects=user.projects,
                           isVerify=user.confirmed)


@main.route('/addProject', methods=['GET', 'POST'])
@login_required
@role_required(Role.Employee)
def add_project_page():
    '''
    Только для пользователей с ролью Employee (role_required)
    Для пользователей в системе (login_required)
    Создает и добавляет новый проект текущему пользователю
    :return: при успехе: перенаправляет на projects, при неудаче прогружает projectFormTemplate
    '''
    form = ProjectForm()
    if form.validate_on_submit():
        project = Project(name=form.name.data,
                          description=form.description.data,
                          features=form.features.data,
                          prog_languages=form.prog_languages.data,
                          link=form.link.data,
                          user_id=current_user.get_id())
        db.session.add(project)
        db.session.commit()
        return redirect('/projects')
    return render_template('formTemplates/projectFormTemplate.html', form=form)


@main.route('/companies')
@login_required
def companies():
    '''
    Для пользователей в системе (login_required)
    Передаем все компании и роль пользователя для отображения
    '''
    user = User.query.filter_by(email=session.get('name')).first()
    comps = Company.query.all()
    return render_template('agonyTemplates/companies.html', companies=comps, role=user.role.name)


@main.route('/addCompany', methods=['GET', 'POST'])
@role_required(Role.Employer)
@login_required
def add_company():
    '''
    Только для пользователей с ролью Employer (role_required)
    Для пользователей в системе (login_required)
    Создает и добавляет компанию к текущему пользователю
    :return: при успехе: перенаправляет на companies, при неудаче прогружает companyFormTemplate
    '''
    form = CompanyForm()
    if form.validate_on_submit():
        company = Company(name=form.name.data,
                          description=form.description.data,
                          user_id=current_user.get_id())
        db.session.add(company)
        db.session.commit()
        return redirect('/companies')
    return render_template('formTemplates/companyFormTemplate.html', form=form)


@main.route('/delete/<id>')
@role_required(Role.Admin)
@login_required
def delete_company(id):
    '''
    Только для пользователей с ролью Admin (role_required)
    Для пользователей в системе (login_required)
    Удаляет компанию, которую захотел удалить админ
    :param id: идентификатор компании
    :return: при успехе: перенаправляет на companies, при неудаче выводит сообщение
    '''
    try:
        x = Company.query.filter_by(id=id).first()
        db.session.delete(x)
        db.session.commit()
    except Exception:
        return 'Something went wrong with your db...'
    return redirect('/companies')
