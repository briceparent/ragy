import sqlite3


class DatabaseContextManager:
    """
    Simple context manager to open a connection to a database, set its settings, and commit upon leaving
    """
    def __init__(self, path):
        self.path = path
        self.conn = None
        self.cursor = None

    def __enter__(self):
        self.conn = sqlite3.connect(self.path)
        self.conn.row_factory = sqlite3.Row
        self.cursor = self.conn.cursor()
        return self.cursor

    def __exit__(self, exc_class, exc, traceback):
        self.conn.commit()
        self.conn.close()


class DatabaseManager:
    _queries = {
        'get_one': 'SELECT link, single FROM links WHERE id=:id',
        'get_all_public': 'SELECT id, link, single FROM links WHERE private=0',
        'create_one': "INSERT INTO links(creator, private, dropable, single, link, id) "
                      "VALUES(:creator, :private, :dropable, :single, :link, :id)",
        'add_access': "UPDATE links SET accesses = (accesses + 1), access = datetime('now') WHERE id=:id"
    }

    class IntegrityError(sqlite3.IntegrityError):
        pass

    def get_one(self, **kwargs):
        with DatabaseContextManager('db.sqlite') as cursor:
            cursor.execute(self._queries['get_one'], kwargs)
            return cursor.fetchone()

    def create_one(self, **kwargs):
        with DatabaseContextManager('db.sqlite') as cursor:
            try:
                kwargs['private'] = False
                kwargs['dropable'] = ""
                kwargs['single'] = False
                cursor.execute(self._queries['create_one'], kwargs)
            except sqlite3.IntegrityError:
                raise self.IntegrityError

    def get_all_public(self):
        with DatabaseContextManager('db.sqlite') as cursor:
            cursor.execute(self._queries['get_all_public'])
            return cursor.fetchall()

    def add_access(self, **kwargs):
        with DatabaseContextManager('db.sqlite') as cursor:
            cursor.execute(self._queries['add_access'], kwargs)
