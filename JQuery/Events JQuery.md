# Events afhandelen in JQuery
### Beginnend met bladzijde 205
#### Samenvatting geschreven door Wouter en boek geschreven door Peter Kassenaar

*handig om eerst [dit](CSS in JQuery.md) te lezen*

Met JQuery kan je ook events afhandelen. De meestgebruikete events zijn:

```
.hover() // wanneer je met je muis over een element gaat
.click() // wanneer je op een element klikt
.dblclick() // wanneer je dubbelklikt op een element
.focus() // wanneer je op een element klikt
.blur() // wanneer je een element verlaat
.ready() // wanneer de pagina geladen is
.scroll() // wanneer je scrollt
.on() // wanneer een event afgehandeld wordt
.error() // wanneer er een error is
```

```html
<p>Dit is de eerste paragraaf</p>
<p>Dit is de tweede paragraaf</p>
<div id="resultaat"></div>
```

```js
$('p').click(function () {
    $('#resultaat').text('Geklikt op: ' + $(this).text());
});
```
