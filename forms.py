from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, validators
from wtforms.validators import DataRequired, Length
from models import User


class LoginForm(FlaskForm):
    username = StringField('username', [DataRequired(), Length(max=255)])
    password = PasswordField('password', [DataRequired()])
    remember = BooleanField('Remember me')

    def validate(self):
        check_validate = super(LoginForm, self).validate()

        if not check_validate:
            return False
        user = User.query.filter_by(username=self.username.data).first()
        if not user:
            self.username.errors.append('用户不存在')
            return False
        if not user.check_password(self.password.data):
            self.username.errors.append('密码错误')
            return False
        return True


class RegisterForm(FlaskForm):
    username = StringField('username', [DataRequired(), Length(max=255)])
    password = PasswordField('password', [DataRequired(), Length(min=6)])
    check_password = PasswordField('password', [DataRequired()])

    def validate(self):
        check_validate = super(RegisterForm, self).validate()

        if not check_validate:
            return False
        user = User.query.filter_by(username=self.username.data).first()
        if user:
            self.username.errors.append('用户已存在')
            return False
        if self.password.data != self.check_password.data:
            self.password.errors.append('两次输入密码不一致')
            return False
        return True


class CommentForm(FlaskForm):

    name = StringField('Name', validators=[DataRequired(), Length(max=255)])
    text = StringField('Comment', validators=[DataRequired()])
