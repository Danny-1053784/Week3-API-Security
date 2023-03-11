import os
import sqlite3

class DatabaseModel:
    """This class is a wrapper around the sqlite3 database. It provides a simple interface that maps methods
    to database queries. The only required parameter is the database file."""

    def __init__(self, database_file):
        self.database_file = database_file
        if not os.path.exists(self.database_file):
            raise FileNotFoundError(f"Could not find database file: {database_file}")

    # Using the built-in sqlite3 system table, return a list of all tables in the database
    def get_table_list(self):
        cursor = sqlite3.connect(self.database_file).cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = [table[0] for table in cursor.fetchall()]
        return tables

    # Given a table name, return the rows and column names
    def get_table_content(self, table_name):
        cursor = sqlite3.connect(self.database_file).cursor()
        cursor.execute(f"SELECT * FROM {table_name} ")
        # An alternative for this 2 var approach is to set a sqlite row_factory on the connection
        table_headers = [column_name[0] for column_name in cursor.description]
        table_content = cursor.fetchall()

        # Note that this method returns 2 variables!
        return table_content, table_headers

    def get_les_docent(self, docent_id):
        cursor = sqlite3.connect(self.database_file).cursor()
        cursor.execute(f"SELECT * FROM les WHERE docent_id = {docent_id}")
        docent = cursor.fetchall()
        return docent

    # Dit is een functie die de les actief of niet zet op basis van de actief parameter (Wouter)
    def update_les_actief(self, les_id, actief):
        print("We zijn nu in de update_les_actief funtie en de les " + les_id + " wordt actief gezet")
        cursor = sqlite3.connect(self.database_file).cursor()
        cursor.execute(f"UPDATE les SET actief = {actief} WHERE les_id = {les_id}")
        cursor.connection.commit()

    # Dit is een functie die alle studenten ophaalt uit de database (Wouter)
    def get_students(self):
        cursor = sqlite3.connect(self.database_file).cursor()
        cursor.execute(f"SELECT * FROM student")
        students = cursor.fetchall()
        return students

    # Dit is een functie die alle studenten ophaalt op basis van de aanwezigheid tabel. Hij haalt dan meteen ook alle data op uit de les tabel(Wouter)
    def get_aanwezigheid_student(self, studentid):
        cursor = sqlite3.connect(self.database_file).cursor()
        # pak de aanwezigheid van de student en de les
        cursor.execute(f"SELECT * FROM aanwezigheid, les WHERE student_fk is 1 and aanwezigheid.les_fk = les.les_id ORDER BY les.start_date DESC")
        aanwezigheid = cursor.fetchall()
        return aanwezigheid