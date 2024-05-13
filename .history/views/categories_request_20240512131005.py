import sqlite3
import json
from models import Categories

def get_all_categories():
    with sqlite3.connect("./db.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()
        db_cursor.execute("""
            SELECT                  
                id,
                label
            FROM Categories
        """) 
        
        categories = []
        dataset = db_cursor.fetchall()
        
        for row in dataset:
            category = Categories(row['id'], row['label'])
            categories.append(category.__dict__)
    
    return categories

def get_single_category(category_id):
    with sqlite3.connect("./db.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute("""
        SELECT                  
            id,
            label
        FROM Categories
        WHERE id = ?
        """, (category_id,))
        
        row = db_cursor.fetchone()
        if row:
            category = Categories(row['id'], row['label'])
            return category.__dict__
        else:
            return None

def delete_category(category_id):
    with sqlite3.connect("./db.sqlite3") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        DELETE FROM Categories
        WHERE id = ?
        """, (category_id, ))

def create_category(category):
    with sqlite3.connect("./db.sqlite3") as conn:
        db_cursor = conn.cursor()

        # Get the maximum id from the database
        db_cursor.execute("SELECT MAX(id) FROM Categories")
        max_id = db_cursor.fetchone()[0]

        # Calculate the new id
        new_id = max_id + 1 if max_id else 1

        # Add the id to the category dictionary
        category["id"] = new_id

        # Insert the category into the database
        db_cursor.execute("""
            INSERT INTO Categories (id, label)
            VALUES (?, ?)
        """, (new_id, category["label"]))

    return category
   