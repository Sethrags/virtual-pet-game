# Filename: lightDatabase.py
# Author: Brent
# Description: This file handles all interactions with the SQLite database for the virtual pet game.
# It provides functions to initialize the database, load pet data, save pet data, and ensure user records exist.
# The database consists of two tables: pet_stats (for hunger, happiness, energy) and inventory (for food items).
# Note: The connection is shared across the file for simplicity, but in a larger application, 
# we would manage connections more robustly (e.g., using context managers or a connection pool).
#
import sqlite3
import os


# DATABASE INITIALIZATION
DB_PATH = "petdata.db"

# Create connection (shared across functions for simplicity)
connection = sqlite3.connect(DB_PATH)
cursor = connection.cursor()

# Table creation (if not exists)
cursor.execute("""
CREATE TABLE IF NOT EXISTS pet_stats (
    username TEXT PRIMARY KEY,
    hunger REAL NOT NULL,
    happiness REAL NOT NULL,
    energy REAL NOT NULL
)
""")

# Table for inventory (if not exists)
cursor.execute("""
CREATE TABLE IF NOT EXISTS inventory (
    username TEXT PRIMARY KEY,
    blueberry INTEGER NOT NULL,
    raspberry INTEGER NOT NULL,
    cookie INTEGER NOT NULL
)
""")
connection.commit() #commit changes to create base tables

# load_pet_data
# Load Pet Data from the database for a given username. Returns a tuple of (stats, inventory) where:
# - stats: is a tuple of (hunger, happiness, energy) or None if the user does not exist.
# - inventory: is a tuple of (blueberry, raspberry, cookie) or None if the user does not exist.
def load_pet_data(username):
    cursor = connection.cursor()

    # Fetch pet stats
    cursor.execute("""
        SELECT hunger, happiness, energy
        FROM pet_stats
        WHERE username=?
    """, (username,))
    stats = cursor.fetchone()

    # Fetch inventory
    cursor.execute("""
        SELECT blueberry, raspberry, cookie
        FROM inventory
        WHERE username=?
    """, (username,))
    inv = cursor.fetchone()

    return stats, inv # Return both stats and inventory as tuples, or None if user does not exist

# save_pet_data
# Save Pet Data to the database for a given username. 
# Takes a pet object with attributes hunger, happiness, energy, 
# and inventory (a dict with keys "Blueberry", "Raspberry", "Cookie").
def save_pet_data(username, pet):
    cursor = connection.cursor()

    # Update pet stats
    cursor.execute("""
        UPDATE pet_stats
        SET hunger=?, happiness=?, energy=?
        WHERE username=?
    """, (pet.hunger, pet.happiness, pet.energy, username))

    # Update inventory
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

    connection.commit() # Commit changes to save updates to the database

# Ensure_user_exists
# This function checks if a user record exists in both pet_stats and inventory tables.
# If not, it creates new records with default values (hunger=100, happiness=100, energy=100 for pet_stats 
# and 7 blueberries, 5 raspberries, 3 cookies for inventory).
def ensure_user_exists(username):
    cursor = connection.cursor()

    # Check if user exists in pet_stats, if not create new record with default values
    cursor.execute("SELECT 1 FROM pet_stats WHERE username=?", (username,))
    if cursor.fetchone() is None:
        cursor.execute("""
            INSERT INTO pet_stats (username, hunger, happiness, energy)
            VALUES (?, 100, 100, 100)
        """, (username,))

    # Check if user exists in inventory, if not create new record with default values
    cursor.execute("SELECT 1 FROM inventory WHERE username=?", (username,))
    if cursor.fetchone() is None:
        cursor.execute("""
            INSERT INTO inventory (username, blueberry, raspberry, cookie)
            VALUES (?, 7, 5, 3)
        """, (username,))

    connection.commit() # Commit changes to ensure new records are saved to the database

# close_db
# This function closes the database connection. 
# It should be called when the application is shutting down to ensure resources are properly released.
def close_db():
    connection.close() # Close the database connection when the application is done using it.