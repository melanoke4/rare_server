import sqlite3
import json
from models import Posts

# class Posts():
#     def __init__(self, id, user_id, category_id, title, publication_date, image_url, content, approved):
#         self.id = id
#         self.user_id = user_id
#         self.category_id = category_id
#         self.title = title
#         self.publication_date = publication_date
#         self.image_url = image_url
#         self.content = content
#         self.approved = approved
        
POSTS = [
    {
        "id": 1,
        "user_id": 1,
        "category_id": 1,
        "title": "title1",
        "publication_date": "01012021",
        "image_url": "img.url",
        "content": "content1",
        "approved": "approved"
    },
    {
        "id": 2,
        "user_id": 2,
        "category_id": 1,
        "title": "title2",
        "publication_date": "01012021",
        "image_url": "img.url",
        "content": "content2",
        "approved": "approved"
    },
    {
        "id": 3,
        "user_id": 3,
        "category_id": 1,
        "title": "title3",
        "publication_date": "01012021",
        "image_url": "img.url",
        "content": "content3",
        "approved": "approved"
    }
]

def create_post(new_post):
    with sqlite3.connect("./db.sqlite3") as conn:
        db_cursor = conn.cursor()
        
        db_cursor.execute("""
        INSERT INTO Posts
            ( user_id, category_id, title, publication_date, image_url, content, approved)
        VALUES
            ( ?, ?, ?, ?, ?, ?, ?);
        """, (new_post['user_id'], 
              new_post['category_id'], 
              new_post['title'], 
              new_post['publication_date'], 
              new_post['image_url'], 
              new_post['content'],
              new_post['approved'] ))
        
        id = db_cursor.lastrowid
        
        new_post['id'] = id
        
    return new_post
        
def delete_post(id):
    with sqlite3.connect("./db.sqlite3") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        DELETE 
        FROM Posts
        WHERE id = ?
        """, (id, ))
        
def update_post(id, new_post):
    with sqlite3.connect("./db.sqlite3") as conn:
        db_cursor = conn.cursor()
        db_cursor.execute("""
        UPDATE Posts
            SET 
                user_id = ?,
                category_id = ?,
                title = ?,
                publication_date = ?,
                image_url = ?,
                content = ?
        WHERE id = ?
        """, (new_post['user_id'], 
              new_post['category_id'], 
              new_post['title'], 
              new_post['publication_date'], 
              new_post['image_url'], 
              new_post['content'], 
              new_post['approved'], 
              id, ))
        
        rows_affected = db_cursor.rowcount
        
        if rows_affected == 0:
            return False
        else: 
            return True
        
def get_single_post(id):
    with sqlite3.connect("./db.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()
        
        db_cursor.execute("""
        SELECT
            p.id,
            p.user_id,
            p.category_id,
            p.title,
            p.publication_date,
            p.image_url,
            p.content,
            p.approved
        FROM Posts p
        WHERE p.id = ?
        """, ( id, ))
        
        data = db_cursor.fetchone()
        
        post = Posts(data['id'],
                     data['user_id'],
                     data['category_id'],
                     data['title'],
                     data['publication_date'],
                     data['image_url'],
                     data['content'],
                     data['approved'])
        
        return post.__dict__
    
def get_all_posts():
    with sqlite3.connect("./db.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()
        db_cursor.execute("""
        SELECT
            p.id,
            p.user_id,
            p.category_id,
            p.title,
            p.publication_date,
            p.image_url,
            p.content,
            p.approved
        FROM Posts p
        """)
        
        posts = []
        dataset = db_cursor.fetchall()
        
        for row in dataset:
            post = Posts(row['id'], 
                         row['user_id'], 
                         row['category_id'], 
                         row['title'], 
                         row['publication_date'],
                         row['image_url'], 
                         row['content'], 
                         row['approved'])
            posts.append(post.__dict__)

    return posts
        