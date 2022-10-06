import sqlite3


class BaseManagement:

    def __init__(self, bd_name):
        self.bd_name = bd_name
        self.con = sqlite3.connect(self.bd_name)
        self.cursor = self.con.cursor()

    def type_adapter(self, what_to_adapt):
        types = {
            'int': 'INTEGER',
            'integer': 'INTEGER',
            'float': 'REAL',
            'str': 'TEXT',
            'string': 'TEXT',
            'bytes': 'BLOB',
            'none': 'NULL'
        }
        try:
            if types.get(what_to_adapt.lower()) is not None:
                return types[what_to_adapt.lower()]
            elif what_to_adapt.upper() in types.values():
                return what_to_adapt.upper()
            else:
                raise ValueError
        except ValueError:
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
        """ Use the following construction [column_name, column_type, column_options]. Type by default is TEXT.
            In [column_options] you can set PRIMARY KEY, AUTOINCREMENT, NOT NULL etc: ['table_name', 'text', 'primary key not null'].
            You can set ONLY ONE foreign_key='table_key' and references='table_name table_key'.
            The very first argument must contain only a string with a table name. """

        query_body = str()
        for arg in args[1:]:
            if len(arg) < 1:
                query_body += f'{arg[0]} TEXT,\n'
            elif len(arg) > 2:
                query_body += f'{arg[0]} {self.type_adapter(arg[1])} {arg[2]},\n'
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

    def select_all(self, table_name):
        self.cursor.execute(
            f'SELECT * FROM {table_name}'
        )
        print(self.cursor.fetchall())

    def drop_table(self, *table_name):
        for name in table_name:
            self.cursor.execute(f'DROP TABLE IF EXISTS {name};')
        self.con.commit()
        return print(f'The table -- {table_name} -- has been REMOVED')

    def insert(self, table_name, column_names, *column_values):
        """
        Use construction to set values
        :param ('table_name'):
        :param ('column_names'):
        :param ('column_values'):
        :return: printed status of inserting operation
        """
        try:
            for arg in column_values:
                if isinstance(column_names, str):
                    self.cursor.execute(
                        f'INSERT INTO {table_name}("{column_names}") VALUES("{arg}");'
                    )
                    self.con.commit()
                else:
                    self.cursor.execute(
                        f'INSERT INTO {table_name}{column_names} VALUES{arg};'
                    )
                    self.con.commit()
            return print(f'Rows have been added into -- {table_name} --')
        except sqlite3.OperationalError:
            return print(f'ERROR OCCURRED during inserting in -- {table_name} --! Check you query parameters: table name, column name or values')

    def update(self, table_name, target, **kwargs):
        """ Use kwargs for setting the parameters to update.
            Target for setting WHERE conditions: UPDATE {table_name} SET {kwargs} WHERE {target} """
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
