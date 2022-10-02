import sqlite3


class BaseManagement:

    def __init__(self, bd_name):
        self.bd_name = bd_name
        self.con = sqlite3.connect(self.bd_name)
        self.cursor = self.con.cursor()

    def insert_column(self, table_name, column_name, column_type):
        try:
            self.cursor.execute(
                f'ALTER table {table_name}'
                f'ADD COLUMN IF NOT EXISTS {column_name} {column_type.upper()};'
            )
        except sqlite3.OperationalError:
            return print(f'A column {column_name} you tried to create is already exists. Check you request for '
                         f'other duplicates')
        finally:
            self.con.commit()
        return print(f'Column {column_name} with type {column_type.upper()} has been added')

    def create_table(self, *args):
        """ Use the following construction [column_name, column_type]. Type by default is TEXT.
            The very first argument must contain only a table [name]"""

        query_body = str()
        for arg in args[1:]:
            if len(arg) > 1:
                query_body += f'{arg[0]} {arg[1].upper()},\n'
            else:
                query_body += f'{arg[0]} TEXT,\n'

        self.cursor.execute(f'CREATE TABLE IF NOT EXISTS {args[0]} ('
                            f'id INTEGER PRIMARY KEY AUTOINCREMENT,\n'
                            f'{query_body[:-2]}\n'
                            f');')
        self.con.commit()
        return print(f'Table {args[0]} has been created')

    def select(self, selector, table_name):
        self.cursor.execute(
            f'SELECT {selector} FROM {table_name}'
        )
        print(self.cursor.fetchall())

    def drop_table(self, table_name):
        self.cursor.execute(f'DROP TABLE IF EXISTS {table_name};')
        self.con.commit()
