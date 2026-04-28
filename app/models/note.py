from .db import get_db_connection
import sqlite3

class Note:
    @staticmethod
    def get_by_recipe(recipe_id):
        """
        取得指定食譜的所有筆記與評價。
        """
        try:
            conn = get_db_connection()
            items = conn.execute('SELECT * FROM notes WHERE recipe_id = ? ORDER BY created_at DESC', (recipe_id,)).fetchall()
            conn.close()
            return [dict(row) for row in items]
        except sqlite3.Error as e:
            print(f"資料庫錯誤: {e}")
            return []

    @staticmethod
    def create(recipe_id, content, rating=None):
        """
        為指定食譜新增一筆筆記與評價。
        """
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(
                'INSERT INTO notes (recipe_id, content, rating) VALUES (?, ?, ?)',
                (recipe_id, content, rating)
            )
            conn.commit()
            new_id = cursor.lastrowid
            conn.close()
            return new_id
        except sqlite3.Error as e:
            print(f"資料庫錯誤: {e}")
            return None
