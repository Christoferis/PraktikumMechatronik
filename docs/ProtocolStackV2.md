*A second Version of Protocols*
***
## ProtocolStack: Abstract
Es kommt ein ProtocolStack zum Einsatz, welches aus zwei Teilprotokollen zusammensetzt:
- Transportprotokoll (zum reinen Übertragen von Daten)
- Kommunikationsprotokoll (Protokoll zum Steuern und informieren, wird als Daten in TP gewrappt)
## TransportProtocol
 Funktionieren tut das TransportProtocol wie UDP: Weder Host noch Device wissen explizit voneinander. Macht plötzliche Verbindungsabbrüche und die Programmierung wesentlich einfacher zu handhaben
 (Kein Buffer, keine komplizierten Edgecases und handhaben von Verbindungsabbrüchen)
### Umfang
- verwaltet Verbindung
- tut jede form von Daten übertragen
### Anforderungen
- leichtgewichtig (für schnelles sortieren, mehr speicherplatz)
- timeoutless (meistens)
- einfache Implimentation
- UDP inspired: no ID or ACK (neben ping)
- full duplex (senden und empfangen parallel)
### Spec
#### TP commands

| command header | desc                                                                                                                                                               | Daten                          |
| -------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------ | ------------------------------ |
| m              | ping command: in regulären Intervalen gesendet (zusammen mit p für marco - polo)                                                                                   | /                              |
| p              | ping command: in regulären Intervalen gesendet, sollte nur als Empfehlung gelten, senden und empfangen sollten nicht beeinflusst werden (auch wenn ping unendlich) | /                              |
| r              | request                                                                                                                                                            | ja: Alle ASCII Zeichen erlaubt |
| e              | error command: falls ein request einen Fehler wirft                                                                                                                | 3 stelliger Int                |
| l              | kann ASCII Zeichenketten verschicken, für Logging und Debug Nutzung                                                                                                | ja: Alle ASCII Zeichen erlaubt |
>[!note]
> jeder Eingang und Ausgang des Transportprotocols soll geloggt werden
> Ursprung der Nachricht im Log sollte mit folgenden Präfixen markiert werden:
> - o *outgoing; zum Bot*
> - i *incoming; vom Bot*
> Dies immer relativ zu dem Device, auf dem diesen Log angezeigt wird

Requests nur aus Newlines oder Spaces sollten ignoriert werden (Space, newline, carriage)

#### TP Syntax
##### Erweiterte Backus Naur Form
```
€ sei epsilon (null / "")

command = "r" | "m" | "p" | "e" | "l"
request = ("r" | "l") data
number = "1" | "2" | "3" | "4" | "5" | "6" | "7" | "8" | "9" | "0"
error = "e" number {0-9}
newline = '\' 'r'
data = alphabet {alphabet}
com = (request | "m" | "p" | error) newline
```
##### Beispiel
```
m\r <- start ping funktion
rSomeCommandHere\r
p\r <- Ende Ping Funktion
e404\r
```
***
## Communication Protocol
Siehe [[pm_CommunicationProtocol.md]]