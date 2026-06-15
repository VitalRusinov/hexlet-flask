from psycopg2.extras import DictCursor

class UserRepository:
    def __init__(self, conn):
        self.conn = conn

    def get_all(self):
        with self.conn.cursor(cursor_factory=DictCursor) as cur:
            cur.execute("SELECT * FROM users ORDER BY id")
            return [dict(row) for row in cur]

    def find(self, id):
        with self.conn.cursor(cursor_factory=DictCursor) as cur:
            cur.execute("SELECT * FROM users WHERE id = %s", (id,))
            row = cur.fetchone()
            return dict(row) if row else None

    def add(self, user):
        with self.conn.cursor() as cur:
            cur.execute(
                "INSERT INTO users (name, email) VALUES (%s, %s) RETURNING id",
                (user["name"], user["email"]),
            )
            user["id"] = cur.fetchone()[0]
        self.conn.commit()
        return user

    def get_by_query(self, query=""):
        with self.conn.cursor(cursor_factory=DictCursor) as cur:
            cur.execute(
                """
                    SELECT * FROM users
                    WHERE name ILIKE %(search)s OR email ILIKE %(search)s
                    ORDER BY id
                """,
                {"search": f"%{query}%"},
            )
            return [dict(row) for row in cur]

    def update(self, id, user):
        with self.conn.cursor() as cur:
            cur.execute(
                "UPDATE users SET name = %s, email = %s WHERE id = %s",
                (user["name"], user["email"], id),
            )
        self.conn.commit()

    def delete(self, id):
        with self.conn.cursor() as cur:
            cur.execute(
                "DELETE FROM users WHERE id = %s",
                (id,),
            )
        self.conn.commit()