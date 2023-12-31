import os
import sqlite3
from flask import session

class UserDatabaseModel:
    """This class is a wrapper around the sqlite3 database. It provides a simple interface that maps methods
    to database queries. The only required parameter is the database file."""

    def __init__(self, user_database_file):
        self.user_database_file = user_database_file
        if not os.path.exists(self.user_database_file):
            raise FileNotFoundError(f"Could not find database file: {user_database_file}")

    # Login function (Danny)  
    def user_login(self,gebruikersnaam, hashed_password):
            con = sqlite3.connect(self.user_database_file)
            cur = con.cursor()
            cur.execute('Select docent_id,gebruikersnaam,wachtwoord,voornaam,achternaam FROM docent WHERE gebruikersnaam=? and wachtwoord=?', (gebruikersnaam, hashed_password))
            
            result = cur.fetchone()
            if result:
                docent_id = result[0]
                docent_naam = result[3]
                docent_achternaam = result[4]
                print(docent_id)
                session['docent_id'] = docent_id
                session['docent_naam'] = docent_naam
                session['docent_achternaam'] = docent_achternaam
            # checks to see if user exists in db (shows in terminal)
                return True
            else:
                return False

