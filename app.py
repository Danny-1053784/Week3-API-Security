import os.path

import sys
from flask import Flask, render_template, redirect , request, session ,url_for, abort, make_response


from lib.tablemodel import DatabaseModel
from lib.loginmodel import UserDatabaseModel



LISTEN_ALL = "0.0.0.0"
FLASK_IP = LISTEN_ALL
FLASK_PORT = 81
FLASK_DEBUG = True

app = Flask(__name__)
app.secret_key = "ImTheOneAndOnlyLegendaryPatatoFarmer69"

# This command creates the "<application directory>" path
# DATABASE_FILE = os.path.join(app.root_path, 'databases', '   .db')

USER_DATABASE_FILE = os.path.join(app.root_path, 'databases', 'user_details.db')

   
# dbm = DatabaseModel(DATABASE_FILE)
dbu = UserDatabaseModel(USER_DATABASE_FILE)


#Login as landing page
@app.route("/")
def index():
    return render_template("index.html")



if __name__ == "__main__":
    app.run(host=FLASK_IP, port=FLASK_PORT, debug=FLASK_DEBUG)

