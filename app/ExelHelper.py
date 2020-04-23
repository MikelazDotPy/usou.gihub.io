import xlrd, xlwt
from DB import DB


def add_students(way):
    wb = xlrd.open_workbook(way)
    sheet = wb.sheet_by_index(0)
    for i in range(sheet.nrows):
        classs = ""
        groupp = ""
        school = ""
        name = ""
        surname = ""
        patronymic = ""
        sex = ""
        hash_password = ""
        classs = sheet.row_values(i)[0]
        groupp = sheet.row_values(i)[1]
        school = sheet.row_values(i)[2]
        name = sheet.row_values(i)[3]
        surname = sheet.row_values(i)[4]
        patronymic = sheet.row_values(i)[5]
        sex = sheet.row_values(i)[6]
        hash_password = sheet.row_values(i)[7]
        DB.get().add_student(int(classs), int(groupp), int(school), str(name), str(surname), str(patronymic), str(sex), str(hash_password))


def add_teachers(way):
    wb = xlrd.open_workbook(way)
    sheet = wb.sheet_by_index(0)
    for i in range(sheet.nrows):
        subject = ""
        school = ""
        name = ""
        surname = ""
        patronymic = ""
        sex = ""
        hash_password = ""
        subject = sheet.row_values(i)[0]
        school = sheet.row_values(i)[1]
        name = sheet.row_values(i)[2]
        surname = sheet.row_values(i)[3]
        patronymic = sheet.row_values(i)[4]
        sex = sheet.row_values(i)[5]
        hash_password = sheet.row_values(i)[6]
        DB.add_teacher(str(school), str(subject), str(name), str(surname), str(patronymic), str(sex), str(hash_password))


def add_class(way):
    wb = xlrd.open_workbook(way)
    sheet = wb.sheet_by_index(0)
    for i in range(sheet.nrows):
        id_sc = 0
        name = ""
        id_sc = sheet.row_values(i)[0]
        name = sheet.row_values(i)[1]
        DB.add_class(str(id_sc), str(name))


def add_group(way):
    wb = xlrd.open_workbook(way)
    sheet = wb.sheet_by_index(0)
    for i in range(sheet.nrows):
        id_sc = 0
        name = ""
        id_sc = sheet.row_values(i)[0]
        name = sheet.row_values(i)[1]
        DB.add_group(str(id_sc), str(name))


def add_ttogroup(way):
    wb = xlrd.open_workbook(way)
    sheet = wb.sheet_by_index(0)
    for i in range(sheet.nrows):
        id_sc = 0
        name = ""
        id_sc = sheet.row_values(i)[0]
        name = sheet.row_values(i)[1]
        DB.add_ttogroup(str(id_sc), str(name))