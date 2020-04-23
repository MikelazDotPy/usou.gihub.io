from app.models import *


def add_student(school_id, class_id, name, surname, patronymic, sex, password):
    user = User(admin=False, email=None, confirmed=False)
    user.set_password(str(password))
    db.session.add(user)
    db.session.commit()
    id_user = db.session.query(User).order_by(User.id)[-1]
    id_user = id_user.id
    db.session.add(Students(school_id=school_id, class_id=class_id, name=name, surname=surname, patronymic=patronymic, sex=sex, id_user=id_user))
    db.session.commit()


def get_last_added_userid():
    a = db.session.query(Students).order_by(Students.id_user)[-1]
    return a.id_user


def delete_student(id):
    a = db.session.query(Students).filter_by(id=id)
    db.session.query(StudentsGroup).filter_by(id_student=a[0].id).delete()
    student = db.session.query(Students).filter_by(id=id)
    student = student.all()
    user_id = student[0].id_user
    db.session.query(User).filter_by(id=user_id).delete()
    db.session.query(Students).filter_by(id=id).delete()
    db.session.commit()


def student_list_form():
    a = db.session.query(Students).all()
    st_list = []
    for i in a:
        class_name = Classes.query.filter_by(id=i.class_id).all()
        class_name = class_name[0].name
        st_list.append((i.id, str(i.name) + " " + str(i.surname) + " " + str(class_name)))
    return st_list


def get_student_name(usr_id):
    a = db.session.query(Students).filter_by(id_user=usr_id).all()
    a = a[0].name
    return a


def student_list():
    st_list = []
    a = db.session.query(Students).all()
    for i in a:
        class_name = Classes.query.filter_by(id=i.class_id).all()
        class_name = class_name[0].name
        school_name = School.query.filter_by(id=i.school_id).all()
        school_name = school_name[0].school
        st_list.append(str(i.id) + " " + str(school_name) + " " + str(class_name) + " " + str(i.name) + " " + str(i.surname) + " " + str(i.patronymic) + " " + str(i.sex))
    return st_list


def update_student(id, class_id="", name="", surname="", patronymic="", sex="", password=""):

    if class_id != "":
        # = Classes.query.filter_by(name=class_name)
        #class_id = class_id.all()
        #class_id = class_id[0].id
        db.session.query(Students).filter_by(id=id).update(({"class_id": class_id}))
        db.session.commit()

    if name != "":
        db.session.query(Students).filter_by(id=id).update(({"name": name}))
        db.session.commit()

    if surname != "" :
        db.session.query(Students).filter_by(id=id).update(({"surname": surname}))
        db.session.commit()

    if patronymic != "" :
        db.session.query(Students).filter_by(id=id).update(({"patronymic": patronymic}))
        db.session.commit()

    if sex != "" :
        db.session.query(Students).filter_by(id=id).update(({"sex": sex}))
        db.session.commit()

    if password != "" :
        st_id = db.session.query(Students).filter_by(id=id)
        st_id = st_id.all()
        st_id = st_id[0].id_user
        password = generate_password_hash(str(password))
        db.session.query(User).filter_by(id=st_id).update(({"password_hash": password}))
        db.session.commit()


def add_school(school, locality):
    db.session.add(School(school, locality))
    db.session.commit()


def school_list():
    st_list = []
    a = db.session.query(School).all()
    for i in a:
        st_list.append(str(i.id) + " " + str(i.school) + " " + str(i.locality))
    return st_list


def list_school_form():
    a = db.session.query(School).all()
    sc_list = []
    for i in a:
        sc_list.append((i.id, str(i.school) + " " + str(i.locality)))
    return sc_list


def delete_school(id):
    a = db.session.query(Students).filter_by(school_id=id).all()
    b = db.session.query(Teachers).filter_by(school_id=id).all()
    c = db.session.query(Classes).filter_by(id_school=id).all()
    for i in a:
        db.session.query(StudentsGroup).filter_by(id_student=i.id).delete()
        db.session.query(User).filter_by(id=i.user_id).delete()
    for i in b:
        db.session.query(TeachersGroup).filter_by(id_teacher=i.id).delete()
    for i in c:
        db.session.query(Groups).filter_by(class_id=i.id).delete()
        d = db.session.query(Schedule).filter_by(class_id=i.id).all()
        for j in d:
            db.session.query(ScheduleDays).filter_by(schedule_id=j.id).delete()
        db.session.query(Schedule).filter_by(class_id=i.id).delete()
    db.session.query(Admin).filter_by(school_id=id).delete()
    db.session.query(Classes).filter_by(id_school=id).delete()
    db.session.query(Teachers).filter_by(school_id=id).delete()
    db.session.query(Students).filter_by(school_id=id).delete()
    db.session.query(School).filter_by(id=id).delete()
    db.session.commit()


def add_teacher(school_id, name, surname, patronymic, sex, subject):
    db.session.add(Teachers(school_id=school_id, name=name, surname=surname, patronymic=patronymic, sex=sex, subject=subject))
    db.session.commit()


def teacher_list_form():
    a = db.session.query(Teachers).all()
    t_list = []
    for i in a:
        t_list.append((i.id, str(i.name) + " " + str(i.surname) + " " + str(i.subject)))
    return t_list


def teacher_list():
    st_list = []
    a = db.session.query(Teachers).all()
    for i in a:
        school_name = School.query.filter_by(id=i.school_id).all()
        school_name = school_name[0].school
        st_list.append(str(i.id) + " " + str(school_name) + " " + str(i.subject) + " " + str(i.name) + " " + str(i.surname) + " " + str(i.patronymic) + " " + str(i.sex))
    return st_list


def delete_teacher(id):
    db.session.query(TeachersGroup).filter_by(id_teacher=id).delete()
    db.session.query(Teachers).filter_by(id=id).delete()
    db.session.commit()


def update_teacher(id, name="", surname="", patronymic="", sex="", subject=""):

    if name != "":
        db.session.query(Teachers).filter_by(id=id).update(({"name": name}))
        db.session.commit()

    if surname != "" :
        db.session.query(Teachers).filter_by(id=id).update(({"surname": surname}))
        db.session.commit()

    if patronymic != "" :
        db.session.query(Teachers).filter_by(id=id).update(({"patronymic": patronymic}))
        db.session.commit()

    if sex != "" :
        db.session.query(Teachers).filter_by(id=id).update(({"sex": sex}))
        db.session.commit()

    if subject != "" :
        db.session.query(Teachers).filter_by(id=id).update(({"subject": subject}))
        db.session.commit()


def add_class(school_id, name):
    db.session.add(Classes(school_id, name))
    db.session.commit()


def class_list_form():
    a = db.session.query(Classes).all()
    cl_list = []
    for i in a:
        cl_list.append((i.id, str(i.name)))
    return cl_list


def class_list():
    st_list = []
    a = db.session.query(Classes).all()
    for i in a:
        school_name = db.session.query(School).filter_by(id=i.id_school).all()
        school_name = school_name[0].school
        st_list.append(str(i.id) + " " + str(school_name) + " " + str(i.name))
    return st_list


def delete_class(class_id):
    a = db.session.query(Groups).filter_by(class_id=class_id).all()
    for i in a:
        idd=i.id
        db.session.query(StudentsGroup).filter_by(id_group=idd).delete()
        db.session.query(TeachersGroup).filter_by(id_group=idd).delete()
    db.session.query(Groups).filter_by(class_id=class_id).delete()
    db.session.query(Classes).filter_by(id=class_id).delete()
    db.session.commit()


def add_group(class_id, name):
    db.session.add(Groups(class_id, name))
    db.session.commit()


def group_list():
    st_list = []
    a = db.session.query(Groups).all()
    for i in a:
        class_name = db.session.query(Classes).filter_by(id=i.class_id).all()
        class_name = class_name[0].name
        st_list.append(str(i.id) + " " + str(class_name) + " " + str(i.name))
    return st_list


def group_list_form(class_id):
    a = db.session.query(Groups).filter_by(class_id=class_id).all()
    gr_list = []
    for i in a:
        gr_list.append((i.id, str(i.name)))
    return gr_list


def delete_group(group_id):
    a = db.session.query(Groups).filter_by(id=group_id).all()
    for i in a:
        idd = i.id
        db.session.query(TeachersGroup).filter_by(id_group=idd).delete()
    db.session.query(Groups).filter_by(id=group_id).delete()
    db.session.commit()


def add_teacher_to_group(id_teacher, group_id):
    for i in id_teacher:
        db.session.add(TeachersGroup(i, group_id))
    db.session.commit()


def add_student_to_group(id_student, group_id):
    for i in id_student:
        db.session.add(StudentsGroup(i, group_id))
    db.session.commit()


def teachergroup_list_form():
    a = db.session.query(TeachersGroup).all()
    gr_list = []
    for i in a:
        teacher = db.session.query(Teachers).filter_by(id=i.id_teacher).all()
        teacher_id = teacher[0].id
        teacher = str(teacher[0].name) + " " + str(teacher[0].surname) + " " + str(teacher[0].subject)
        group_name = db.session.query(Groups).filter_by(id=i.id_group).all()
        group_name = group_name[0].name
        gr_list.append((str(i.id_group) + " " + str(teacher_id), teacher + " " + group_name))
    return gr_list


def studentgroup_list_form():
    a = db.session.query(StudentsGroup).all()
    gr_list = []
    for i in a:
        teacher = db.session.query(Students).filter_by(id=i.id_student).all()
        teacher_id = teacher[0].id
        teacher = str(teacher[0].name) + " " + str(teacher[0].surname)
        group_name = db.session.query(Groups).filter_by(id=i.id_group).all()
        group_name = group_name[0].name
        gr_list.append((str(i.id_group) + " " + str(teacher_id), teacher + " " + group_name))
    return gr_list


def delete_teacher_from_group(id_teacher, group_id):
    db.session.query(TeachersGroup).filter_by(id_group=group_id, id_teacher=id_teacher).delete()
    db.session.commit()


def delete_student_from_group(id_teacher, group_id):
    db.session.query(StudentsGroup).filter_by(id_group=group_id, id_student=id_teacher).delete()
    db.session.commit()


def add_rating(id_school, id_student, id_teacher, text_field, lesson_interest, lesson_comprehensibility, teacher_behavior):
    db.session.add(Assessment(id_school, id_student, id_teacher, text_field, lesson_interest, lesson_comprehensibility, teacher_behavior))
    db.session.commit()


def add_schedule(class_id):
    db.session.add(Schedule(class_id))
    db.session.commit()


def get_schedule_id(class_id):
    a = db.session.query(Schedule).filter_by(class_id=class_id).all()
    return a[0].id


def subject_list(class_id):
    a = db.session.query(Groups).filter_by(class_id=class_id).all()
    gr_list = []
    for i in a:
        b = db.session.query(TeachersGroup).filter_by(id_group=i.id).all()
        for j in b:
            c = db.session.query(Teachers).filter_by(id=j.id_teacher).all()
            c = c[0].subject
            gr_list.append((c, c))
    gr_list.append(("Пустой", "Пустой"))
    return gr_list


def add_schedule_days(schedule_id, day, subject, lesson_number):
    db.session.add(ScheduleDays(schedule_id, day, subject, lesson_number))
    db.session.commit()


def schedule_list():
    st_list = []
    a = db.session.query(Schedule).all()
    for i in a:
        class_name = db.session.query(Classes).filter_by(id=i.class_id).all()
        class_name = class_name[0].name
        st_list.append((i.id, str(class_name)))
    return st_list


def delete_schedule(schedule_id):
    db.session.query(Schedule).filter_by(id=schedule_id).delete()
    db.session.query(ScheduleDays).filter_by(schedule_id=schedule_id).delete()
    db.session.commit()


def add_admin(school_id, password):
    user = User(admin=True, email=None, confirmed=False)
    user.set_password(str(password))
    db.session.add(user)
    db.session.commit()
    id_user = db.session.query(User).order_by(User.id)[-1]
    id_user = id_user.id
    db.session.add(Admin(school_id=school_id, id_user=id_user))
    db.session.commit()


def delete_admin(id):
    student = db.session.query(Admin).filter_by(id=id)
    student = student.all()
    user_id = student[0].id_user
    db.session.query(User).filter_by(id=user_id).delete()
    db.session.query(Admin).filter_by(id=id).delete()
    db.session.commit()


def admin_list():
    st_list = []
    a = db.session.query(Admin).all()
    for i in a:
        school_name = School.query.filter_by(id=i.school_id).all()
        school_name = school_name[0].school
        st_list.append((str(i.id), str(school_name)))
    return st_list


if __name__ == "__main__":
    #add_student(21, 1, 2, 1, 2, 3, 4, 12345)
    #delete_student(3)
    #update_student(1, name="vany", password="1000")
    #add_school("Киевская школа 100241", "Kiiv")
    #delete_school(2)
    #add_teacher(21, "Ukrain", "nata", "fa", "ad", "as")
    #delete_teacher(1)
    #update_teacher(1, name="Lox", surname="Zmix", subject="Russiy")
    #add_class(21, "67v")
    #add_group("67v","67v1")
    #add_teacher_to_group(1, "67v1")
    #add_rating(1, 1, 1, "gaga", "1", "2", "3")
    #add_schedule("67v")
    #add_schedule_days(1, "vt", "dad", "1")
    #delete_group("67v1")
    #delete_class("67v")
    #delete_teacher_from_group(1, "2")
    #delete_schedule(111)
    #student_list_form()
    pass