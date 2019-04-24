
import hashlib
from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3 as sql
from login import LoginForm, PwReset, addclass
from parse import ParseStudent, ParseHWgrades, ParseProfTID, ParseExamgrades, ParseExams, ParseProfessor, ParseDept, ParseCourse, ParseSection, ParseHW, ParseEnrolls
import math

app = Flask(__name__)

host = 'http://127.0.0.1:5000/'

# WARNING: All tables are emptied and repopulated each time the server is restarted

@app.route('/')
def index():
    return render_template('index.html', url=host)
    #return render_template('index.html', error=error, url=host)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm(request.form)
    if request.method == 'POST' and form.validate():
        user = form.username.data
        #pw = sha256_crypt.encrypt(str(form.password.data))
        pw = form.password.data
        if valid_login(user, pw) == 1:
            flash('Username/Password Successfully found in Database!', 'Success')
            #redirect(url_for('Landing'))
            usr.set_user(user)
            return redirect(url_for('Landing'))
            #return Landing()
            #return render_template('Landing.html', url=host, form=form)
        elif valid_login(user, pw) == 2:
            flash('Error: Incorrect password', 'Error')
            redirect(url_for('login'))
        elif valid_login(user, pw) == 0:
            flash('Error: Username not found', 'Error')
            redirect(url_for('login'))
        else:
            flash('Admin mode engaged', 'Success')
            return redirect(url_for("Admin"))
            #return Admin()
            # return render_template('Admin.html', url=host, form=form)


    return render_template('login.html', url=host, form=form)


@app.route('/landing', methods=['GET', 'POST'])
def Landing():
    getCourses = query_courses(usr.get_user())
    getGrades, avg1, avg2 = query_grades(usr.get_user())
    print(getGrades)
    name = query_name(usr.get_user())
    email, age, gender, major = query_personal(usr.get_user())
    street, city, state, zip = query_Addr(usr.get_user())
    return render_template('Landing.html', url=host, getCourses=getCourses, getGrades=getGrades, avg1=avg1, avg2=avg2, name=name, email=email, age=age, gender=gender, major=major, street=street, city=city, state=state, zip=zip)


@app.route('/reset', methods=['GET', 'POST'])
def Reset():
    form = PwReset(request.form)
    if request.method == 'POST' and form.validate():
        user = form.user.data
        old = form.old.data
        new = form.new.data
        confirm = form.confirm.data
        if valid_login(user, old) == 1:
            if new == confirm:
                usr.set_user(user)
                flash('Password successfully updated!', 'Success')
                # encrypt user entered password
                paddr = hashlib.md5(new.encode())
                password = paddr.hexdigest()
                update_password(user, password)
                return Landing()
                #return render_template('Landing.html', url=host, form=form)
            else:
                flash('New passwords do not match', 'Error')
            # return render_template('Landing.html', url=host, form=form)
        elif valid_login(user, old) == 2:
            flash('Error: Incorrect password', 'Error')
            redirect(url_for('Reset'))
        else:
            flash('Error: Username not found', 'Error')
            redirect(url_for('Reset'))
    return render_template('pwreset.html', url=host, form=form)


@app.route('/Admin', methods=['GET', 'POST'])
def Admin():
    form = addclass(request.form)
    if request.method == 'POST' and form.validate():
        course = form.course_id.data
        name = form.course_name.data
        desc = form.course_desc.data

        course_id2 = form.course_id2.data
        prof_email = form.prof_email.data

        course_id3 = form.course_id3.data
        sec_no = form.sec_no.data
        stud_email = form.stud_email.data

        # print(course_id3, sec_no, stud_email)
        if (course != "") and (name != "") and (desc != ""):
            if addcourse(course, name, desc) == 1:
                flash('Course successfully added', 'Success')
            else:
                flash('Unable to add course', 'Error')
                redirect(url_for('Admin'))
        # intrinsically makes sure that all professor entries must be assigned to a course
        if (course_id2 != "") and (prof_email != ""):
            if addteacher(course_id2, prof_email) == 1:
                flash('Professor successfully added', 'Success')
            else:
                flash('Unable to add course', 'Error')
                redirect(url_for('Admin'))
        if (course_id3 != "") and (stud_email != "") and (sec_no != ""):
            if addstud(course_id3, sec_no, stud_email) == 1:
                flash('Student successfully added', 'Success')
            elif addstud(course_id3, sec_no, stud_email) == 0:
                flash('Class is full! try a different section', 'Error')
            else:
                flash('Unable to add course', 'Error')
                redirect(url_for('Admin'))

    return render_template("Admin.html", url=host, form=form)


#not sure what to do with capstone tables
def create_users():
    conn = sql.connect('database.db')
    cur = conn.cursor()
    cur.execute('DROP TABLE IF EXISTS Department')
    cur.execute('DROP TABLE IF EXISTS Course')
    cur.execute('DROP TABLE IF EXISTS Students')
    cur.execute('DROP TABLE IF EXISTS Zipcode')
    cur.execute('DROP TABLE IF EXISTS Professors')
    cur.execute('DROP TABLE IF EXISTS Sections')
    cur.execute('DROP TABLE IF EXISTS Sections2')
    cur.execute('DROP TABLE IF EXISTS Sections3')
    cur.execute('DROP TABLE IF EXISTS Homework')
    cur.execute('DROP TABLE IF EXISTS Homework_grades')
    cur.execute('DROP TABLE IF EXISTS Exams')
    cur.execute('DROP TABLE IF EXISTS Exam_grades')
    cur.execute('DROP TABLE IF EXISTS Enrolls')
    cur.execute('DROP TABLE IF EXISTS Prof_team_members')
    cur.execute('DROP TABLE IF EXISTS Capstone_section')
    cur.execute('DROP TABLE IF EXISTS Capstone_Team')
    cur.execute('DROP TABLE IF EXISTS Capstone_Team_Members')
    cur.execute('DROP TABLE IF EXISTS Capstone_grades')
    cur.execute('CREATE TABLE IF NOT EXISTS Students(email TEXT, password TEXT, name TEXT, age INT, gender TEXT, major TEXT, street TEXT, zipcode INT);')
    cur.execute('CREATE TABLE IF NOT EXISTS Zipcode(zipcode INT, city TEXT, state TEXT);')
    ParseStudent(cur)
    cur.execute('CREATE TABLE IF NOT EXISTS Professors(email TEXT, password TEXT, name TEXT, age INT, gender TEXT, office_address TEXT, department TEXT, title TEXT);')
    ParseProfessor(cur)
    cur.execute('CREATE TABLE IF NOT EXISTS Department(dept_id TEXT, dept_name TEXT, dept_head TEXT);')
    ParseDept(cur)
    cur.execute('CREATE TABLE IF NOT EXISTS Course(course_id TEXT, course_name TEXT, course_description TEXT);')
    ParseCourse(cur)
    cur.execute('CREATE TABLE IF NOT EXISTS Sections(course_id TEXT, sec_no INT, section_type TEXT, seats INT, prof_team_id INT);')
    cur.execute('CREATE TABLE IF NOT EXISTS Sections2(course_id TEXT, sec_no INT, section_type TEXT, seats INT, prof_team_id INT);')
    cur.execute('CREATE TABLE IF NOT EXISTS Sections3(course_id TEXT, sec_no INT, section_type TEXT, seats INT, prof_team_id INT);')
    ParseSection(cur)
    # Checks course1 course2 and course3 for unique values, and compiles a cumulative table of all unique classes and sections
    # just so happens that there is nothing unique between course+section 1, 2, and 3
    cur.execute('SELECT S.course_id, S.sec_no, S.section_type, S.seats, S.prof_team_id FROM Sections S LEFT JOIN Sections2 S2 USING(course_id) UNION ALL SELECT S2.course_id, S2.sec_no, S2.section_type, S2.seats, S2.prof_team_id FROM Sections2 S2 LEFT JOIN Sections S USING(course_id) WHERE S.course_id IS NULL OR S2.course_id IS NULL;')
    cur.execute('SELECT S.course_id, S.sec_no, S.section_type, S.seats, S.prof_team_id FROM Sections S LEFT JOIN Sections3 S3 USING(course_id) UNION ALL SELECT S3.course_id, S3.sec_no, S3.section_type, S3.seats, S3.prof_team_id FROM Sections3 S3 LEFT JOIN Sections S USING(course_id) WHERE S.course_id IS NULL OR S3.course_id IS NULL;')
    cur.execute('DROP TABLE IF EXISTS Sections3')
    cur.execute('DROP TABLE IF EXISTS Sections2')

    cur.execute('CREATE TABLE IF NOT EXISTS Enrolls(student_email TEXT, course_id TEXT, sec_no INT);')
    ParseEnrolls(cur)
    #Going to ignore Prof_teams table because Prof_team_members seems to achieve the same thing
    cur.execute('CREATE TABLE IF NOT EXISTS Prof_team_members(prof_email TEXT, teaching_team_id INT)')
    ParseProfTID(cur)


    cur.execute('CREATE TABLE IF NOT EXISTS Homework(course_id TEXT, sec_no INT, hw_no INT, hw_details TEXT);')
    ParseHW(cur)

    cur.execute('CREATE TABLE IF NOT EXISTS Homework_grades(student_email TEXT, course_id TEXT, sec_no INT, hw_no INT, grade INT);')
    ParseHWgrades(cur)

    cur.execute('CREATE TABLE IF NOT EXISTS Exams(course_id TEXT, sec_no INT, exam_no INT, exam_details TEXT);')
    ParseExams(cur)

    cur.execute('CREATE TABLE IF NOT EXISTS Exam_grades(student_email TEXT, course_id TEXT, sec_no INT, exam_no INT, grade INT);')
    ParseExamgrades(cur)

    cur.execute('CREATE TABLE IF NOT EXISTS Capstone_section(course_id TEXT, sec_no INT, project_no INT, sponsor_id INT);')
    cur.execute('CREATE TABLE IF NOT EXISTS Capstone_Team(course_id TEXT, sec_no INT, team_id INT, project_no INT);')
    cur.execute('CREATE TABLE IF NOT EXISTS Capstone_Team_Members(student_email TEXT, team_id INT, course_id TEXT, sec_no INT);')
    cur.execute('CREATE TABLE IF NOT EXISTS Capstone_grades(course_id TEXT, sec_no INT, grade INT);')


    conn.commit()
    cur.close()
    conn.close()
    return


def addcourse(course_id, course_name, course_desc):
    conn = sql.connect('database.db')
    cur = conn.cursor()
    cur.execute('INSERT INTO Course(course_id, course_name, course_description) VALUES (?,?,?)', (course_id, course_name, course_desc))
    conn.commit()
    return 1


def addstud(course_id, sec_no, stud_email):
    conn = sql.connect('database.db')
    cur = conn.cursor()
    cur.execute('SELECT c, s, ct, l '
                'FROM ('
                'SELECT course_id c, sec_no s, COUNT(sec_no) AS ct, l '
                'FROM Enrolls E '
                'JOIN (SELECT course_id c2, sec_no s2, seats l '
                'FROM Sections S) '
                'ON c2=c AND s2=s '
                'GROUP BY c, s '
                'HAVING COUNT(sec_no) < l) '
                'WHERE c=? AND s=?', (course_id, int(sec_no),))
    conn.commit()
    options = cur.fetchall()
    if len(options) == 0:
        return 0
    else:
        cur.execute('INSERT INTO Enrolls(student_email, course_id, sec_no) VALUES (?,?,?)', (stud_email, course_id, sec_no))
        conn.commit()
    return 1


def addteacher(course_id, prof_email):
    conn = sql.connect('database.db')
    cur = conn.cursor()
    cur.execute('SELECT course_id c, prof_team_id p, e '
                'FROM Sections S '
                'JOIN (SELECT prof_email e, teaching_team_id t '
                'FROM Prof_team_members M) '
                'ON p=t '
                'WHERE c=?', (course_id,))
    conn.commit()
    dump = cur.fetchall()
    cur.execute('INSERT INTO Prof_team_members(prof_email, teaching_team_id) VALUES (?,?)', (prof_email, dump[0][1]))
    conn.commit()

    return 1

def update_password(email, password):
    conn = sql.connect('database.db')
    cur = conn.cursor()
    cur.execute('UPDATE Students SET password = ? WHERE email = ?', (password, email,))
    conn.commit()
    return


def query_personal(username):
    conn = sql.connect('database.db')
    cur = conn.cursor()
    cur.execute('SELECT age a, email e, gender g, major m FROM Students S WHERE email=?', (username,))
    conn.commit()
    stuff=cur.fetchone()
    age=str(stuff[0])
    email=str(stuff[1])
    gender=str(stuff[2])
    major=str(stuff[3])
    return email, age, gender, major


def query_Addr(username):
    conn = sql.connect('database.db')
    cur = conn.cursor()
    cur.execute('SELECT street s, c, es, zipcode z '
                'FROM Students S '
                'JOIN(SELECT zipcode z2, city c, state es FROM zipcode Z) '
                'ON z=z2 '
                'WHERE S.email=?', (username,))
    conn.commit()
    return cur.fetchone()


def query_name(username):
    conn = sql.connect('database.db')
    cur = conn.cursor()
    cur.execute('SELECT name n FROM Students S WHERE email=?',(username,))
    conn.commit()
    name = cur.fetchone()[0]
    name = name.strip()
    return name


def query_grades(username):
    conn = sql.connect('database.db')
    cur = conn.cursor()
    cur.execute('SELECT student_email se, course_id c, hw_no h, grade g FROM Homework_grades H WHERE se=? GROUP BY se, c;', (username,))
    conn.commit()
    homework = cur.fetchall()
    cur.execute('SELECT student_email se, course_id c, exam_no e, grade g FROM Exam_grades E WHERE se=? GROUP BY se, c;',(username,))
    conn.commit()
    exam = cur.fetchall()
    print(homework, exam)
    send=[]
    for i in exam:
        classn = i[1]
        number = i[2]
        grade = i[3]
        for j in homework:
            if j[1] == classn:
                cur.execute('SELECT course_id c, hw_no h, AVG(grade), MIN(grade), MAX(grade) '
                            'FROM Homework_grades '
                            'WHERE c=? AND h=?'
                            'GROUP BY h', (j[1], j[2],))
                conn.commit()
                minmax = cur.fetchall()
                minmax=minmax[0]
                #print(minmax)
                minmax=(math.floor(minmax[2]*100)/100, minmax[3], minmax[4])
                #print(minmax)
                element = j + (minmax, number, grade)
                cur.execute('SELECT course_id c, exam_no h, AVG(grade), MIN(grade), MAX(grade) '
                            'FROM Exam_grades '
                            'WHERE c=? AND h=? '
                            'GROUP BY h', (classn, number,))
                conn.commit()
                minmax2 = cur.fetchall()
                print(minmax2)
                minmax2 = minmax2[0]
                # print(minmax2)
                minmax2 = (math.floor(minmax2[2] * 100) / 100, minmax2[3], minmax2[4])
                element = element + (minmax2,)
        send.append(element)
    #Capstone classes
    if len(homework) > len(exam):
        check = []
        for i in range(len(homework)):
            check.append(homework[i][1])
        for j in range(len(exam)):
            check.remove(exam[j][1])
        for i in homework:
            if i[1] == check[0]:
                cur.execute('SELECT course_id c, hw_no h, AVG(grade), MIN(grade), MAX(grade) '
                            'FROM Homework_grades '
                            'WHERE c=? AND h=?'
                            'GROUP BY h', (i[1], i[2],))
                conn.commit()
                minmax = cur.fetchall()

                element = i + (minmax2,)
                element = element+("NA","NA","NA")
                send.append(element)

    average1=0
    average2=0
    check=0
    letters=[]
    for i in send:
        average1+=int(i[3])
        if i[5] != "NA":
            average2+=int(i[6])
            letters.append((int(i[3])+int(i[6]))/2)
            check+=1
        else:
            letters.append("NA")
    if len(send) != 0:
        average1 = math.floor((average1/len(send))*100)/100
        average2 = math.floor((average2/check)*100)/100
    finals=[]
    for i in letters:
        if i == "NA":
            letter = "NA"
        elif int(i) > 93:
            letter = 'A'
        elif int(i) > 90:
            letter = 'A-'
        elif int(i) > 86:
            letter = 'B+'
        elif int(i) > 83:
            letter = 'B'
        elif int(i) > 80:
            letter = 'B-'
        elif int(i) > 76:
            letter = 'C+'
        elif int(i) >= 70:
            letter = "C"
        elif int(i) >= 60:
            letter = "D"
        else:
            letter = "F"
        finals.append(letter)
    for i in range(len(send)):
        send[i] = send[i]+(finals[i],)
    return send, average1, average2


def query_courses(username):
    conn = sql.connect('database.db')
    cur = conn.cursor()
    cur.execute('SELECT student_email se, course_id c, sec_no n, en, d, pe, n, o '
                'FROM Enrolls E '
                'JOIN( SELECT course_id, sec_no, course_description d, course_name en, pe, n, o '
                'FROM Course C '
                'JOIN (SELECT course_id, sec_no, prof_team_id ps, pe, n, o '
                'FROM Sections S '
                'JOIN (SELECT prof_email pe, teaching_team_id pt, n, o '
                'FROM Prof_team_members P '
                'JOIN (SELECT name n, office_address o, email e '
                'FROM Professors) '
                'ON e=pe) '
                'ON ps=pt) '
                'USING (course_id)) '
                'USING(course_id, sec_no) WHERE se=? GROUP BY se, c;', (username,))
    conn.commit()
    #print(cur.fetchall())
    return cur.fetchall()


#binary search?
def valid_login(username, password):
    conn = sql.connect('database.db')
    cur = conn.cursor()
    cur.execute('SELECT email, password FROM Students WHERE email=?', (username,))
    conn.commit()
    db = cur.fetchone()

    cur.execute('SELECT email, password FROM Professors WHERE email=?', (username,))
    conn.commit()
    db2 = cur.fetchone()

    tell = username.split("@")

    #encrypt user entered password
    paddr = hashlib.md5(password.encode())
    password = paddr.hexdigest()

    # admin
    if tell[0] == 'admin':
        return 3
    # student
    elif len(tell[0]) > 3:
        # user/pass not found in database
        if db is None:
            cur.close()
            conn.close()
            return 0
        elif password == db[1]:
            cur.close()
            conn.close()
            return 1
        else:
            cur.close()
            conn.close()
            return 2
    #faculty
    else:
        # user/pass not found in database
        if db2 is None:
            cur.close()
            conn.close()
            return 0
        elif password == db2[1]:
            cur.close()
            conn.close()
            return 1
        else:
            cur.close()
            conn.close()
            return 2


class Username:
    def __init__(self, user=""):
        self._user = user

    def get_user(self):
        return self._user

    def set_user(self, x):
        self._user = x

#unused
def view_students():
    conn = sql.connect('database.db')
    cur = conn.cursor()
    cur.execute("SELECT * FROM Students;")
    for (email) in cur:
        print(email)


if (__name__ == '__main__'):
    create_users()
    app.secret_key='test_session'
    #view_students()
    usr = Username()
    app.run(debug=True)