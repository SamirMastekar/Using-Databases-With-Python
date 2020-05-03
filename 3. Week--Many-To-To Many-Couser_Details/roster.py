import json
import sqlite3

conn = sqlite3.connect('myResult.sqlite')
cur = conn.cursor()

# Do some setup
cur.executescript('''
DROP TABLE IF EXISTS User;
DROP TABLE IF EXISTS Member;
DROP TABLE IF EXISTS Course;

CREATE TABLE User (
    id     INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    name   TEXT UNIQUE
);

CREATE TABLE Course (
    id     INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    title  TEXT UNIQUE
);

CREATE TABLE Member (
    user_id     INTEGER,
    course_id   INTEGER,
    role        INTEGER,
    PRIMARY KEY (user_id, course_id)
)
''')

fname = input('Enter file name: ')
if len(fname) < 1:
    fname = 'roster.json'

# [
#   [ "Charley", "si110", 1 ],
#   [ "Mea", "si110", 0 ],

str_data = open(fname).read()
json_data = json.loads(str_data)

#PART 3: INSERTING DATA
for entry in json_data:
    user = entry[0]
    course = entry[1]
    instructor = entry[2]

    #Inserting user
    user_statement = """INSERT OR IGNORE INTO User(name) VALUES( ? )"""
    SQLparams = (user, )
    cur.execute(user_statement, SQLparams)

    #Inserting course
    course_statement = """INSERT OR IGNORE INTO Course(title) VALUES( ? )"""
    SQLparams = (course, )
    cur.execute(course_statement, SQLparams)

    userID_statement = """SELECT id FROM User WHERE name = ?"""
    SQLparams = (user, )
    cur.execute(userID_statement, SQLparams)
    userID = cur.fetchone()[0]
    
    #Getting user and course id
    courseID_statement = """SELECT id FROM Course WHERE title = ?"""
    SQLparams = (course, )
    cur.execute(courseID_statement, SQLparams)
    courseID = cur.fetchone()[0]

    #Inserting the entry
    member_statement = """INSERT OR IGNORE INTO Member(user_id, course_id, role) VALUES(?, ?, ?)"""
    SQLparams = (userID, courseID, instructor)
    cur.execute(member_statement, SQLparams)

#Saving the changes
conn.commit()

#PART 4: Testing and obtaining the results
test_statement = """SELECT hex(User.name || Course.title || Member.role ) AS X FROM 
    User JOIN Member JOIN Course 
    ON User.id = Member.user_id AND Member.course_id = Course.id
    ORDER BY X
"""
cur.execute(test_statement)
result = cur.fetchone()
print("RESULT: " + str(result))

#Closing the connection
cur.close()
conn.close()
