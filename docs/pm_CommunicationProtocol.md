## pm_CommunicationProtocol

### Mechanismus
Das CommunicationsProtocol ist TCP basiert um auch blockende Aktionen zu ermöglichen. Blockende Aktionen sind Aktionen die eine längere Zeit andauern und während dieser Zeit diese Aktion nicht nochmal aufgerufen werden kann (können auch den Bot blockieren)

Das Protokoll ist einseitig, es werden vom Bot keine Daten oder Funktionen erwartet, es werden nur Hinweise über die Fertigstellung eines Befehls zurückgesendet

Messages der Kategorie Joystick erwarten keine Antwort.

Solange ein gedrückter Button keine Antwort erhalten hat, soll dieser Button von weiterem betätigen geblockt werden.

Messages von Host an den Bot können gebündelt werden (N-Key Rollover für Controller). Sie werden mit einem Semikolon geteilt und somit gebündelt

### Definition

#### Host -> Bot
Messages des CP bestehen aus:
- 1 byte type designation
- 2 byte name designation
- csv typed array

|Designation|Bedeutung|
|-|-|
|j|joystick|
|b|button|

##### Button
Designation as defined in mapping.py

|Designation|Bedeutung|
|-|-|
|00| Playstation X Button|
|01| PS Triangle Button|
|02| PS O Button|
|03| PS Square Button|
|04| shoulder left|
|05| shoulder right|
|06| trigger left|
|07| trigger right|
|08| select|
|09| start|
|10| PS L3|
|11| PS R3|
|d0| PS D-Pad Up|
|d1| Up + Right|
|d2| PS D-Pad Right|
|d3| Down + Right|
|d4| PS D-Pad Down|
|d5| Down + Left|
|d6| PS D-Pad Left|
|d7| Up + Left|
|14| None|

##### Joystick
|Designation|Description|Data|
|-|-|-|
|r|Right Joystick|Tuple(x, y) in Range (0, 1000), Midpoint 500|
|l|Left Joystick|Tuple(x, y) in Range (0,1000), Midpoint 500|

#### Bot -> Host
|Designation|Bedeutung|
|-|-|
|a<buttoncombo>|acknowledged: Button Combo wurde erfolgreich ausgeführt|