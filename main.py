# entry point for the server
"""
main.py

This is your application's entry point -- equivalent to app.js or index.js
in a Node/Express project. Running this file (via uvicorn) starts your web server.

Run it with:
    uvicorn main:app --reload

Then visit:
    http://localhost:8000/docs       -> interactive API docs (like Postman, built in)
    http://localhost:8000/employees  -> raw JSON data
    http://localhost:8000/dashboard  -> HTML dashboard with a chart
"""

from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import pandas as pd
import plotly.express as px
from fastapi.responses import Response
from analytics import average_salary_by_department


from models import Employee, Base  # our table model from models.py

# ---------------------------------------------------------------------------
# 1. DATABASE CONNECTION
# ---------------------------------------------------------------------------

# This is the equivalent of a DB connection string in a Node app.
# "sqlite:///store.db" tells SQLAlchemy: use SQLite, and the file is store.db
# in the same folder as this script.
engine = create_engine("sqlite:///store.db")

# Base.metadata.create_all() checks if the tables defined in models.py already
# exist in store.db -- if they do (which they should, since you already ran
# 001_create_employees.sql), it does nothing. This line is just a safety net.
Base.metadata.create_all(engine)

# sessionmaker() creates a factory for "sessions" -- a session is basically
# one conversation with the database (open it, do some queries, close it).
# This is roughly equivalent to opening a connection/client in a Node DB library.
SessionLocal = sessionmaker(bind=engine)


def get_db_session():
    """
    Small helper that opens a new database session, hands it to whichever
    route needs it, and guarantees it gets closed afterward -- even if
    something goes wrong. This pattern (open, yield, close) is common in FastAPI.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ---------------------------------------------------------------------------
# 2. APP SETUP
# ---------------------------------------------------------------------------

# This creates your actual FastAPI application object -- equivalent to
# "const app = express()" in a Node project. Every route gets attached to this.
app = FastAPI()

# Jinja2Templates tells FastAPI where to find your HTML template files.
# This is the same idea as app.set('view engine', 'ejs') in Express.
templates = Jinja2Templates(directory="templates")


@app.get("/favicon.ico")
def favicon():
    return Response(status_code=204)  # 204 = "no content", not an error



# ---------------------------------------------------------------------------
# 3. JSON API ROUTE
# ---------------------------------------------------------------------------

@app.get("/employees")
def get_employees():
    """
    Equivalent of:  app.get('/employees', (req, res) => { ... res.json(data) })

    @app.get("/employees") is a "decorator" -- it tells FastAPI
    "run this function whenever someone makes a GET request to /employees".
    """
    db = SessionLocal()

    # This line queries ALL rows from the employees table.
    # It's the SQLAlchemy equivalent of: SELECT * FROM employees;
    employees = db.query(Employee).all()

    db.close()

    # FastAPI automatically converts the list of Employee objects into JSON
    # for us, but we build a clean list of dictionaries ourselves here so we
    # control exactly which fields get sent back.
    return [
        {
            "id": e.id,
            "first_name": e.first_name,
            "last_name": e.last_name,
            "department": e.department,
            "salary": e.salary,
        }
        for e in employees
    ]


# ---------------------------------------------------------------------------
# 4. HTML DASHBOARD ROUTE
# ---------------------------------------------------------------------------


@app.get("/dashboard")
def dashboard(request: Request):
    db = SessionLocal()
    employees = db.query(Employee).all()
    db.close()

    chart_html = average_salary_by_department(employees)

    return templates.TemplateResponse(
        request,
        "dashboard.html",
        {"chart_html": chart_html},
    )