import sqlite3

connection = sqlite3.connect('example.db')

#Creates a table in the file if it doesn't already exist
connection.execute('''CREATE TABLE IF NOT EXISTS users
                 (id INTEGER PRIMARY KEY, 
                hunger INTEGER, 
                happiness INTEGER,
                energy INTEGER)''')

#Inserts data into the table
connection.execute("INSERT INTO users (hunger, happiness, energy) VALUES (5, 7, 8)")

#Writes data to the file
connection.commit()

#Retrieves data from the table
cursor = connection.execute("SELECT * FROM users")
for row in cursor:
    print(f"id: {row[0]}, hunger: {row[1]}, happiness: {row[2]}, energy: {row[3]}")

#Closes the connection to the file
connection.close()