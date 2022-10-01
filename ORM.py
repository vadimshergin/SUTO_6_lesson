import sqlite3


class BaseManagement:

    def __init__(self, bd_name):
        con = sqlite3.connect(bd_name)
        self.cursor = con.cursor()

    def create_table(self, *args):
        ''' Use the following construction [RAW_NAME, RAW_TYPE]. Type by default is TEXT.
            The very first argument must contain only a table [NAME]'''
