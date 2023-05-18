
# Installatie
Om Flask te kunnen starten zul je eerst de Flask packages moeten installeren. Wil je latere problemen met versies voorkomen, dan raden we je aan een virtual environment te maken en daar de modules in te installeren:  
```
pip install virtualenv
virtualenv venv
.\venv\Scripts\activate
pip install -r requirements.txt
```

Om de demo applicatie te starten: 
``` 

python app.py
```
# Login docent
- Gebruikersnaam: markhr
- Wachtwoord: mark321!
-----------------------------
- Gebruikersnaam: Tjiddehr
- Wachtwoord: Tjidde321!

# Studenten 
er staan tot nu toe 3 studenten in de database:
- 0  Danny	van Schijndel	1053784@hr.nl
- 1	 Bryan	Booij	1025561@hr.nl
- 2	 Wouter	Oogjen	1052935@hr.nl


## QR genereren
De QR code word gegenereerd door een library. In de div met de ID `qrcode` word een qr code gezet

## Ajax vraag
##### Wouter Oogjen
De vraag word opgehaald met een ajax call. Maar hoe weet je of je iets moet inserten of updaten?
Mijn plan daarvoor was om een hidden input te maken met de vraagID, maar dat zou niet secuur zijn. Een student
zou met inspect element het uit kunnen zetten en aanpassen.

Ik zou een functie kunnen maken dat ophaalt in de database of de vraag al bestaat, maar ik ben bang dat
je dan de server gaat ddos-en. Met elke toetsaanslag de database checken is niet echt slim. 2 toetsaanslagen
per seconde (misschien nog wel meer) is 4 query's loslaten op de database per seconde.

Toen was mijn plan om dit op te lossen met een slimme SQL Query.
```` SQLite
INSERT INTO Vraag (vraag_id, les_id, vraag) VALUES ("vraagid", Lesid, "vraag") ON CONFLICT DO UPDATE SET vraag = 'Nieuwe waarde') 
````

Maar, in de functie insert_vraag maak je al een vraagid aan. Dat betekent dat alle vragen die je aanmaakt
een uniek id hebben. Dus ze hebben altijd een uniek id. Toen heb ik besloten om een andere manier te gebruiken.

```SQLite
DELETE FROM Vraag WHERE les_id = {lesid};
INSERT INTO Vraag (vraag_id, les_id, vraag) VALUES ('{vraag_id}', {lesid}, '{vraag}');
```

Kortom, eerst deleten en dan inserten. Ik ben er niet blij mee, maar het werkt wel. 
# Bronnen
- https://getbootstrap.com/
- https://getbootstrap.com/docs/5.2/examples/

# [leerling_details](templates/leerling_details.html) (wouter)
Ik ga het er snel over hebben wat voor werk is gegaan in de leerling_details pagina. 
Als je links op de "Lijst van leerlingen" klikt, dan krijg je een lijst van al de leerlingen.
Bij elke leerling staat een knop "Details". Als je daar op klikt, dan krijg je de leerling_details pagina. 

Ik wilde een pagina maken waarin je dan kan slecteren van welk vak je de presentie wilt van de desbetreffende leerling.
Maak ik wil alleen de vakken laten zien waarvan de leerling er moest zijn. Dus al de vakken die voor zijn klas is, zodat je niet een dropdown krijgt met meer dan 100 opties.

In [app.py](app.py) is de functie die ik gebruik om de pagina te laten zien. Voor de pagina hebben we de studentenId nodig, dus dat is het eerste stuk.
```python
@app.route("/leerling_details/<studentid>", methods=["POST"])
def leerling_details(studentid):
    if not studentid:
        print("studentid is none")
    else:
```
Dan gaan we de vakken ophalen die de student heeft en gaan we kijken of de form is ingevuld. Ik wilde dezelfde pagina gebruiken voor als je al
wel de form had ingevuld (Je had geselecteerd met de dropdown wel vak je wilde zien of niet) of dat je dat nog niet had gedaan.
```python
        # hier halen we lessen op van de student. Die zetten we dan in de dropdown zodat je alleen kan kiezen uit de lessen die je volgt en niet dat je lessen krijgt van andere studenten.
        lessen = dbm.get_lesnaam_klas_student(studentid)
        print("studentid is " + studentid)
        # nu moeten we kijken of de form is ingevuld
        lesid = request.form.get('lesid')
        # nu gaan we checken of lesid none is
```
Dus als de gebruiker weet van welk vak hij de presentie wilt zien, moeten we de database aanroepen en die data 
meegeven aan de pagina
```python
        if not lesid:
            print("lesid is none")
            return render_template("leerling_details.html", studentid=studentid, lessen=lessen)
        else:
            print("lesid is " + lesid)
            # nu moeten we de lessen ophalen die de klas van de student had en of hij/zij/hun wel of niet aanwezig was
            aangevraagdelessen = dbm.get_student_aanwezigheid(lesid, studentid)
            print(aangevraagdelessen)
            return render_template("leerling_details.html", studentid=studentid, lessen=lessen, aangevraagdelessen=aangevraagdelessen)
```
In geval van vargen, stuur me een berichtje op Discord of Whatsapp.
