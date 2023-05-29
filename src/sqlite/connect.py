import sqlite3
from prettytable import PrettyTable

conn = sqlite3.connect('test.db')
cursor = conn.cursor()

# Enable column headers
cursor.execute("PRAGMA header = 1")

# Execute your query
cursor.execute("SELECT * FROM dbstat")

x = PrettyTable()
# Get the column names
x.field_names = [description[0] for description in cursor.description]

for row in cursor.fetchall():
    x.add_row(row)

print(x)

conn.close()

