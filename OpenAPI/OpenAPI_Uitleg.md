# OpenAPI Uitleg Wouter

## Wat is OpenAPI?
OpenAPI is een standaard voor het beschrijven van RESTful APIs. Het is een open standaard die door 
veel verschillende bedrijven wordt ondersteund. 
Vroeger heette OpenAPI Swagger, maar in 2016 is de naam veranderd. De naam Swagger is nog steeds in 
gebruik, maar OpenAPI is de officiële naam.

## Wat is een RESTful API?
Een RESTful api is een API die gebruik maakt van de REST architectuur. REST staat voor 
Representational State Transfer. REST is een architectuur 
die gebruik maakt van HTTP requests om data op te halen of te versturen. 
REST is een architectuur die gebruik maakt van HTTP requests om data op te halen of te versturen.

## Schrijven van de OpenAPI specificatie
De OpenAPI specificatie is een YAML bestand. Je kan het ook in JSON schrijven, wat ik heb gedaan. 
Dit bestand beschrijft de API.

Je begint het bestand met een aantal standaard dingen, net zoals HTML.
```json
{
  "openapi": "3.0.0",
  "info": {
    "title": "OpenAPI Uitleg",
    "version": "1.0.0"
  },
  "servers": [
    {
      "url": "http://localhost:5000"
    }
  ]
}
```
Hier staat wat informatie over de API. De versie, de titel en de server waar de API draait.

Dan kunnen we de endpoints beschrijven. Dit doe je met de `paths` key. 
```json
"paths": {
  "/api/v1/": {
    "get": {
      "summary": "Get all users",
      "description": "Get all users",
      "responses": {
        "200": {
          "description": "OK",
          "content": {
            "application/json": {
              "schema": {
                "type": "array",
                "items": {
                  "$ref": "#/components/schemas/User"
                }
              }
            }
          }
        }
      }
    }
  }
}
```

In dit geval, is er een endpoint `/api/v1/` met een GET request. 
Dus, als je naar `http://localhost:5000/api/v1/` gaat, krijg je een lijst met alle gebruikers.

#### Responses?
Een response is een message die je terug krijgt van de server nadat je een request hebt gedaan.
Als je een code 200 terug krijgt, betekent dit dat de request is gelukt. 

#### Content?
Stel je voor dat een envelop terug krijgt van de server. Dan is `response` en envelop 
en `content` de inhoud van de envelop.
Stel je voor dat je om een foto vroeg, de `response` geeft je dan informatie of de request is gelukt
en nog wat extra info zoals in dit geval de `description`. De `content` is dan de foto zelf.

#### Schema?
Schema verteld ons wat de structuur is van de data die we terug krijgen. In dit geval is het een array.
Items geeft dan aan wat de structuur is van de items in de array. In dit geval is het een User. Het kan ook
een string zijn, een integer, een boolean, etc.

#### $ref?
Dit is een referentie naar een andere plek in het bestand. In dit geval naar de User structuur.