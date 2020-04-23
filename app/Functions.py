from app.models import *


def add_student(school_name, class_name, group_name, name, surname, patronymic, sex, password):
    user = User(admin=False, email=None, confirmed=False)
    user.set_password(str(password))
    db.session.add(user)
    db.session.commit()
    id_user = db.session.query(User).order_by(User.id)[-1]
    id_user = id_user.id
    school_id = School.query.filter_by(school=school_name)
    school_id = school_id.all()
    school_id = school_id[0].id
    class_id = Classes.query.filter_by(name=class_name)
    class_id = class_id.all()
    class_id = class_id[0].id
    group_id = Groups.query.filter_by(name=group_name)
    group_id = group_id.all()
    group_id = group_id[0].id
    db.session.add(Students(school_id=school_id, group_id=group_id, class_id=class_id, name=name, surname=surname, patronymic=patronymic, sex=sex, id_user=id_user))
    db.session.commit()


def delete_student(id):
    student = db.session.query(Students).filter_by(id=id)
    student = student.all()
    user_id = student[0].id_user
    db.session.query(User).filter_by(id=user_id).delete()
    db.session.query(Students).filter_by(id=id).delete()
    db.session.commit()


def update_student(id, class_name="", group_name="", name="", surname="", patronymic="", sex="", password=""):

    if class_name != "":
        class_id = Classes.query.filter_by(name=class_name)
        class_id = class_id.all()
        class_id = class_id[0].id
        db.session.query(Students).filter_by(id=id).update(({"class_id": class_id}))
        db.session.commit()

    if group_name != "":
        group_id = Groups.query.filter_by(name=group_name)
        group_id = group_id.all()
        group_id = group_id[0].id
        db.session.query(Students).filter_by(id=id).update(({"group_id": group_id}))
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


def delete_school(id):
    db.session.query(School).filter_by(id=id).delete()
    db.session.commit()


def add_teacher(school_name, name, surname, patronymic, sex, subject):
    school_id = School.query.filter_by(school=school_name)
    school_id = school_id.all()
    school_id = school_id[0].id
    db.session.add(Teachers(school_id=school_id, name=name, surname=surname, patronymic=patronymic, sex=sex, subject=subject))
    db.session.commit()


def delete_teacher(id):
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


def add_class(school_name, name):
    school_id = School.query.filter_by(school=school_name)
    school_id = school_id.all()
    school_id = school_id[0].id
    db.session.add(Classes(school_id, name))
    db.session.commit()


def delete_class(class_name):
    class_id = Classes.query.filter_by(name=class_name)
    class_id = class_id.all()
    class_id = class_id[0].id
    db.session.query(Classes).filter_by(id=class_id).delete()
    db.session.commit()


def add_group(class_name, name):
    class_id = Classes.query.filter_by(name=class_name)
    class_id = class_id.all()
    class_id = class_id[0].id
    db.session.add(Groups(class_id, name))
    db.session.commit()


def delete_group(group_name):
    group_id = Groups.query.filter_by(name=group_name)
    group_id = group_id.all()
    group_id = group_id[0].id
    db.session.query(Groups).filter_by(id=group_id).delete()
    db.session.commit()


def add_teacher_to_group(id_teacher, group_name):
    group_id = Groups.query.filter_by(name=group_name)
    group_id = group_id.all()
    group_id = group_id[0].id
    db.session.add(TeachersGroup(id_teacher, group_id))
    db.session.commit()


def delete_teacher_from_group(id_teacher, group_name):
    group_id = Groups.query.filter_by(name=group_name)
    group_id = group_id.all()
    group_id = group_id[0].id
    db.session.query(TeachersGroup).filter_by(id_group=group_id, id_teacher=id_teacher).delete()
    db.session.commit()


def add_rating(id_school, id_student, id_teacher, text_field, lesson_interest, lesson_comprehensibility, teacher_behavior):
    db.session.add(Assessment(id_school, id_student, id_teacher, text_field, lesson_interest, lesson_comprehensibility, teacher_behavior))
    db.session.commit()


def add_schedule(class_name):
    class_id = Classes.query.filter_by(name=class_name)
    class_id = class_id.all()
    class_id = class_id[0].id
    db.session.add(Schedule(class_id))
    db.session.commit()


def add_schedule_days(schedule_id, day, subject, lesson_number):
    db.session.add(ScheduleDays(schedule_id, day, subject, lesson_number))
    db.session.commit()


def delete_schedule(class_name):
    class_id = Classes.query.filter_by(name=class_name)
    class_id = class_id.all()
    class_id = class_id[0].id
    schedule_id = db.session.query(Schedule).filter_by(class_id=class_id)
    schedule_id = schedule_id.all()
    schedule_id = schedule_id[0].id
    db.session.query(Schedule).filter_by(class_id=class_id).delete()
    db.session.query(ScheduleDays).filter_by(schedule_id=schedule_id).delete()
    db.session.commit()


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
    pass