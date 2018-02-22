from flask import render_template, Blueprint, redirect, url_for, request
from models import db, User
from forms import RegisterForm, LoginForm
from flask_login import login_user, logout_user, login_required


control_blueprint = Blueprint('manage', __name__, template_folder='templates/control_template')


@control_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).one()
        login_user(user, remember=form.remember.data)

        return redirect(url_for('blog.home'))
    else:
        print(form.username.errors)
    return render_template('control_template/login.html', form=form)


@login_required
@control_blueprint.route('/logout', methods=['GET', 'POST'])
def logout():
    logout_user()
    return redirect(url_for('blog.home'))


@control_blueprint.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            print(form.username.data, form.password.data)
            new_user = User(username=form.username.data, password=User.set_password(form.password.data))
            db.session.add(new_user)
            db.session.commit()
            return redirect(url_for('manage.login'))

    return render_template('control_template/register.html', form=form)