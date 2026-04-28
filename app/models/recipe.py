from .db import get_db_connection

class Recipe:
    @staticmethod
    def get_all():
        conn = get_db_connection()
        recipes = conn.execute('SELECT * FROM recipes ORDER BY created_at DESC').fetchall()
        conn.close()
        return [dict(row) for row in recipes]

    @staticmethod
    def get_by_id(recipe_id):
        conn = get_db_connection()
        recipe = conn.execute('SELECT * FROM recipes WHERE id = ?', (recipe_id,)).fetchone()
        conn.close()
        return dict(recipe) if recipe else None

    @staticmethod
    def create(title, description='', tags=''):
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

    @staticmethod
    def update(recipe_id, title, description, tags):
        conn = get_db_connection()
        conn.execute(
            'UPDATE recipes SET title = ?, description = ?, tags = ? WHERE id = ?',
            (title, description, tags, recipe_id)
        )
        conn.commit()
        conn.close()

    @staticmethod
    def delete(recipe_id):
        conn = get_db_connection()
        conn.execute('DELETE FROM recipes WHERE id = ?', (recipe_id,))
        conn.commit()
        conn.close()
