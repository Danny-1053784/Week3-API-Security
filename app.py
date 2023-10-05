import os.path
import hashlib

import sys
from flask import Flask, render_template, redirect, request, send_from_directory, jsonify, session ,url_for, abort, make_response
# from flask_wtf import CSRFProtect

from lib.tablemodel import DatabaseModel
from lib.loginmodel import UserDatabaseModel

import os
keycode = os.urandom(12).hex()


LISTEN_ALL = "0.0.0.0"
FLASK_IP = LISTEN_ALL
FLASK_PORT = 81
FLASK_DEBUG = False

app = Flask(__name__)
app.secret_key = keycode
# csrf = CSRFProtect(app)
# This command creates the "<application directory>" path
DATABASE_FILE = os.path.join(app.root_path, 'databases', 'aanwezigheid.db')

USER_DATABASE_FILE = os.path.join(app.root_path, 'databases', 'aanwezigheid.db')

   
dbm = DatabaseModel(DATABASE_FILE)
dbu = UserDatabaseModel(USER_DATABASE_FILE)


#Login as landing page
@app.route("/")
def index():
    response = make_response(render_template('index.html'))
    response.headers['Content-Security-Policy'] = "default-src 'self'"
    response.headers['X-Frame-Options'] = 'SAMEORIGIN'
    response.headers['Server'] = ''
    return response

# Login function with username session and redirect (Danny)
@app.route('/login', methods=["POST", "GET"])
def login():
    if request.method == 'POST':
        gebruikersnaam = request.form['gebruikersnaam']
        wachtwoord = request.form['wachtwoord']
        hash = hashlib.sha1(wachtwoord.encode())
        print(hash)
        hashed_password = hash.hexdigest()
        print(hashed_password)

       
        if dbu.user_login(gebruikersnaam, hashed_password):
            session['username'] = gebruikersnaam
            voornaam=session['docent_naam']
            achternaam = session['docent_achternaam']
            return render_template(
            "admin.html", voornaam=voornaam, achternaam=achternaam)
        else:
            return redirect(url_for('index'))

@app.route("/meeting", methods=["GET"])
def meeting_docent():
    docent_id=session['docent_id']  
    meeting_docent = dbm.get_les_docent(docent_id)
    return jsonify(meeting_docent)

@app.route("/meeting_old", methods=["GET"])
def meeting_docent_old():
    docent_id=session['docent_id']  
    meeting_docent = dbm.get_les_docent_old(docent_id)
    return jsonify(meeting_docent)

@app.route('/aanwezigheid/<lesid>', methods=["GET", "POST"])
def aanwezigheid(lesid):
    content = dbm.get_table_content("Vraag", "les_id", lesid)
    print(content)
    content = content[0]
    print(content)
    # get the last element of the list
    content = content[0]
    print(content)
    return render_template('aanwezigheid.html', lesid=lesid, content=content)

# Deze route word aangeroepen door de Ajax om studenten te halen die zich in de les hebben ingeschreven.
@app.route("/getleerlingen/<lesid>", methods=["GET"])
def getleerlingen(lesid = None):
    aanwezigeleerlingen = dbm.get_aanwezige_studenten(lesid)
    return jsonify(aanwezigeleerlingen)

# Gemaakt door Bryan, ik (Wouter) heb een paar dingen aangepast
@app.route("/aanwezigheidpost/<lesid>", methods=["POST"])
def aanwezigheid_post(lesid = None):
    output = request.get_json()
    studentnummer = output["studentnummer"]
    antwoord_vraag = output["vraag"]
    print("We gaan nu de output printen")
    print(output)
    student_id_raw = dbm.get_student_id(studentnummer)
    student_id = ','.join(str(x) for x in student_id_raw)

    print(student_id)
    dbm.insert_aanwezigheid(student_id, lesid, antwoord_vraag)
    return render_template('admin.html' , lesid=lesid)


@app.route('/set_student_aanwezig', methods=['GET', 'POST'])
def set_student_aanwezig():
    if request.method == "POST":
        aanwezigheid_data = request.get_json()
        studentnummer = aanwezigheid_data[1]
        naam = aanwezigheid_data[0]
        vraag = aanwezigheid_data[2]
        print(aanwezigheid_data)
        return ("je staat aanwezig")
    
# route voor de docent om een les aan te maken (Danny)
@app.route('/les-aanmaken')
def lesAanmaken():
    voornaam=session['docent_naam']
    achternaam = session['docent_achternaam']
    klas = dbm.read_klas_name_update()
    return render_template('les-aanmaken.html', voornaam=voornaam,achternaam=achternaam,klas=klas)

# insert les docent (Danny)
@app.route('/les_aanmaken_post', methods=['POST', 'GET'])
def les_aanmaken_docent():
  if request.method == "POST":
    les_aanmaken_data = request.get_json()
    docent_id = session['docent_id']
    klas = les_aanmaken_data[0]
    les_naam = les_aanmaken_data[1]
    lokaal = les_aanmaken_data[2]
    start_date = les_aanmaken_data[3]
    end_date = les_aanmaken_data[4]
    klas_value = dbm.read_klas_by_name(klas)

    # print(test_id)
    print(start_date)
    print(end_date)
    print(klas_value)
    dbm.insert_les_docent(docent_id,klas_value,les_naam,lokaal,start_date,end_date)


    return ("les aangemaakt")
# Route for the dashboard with user authentication (Danny)
@app.route('/admin')
def admin():
    if 'username' in session:
        voornaam=session['docent_naam']
        achternaam = session['docent_achternaam']
        return render_template('admin.html', voornaam=voornaam, achternaam=achternaam)
    else:
        return redirect(url_for('index'))


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
@app.route("/leerlingen_lijst", methods=["GET", "POST"])
def leerlingen_aanwezigheid(naam = None):
    # haal de leerlingen op uit de database als naam niet is meegegeven
    # zoek naar een specifieke leerling uit de database als naam wel is meegegeven
    naam = request.form.get("naam")
    voornaam=session['docent_naam']
    if naam is None or naam == '':
        print("naam is none")
        students = dbm.get_students()
    else:
        print("naam is niet none")
        students = dbm.get_students(naam)
    return render_template("leerlingen_aanwezigheid.html", students=students, voornaam=voornaam)

# Op deze pagina kan je selecteren van welk vak je de presentie van de student wilt zien (Wouter)
@app.route("/leerling_details/<studentid>", methods=["POST"])
def leerling_details(studentid):
    if not studentid:
        print("studentid is none")
    else:
        # hier halen we lessen op van de student. Die zetten we dan in de dropdown zodat je alleen kan kiezen uit de lessen die je volgt en niet dat je lessen krijgt van andere studenten.
        lessen = dbm.get_lesnaam_klas_student(studentid)
        print("studentid is " + studentid)
        # nu moeten we kijken of de form is ingevuld
        lesid = request.form.get('lesid')
        # nu gaan we checken of lesid none is
        if not lesid:
            print("lesid is none")
            return render_template("leerling_details.html", studentid=studentid, lessen=lessen)
        else:
            print("lesid is " + lesid)
            # nu moeten we de lessen ophalen die de klas van de student had en of hij/zij/hun wel of niet aanwezig was
            aangevraagdelessen = dbm.get_student_aanwezigheid(lesid, studentid)
            print(aangevraagdelessen)
            return render_template("leerling_details.html", studentid=studentid, lessen=lessen, aangevraagdelessen=aangevraagdelessen)


# Dit is een functie die de vraag tabel gaat invullen (Wouter)
@app.route("/vraagles/<lesid>", methods=["POST"])
def vraagles(lesid = None):
    vraag = request.form.get("vraag")
    print(vraag)
    print(lesid)
    dbm.insert_vraag(lesid, vraag)
    return ("De vraag is toegevoegd aan de les ")


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(host=FLASK_IP, port=FLASK_PORT, debug=FLASK_DEBUG)

#Function to show image (Danny) 
def ShowImage():    
 app = Flask(__name__, static_url_path='/static')
 return app

ShowImage()