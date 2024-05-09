import sqlite3
import json
from models import Comments

class Comments():
    def __init__(self, id, author_id, post_id, content):
        self.id = id
        self.author_id = author_id
        self.post_id = post_id
        self.content = content

COMMENTS = [
  {
    "id": 1,
    "authorId": 1,
    "postId": 1,
    "content": "content test 1" 
  },
  {
    "id": 2,
    "authorId": 2,
    "postId": 2,
    "content": "content test 2" 
  },
  {
   "id": 3,
    "authorId": 3,
    "postId": 3,
    "content": "content test 3"  
  },
  {
    "id": 4,
    "authorId": 4,
    "postId": 4,
    "content": "content test 4" 
  },
]
def create_comment(comment):
    # Get the id value of the last customer in the list
    max_id = COMMENTS[-1]["id"]

    # Add 1 to whatever that number is
    new_id = max_id + 1

    # Add an `id` property to the customer dictionary
    comment["id"] = new_id

    # Add the customer dictionary to the list
    COMMENTS.append(comment)

    # Return the dictionary with `id` property added
    return comment
  
  
def get_all_comments():
    with sqlite3.connect("./db.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()
        db_cursor.execute("""
            SELECT                  
                a.id,
                a.author_id,
                a.post_id,
                a.content
            FROM Comments a
        """)
        
        comments = []
        dataset = db_cursor.fetchall()
        
        for row in dataset:
            comment = Comments(row['id'], 
                              row['author_id'], 
                              row['post_id'], 
                              row['content'])
            comments.append(comment.__dict__)
          
    return comments    

def get_comment_by_id(comment_id):
    with sqlite3.connect("./db.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute("""
        SELECT                  
            a.id,
            a.author_id,
            a.post_id,
            a.content
        FROM Comments a
        WHERE a.id = ?
        """, (comment_id,))
        
        row = db_cursor.fetchone()
        if row:
            comment = Comments(row['id'], 
                              row['author_id'], 
                              row['post_id'], 
                              row['content'])
            return comment.__dict__
        else:
            return None

def delete_comment(id):
    with sqlite3.connect("./db.sqlite3") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        DELETE FROM Comments
        WHERE id = ?
        """, (id, ))

def update_comment(id, new_comment):
    with sqlite3.connect("./db.sqlite3") as conn:
        db_cursor = conn.cursor()
      
        db_cursor.execute("""
            UPDATE Comments
            SET
                author_id = ?,
                post_id = ?,
                content = ?
            WHERE id = ?
        """, (new_comment['author_id'], 
              new_comment['post_id'], 
              new_comment['content'], id))

        # Check if any rows were affected
        rows_affected = db_cursor.rowcount

    # Return value indicating success or failure
    return rows_affected > 0
