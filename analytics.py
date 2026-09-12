"""
analytics.py

Data processing and chart generation, kept separate from main.py so that
routing logic (main.py) doesn't get tangled up with data logic (this file).
This also means you could reuse these functions elsewhere later --
e.g. in a Jupyter notebook, a scheduled report script, or a test file --
without needing FastAPI running at all.
"""

import pandas as pd
import plotly.express as px


def average_salary_by_department(employees):
    """
    Takes a list of Employee objects, returns a Plotly chart (as HTML)
    showing average salary per department.
    """
    df = pd.DataFrame(
        [{"department": e.department, "salary": e.salary} for e in employees]
    )

    avg_salary_by_dept = df.groupby("department", as_index=False)["salary"].mean()

    fig = px.bar(
        avg_salary_by_dept,
        x="department",
        y="salary",
        title="Average Salary by Department",
    )

    return fig.to_html(full_html=False)