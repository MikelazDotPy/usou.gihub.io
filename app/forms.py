from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField, SelectMultipleField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
from app.models import User


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')
    submit2 = SubmitField('Sign In', validators=[DataRequired()])


class SelectForm(FlaskForm):
    schedule_list = SelectField("Расписание", choices=[], validators=[DataRequired()])
    student_list = SelectField("Ученики", choices=[], validators=[DataRequired()])
    student_list3 = SelectField("Ученики", choices=[], validators=[DataRequired()])
    school_list = SelectField("Школы", choices=[], validators=[DataRequired()])
    class_list = SelectField("Классы", choices=[], validators=[DataRequired()])
    group_list = SelectField("Group", choices=[], validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    teacher_list = SelectField("Учителя", choices=[], validators=[DataRequired()])
    teacher_list2 = SelectField("Учителя", choices=[], validators=[DataRequired()])
    teacher_list3 = SelectField("Учителя", choices=[], validators=[DataRequired()])
    name = StringField("Имя", validators=[DataRequired()])
    email2 = StringField('Email', validators=[DataRequired(), Email()])
    subject = StringField("Предмет", validators=[DataRequired()])
    subject2 = StringField("Предмет", validators=[DataRequired()])
    surname = StringField("Фамилия", validators=[DataRequired()])
    patronymic = StringField("Отчество", validators=[DataRequired()])
    password = StringField("Пароль", validators=[DataRequired()])
    sex = SelectField("Group", choices=[("М", "М"), ("Ж", "Ж")], validators=[DataRequired()])
    student_list2 = SelectField("Ученики", choices=[], validators=[DataRequired()])
    class_list2 = SelectField("Классы", choices=[], validators=[DataRequired()])
    name2 = StringField("Имя", validators=[DataRequired()])
    surname2 = StringField("Фамилия", validators=[DataRequired()])
    patronymic2 = StringField("Отчество", validators=[DataRequired()])
    password2 = StringField("Пароль", validators=[DataRequired()])
    sex2 = SelectField("Group", choices=[("М", "М"), ("Ж", "Ж")], validators=[DataRequired()])
    submit = SubmitField('Далее', validators=[DataRequired()])
    submit2 = SubmitField('Добавить', validators=[DataRequired()])
    submit3 = SubmitField('Добавить', validators=[DataRequired()])
    a1 = SelectMultipleField("Group", choices=[("М", "М"), ("Ж", "Ж")], validators=[DataRequired()])


class ScheduleForm(FlaskForm):
    monday1 = SelectField("Понедельник1", choices=[], validators=[DataRequired()])
    monday2 = SelectField("Понедельник1", choices=[], validators=[DataRequired()])
    monday3 = SelectField("Понедельник1", choices=[], validators=[DataRequired()])
    monday4 = SelectField("Понедельник1", choices=[], validators=[DataRequired()])
    monday5 = SelectField("Понедельник1", choices=[], validators=[DataRequired()])
    monday6 = SelectField("Понедельник1", choices=[], validators=[DataRequired()])
    tuesday1 = SelectField("Вторник", choices=[], validators=[DataRequired()])
    tuesday2 = SelectField("Вторник", choices=[], validators=[DataRequired()])
    tuesday3 = SelectField("Вторник", choices=[], validators=[DataRequired()])
    tuesday4 = SelectField("Вторник", choices=[], validators=[DataRequired()])
    tuesday5 = SelectField("Вторник", choices=[], validators=[DataRequired()])
    tuesday6 = SelectField("Вторник", choices=[], validators=[DataRequired()])
    wednesday1 = SelectField("Среда", choices=[], validators=[DataRequired()])
    wednesday2 = SelectField("Среда", choices=[], validators=[DataRequired()])
    wednesday3 = SelectField("Среда", choices=[], validators=[DataRequired()])
    wednesday4 = SelectField("Среда", choices=[], validators=[DataRequired()])
    wednesday5 = SelectField("Среда", choices=[], validators=[DataRequired()])
    wednesday6 = SelectField("Среда", choices=[], validators=[DataRequired()])
    thursday1 = SelectField("Четверг", choices=[], validators=[DataRequired()])
    thursday2 = SelectField("Четверг", choices=[], validators=[DataRequired()])
    thursday3 = SelectField("Четверг", choices=[], validators=[DataRequired()])
    thursday4 = SelectField("Четверг", choices=[], validators=[DataRequired()])
    thursday5 = SelectField("Четверг", choices=[], validators=[DataRequired()])
    thursday6 = SelectField("Четверг", choices=[], validators=[DataRequired()])
    friday1 = SelectField("Пятница", choices=[], validators=[DataRequired()])
    friday2 = SelectField("Пятница", choices=[], validators=[DataRequired()])
    friday3 = SelectField("Пятница", choices=[], validators=[DataRequired()])
    friday4 = SelectField("Пятница", choices=[], validators=[DataRequired()])
    friday5 = SelectField("Пятница", choices=[], validators=[DataRequired()])
    friday6 = SelectField("Пятница", choices=[], validators=[DataRequired()])
    saturday1 = SelectField("Суббота", choices=[], validators=[DataRequired()])
    saturday2 = SelectField("Суббота", choices=[], validators=[DataRequired()])
    saturday3 = SelectField("Суббота", choices=[], validators=[DataRequired()])
    saturday4 = SelectField("Суббота", choices=[], validators=[DataRequired()])
    saturday5 = SelectField("Суббота", choices=[], validators=[DataRequired()])
    saturday6 = SelectField("Суббота", choices=[], validators=[DataRequired()])

    submit = SubmitField('Добавить', validators=[DataRequired()])


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')


class EmailForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    email2 = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Далее', validators=[DataRequired()])

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')