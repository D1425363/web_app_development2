from .db import get_db_connection
import sqlite3

class Recipe:
    @staticmethod
    def get_all():
        """
        取得所有食譜。
        """
        try:
            conn = get_db_connection()
            recipes = conn.execute('SELECT * FROM recipes ORDER BY created_at DESC').fetchall()
            conn.close()
            return [dict(row) for row in recipes]
        except sqlite3.Error as e:
            print(f"資料庫錯誤: {e}")
            return []

    @staticmethod
    def get_by_id(recipe_id):
        """
        根據 ID 取得單筆食譜。
        """
        try:
            conn = get_db_connection()
            recipe = conn.execute('SELECT * FROM recipes WHERE id = ?', (recipe_id,)).fetchone()
            conn.close()
            return dict(recipe) if recipe else None
        except sqlite3.Error as e:
            print(f"資料庫錯誤: {e}")
            return None

    @staticmethod
    def create(title, description='', tags=''):
        """
        建立新食譜。
        """
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(
                'INSERT INTO recipes (title, description, tags) VALUES (?, ?, ?)',
                (title, description, tags)
            )
            conn.commit()
            new_id = cursor.lastrowid
            conn.close()
            return new_id
        except sqlite3.Error as e:
            print(f"資料庫錯誤: {e}")
            return None

    @staticmethod
    def update(recipe_id, title, description, tags):
        """
        更新食譜資訊。
        """
        try:
            conn = get_db_connection()
            conn.execute(
                'UPDATE recipes SET title = ?, description = ?, tags = ? WHERE id = ?',
                (title, description, tags, recipe_id)
            )
            conn.commit()
            conn.close()
            return True
        except sqlite3.Error as e:
            print(f"資料庫錯誤: {e}")
            return False

    @staticmethod
    def delete(recipe_id):
        """
        刪除食譜。
        """
        try:
            conn = get_db_connection()
            conn.execute('DELETE FROM recipes WHERE id = ?', (recipe_id,))
            conn.commit()
            conn.close()
            return True
        except sqlite3.Error as e:
            print(f"資料庫錯誤: {e}")
            return False
