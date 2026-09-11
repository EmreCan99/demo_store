import sqlite3

# Connect creates the file if it doesn't exist yet
conn = sqlite3.connect("store.db")
cursor = conn.cursor()

# Create a simple employees table to start with
cursor.execute("""
CREATE TABLE IF NOT EXISTS employees (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    department TEXT,
    salary REAL
)
""")

# Manually add a few rows so you can see it working
employees = [
    ("Ragnar", "Lodbrok", "King", 5200),
    ("Michael", "Scott", "Manager", 1200),
    ("Bruce", "Wayne", "IT", 3200),
]

cursor.executemany(
    "INSERT INTO employees (first_name, last_name, department, salary) VALUES (?, ?, ?, ?)",
    employees
)

conn.commit()

# Verify: read back what we just inserted
print("Rows currently in employees table:")
for row in cursor.execute("SELECT * FROM employees"):
    print(row)

conn.close()
print("\nDone. Check for a new file called store.db in this folder.")