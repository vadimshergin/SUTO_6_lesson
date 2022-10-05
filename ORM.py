import sqlite3


class BaseManagement:

    def __init__(self, bd_name):
        self.bd_name = bd_name
        self.con = sqlite3.connect(self.bd_name)
        self.cursor = self.con.cursor()

    def type_adapter(self, what_to_adapt):
        try:
            types = {
                'int': 'INTEGER',
                'integer': 'INTEGER',
                'float': 'REAL',
                'str': 'STRING',
                'string': 'STRING',
                'bytes': 'BLOB',
                'None': 'NULL'
            }
            return types[what_to_adapt]
        except KeyError:
            return print(f'The type of value -- {what_to_adapt} -- is not acceptable')

    def add_column(self, table_name, column_name, column_type):
        try:
            self.cursor.execute(
                f'ALTER table {table_name}'
                f'ADD COLUMN IF NOT EXISTS {column_name} {self.type_adapter(column_type)};'
            )
        except sqlite3.OperationalError:
            return print(f'ERROR OCCURRED! The column -- {column_name} -- you tried to create is already exists. '
                         f'Check you request for other duplicates')
        finally:
            self.con.commit()
        return print(f'Column -- {column_name} -- with type -- {column_type.upper()} -- has been ADDED')

    def create_table(self, *args, foreign_key=None, references=None):
        """ Use the following construction [column_name, column_type]. Type by default is TEXT.
            In [column_type] you can set PRIMARY KEY, AUTOINCREMENT, NOT NULL etc: ['office_name', 'text not null'].
            To set foreign_key='table_key' and references='table_name table_key'.
            The very first argument must contain only a string with a table name. """

        query_body = str()
        for arg in args[1:]:
            if len(arg) < 1 or arg[1] not in ['int', 'integer', 'float', 'str', 'string', 'bytes']:
                query_body += f'{arg[0]} TEXT,\n'
            else:
                query_body += f'{arg[0]} {self.type_adapter(arg[1])},\n'

        if foreign_key is not None:
            foreign_key = f',\nFOREIGN KEY ({foreign_key})'
            references = f'REFERENCES {references.split()[0]} ({references.split()[1]})'

        self.cursor.execute(f'CREATE TABLE IF NOT EXISTS {args[0]} ('
                            f'{query_body[:-2]}{foreign_key} {references}'
                            f');')
        self.con.commit()
        return print(f'Table -- {args[0]} -- has been CREATED')

#TODO increase functionality of the method
    def select(self, selector, table_name):
        self.cursor.execute(
            f'SELECT {selector} FROM {table_name}'
        )
        print(self.cursor.fetchall())

    def drop_table(self, *table_name):
        for name in table_name:
            self.cursor.execute(f'DROP TABLE IF EXISTS {name};')
        self.con.commit()
        return print(f'The table -- {table_name} -- has been REMOVED')

    def insert(self, table_name, **kwargs):
        """ Use key word construction 'onepiece'='argument, argument, etc' for inserting row at once.
            Use named argument for inserting certain key-value pairs."""
        if kwargs.get('onepiece') is not None:
            try:
                values = tuple([i.strip() for i in kwargs['onepiece'].split(',')])
                self.cursor.execute(f'INSERT INTO {table_name} VALUES {values}')
                self.con.commit()
                return print('Row has been added')
            except sqlite3.OperationalError:
                return print('ERROR OCCURRED! Columns amount in the table does not match the amount in your query')
        else:
            try:
                query_column = []
                query_value = []
                for key, value in kwargs.items():
                    query_column.append(key)
                    query_value.append(value)
                if len(query_column) > 1:
                    self.cursor.execute(f'INSERT INTO {table_name} {tuple(query_column)} VALUES {tuple(query_value)}')
                    self.con.commit()
                else:
                    self.cursor.execute(f'INSERT INTO {table_name} ("{query_column[0]}") VALUES ("{query_value[0]}")')
                    self.con.commit()
                return print('Row has been added')
            except sqlite3.OperationalError:
                return print('ERROR OCCURRED! Check columns names in your query')

    def update(self, table_name, target, **kwargs):
        """ Use kwargs for setting the parameters to update.
            Target for setting WHERE conditions. """
        query_body = str()
        for key, value in kwargs.items():
            query_body += f"'{key}'='{value}', "
        self.cursor.execute(
            f'UPDATE {table_name} SET {query_body[:-2]} WHERE {target};'
        )
        self.con.commit()
        return print(f'Update operation for table -- {table_name} -- has been done')

    def delete_from_table(self, table_name, target=None):
        if target is not None:
            self.cursor.execute(
                f'DELETE FROM {table_name} WHERE {target}'
            )
            self.con.commit()
            return print(f'Deleting from table -- {table_name} -- done')
        else:
            self.cursor.execute(
                f'DELETE FROM {table_name}'
            )
            self.con.commit()
            return print(f'All rows from -- {table_name} --have been deleted')
