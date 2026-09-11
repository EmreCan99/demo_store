"""
Seed the employees table with fake data.
Run this AFTER the schema exists (i.e. after 001_create_employees.sql has been applied).

First time setup:
    pip install faker
    pip freeze > requirements.txt   (run from project root, to lock the version)

Usage:
    python database/seed_data.py
"""

import sqlite3
from faker import Faker

DB_PATH = "store.db"
NUM_EMPLOYEES = 10  # bump this up later once you want more realistic volumes

departments = ["Sales", "IT", "Marketing", "Finance", "HR", "Operations"]

fake = Faker()


def seed_employees(cursor, count):
    employees = []
    for _ in range(count):
        first_name = fake.first_name()
        last_name = fake.last_name()
        department = fake.random_element(elements=departments)
        salary = round(fake.random_int(min=40000, max=95000), -2)  # round to nearest 100
        employees.append((first_name, last_name, department, salary))

    cursor.executemany(
        "INSERT INTO employees (first_name, last_name, department, salary) VALUES (?, ?, ?, ?)",
        employees,
    )


def main():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    seed_employees(cursor, NUM_EMPLOYEES)
    conn.commit()

    print(f"Inserted {NUM_EMPLOYEES} fake employees.\n")
    print("Current employees table:")
    for row in cursor.execute("SELECT * FROM employees"):
        print(row)

    conn.close()


if __name__ == "__main__":
    main()