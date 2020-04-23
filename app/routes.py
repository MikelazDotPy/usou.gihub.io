from flask import render_template, flash, redirect, url_for, request
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.urls import url_parse
from app.tokenn import generate_confirmation_token, confirm_token
from app.mail import send_email
import datetime
from app import app, db
from app.forms import LoginForm, RegistrationForm, EmailForm, SelectForm, ScheduleForm
from app.models import User, Students
import json
from app import DB
from flask import send_from_directory
import os


@app.route('/base')
def base():
    return render_template("base.html")


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='favicon.ico')


@app.route('/')
@login_required
def index():
    if current_user.super_admin:
        return redirect(url_for('hello_admin'))
    elif current_user.admin:
        return redirect(url_for('adm_school'))
    else:
        return redirect(url_for("tst"))
    return render_template("hh.html")


"""
@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    #if form.validate_on_submit():
    if request.method == "POST":
        user = User.query.filter_by(id=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)
"""


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    #if form.validate_on_submit():
    if request.method == "POST":
        user = User.query.filter_by(id=form.username.data).first()
        if user is not None and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            next_page = request.args.get('next')
            if not next_page or url_parse(next_page).netloc != '':
                next_page = url_for('index')
            return redirect(next_page)
        user = User.query.filter_by(email=form.username.data).first()
        if user is not None and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            next_page = request.args.get('next')
            if not next_page or url_parse(next_page).netloc != '':
                next_page = url_for('index')
            return redirect(next_page)

        flash('Invalid username or password')
        return redirect(url_for('login'))
    return render_template('login.html', title='Sign In', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route("/change_pass", methods=["GET", "POST"])
def change_pass():
    form = SelectForm()
    if form.submit.data:
        token = generate_confirmation_token(form.email.data)
        confirm_url = url_for('confirm_pass', token=token, _external=True)
        html = render_template('change_pass.html', confirm_url=confirm_url)
        subject = "Сылка для изменения пароля"
        send_email(form.email.data, subject, html)
        return "На ваш email отправлено письмо"
    return render_template('email_pass.html', title='Email', form=form)


@app.route('/confirm_pass/<token>', methods=["GET", "POST"])
def confirm_pass(token):
    form = SelectForm()
    try:
        email = confirm_token(token)
    except:
        flash('The confirmation link is invalid or has expired.', 'danger')
    user = User.query.filter_by(email=email).first_or_404()
    if form.submit.data:
        user.set_password(str(form.name.data))
        db.session.commit()
        return redirect(url_for("logout"))
    return render_template("ch_pass.html", form=form)


@app.route("/email", methods=["GET", "POST"])
@login_required
def add_email():
    form = SelectForm()
    if form.submit.data:
        User.query.filter_by(id=current_user.id).update({"email":form.email.data})
        db.session.commit()
        token = generate_confirmation_token(current_user.email)
        confirm_url = url_for('confirm_email', token=token, _external=True)
        html = render_template('activate.html', confirm_url=confirm_url)
        subject = "Please confirm your email"
        send_email(current_user.email, subject, html)
        print(1)
        flash('Congratulations, you are now a registered user!')
        return "На ваш email было высланно письмо"
    return render_template('email.html', title='Email', form=form)


@app.route('/confirm/<token>')
@login_required
def confirm_email(token):
    try:
        email = confirm_token(token)
    except:
        flash('The confirmation link is invalid or has expired.', 'danger')
    user = User.query.filter_by(email=email).first_or_404()
    if user.confirmed:
        flash('Account already confirmed. Please login.', 'success')
    else:
        user.confirmed = True
        user.confirmed_on = datetime.datetime.now()
        db.session.add(user)
        db.session.commit()
        flash('You have confirmed your account. Thanks!', 'success')
    return redirect(url_for('tst'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        a = User.query.filter_by(id = current_user.id).update({"email":form.email.data})
        db.session.commit
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route("/admin_school")
@login_required
def adm_school():
    if current_user.admin:
        return render_template("adm_school.html")
    else:
        return redirect(url_for(index))


@app.route('/admin')
@login_required
def hello_admin():
    if current_user.super_admin:
        return render_template('admin_panel.html')
    else:
        return redirect(url_for(index))


@app.route("/add_student", methods=['GET', "POST"])
@login_required
def add_student():
    if current_user.admin:
        form = SelectForm()
        form.student_list.choices = DB.student_list_form()
        form.class_list.choices = DB.class_list_form()
        form.school_list.choices = DB.list_school_form()
        form.student_list2.choices = DB.student_list_form()
        form.class_list2.choices = DB.class_list_form()
        if form.submit.data:
            DB.add_student(form.school_list.data, form.class_list.data, form.name.data, form.surname.data,
                           form.patronymic.data,
                           form.sex.data, form.password.data)
            return "Данные для " + str(form.name.data) + " " + str(form.surname.data) + " " + str(
                form.patronymic.data) + " Логин:пароль  " + str(DB.get_last_added_userid()) + " : " + form.password.data + """ <a href="/add_student" font-size="16">ок</a>"""

        if form.submit3.data:
            DB.update_student(id=form.student_list2.data, class_id=form.class_list2.data, sex=form.sex2.data, name=form.name2.data, surname=form.surname2.data, patronymic=form.patronymic2.data, password=form.password2.data)
            return redirect(url_for("add_student"))
        if form.submit2.data:
            student = db.session.query(Students).filter_by(id=form.student_list.data)
            student = student.all()
            user_id = student[0].id_user
            db.session.query(User).filter_by(id=user_id).delete()
            db.session.query(Students).filter_by(id=form.student_list.data).delete()
            db.session.commit()
            return redirect(url_for("add_student"))
        return render_template("add_student2.html", form=form, rows=DB.student_list())
    else:
        return redirect(url_for("index"))

"""
@app.route("/admin/update_student", methods=['GET', "POST"])
@login_required
def update_student():
    if current_user.admin:
        form = SelectForm()
        form.student_list.choices = DB.student_list_form()
        form.class_list.choices = DB.class_list_form()
        if form.submit2.data:
            DB.update_student(id=form.student_list.data, class_id=form.class_list.data, sex=form.sex.data, name=form.name.data, surname=form.surname.data, patronymic=form.patronymic.data, password=form.password.data)
            return "Данные ученика успешно изменнены"
        return render_template("up_student2.html", form=form)
    else:
        return redirect(url_for("index"))


@app.route('/admin/delete_student', methods=['GET', "POST"])
@login_required
def delete_student():
    if current_user.admin:
        form = SelectForm()
        form.student_list.choices = DB.student_list_form()
        form.class_list.choices = DB.class_list_form()
        form.school_list.choices = DB.list_school_form()
        if form.submit.data:
            DB.delete_student(form.student_list.data)
            return redirect(url_for('index'))
        return render_template('delstudent.html', title='Email', form=form)
    else:
        return redirect(url_for("index"))


@app.route('/admin/students_list')
@login_required
def students_list():
    if current_user.admin:
        return render_template("st_list.html", rows = DB.student_list())
    else:
        return redirect(url_for("index"))


@app.route('/admin/delete_teacher', methods=['GET', "POST"])
@login_required
def delete_teacher():
    if current_user.admin:
        form = SelectForm()
        form.teacher_list.choices = DB.teacher_list_form()
        if form.submit.data:
            DB.delete_teacher(form.teacher_list.data)
            return redirect(url_for("index"))
        return render_template("delete_teacher.html", form=form)
    else:
        return redirect(url_for("index"))


@app.route('/admin/teachers_list')
@login_required
def teachers_list():
    if current_user.admin:
        return render_template("tc_list.html", rows=DB.teacher_list())
    else:
        return redirect(url_for("index"))
        
        
@app.route("/admin/update_teacher", methods=['GET', "POST"])
@login_required
def update_teacher():
    if current_user.admin:
        form = SelectForm()
        form.teacher_list.choices = DB.teacher_list_form()
        if form.submit2.data:
            DB.update_teacher(id=form.teacher_list.data, sex=form.sex.data, name=form.name.data, surname=form.surname.data, patronymic=form.patronymic.data, subject=form.subject.data)
            return redirect(url_for("index"))
        return render_template("up_teacher.html", form=form)
    else:
        return redirect(url_for("index"))
"""


@app.route("/add_teacher", methods=['GET', "POST"])
@login_required
def add_teacher():
    if current_user.admin:
        form = SelectForm()
        form.school_list.choices = DB.list_school_form()
        form.teacher_list2.choices = DB.teacher_list_form()
        form.teacher_list3.choices = DB.teacher_list_form()
        form.teacher_list.choices = DB.teacher_list_form()
        if form.submit.data:
            DB.add_teacher(form.school_list.data, form.name.data, form.surname.data, form.patronymic.data, form.sex.data, form.subject.data)
            return redirect(url_for("add_teacher"))
        if form.submit3.data:
            DB.update_teacher(id=form.teacher_list2.data, name=form.name2.data, surname=form.surname2.data, patronymic=form.patronymic2.data, subject=form.subject2.data, sex=form.sex2.data)
            return redirect(url_for("add_teacher"))
        if form.submit2.data:
            DB.delete_teacher(form.teacher_list3.data)
            return redirect(url_for("add_teacher"))
        return render_template("add_teacher.html", form=form, rows=DB.teacher_list())
    else:
        return redirect(url_for("index"))


@app.route("/add_school", methods=["GET", "POST"])
@login_required
def add_school():
    if current_user.super_admin:
        form = SelectForm()
        form.school_list.choices = DB.list_school_form()
        if form.submit2.data:
            DB.add_school(form.name.data, form.surname.data)
            return redirect(url_for("add_school"))
        if form.submit.data:
            DB.delete_school(form.school_list.data)
            return redirect(url_for("add_school"))
        return render_template("school.html", form=form, rows=DB.school_list())
    else:
        return redirect(url_for("index"))


"""
@app.route('/admin/delete_school', methods=['GET', "POST"])
@login_required
def delete_school():
    if current_user.super_admin:
        form = SelectForm()
        form.school_list.choices = DB.list_school_form()
        if form.submit.data:
            DB.delete_school(form.school_list.data)
            return redirect(url_for("index"))
        return render_template("del_school.html", form=form)
    else:
        return redirect(url_for("index"))


@app.route('/admin/schools_list')
@login_required
def schools_list():
    if current_user.super_admin:
        return render_template("sc_list.html", rows=DB.school_list())
    else:
        return redirect(url_for("index"))
        
@app.route("/admin/class_list")
@login_required
def class_list():
    if current_user.admin:
        return render_template("cl_list.html", rows=DB.class_list())
    else:
        return redirect(url_for("index"))


@app.route("/admin/delete_class", methods=['GET', "POST"])
@login_required
def del_class():
    if current_user.admin:
        form = SelectForm()
        form.class_list.choices = DB.class_list_form()
        if form.submit.data:
            DB.delete_class(form.class_list.data)
            return redirect(url_for("index"))
        return render_template("del_class.html", form=form)
    else:
        return redirect(url_for("index"))
        

@app.route("/admin/delete_group", methods=['GET', "POST"])
@login_required
def del_group():
    if current_user.admin:
        form = SelectForm()
        form.class_list.choices = DB.class_list_form()
        if form.submit2.data:
            return redirect(url_for("dell_group", class_id=form.class_list.data))
        return render_template("de_group.html", form=form, rows=DB.group_list())
    else:
        return redirect(url_for("index"))
        
@app.route("/admin/group_list")
@login_required
def group_list():
    if current_user.admin:
        return render_template("gg_list.html", rows=DB.group_list())
    else:
        return redirect(url_for("index"))
"""


@app.route("/add_class", methods=['GET', "POST"])
@login_required
def add_class():
    if current_user.admin:
        form = SelectForm()
        form.school_list.choices = DB.list_school_form()
        form.class_list.choices = DB.class_list_form()
        if form.submit.data:
            DB.add_class(form.school_list.data, form.name.data)
            return redirect(url_for("add_class"))
        if form.submit2.data:
            DB.delete_class(form.class_list.data)
            return redirect(url_for("add_class"))
        return render_template("add_class.html", form=form, rows=DB.class_list())
    else:
        return redirect(url_for("index"))


@app.route("/add_group", methods=['GET', "POST"])
@login_required
def add_group():
    if current_user.admin:
        form = SelectForm()
        form.class_list.choices = DB.class_list_form()
        form.class_list2.choices = DB.class_list_form()
        if form.submit.data:
            DB.add_group(form.class_list.data, form.name.data)
            return redirect(url_for("add_group"))
        if form.submit2.data:
            return redirect(url_for("dell_group", class_id=form.class_list2.data))
        return render_template("add_groupp.html", form=form, rows=DB.group_list())
    else:
        return redirect(url_for("index"))


@app.route("/delete_group2/<class_id>", methods=['GET', "POST"])
@login_required
def dell_group(class_id):
    if current_user.admin:
        form = SelectForm()
        form.group_list.choices = DB.group_list_form(class_id)
        if form.submit2.data:
            DB.delete_group(form.group_list.data)
            return redirect(url_for("add_group"))
        return render_template("de_group.html", form=form, rows=DB.group_list())
    else:
        return redirect(url_for("index"))


@app.route("/add_teachergroup", methods=["GET", "POST"])
@login_required
def add_teacher_to_group():
    if current_user.admin:
        form = SelectForm()
        form.class_list.choices = DB.class_list_form()
        form.group_list.choices = DB.teachergroup_list_form()
        if form.submit2.data:
            return redirect(url_for("add_teacher_to_group2", class_id=form.class_list.data))
        if form.submit.data:
            a = form.group_list.data
            a = a.split(" ")
            DB.delete_teacher_from_group(a[1], a[0])
            return redirect(url_for("add_teacher_to_group"))
        return render_template("add_teacher_to_group.html", form=form, rows=DB.teachergroup_list_form())
    else:
        return redirect(url_for("index"))


@app.route("/add_teachergroup2<class_id>", methods=["GET", "POST"])
@login_required
def add_teacher_to_group2(class_id):
    if current_user.admin:
        form = SelectForm()
        form.group_list.choices = DB.group_list_form(class_id)
        form.a1.choices = DB.teacher_list_form()
        if form.submit2.data:
            DB.add_teacher_to_group(form.a1.data, form.group_list.data)
            return redirect(url_for("add_teacher_to_group"))
        return render_template("add_teacher_to_group2.html", form=form, rows=DB.teachergroup_list_form())
    else:
        return redirect(url_for("index"))


@app.route("/add_studentgroup", methods=["GET", "POST"])
@login_required
def add_studentgroup():
    if current_user.admin:
        form = SelectForm()
        form.class_list.choices = DB.class_list_form()
        form.group_list.choices = DB.studentgroup_list_form()
        if form.submit2.data:
            return redirect(url_for("add_studentgroup2", class_id=form.class_list.data))
        if form.submit.data:
            a = form.group_list.data
            a = a.split(" ")
            DB.delete_student_from_group(a[1], a[0])
            return redirect(url_for("add_studentgroup"))
        return render_template("add_studentgroup.html", form=form, rows=DB.studentgroup_list_form())
    else:
        return redirect(url_for("index"))


@app.route("/admin/add_studentgroup2/<class_id>", methods=["GET", "POST"])
@login_required
def add_studentgroup2(class_id):
    if current_user.admin:
        form = SelectForm()
        form.group_list.choices = DB.group_list_form(class_id)
        form.a1.choices = DB.student_list_form()
        if form.submit2.data:
            DB.add_student_to_group(form.a1.data, form.group_list.data)
            return redirect(url_for("add_studentgroup"))
        return render_template("add_stundentgroup2.html", form=form)
    else:
        return redirect(url_for("index"))


@app.route("/admin/delete_teachergroup", methods=["GET", "POST"])
@login_required
def del_teacher_to_group():
    if current_user.admin:
        form = SelectForm()
        form.group_list.choices = DB.teachergroup_list_form()
        if form.submit2.data:
            a = form.group_list.data
            a = a.split(" ")
            DB.delete_teacher_from_group(a[1], a[0])
            return redirect(url_for("index"))
        return render_template("del_teacher_to_group.html", form=form)
    else:
        return redirect(url_for("index"))


@app.route("/admin/delete_studentgroup", methods=["GET", "POST"])
@login_required
def del_student_to_group():
    if current_user.admin:
        form = SelectForm()
        form.group_list.choices = DB.studentgroup_list_form()
        if form.submit2.data:
            a = form.group_list.data
            a = a.split(" ")
            DB.delete_student_from_group(a[1], a[0])
            return redirect(url_for("index"))
        return render_template("del_student_group.html", form=form)
    else:
        return redirect(url_for("index"))


@app.route("/add_rating", methods=["GET", "POST"])
def add_rating():
    if request.method == "POST":
        data = request.data
        json_object = json.loads(data)
        DB.get().add_rating(json_object["id_school"], json_object["id_student"] , json_object["id_teacher"], json_object["text_field"], json_object["lesson_interest"], json_object["lesson_comprehensibility"], json_object["teacher_behavior"])
    return "ok"


@app.route("/admin/add_schedule_class", methods=["GET", "POST"])
def add_schedule():
    if current_user.admin:
        form = SelectForm()
        form.class_list.choices = DB.class_list_form()
        if form.submit2.data:
            DB.add_schedule(form.class_list.data)
            return redirect(url_for("add_schedule2", class_id = form.class_list.data))
        return render_template("add_schedule1.html", form=form)
    else:
        return redirect(url_for("index"))


@app.route("/admin/add_schedule/<class_id>", methods=["GET", "POST"])
@login_required
def add_schedule2(class_id):
    if current_user.admin:
        form = ScheduleForm()
        form.monday1.choices = DB.subject_list(class_id)
        form.monday2.choices = DB.subject_list(class_id)
        form.monday3.choices = DB.subject_list(class_id)
        form.monday4.choices = DB.subject_list(class_id)
        form.monday5.choices = DB.subject_list(class_id)
        form.monday6.choices = DB.subject_list(class_id)

        form.tuesday1.choices = DB.subject_list(class_id)
        form.tuesday2.choices = DB.subject_list(class_id)
        form.tuesday3.choices = DB.subject_list(class_id)
        form.tuesday4.choices = DB.subject_list(class_id)
        form.tuesday5.choices = DB.subject_list(class_id)
        form.tuesday6.choices = DB.subject_list(class_id)

        form.wednesday1.choices = DB.subject_list(class_id)
        form.wednesday2.choices = DB.subject_list(class_id)
        form.wednesday3.choices = DB.subject_list(class_id)
        form.wednesday4.choices = DB.subject_list(class_id)
        form.wednesday5.choices = DB.subject_list(class_id)
        form.wednesday6.choices = DB.subject_list(class_id)

        form.thursday1.choices = DB.subject_list(class_id)
        form.thursday2.choices = DB.subject_list(class_id)
        form.thursday3.choices = DB.subject_list(class_id)
        form.thursday4.choices = DB.subject_list(class_id)
        form.thursday5.choices = DB.subject_list(class_id)
        form.thursday6.choices = DB.subject_list(class_id)

        form.friday1.choices = DB.subject_list(class_id)
        form.friday2.choices = DB.subject_list(class_id)
        form.friday3.choices = DB.subject_list(class_id)
        form.friday4.choices = DB.subject_list(class_id)
        form.friday5.choices = DB.subject_list(class_id)
        form.friday6.choices = DB.subject_list(class_id)

        form.saturday1.choices = DB.subject_list(class_id)
        form.saturday2.choices = DB.subject_list(class_id)
        form.saturday3.choices = DB.subject_list(class_id)
        form.saturday4.choices = DB.subject_list(class_id)
        form.saturday5.choices = DB.subject_list(class_id)
        form.saturday6.choices = DB.subject_list(class_id)
        schedule_id = DB.get_schedule_id(class_id)
        if form.submit.data:
            DB.add_schedule_days(schedule_id, "monday", form.monday1.data, 1)
            DB.add_schedule_days(schedule_id, "monday", form.monday2.data, 2)
            DB.add_schedule_days(schedule_id, "monday", form.monday3.data, 3)
            DB.add_schedule_days(schedule_id, "monday", form.monday4.data, 4)
            DB.add_schedule_days(schedule_id, "monday", form.monday5.data, 5)
            DB.add_schedule_days(schedule_id, "monday", form.monday6.data, 6)

            DB.add_schedule_days(schedule_id, "tuesday", form.tuesday1.data, 1)
            DB.add_schedule_days(schedule_id, "tuesday", form.tuesday2.data, 2)
            DB.add_schedule_days(schedule_id, "tuesday", form.tuesday3.data, 3)
            DB.add_schedule_days(schedule_id, "tuesday", form.tuesday4.data, 4)
            DB.add_schedule_days(schedule_id, "tuesday", form.tuesday5.data, 5)
            DB.add_schedule_days(schedule_id, "tuesday", form.tuesday6.data, 6)

            DB.add_schedule_days(schedule_id, "wednesday", form.wednesday1.data, 1)
            DB.add_schedule_days(schedule_id, "wednesday", form.wednesday2.data, 2)
            DB.add_schedule_days(schedule_id, "wednesday", form.wednesday3.data, 3)
            DB.add_schedule_days(schedule_id, "wednesday", form.wednesday4.data, 4)
            DB.add_schedule_days(schedule_id, "wednesday", form.wednesday5.data, 5)
            DB.add_schedule_days(schedule_id, "wednesday", form.wednesday6.data, 6)

            DB.add_schedule_days(schedule_id, "thursday", form.thursday1.data, 1)
            DB.add_schedule_days(schedule_id, "thursday", form.thursday2.data, 2)
            DB.add_schedule_days(schedule_id, "thursday", form.thursday3.data, 3)
            DB.add_schedule_days(schedule_id, "thursday", form.thursday4.data, 4)
            DB.add_schedule_days(schedule_id, "thursday", form.thursday5.data, 5)
            DB.add_schedule_days(schedule_id, "thursday", form.thursday6.data, 6)

            DB.add_schedule_days(schedule_id, "friday", form.friday1.data, 1)
            DB.add_schedule_days(schedule_id, "friday", form.friday2.data, 2)
            DB.add_schedule_days(schedule_id, "friday", form.friday3.data, 3)
            DB.add_schedule_days(schedule_id, "friday", form.friday4.data, 4)
            DB.add_schedule_days(schedule_id, "friday", form.friday5.data, 5)
            DB.add_schedule_days(schedule_id, "friday", form.friday6.data, 6)

            DB.add_schedule_days(schedule_id, "saturday", form.saturday1.data, 1)
            DB.add_schedule_days(schedule_id, "saturday", form.saturday2.data, 2)
            DB.add_schedule_days(schedule_id, "saturday", form.saturday3.data, 3)
            DB.add_schedule_days(schedule_id, "saturday", form.saturday4.data, 4)
            DB.add_schedule_days(schedule_id, "saturday", form.saturday5.data, 5)
            DB.add_schedule_days(schedule_id, "saturday", form.saturday6.data, 6)
            return redirect(url_for("index"))
        return render_template("add_schedule2.html", form=form)
    else:
        return redirect(url_for("index"))


@app.route("/admin/del_schedule", methods=["GET", "POST"])
@login_required
def del_schedule():
    if current_user.admin:
        form = SelectForm()
        form.schedule_list.choices = DB.schedule_list()
        if form.submit2.data:
            DB.delete_schedule(form.schedule_list.data)
            return redirect(url_for("index"))
        return render_template("del_schedule.html", form=form)
    else:
        return redirect(url_for("index"))


@app.route("/tst", methods=["GET", "POST"])
@login_required
def tst():
    form = SelectForm()
    if form.submit.data:
        print(form.a1.data)
    if not current_user.admin or not current_user.super_admin:
        return render_template("jq.html", form=form, name=DB.get_student_name(current_user.id))
    return render_template("jq.html", form=form, name="Админ")


@app.route("/add_admin", methods=['GET', "POST"])
@login_required
def add_admin():
    if current_user.super_admin:
        form = SelectForm()
        form.school_list.choices = DB.list_school_form()
        form.student_list.choices = DB.admin_list()
        if form.submit.data:
            DB.add_admin(form.school_list.data, form.name.data)
            return redirect(url_for("add_admin"))
        if form.submit2.data:
            DB.delete_admin(form.student_list.data)
            return redirect(url_for("add_admin"))
        return render_template("admin.html", form=form, rows=DB.admin_list())
    else:
        return redirect(url_for("index"))


@app.route("/star", methods=['GET', "POST"])
def star():
    if request.method == "POST":
        data = request.data
        jo = json.loads(data)
        print(jo["r1"], jo["r2"], jo["r3"], jo["com"])
    return render_template("starr.html")


"""
@app.route('/admin/delete_admin', methods=['GET', "POST"])
@login_required
def delete_admin():
    if current_user.admin:
        form = SelectForm()
        form.student_list.choices = DB.admin_list()
        if form.submit.data:
            DB.delete_admin(form.student_list.data)
            return redirect(url_for('index'))
        return render_template('deladmin.html', title='Email', form=form)
    else:
        return redirect(url_for("index"))
"""

if __name__ == '__main__':
    app.run(debug=True)
