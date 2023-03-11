import os.path

import sys
from flask import Flask, render_template, redirect , request,send_from_directory, jsonify, session ,url_for, abort, make_response


from lib.tablemodel import DatabaseModel
from lib.loginmodel import UserDatabaseModel



LISTEN_ALL = "0.0.0.0"
FLASK_IP = LISTEN_ALL
FLASK_PORT = 81
FLASK_DEBUG = True

app = Flask(__name__)
app.secret_key = "ImTheOneAndOnlyLegendaryPatatoFarmer69"

# This command creates the "<application directory>" path
DATABASE_FILE = os.path.join(app.root_path, 'databases', 'aanwezigheid.db')

USER_DATABASE_FILE = os.path.join(app.root_path, 'databases', 'aanwezigheid.db')

   
dbm = DatabaseModel(DATABASE_FILE)
dbu = UserDatabaseModel(USER_DATABASE_FILE)


#Login as landing page
@app.route("/")
def index():
    return render_template("index.html")

# Login function with username session and redirect (Danny)
@app.route('/login', methods=["POST", "GET"])
def login():
    if request.method == 'POST':
        gebruikersnaam = request.form['gebruikersnaam']
        wachtwoord = request.form['wachtwoord']
        print(dbu.user_login(gebruikersnaam, wachtwoord))
        if dbu.user_login(gebruikersnaam, wachtwoord):
            session['username'] = gebruikersnaam
           
            return render_template(
            "admin.html")
        else:
            return redirect(url_for('index'))

@app.route("/meeting", methods=["GET"])
def meeting_docent():
    docent_id=session['docent_id']  
    meeting_docent = dbm.get_les_docent(docent_id)
    return jsonify(meeting_docent)

@app.route('/aanwezigheid')
def aanwezigheid():
    return render_template('aanwezigheid.html')

# de pagina waar de qr code op komt te staan (Wouter)
@app.route("/qrcode/<lesid>", methods=["GET", "POST"])
def qrcode(lesid = None):
    # De lesid is standaard null, maar als er een lesid wordt meegegeven, dan wordt die gebruikt
    print(lesid)
    # zet de les op actief
    dbm.update_les_actief(lesid, 1)
    print("De les " + lesid + " is actief gezet")
    # Ga naar qrcode.html en geef lesid mee
    return render_template("qrcode.html", lesid=lesid)

# De pagina waar de lijst van leerlingen staat (Wouter)
@app.route("/leerlingen_lijst")
def leerlingen_aanwezigheid():
    # haal de leerlingen op uit de database
    students = dbm.get_students()
    return render_template("leerlingen_aanwezigheid.html", students=students)

# De pagina waar de details van de leerlingen staan (Wouter)
@app.route("/leerling_details/<studentid>", methods=["GET", "POST"])
def leerling_details(studentid = None):
    # haal alles op uit de aanwezigheid tabel met de studentid
    aanwezigheid = dbm.get_aanwezigheid_student(studentid)
    # ga naar leerling_details.html en geef studentid mee
    return render_template("leerling_details.html", studentid=studentid)

if __name__ == "__main__":
    app.run(host=FLASK_IP, port=FLASK_PORT, debug=FLASK_DEBUG)

#Function to show image (Danny) 
def ShowImage():    
 app = Flask(__name__, static_url_path='/static')
 return app

ShowImage()