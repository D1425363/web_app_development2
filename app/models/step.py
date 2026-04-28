from .db import get_db_connection

class Step:
    @staticmethod
    def get_by_recipe(recipe_id):
        conn = get_db_connection()
        items = conn.execute('SELECT * FROM steps WHERE recipe_id = ? ORDER BY step_order ASC', (recipe_id,)).fetchall()
        conn.close()
        return [dict(row) for row in items]

    @staticmethod
    def create(recipe_id, step_order, instruction):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            'INSERT INTO steps (recipe_id, step_order, instruction) VALUES (?, ?, ?)',
            (recipe_id, step_order, instruction)
        )
        conn.commit()
        new_id = cursor.lastrowid
        conn.close()
        return new_id

    @staticmethod
    def delete_by_recipe(recipe_id):
        conn = get_db_connection()
        conn.execute('DELETE FROM steps WHERE recipe_id = ?', (recipe_id,))
        conn.commit()
        conn.close()
