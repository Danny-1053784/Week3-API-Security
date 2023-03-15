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
    # Je kan een column name en value meegeven om een specifieke rij op te halen
    def get_table_content(self, table_name, column_name=None, column_value=None):
        cursor = sqlite3.connect(self.database_file).cursor()
        print(table_name, column_name, column_value)
        if column_name and column_value is not None:
            print("De column name en value zijn niet none")
            cursor.execute(f"SELECT * FROM {table_name} WHERE {column_name} LIKE '%{column_value}%'")
        else:
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
    def get_students(self, zoekterm=None):
        # Hier moet iets komen om specifieke studenten op te halen
        cursor = sqlite3.connect(self.database_file).cursor()
        if zoekterm is None:
            cursor.execute(f"SELECT * FROM student")
        else:
            cursor.execute(f"SELECT * FROM student WHERE student_id LIKE '%{zoekterm}%' OR voornaam LIKE '%{zoekterm}%' OR achternaam LIKE '%{zoekterm}%'")
        students = cursor.fetchall()
        return students

    # Dit is een functie die alle studenten ophaalt op basis van de aanwezigheid tabel. Hij haalt dan meteen ook alle data op uit de les tabel(Wouter)
    def get_aanwezigheid_student(self, studentid):
        cursor = sqlite3.connect(self.database_file).cursor()
        # pak de aanwezigheid van de student en de les
        cursor.execute(f"SELECT * FROM aanwezigheid, les WHERE student_id is {studentid} and aanwezigheid.les_id = les.les_id ORDER BY les.start_date DESC")
        # 0 = aanwezigheid_id
        # 1 = inchecktijd
        # 2 = les_fk
        # 3 = student_fk
        # 4 = les_id
        # 5 = docent_id
        # 6 = klas_id
        # 7 = les_naam
        # 8 = lokaal
        # 9 = start_date
        # 10 = end_date
        # 11 = actief
        aanwezigheid = cursor.fetchall()
        return aanwezigheid