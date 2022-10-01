import sqlite3


class BaseManagement:

    def __init__(self, bd_name):
        con = sqlite3.connect(bd_name)
        self.cursor = con.cursor()

    def insert_column(self, table_name, column_name, column_type):
        self.cursor.execute(
            f'ALTER TABLE {table_name}'
            f'ADD COLUMN {column_name} {column_type.upper()};'
        )
        return print(f'Column {column_name} has been added')

    def create_table(self, *args):
        """ Use the following construction [column_name, column_type]. Type by default is TEXT.
            The very first argument must contain only a table [name]"""

        self.cursor.execute(f'CREATE TABLE IF NOT EXISTS {args[0]}'
                            f'  (id INTEGER PRIMARY KEY AUTOINCREMENT);')

        for arg in args[1:]:
            self.insert_column(args[0], arg[0], arg[1])

        return print(f'Table {args[0]} has been created')