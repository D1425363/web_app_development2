from .db import get_db_connection
import sqlite3

class Ingredient:
    @staticmethod
    def get_by_recipe(recipe_id):
        """
        取得指定食譜的所有材料。
        """
        try:
            conn = get_db_connection()
            items = conn.execute('SELECT * FROM ingredients WHERE recipe_id = ?', (recipe_id,)).fetchall()
            conn.close()
            return [dict(row) for row in items]
        except sqlite3.Error as e:
            print(f"資料庫錯誤: {e}")
            return []

    @staticmethod
    def create(recipe_id, name, amount):
        """
        為指定食譜建立材料紀錄。
        """
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(
                'INSERT INTO ingredients (recipe_id, name, amount) VALUES (?, ?, ?)',
                (recipe_id, name, amount)
            )
            conn.commit()
            new_id = cursor.lastrowid
            conn.close()
            return new_id
        except sqlite3.Error as e:
            print(f"資料庫錯誤: {e}")
            return None

    @staticmethod
    def delete_by_recipe(recipe_id):
        """
        刪除指定食譜的所有材料。
        """
        try:
            conn = get_db_connection()
            conn.execute('DELETE FROM ingredients WHERE recipe_id = ?', (recipe_id,))
            conn.commit()
            conn.close()
            return True
        except sqlite3.Error as e:
            print(f"資料庫錯誤: {e}")
            return False
