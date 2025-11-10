"""
app/main.py

A minimal Python application that connects to PostgreSQL and exposes CRUD functions
for the students table described in the assignment.

Usage examples (after setting environment variables; see README):

    # Get all students
    python app/main.py get-all

    # Add a student
    python app/main.py add --first "Hussam" --last "Nabtiti" --email "hussam.nabtiti@example.com" --date 2023-09-03

    # Update a student's email
    python app/main.py update-email --id 1 --email "new.email@example.com"

    # Delete a student
    python app/main.py delete --id 3
"""
import os
import sys
import argparse
from datetime import date
from typing import Optional, List, Tuple

import psycopg2
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv

env_path = os.path.join(os.path.dirname(__file__), ".env")
if os.path.exists(env_path):
    load_dotenv(env_path)


def get_conn():
    required_vars = ["PGHOST", "PGPORT", "PGUSER", "PGPASSWORD", "PGDATABASE"]
    missing = [v for v in required_vars if not os.getenv(v)]
    if missing:
        raise RuntimeError(f"Missing env vars: {', '.join(missing)}. "
                           f"Set them in your environment or app/.env")
    conn = psycopg2.connect(
        host=os.getenv("PGHOST"),
        port=int(os.getenv("PGPORT")),
        user=os.getenv("PGUSER"),
        password=os.getenv("PGPASSWORD"),
        dbname=os.getenv("PGDATABASE"),
    )
    return conn


def getAllStudents() -> List[dict]:
    """
    Retrieves and returns all records from the students table.
    """
    with get_conn() as conn:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute("SELECT student_id, first_name, last_name, email, enrollment_date FROM students ORDER BY student_id;")
            rows = cur.fetchall()
            return [dict(r) for r in rows]


def addStudent(first_name: str, last_name: str, email: str, enrollment_date: Optional[str] = None) -> int:
    """
    Inserts a new student record.
    Returns the new student_id.
    """
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO students (first_name, last_name, email, enrollment_date)
                VALUES (%s, %s, %s, %s)
                RETURNING student_id;
                """,
                (first_name, last_name, email, enrollment_date),
            )
            new_id = cur.fetchone()[0]
            conn.commit()
            return new_id


def updateStudentEmail(student_id: int, new_email: str) -> int:
    """
    Updates the email for a student by id.
    Returns the number of affected rows (0 or 1).
    """
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                UPDATE students
                SET email = %s
                WHERE student_id = %s;
                """,
                (new_email, student_id),
            )
            affected = cur.rowcount
            conn.commit()
            return affected


def deleteStudent(student_id: int) -> int:
    """
    Deletes the student with the given id.
    Returns the number of affected rows (0 or 1).
    """
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "DELETE FROM students WHERE student_id = %s;",
                (student_id,),
            )
            affected = cur.rowcount
            conn.commit()
            return affected


def print_table(rows: List[dict]) -> None:
    if not rows:
        print("(no rows)")
        return

    headers = rows[0].keys()
    widths = {h: len(h) for h in headers}
    for r in rows:
        for h in headers:
            widths[h] = max(widths[h], len(str(r[h])) if r[h] is not None else 0)

    def line(char="-"):
        print("+" + "+".join(char * (widths[h] + 2) for h in headers) + "+")

    # Header
    line("=")
    print("| " + " | ".join(f"{h:<{widths[h]}}" for h in headers) + " |")
    line("=")

    # Rows
    for r in rows:
        print("| " + " | ".join(f"{str(r[h]) if r[h] is not None else '':<{widths[h]}}" for h in headers) + " |")
    line("=")


def main():
    parser = argparse.ArgumentParser(description="PostgreSQL CRUD for students table")
    sub = parser.add_subparsers(dest="cmd", required=True)

    # get-all
    sub.add_parser("get-all", help="Retrieve and display all students")

    # add
    p_add = sub.add_parser("add", help="Insert a new student")
    p_add.add_argument("--first", required=True, help="First name")
    p_add.add_argument("--last", required=True, help="Last name")
    p_add.add_argument("--email", required=True, help="Email (unique)")
    p_add.add_argument("--date", required=False, help="Enrollment date (YYYY-MM-DD)")

    # update-email
    p_upd = sub.add_parser("update-email", help="Update a student's email by id")
    p_upd.add_argument("--id", type=int, required=True, help="student_id")
    p_upd.add_argument("--email", required=True, help="New email")

    # delete
    p_del = sub.add_parser("delete", help="Delete a student by id")
    p_del.add_argument("--id", type=int, required=True, help="student_id")

    args = parser.parse_args()

    try:
        if args.cmd == "get-all":
            rows = getAllStudents()
            print_table(rows)

        elif args.cmd == "add":
            new_id = addStudent(args.first, args.last, args.email, args.date)
            print(f"Inserted student_id={new_id}")
            rows = getAllStudents()
            print_table(rows)

        elif args.cmd == "update-email":
            affected = updateStudentEmail(args.id, args.email)
            print(f"Rows updated: {affected}")
            rows = getAllStudents()
            print_table(rows)

        elif args.cmd == "delete":
            affected = deleteStudent(args.id)
            print(f"Rows deleted: {affected}")
            rows = getAllStudents()
            print_table(rows)

    except Exception as e:
        print(f"ERROR: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
