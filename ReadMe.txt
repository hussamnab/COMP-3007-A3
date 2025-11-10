COMP 3007 – Assignment 3
Author: Hussam Nabtiti 101267733
Project: PostgreSQL CRUD Application


OVERVIEW

This project demonstrates how to connect a Python application to a PostgreSQL database and perform CRUD (Create, Read, Update, Delete) operations on a "students" table.

The database is built and populated automatically using the provided "schema.sql" file.
The Python application (main.py) performs all CRUD operations directly through PostgreSQL.


SETUP INSTRUCTIONS


1) Build and Populate the Table
--------------------------------
psql -h 127.0.0.1 -p 5432 -U students_user -d students_db -f "db\schema.sql"

2) Verify Initial Data
--------------------------------
psql -h 127.0.0.1 -p 5432 -U students_user -d students_db -c "SELECT * FROM students;"

------------------------------------------------------------
APPLICATION FUNCTIONS
------------------------------------------------------------
The application (main.py) provides the following functions:

getAllStudents():
    Retrieves and displays all records from the students table.

Command:
python app\main.py get-all

addStudent(first_name, last_name, email, enrollment_date):
    Inserts a new student record.

Command:
python app\main.py add --first "Hussam" --last "Nabtiti" --email "hussam.nabtiti@example.com" --date 2023-09-04

updateStudentEmail(student_id, new_email):
    Updates the email address of a student by ID.

Command:
python app\main.py update-email --id 1 --email "john.doe+updated@example.com"

deleteStudent(student_id):
    Deletes a student record by ID.

Command
python app\main.py delete --id 3

------------------------------------------------------------
VIDEO DEMONSTRATION
------------------------------------------------------------

Video Link: https://youtu.be/6UjZsZdxUy8

