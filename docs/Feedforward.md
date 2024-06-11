# Projectgegevens

**VOORNAAM NAAM:** Kobe Lamote

**Sparringpartner:** Wout Klee

**Projectsamenvatting in max 10 woorden:** Vergelijk zonne-energie met totaal (net)verbruik.

**Projecttitel:** Zonne-energie monitor

# Tips voor feedbackgesprekken

## Voorbereiding

> Bepaal voor jezelf waar je graag feedback op wil. Schrijf op voorhand een aantal punten op waar je zeker feedback over wil krijgen. Op die manier zal het feedbackgesprek gerichter verlopen en zullen vragen, die je zeker beantwoord wil hebben, aan bod komen.

## Tijdens het gesprek:

> **Luister actief:** Schiet niet onmiddellijk in de verdediging maar probeer goed te luisteren. Laat verbaal en non-verbaal ook zien dat je aandacht hebt voor de feedback door een open houding (oogcontact, rechte houding), door het maken van aantekeningen, knikken...

> **Maak notities:** Schrijf de feedback op zo heb je ze nog nadien. Noteer de kernwoorden en zoek naar een snelle noteer methode voor jezelf. Als je goed noteert,kan je op het einde van het gesprek je belangrijkste feedback punten kort overlopen.

> **Vat samen:** Wacht niet op een samenvatting door de docenten, dit is jouw taak: Check of je de boodschap goed hebt begrepen door actief te luisteren en samen te vatten in je eigen woorden.

> **Sta open voor de feedback:** Wacht niet op een samenvatting door de docenten, dit is jouw taak: Check of je de boodschap goed hebt begrepen door actief te luisteren en samen te vatten in je eigen woorden.`

> **Denk erover na:** Denk na over wat je met de feedback gaat doen en koppel terug. Vind je de opmerkingen terecht of onterecht? Herken je je in de feedback? Op welke manier ga je dit aanpakken?

## NA HET GESPREK

> Herlees je notities en maak actiepunten. Maak keuzes uit alle feedback die je kreeg: Waar kan je mee aan de slag en wat laat je even rusten. Wat waren de prioriteiten? Neem de opdrachtfiche er nog eens bij om je focuspunten te bepalen. Noteer je actiepunten op de feedbackfiche.

# Week 1
## to do
- [x] Setup Raspberry Pi
- [x] Fritzing schema schakeling

# Feedforward gesprekken

## Gesprek 1 (Datum: 24/05/2024)

Lector: Geert Desloovere

Vragen voor dit gesprek:

- vraag 1: Current sensor ina226 toevoegen + library?
- vraag 2: Weglaten tweede energiemeter aangezien deze enkel het verbruik van de raspberry meet.
- vraag 3: Hoe correct microcontroller aansluiten voor pulses? Ground verbinden?
- vraag 4: Hoe schakelen verbruiker zonnepaneel 
- vraag 5: Aansluiten relay

Dit is de feedback op mijn vragen.

- feedback 1: Ja, spanning alleen is niet genoeg. Stuur nog een mailtje. Zou zonder library moeten lukken.
- feedback 2: Ja, mag.
- feedback 3: Ja correct, zoals op fritzing is correct.
- feedback 4: Zoals op fritzing maar basisweerstand toevoegen aan transistors en rode leds gebruiken
- feedback 5: Uitleg schakelen relay

Actiepunten:
- wijzigingen maken aan fritzing (prioriteit - deadline)
- mail sturen voor ina226 sensor
- uitzoeken aansturing ina226


## Gesprek 2 (Datum: 24/05/2024)

Lector: Frederik Waeyaert

Vragen voor dit gesprek:

- vraag 1: Tabel aanmaken voor sensortype?
- vraag 2: Datetime notatie? Zowel datum als tijd? Aparte kolom?
- vraag 3: Hoe kan ik best data loggen van twee verschillende eenheden
- vraag 4: actuator en sensor history in zelfde tabel?

Dit is de feedback op mijn vragen.

- feedback 1: Niet doen, overkill
- feedback 2: Nee, datetime, 1 kolom
- feedback 3: Geen eenheden, je weet de sensor dus je weet de eenheid + is eenheid noodzakelijk?
- feedback 4: actuators en sensors in zelfde device tabel. Ook voor history. Niet te complex maken

Actiepunten:
- Database verder afwerken volgens feedback (deadline 27/05)

## Toermoment 1 (Datum: 28/05/2024)

Lector: Dieter Roobrouck, Claudia Eeckhout, Geert Desloovere

- Database minimaal maar goed
  - Eventueel tabel `users` (nice to have)
- Resistors zijn gewijzigd
- Transistors nog aanpassen
- Instructables + foto's - tijdig mee beginnen
- Toggle in orde
- Github project board aanmaken en telkens issues
- Sparringspartner meer noteren

Actiepunten:
- Transistors aanpassen, met ground ipv voeding
- Issues aanmaken en toevoegen aan board

  ## Toermoment 2 (Datum 04/06/2024)

Lector: Dieter Roobrouck, Claudia Eeckhout, Geert Desloovere

- Schakeling: vergelijking om pos zonnepaneel te bepalen is wat raar, als paneel draajt zit je met schaduw, normaal (vanboven), lichtsensor met buisje ervoor (klein kijkgaatje) --> gerichter zoeken. Maar is prototype
- Data in database: puls al in database, nog geen berekeningen.
- Energie via pulsen? Historiek van pulsen? Hoe ga je pulsen van gisteren bekijken
- Schudden wegwerken: alleen sturen als ie moet gestuurd worden (stuur hem iedere 5sec)
- Instructables: fotos plaatsen

## Gesprek 3 (Datum 10/06/2024)

Lector: Christophe

Vragen voor dit gesprek:
- Resolving conflicts
