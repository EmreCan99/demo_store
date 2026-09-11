"""
models.py

This file defines Python classes that mirror your SQL tables.
This is SQLAlchemy's "ORM" layer -- similar to a Sequelize or Prisma model in Node.js.
Once defined, you can query/insert/update rows using Python objects instead of
writing raw SQL strings everywhere.
"""

from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.orm import declarative_base

# declarative_base() gives us a base class that all our table models will inherit from.
# SQLAlchemy uses this to keep track of every table we define.
Base = declarative_base()


class Employee(Base):
    # __tablename__ tells SQLAlchemy which existing SQL table this class maps to.
    # This MUST match the table name you already created in 001_create_employees.sql
    __tablename__ = "employees"

    # Each Column() below matches one column in your existing employees table.
    # primary_key=True marks this as the unique ID column (same as INTEGER PRIMARY KEY in SQL)
    id = Column(Integer, primary_key=True)

    # These map directly to the TEXT columns in your SQL schema
    first_name = Column(String, nullable=False)  # nullable=False = same as "NOT NULL" in SQL
    last_name = Column(String, nullable=False)
    department = Column(String)

    # Maps to the REAL column in SQL -- Float is Python/SQLAlchemy's equivalent
    salary = Column(Float)

    # This isn't a database column -- it's just a helper so that if you ever
    # print an Employee object directly, it shows something readable instead
    # of a generic memory address. Purely for your own debugging convenience.
    def __repr__(self):
        return f"<Employee {self.first_name} {self.last_name} - {self.department}>"