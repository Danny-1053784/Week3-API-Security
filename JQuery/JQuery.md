# Kennismaken met JQuery
### Beginnend met bladzijde 159
#### Samenvatting geschreven door Wouter en boek geschreven door Peter Kassenaar

JQuery is een aanvullende JavaScript bibliotheek die het werken met het DOM sterk vereenvoudigd.
Door JQuery te gebruiken voeg je snel en betrouwbaar interactiviteit toe aan pagina's. JQuery is een 
bibliotheek die de vaak complexe core JavaScript DOM-manipulaties afschermt voor de programmeur.
**Het is geen vervanging van JavaScript**
**Deze samenvatting is van JQuery 1.9.1**

```html
<script src="scripts/jquery-1.9.1.min.js"></script>
```
De andere manier is om JQuery in te sluiten via een CDN, een *Content Delivery Network*. De code
van JQuery staat dan niet op uw eigen site, maar op de server van een centrale aanbieder.

```html
<script src="http://code.jquery.com/jquery-1.9.1.min.js"></script>
<script src="http://ajax.microsoft.com/ajax/jquery/jquery-1.9.1.min.js"></script>
<script src="http://ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min.js"></script>
```

Nu kan je JQuery gebruiken. JQuery definieert een globale functie met de naam `jQuery()` of `$()`.
Omdat JQuery zo'n lang woord is, hebben ze dat afgerond naar `$()`. Je kan JQuery gebruiken door
`$()` te gebruiken. Je kan ook een variabele aanmaken met de naam `$` en daar JQuery in stoppen.
```js
var paragrafen = $('p'); // selecteer alle paragrafen in jquery
var paragrafen = document.querySelectorAll('p'); // selecteer alle paragrafen in javascript
var paragrafen = document.getElementsByTagName('p'); // selecteer alle paragrafen in javascripta
```

```js
paragrafen.css('color', 'red'); // verander de kleur van alle paragrafen naar rood
$('p').css('color', 'red'); // verander de kleur van alle paragrafen naar rood in jquery
```

```js
$('p')
    .css('background-color', 'yellow')
    .on('click', function() {
    $(this).slideUp();
});
```

> This code is written in JavaScript and uses the jQuery library. 
> It sets the background color of all <p> elements on a page to yellow and sets up a click 
> event handler for them. When a <p> element is clicked, the slideUp function is called, 
> which causes the element to slide up and disappear.
> ~CHATGPT

### Elementen selecteren met JQuery
```js
$('p'); // selecteer alle paragrafen
$('p.intro'); // selecteer alle paragrafen met de class intro
$('p:first'); // selecteer de eerste paragraaf
$('ul li:first'); // selecteer de eerste li van de eerste ul
$('ul li:first-child'); // selecteer de eerste li van elke ul
$('[href]'); // selecteer alle elementen met een href attribuut
$('[href="#"]'); // selecteer alle elementen met een href attribuut met de waarde #
$('[href!="#"]'); // selecteer alle elementen met een href attribuut met een waarde die niet #
$('[href^="#"]'); // selecteer alle elementen met een href attribuut die begint met #
$('[href$=".pdf"]'); // selecteer alle elementen met een href attribuut die eindigt op .pdf
$('[href*="jquery"]'); // selecteer alle elementen met een href attribuut die jquery bevat
$('p:even'); // selecteer alle even paragrafen
$('p:odd'); // selecteer alle oneven paragrafen
$('p:gt(2)'); // selecteer alle paragrafen met een index groter dan 2
$('p:lt(2)'); // selecteer alle paragrafen met een index kleiner dan 2
$('p:animated'); // selecteer alle paragrafen die momenteel bezig zijn met een animatie
$('p:hidden'); // selecteer alle verborgen paragrafen
$('p:visible'); // selecteer alle zichtbare paragrafen
$('p:contains("jQuery")'); // selecteer alle paragrafen die jQuery bevatten
$('p:has("span")'); // selecteer alle paragrafen die een span bevatten
$('p:parent'); // selecteer alle paragrafen die een parent hebben
```

### document.ready()
```js
$(document).ready(function() {
    // code
});
```

>"$(document).ready(function() { /* code */ });" is important because it 
> ensures that the JavaScript code inside the function will only be executed once the 
> Document Object Model (DOM) is fully loaded. This is important because the DOM represents 
> the structure of a web page and is used by JavaScript to manipulate HTML elements. 
> Without using "$(document).ready()", there is a risk that your JavaScript code may reference 
> elements that haven't yet been loaded, which can cause errors. By wrapping your code 
> inside the "$(document).ready()" function, you can ensure that your code 
> will only run after the DOM is fully loaded, and all HTML elements are available for manipulation.
> ~CHATGPT

