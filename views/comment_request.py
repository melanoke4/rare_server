import sqlite3
import json

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

def get_all_comments():
    with sqlite3.connect("./rare.sqlite3") as conn:
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
    with sqlite3.connect("./rare.sqlite3") as conn:
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
