import pandas as pd
import csv
from passlib.hash import sha256_crypt
import hashlib

# Tried to limit database commits to as few and unique values as possible,
# resulting in a medium to thorough level of parsing

#pw = sha256_crypt.encrypt(str(form.password.data))

# What is the cost of passing a buffer to a function?
def ParseStudent(cur):
    line = open("Students.csv", "r")
    entry = "blah"
    shift = 0
    while len(entry) > 0:
        entry = line.readline()
        submit = entry.split(',')
        shift+=1
        if shift > 1 and shift < 1002:
            fullname = submit[0].strip()
            email = submit[1].strip()
            age = int(submit[2].strip())
            zip = int(submit[3].strip())
            phone = int(submit[4].strip())
            gender = submit[5].strip()
            city = submit[6].strip()
            state = submit[7].strip()
            password = submit[8].strip()
            #print("Hashing password #%d: " % shift, end='')
            paddr = hashlib.md5(password.encode())
            password = paddr.hexdigest()
            #password = sha256_crypt.encrypt(str(password))
            #print(password)
            street = submit[9].strip()
            major = submit[10].strip()

            cur.execute("INSERT INTO Students (email, password, name, age, gender, major, street, zipcode) VALUES (?,?,?,?,?,?,?,?);", (email, password, fullname, age, gender, major, street, zip))
            cur.execute("INSERT INTO Zipcode (zipcode, city, state) VALUES (?,?,?);",(zip, city, state))
    line.close()
    return cur

# Correct
def ParseProfessor(cur):
    line = open('Professors.csv', 'r')
    entry = "blah"
    shift = 0
    while len(entry) > 0:
        entry = line.readline()
        submit = entry.split(',')
        shift+=1
        if shift > 1 and shift < 56:
            name = submit[0].strip()
            email = submit[1].strip()
            password = submit[2].strip()
            paddr = hashlib.md5(password.encode())
            password = paddr.hexdigest()
            #password = sha256_crypt.encrypt(str(password))
            age = int(submit[3].strip())
            gender = submit[4].strip()
            department = submit[5].strip()
            office= submit[6].strip()
            office2= submit[7].strip()
            office = office + ", " + office2
            office = office.strip("\"")
            #deptname = submit[7].strip()
            title = submit[9].strip()
            #teamID = submit[9].strip()
            #teaching = submit[10].strip()

            cur.execute("INSERT INTO Professors (email, password, name, age, gender, office_address, department, title) VALUES (?,?,?,?,?,?,?,?);", (email, password, name, age, gender, office, department, title))
    line.close()
    return cur

# correct
#figured out how to use pandas
def ParseDept(cur):
    with open("Professors.csv", "r") as readinp:
        readinp1 = csv.reader(readinp)
        readarr = []
        for row in readinp1:
            if len(row) != 0:
                readarr = readarr + [row]

    readinp.close()
    df = pd.DataFrame(readarr)
    departments = {}
    dept_id = df[5]
    dept_name = df[7]
    dept_head = df[8]
    dept_professor = df[0]
    for i in range(len(dept_id)):
        if dept_id[i] not in departments:
            departments[dept_id[i]] = [None, None]
        if dept_name[i] not in departments:
            departments[dept_id[i]][0] = dept_name[i]
        if dept_head[i] == "Head":
            if dept_professor[i] not in departments:
                departments[dept_id[i]][1] = dept_professor[i]
    departments.pop('Department')
    for e in departments:
        dept_id = e
        dept_name = departments[e][0]
        dept_head = departments[e][1]
        cur.execute('INSERT INTO Department (dept_id, dept_name, dept_head) VALUES (?,?,?);',
                    (dept_id, dept_name, dept_head))

    return cur

# Correct
def ParseCourse(cur):
    with open("Students.csv", "r") as readinp:
        readinp1 = csv.reader(readinp)
        readarr = []
        for row in readinp1:
            if len(row) != 0:
                readarr = readarr + [row]

    readinp.close()
    df = pd.DataFrame(readarr)

    course_id = df[11]
    course_name = df[12]
    course_desc = df[13]

    course_id2 = df[23]
    course_name2 = df[24]
    course_desc2 = df[25]

    course_id3 = df[35]
    course_name3 = df[36]
    course_desc3 = df[37]

    repeats = []
    for i in range(1, len(course_id)):
        if course_id[i] not in repeats:
            cur.execute('INSERT INTO Course (course_id, course_name, course_description) VALUES (?,?,?);',
                        (course_id[i], course_name[i], course_desc[i]))
            repeats.append(course_id[i])
        if course_id2[i] not in repeats:
            cur.execute('INSERT INTO Course (course_id, course_name, course_description) VALUES (?,?,?);',
                        (course_id2[i], course_name2[i], course_desc2[i]))
            repeats.append(course_id2[i])
        if course_id3[i] not in repeats:
            cur.execute('INSERT INTO Course (course_id, course_name, course_description) VALUES (?,?,?);',
                        (course_id3[i], course_name3[i], course_desc3[i]))
            repeats.append(course_id3[i])

    return cur

#Correct
def ParseSection(cur):
    with open("Students.csv", "r") as readinp:
        readinp1 = csv.reader(readinp)
        readarr = []
        for row in readinp1:
            if len(row) != 0:
                readarr = readarr + [row]

    readinp.close()
    df = pd.DataFrame(readarr)

    with open("Professors.csv", "r") as readinp2:
        readinp3 = csv.reader(readinp2)
        readarr2 = []
        for row2 in readinp3:
            if len(row2) != 0:
                readarr2 = readarr2 + [row2]

    readinp2.close()
    df2 = pd.DataFrame(readarr2)

    profteam1 = df2[9]
    course1t = df2[10]

    teams = {}

    #matches profteam with course
    for j in range(1, len(profteam1)):
        teams[course1t[j]] = profteam1[j]

    df['count'] = 1
    newdf = pd.DataFrame()
    uniques = df.groupby([11, 15, 14, 16]).count()['count']
    newdf = pd.concat([newdf, uniques])

    for index, row in newdf.iterrows():
        course1 = index[0]
        sec_no1 = index[1]
        section_type1 = index[2]
        seats1 = index[3]


        # special case
        if course1 != "Courses 1":
            cur.execute('INSERT INTO Sections (course_id, sec_no, section_type, seats, prof_team_id) VALUES (?,?,?,?,?);',
                        (course1, sec_no1, section_type1, seats1, teams[course1]))


    df['count'] = 1
    newdf2 = pd.DataFrame()
    uniques2 = df.groupby([23, 27, 26, 28]).count()['count']
    newdf2 = pd.concat([newdf2, uniques2])

    for index, row in newdf2.iterrows():
        course2 = index[0]
        sec_no2 = index[1]
        section_type2 = index[2]
        seats2 = index[3]

        # special case
        if course2 != "Courses 2":
            cur.execute('INSERT INTO Sections2 (course_id, sec_no, section_type, seats, prof_team_id) VALUES (?,?,?,?,?);',
                        (course2, sec_no2, section_type2, seats2, teams[course2]))


    df['count'] = 1
    newdf3 = pd.DataFrame()
    uniques3 = df.groupby([35, 39, 38, 40]).count()['count']
    newdf3 = pd.concat([newdf3, uniques3])

    # , 23, 27, 26, 28, 35, 39, 38, 40
    for index, row in newdf3.iterrows():
        course3 = index[0]
        sec_no3 = index[1]
        section_type3 = index[2]
        seats3 = index[3]

        # special case
        if course3 != "Courses 3":
            cur.execute(
                'INSERT INTO Sections3 (course_id, sec_no, section_type, seats, prof_team_id) VALUES (?,?,?,?,?);',
                (course3, sec_no3, section_type3, seats3, teams[course3]))

    return cur

# Correct
def ParseHW(cur):
    with open("Students.csv", "r") as readinp:
        readinp1 = csv.reader(readinp)
        readarr = []
        for row in readinp1:
            if len(row) != 0:
                readarr = readarr + [row]

    readinp.close()
    df = pd.DataFrame(readarr)

    course_id1 = df[11]
    sec_no1 = df[15]
    hw_no1 = df[17]
    hw_details1 = df[18]

    course_id2 = df[23]
    sec_no2 = df[27]
    hw_no2 = df[29]
    hw_details2 = df[30]

    course_id3 = df[35]
    sec_no3 = df[39]
    hw_no3 = df[41]
    hw_details3 = df[42]

    check1 = 0
    check2 = 0
    check3 = 0
    repeats = {}
    #fix to add each hw assignment for each section and course
    for i in range(1, len(course_id1)):
        if course_id1[i] not in repeats:
            cur.execute('INSERT INTO Homework (course_id, sec_no, hw_no, hw_details) VALUES (?,?,?,?);',
                        (course_id1[i], sec_no1[i], hw_no1[i], hw_details1[i]))
            repeats[course_id1[i]] = [sec_no1[i], "0"]
        elif (repeats[course_id1[i]][0] != sec_no1[i]) and (repeats[course_id1[i]][1] != "2"):
            cur.execute('INSERT INTO Homework (course_id, sec_no, hw_no, hw_details) VALUES (?,?,?,?);',
                        (course_id1[i], sec_no1[i], hw_no1[i], hw_details1[i]))

            repeats[course_id1[i]] = [sec_no1[i], "2"]
        if course_id2[i] not in repeats:
            cur.execute('INSERT INTO Homework (course_id, sec_no, hw_no, hw_details) VALUES (?,?,?,?);',
                        (course_id2[i], sec_no2[i], hw_no2[i], hw_details2[i]))
            repeats[course_id2[i]] = [sec_no2[i], "0"]
        elif (repeats[course_id2[i]][0] != sec_no2[i]) and (repeats[course_id2[i]][1] != "2"):
            cur.execute('INSERT INTO Homework (course_id, sec_no, hw_no, hw_details) VALUES (?,?,?,?);',
                        (course_id2[i], sec_no2[i], hw_no2[i], hw_details2[i]))
            repeats[course_id2[i]] = [sec_no2[i], "2"]
        if course_id3[i] not in repeats:
            cur.execute('INSERT INTO Homework (course_id, sec_no, hw_no, hw_details) VALUES (?,?,?,?);',
                        (course_id3[i], sec_no3[i], hw_no3[i], hw_details3[i]))
            repeats[course_id3[i]] = [sec_no3[i], "0"]
        elif (repeats[course_id3[i]][0] != sec_no3[i]) and (repeats[course_id3[i]][1] != "2"):
            cur.execute('INSERT INTO Homework (course_id, sec_no, hw_no, hw_details) VALUES (?,?,?,?);',
                        (course_id3[i], sec_no3[i], hw_no3[i], hw_details3[i]))
            repeats[course_id3[i]] = [sec_no3[i], "2"]

    return cur

# Assuming correct
def ParseHWgrades(cur):
    with open("Students.csv", "r") as readinp:
        readinp1 = csv.reader(readinp)
        readarr = []
        for row in readinp1:
            if len(row) != 0:
                readarr = readarr + [row]

    readinp.close()
    df = pd.DataFrame(readarr)

    df['count'] = 1
    newdf = pd.DataFrame()
    uniques = df.groupby([1, 11, 15, 17, 19]).count()['count']
    newdf = pd.concat([newdf, uniques])

    for index, row in newdf.iterrows():
        userid = index[0]
        courseid = index[1]
        secno = index[2]
        hwno = index[3]
        grade = index[4]

        if courseid != "Courses 1":
            cur.execute('INSERT INTO Homework_grades (student_email, course_id, sec_no, hw_no, grade) VALUES (?,?,?,?,?);',
                    (userid, courseid, secno, hwno, grade))

    df['count'] = 1
    newdf = pd.DataFrame()
    uniques = df.groupby([1, 23, 27, 29, 31]).count()['count']
    newdf = pd.concat([newdf, uniques])

    for index, row in newdf.iterrows():
        userid = index[0]
        courseid = index[1]
        secno = index[2]
        hwno = index[3]
        grade = index[4]

        if courseid != "Courses 2":
            cur.execute('INSERT INTO Homework_grades (student_email, course_id, sec_no, hw_no, grade) VALUES (?,?,?,?,?);',
                    (userid, courseid, secno, hwno, grade))

    df['count'] = 1
    newdf = pd.DataFrame()
    uniques = df.groupby([1, 35, 39, 41, 43]).count()['count']
    newdf = pd.concat([newdf, uniques])

    for index, row in newdf.iterrows():
        userid = index[0]
        courseid = index[1]
        secno = index[2]
        hwno = index[3]
        grade = index[4]

        if courseid != "Courses 3":
            cur.execute('INSERT INTO Homework_grades (student_email, course_id, sec_no, hw_no, grade) VALUES (?,?,?,?,?);',
                    (userid, courseid, secno, hwno, grade))

    return cur

#Correct, 1st courses column has all unique values
def ParseExams(cur):
    with open("Students.csv", "r") as readinp:
        readinp1 = csv.reader(readinp)
        readarr = []
        for row in readinp1:
            if len(row) != 0:
                readarr = readarr + [row]

    readinp.close()
    df = pd.DataFrame(readarr)

    df['count'] = 1
    newdf = pd.DataFrame()
    uniques = df.groupby([11, 15, 20, 21]).count()['count']
    newdf = pd.concat([newdf, uniques])

    for index, row in newdf.iterrows():
        courseid = index[0]
        secno = index[1]
        exam = index[2]
        desc = index[3]

        if (courseid != "Courses 1") & (exam != ""):
            cur.execute('INSERT INTO Exams (course_id, sec_no, exam_no, exam_details) VALUES (?,?,?,?);',
                        (courseid, secno, exam, desc))

    return cur

#Assuming correct
def ParseExamgrades(cur):
    with open("Students.csv", "r") as readinp:
        readinp1 = csv.reader(readinp)
        readarr = []
        for row in readinp1:
            if len(row) != 0:
                readarr = readarr + [row]

    readinp.close()
    df = pd.DataFrame(readarr)

    df['count'] = 1
    newdf = pd.DataFrame()
    uniques = df.groupby([1, 11, 15, 20, 22]).count()['count']
    newdf = pd.concat([newdf, uniques])

    for index, row in newdf.iterrows():
        userid = index[0]
        courseid = index[1]
        secno = index[2]
        examno = index[3]
        grade = index[4]

        if (courseid != "Courses 1") & (examno != ""):
            cur.execute('INSERT INTO Exam_grades (student_email, course_id, sec_no, exam_no, grade) VALUES (?,?,?,?,?);',
                    (userid, courseid, secno, examno, grade))

    df['count'] = 1
    newdf = pd.DataFrame()
    uniques = df.groupby([1, 23, 27, 32, 34]).count()['count']
    newdf = pd.concat([newdf, uniques])

    for index, row in newdf.iterrows():
        userid = index[0]
        courseid = index[1]
        secno = index[2]
        examno = index[3]
        grade = index[4]

        if (courseid != "Courses 2") & (examno != ""):
            cur.execute(
                'INSERT INTO Exam_grades (student_email, course_id, sec_no, exam_no, grade) VALUES (?,?,?,?,?);',
                (userid, courseid, secno, examno, grade))

    df['count'] = 1
    newdf = pd.DataFrame()
    uniques = df.groupby([1, 35, 39, 44, 46]).count()['count']
    newdf = pd.concat([newdf, uniques])

    for index, row in newdf.iterrows():
        userid = index[0]
        courseid = index[1]
        secno = index[2]
        examno = index[3]
        grade = index[4]

        if (courseid != "Courses 3") & (examno != ""):
            cur.execute(
                'INSERT INTO Exam_grades (student_email, course_id, sec_no, exam_no, grade) VALUES (?,?,?,?,?);',
                (userid, courseid, secno, examno, grade))

    return cur


def ParseEnrolls(cur):
    with open("Students.csv", "r") as readinp:
        readinp1 = csv.reader(readinp)
        readarr = []
        for row in readinp1:
            if len(row) != 0:
                readarr = readarr + [row]

    readinp.close()
    df = pd.DataFrame(readarr)

    df['count'] = 1
    newdf = pd.DataFrame()
    uniques = df.groupby([1, 11, 15]).count()['count']
    newdf = pd.concat([newdf, uniques])

    for index, row in newdf.iterrows():
        email = index[0]
        courseid = index[1]
        secno = index[2]

        if (courseid != "Courses 1"):
            cur.execute('INSERT INTO Enrolls (student_email, course_id, sec_no) VALUES (?,?,?);',
                        (email, courseid, secno))

    df['count'] = 1
    newdf = pd.DataFrame()
    uniques = df.groupby([1, 23, 27]).count()['count']
    newdf = pd.concat([newdf, uniques])

    for index, row in newdf.iterrows():
        email = index[0]
        courseid = index[1]
        secno = index[2]

        if (courseid != "Courses 2"):
            cur.execute('INSERT INTO Enrolls (student_email, course_id, sec_no) VALUES (?,?,?);',
                        (email, courseid, secno))

    df['count'] = 1
    newdf = pd.DataFrame()
    uniques = df.groupby([1, 35, 39]).count()['count']
    newdf = pd.concat([newdf, uniques])

    for index, row in newdf.iterrows():
        email = index[0]
        courseid = index[1]
        secno = index[2]

        if (courseid != "Courses 3"):
            cur.execute('INSERT INTO Enrolls (student_email, course_id, sec_no) VALUES (?,?,?);',
                        (email, courseid, secno))

    return cur


def ParseProfTID(cur):
    with open("Professors.csv", "r") as readinp:
        readinp1 = csv.reader(readinp)
        readarr = []
        for row in readinp1:
            if len(row) != 0:
                readarr = readarr + [row]

    readinp.close()
    df = pd.DataFrame(readarr)

    df['count'] = 1
    newdf = pd.DataFrame()
    uniques = df.groupby([1, 9]).count()['count']
    newdf = pd.concat([newdf, uniques])

    for index, row in newdf.iterrows():
        email = index[0]
        id = index[1]

        if (email != "Email"):
            cur.execute('INSERT INTO Prof_team_members(prof_email, teaching_team_id) VALUES (?,?);',
                        (email, id))

    return cur

# def ParseCapstone(cur):
#     with open("Students.csv", "r") as readinp:
#         readinp1 = csv.reader(readinp)
#         readarr = []
#         for row in readinp1:
#             if len(row) != 0:
#                 readarr = readarr + [row]
#
#     readinp.close()
#     df = pd.DataFrame(readarr)
#
#     df['count'] = 1
#     newdf = pd.DataFrame()
#     uniques = df.groupby([11, 15, 20, 21]).count()['count']
#     newdf = pd.concat([newdf, uniques])
#
#     for index, row in newdf.iterrows():
#         courseid = index[0]
#         secno = index[1]
#         exam = index[2]
#         desc = index[3]
#
#         if (courseid != "Courses 1") & (exam != ""):
#             cur.execute('INSERT INTO Exams (course_id, sec_no, exam_no, exam_details) VALUES (?,?,?,?);',
#                         (courseid, secno, exam, desc))
#
#     return cur
