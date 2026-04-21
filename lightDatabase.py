"""""
import sqlite3

def load_pet_data():
    cursor = connection.cursor()
    cursor.execute("SELECT hunger, happiness, energy FROM pet_stats WHERE id = 1")
    row = cursor.fetchone()

    cursor.execute("SELECT blueberry, raspberry, cookie FROM inventory WHERE id = 1")
    inv = cursor.fetchone()

    return row, inv

def save_pet_data(pet):
    cursor = connection.cursor()
    cursor.execute(""
        UPDATE pet_stats
        SET hunger=?, happiness=?, energy=?
        WHERE id=1
    "", (pet.hunger, pet.happiness, pet.energy))

    cursor.execute(""
        UPDATE inventory
        SET blueberry=?, raspberry=?, cookie=?
        WHERE id=1
    "", (
        pet.inventory["Blueberry"],
        pet.inventory["Raspberry"],
        pet.inventory["Cookie"]
    ))

    connection.commit()

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
"""
import sqlite3
import os

# -----------------------------
# DATABASE INITIALIZATION
# -----------------------------

DB_PATH = "petdata.db"

# Create connection (shared across module)
connection = sqlite3.connect(DB_PATH)
cursor = connection.cursor()

# -----------------------------
# TABLE CREATION
# -----------------------------

cursor.execute("""
CREATE TABLE IF NOT EXISTS pet_stats (
    username INTEGER PRIMARY KEY,
    hunger REAL NOT NULL,
    happiness REAL NOT NULL,
    energy REAL NOT NULL
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS inventory (
    username INTEGER PRIMARY KEY,
    blueberry INTEGER NOT NULL,
    raspberry INTEGER NOT NULL,
    cookie INTEGER NOT NULL
)
""")

connection.commit()

# -----------------------------
# LOAD FUNCTIONS
# -----------------------------

def load_pet_data(username):
    cursor = connection.cursor()

    cursor.execute("""
        SELECT hunger, happiness, energy
        FROM pet_stats
        WHERE username=?
    """, (username,))
    stats = cursor.fetchone()

    cursor.execute("""
        SELECT blueberry, raspberry, cookie
        FROM inventory
        WHERE username=?
    """, (username,))
    inv = cursor.fetchone()

    return stats, inv
# -----------------------------
# SAVE FUNCTIONS
# -----------------------------

def save_pet_data(username, pet):
    cursor = connection.cursor()

    cursor.execute("""
        UPDATE pet_stats
        SET hunger=?, happiness=?, energy=?
        WHERE username=?
    """, (pet.hunger, pet.happiness, pet.energy, username))

    cursor.execute("""
        UPDATE inventory
        SET blueberry=?, raspberry=?, cookie=?
        WHERE username=?
    """, (
        pet.inventory["Blueberry"],
        pet.inventory["Raspberry"],
        pet.inventory["Cookie"],
        username
    ))

    connection.commit()

# -----------------------------
# New USER MANAGEMENT
# -----------------------------
def ensure_user_exists(username):
    cursor = connection.cursor()

    # Pet stats
    cursor.execute("SELECT 1 FROM pet_stats WHERE username=?", (username,))
    if cursor.fetchone() is None:
        cursor.execute("""
            INSERT INTO pet_stats (username, hunger, happiness, energy)
            VALUES (?, 100, 100, 100)
        """, (username,))

    # Inventory
    cursor.execute("SELECT 1 FROM inventory WHERE username=?", (username,))
    if cursor.fetchone() is None:
        cursor.execute("""
            INSERT INTO inventory (username, blueberry, raspberry, cookie)
            VALUES (?, 7, 5, 3)
        """, (username,))

    connection.commit()

# -----------------------------
# OPTIONAL: CLOSE CONNECTION
# -----------------------------

def close_db():
    connection.close()