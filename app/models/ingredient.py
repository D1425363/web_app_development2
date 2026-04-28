from .db import get_db_connection

class Ingredient:
    @staticmethod
    def get_by_recipe(recipe_id):
        conn = get_db_connection()
        items = conn.execute('SELECT * FROM ingredients WHERE recipe_id = ?', (recipe_id,)).fetchall()
        conn.close()
        return [dict(row) for row in items]

    @staticmethod
    def create(recipe_id, name, amount):
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

    @staticmethod
    def delete_by_recipe(recipe_id):
        conn = get_db_connection()
        conn.execute('DELETE FROM ingredients WHERE recipe_id = ?', (recipe_id,))
        conn.commit()
        conn.close()
