from .db import get_db_connection

class Note:
    @staticmethod
    def get_by_recipe(recipe_id):
        conn = get_db_connection()
        items = conn.execute('SELECT * FROM notes WHERE recipe_id = ? ORDER BY created_at DESC', (recipe_id,)).fetchall()
        conn.close()
        return [dict(row) for row in items]

    @staticmethod
    def create(recipe_id, content, rating=None):
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
