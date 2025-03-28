<## pm_CommunicationProtocol

### Mechanismus
Das CommunicationsProtocol ist TCP basiert um auch blockende Aktionen zu ermöglichen. Blockende Aktionen sind Aktionen die eine längere Zeit andauern und während dieser Zeit diese Aktion nicht nochmal aufgerufen werden kann (können auch den Bot blockieren)

Das Protokoll ist einseitig, es werden vom Bot keine Daten oder Funktionen erwartet, es werden nur Hinweise über die Fertigstellung eines Befehls zurückgesendet

Messages der Kategorie Joystick erwarten keine Antwort.

Solange ein gedrückter Button keine Antwort erhalten hat, soll dieser Button von weiterem betätigen geblockt werden.

Button messages von Host an den Bot können gebündelt werden (N-Key Rollover für Controller). Sie werden mit einem Semikolon geteilt und somit gebündelt.

### Definition

#### Host -> Bot
Messages des CP bestehen aus:
- 1 byte type designation
- 2 byte name designation
- csv typed array

| Designation | Bedeutung |
| ----------- | --------- |
| j           | joystick  |
| b           | button    |

##### Button
Designation based on mapping found in mapping.py
Dpad messages need to be offset by 12 to fit the here proposed scheme

| Designation | Bedeutung                           |
| ----------- | ----------------------------------- |
| 00          | Playstation X Button                |
| 01          | PS Triangle Button                  |
| 02          | PS O Button                         |
| 03          | PS Square Button                    |
| 04          | shoulder left                       |
| 05          | shoulder right                      |
| 06          | trigger left                        |
| 07          | trigger right                       |
| 08          | select                              |
| 09          | start                               |
| 10          | PS L3                               |
| 11          | PS R3                               |
| 12          | PS D-Pad Up (N) (mapping offset 12) |
| 13          | Up + Right (NE)                     |
| 14          | PS D-Pad Right (E)                  |
| 15          | Down + Right (SE)                   |
| 16          | PS D-Pad Down (S)                   |
| 17          | Down + Left (SW)                    |
| 18          | PS D-Pad Left (W)                   |
| 19          | Up + Left (NW)                      |
| 14          | None (would never be sent)          |
##### Joystick
| Designation | Description    | Data                                         |
| ----------- | -------------- | -------------------------------------------- |
| r           | Right Joystick | Tuple(x, y) in Range (0, 1000), Midpoint 500 |
| l           | Left Joystick  | Tuple(x, y) in Range (0,1000), Midpoint 500  |

#### Bot -> Host
| Designation    | Bedeutung                                                  |
| -------------- | ---------------------------------------------------------- |
| a<buttoncombo> | acknowledged: Button wurde erfolgreich ausgeführt (ab00\r) |

### Implementation Specifics
Das ProtocolStack wurde folgendermaßen in Python implementiert:

#### pm_CommunicationProtocol (com_impl.py)
- Es wurden beim Gamepad Handler alle Callbacks regristiert
- Callbacks werden pro Tick aufgerufen (CB_Always)
- in com_impl funktion msg_bundle -> bündelt alle vom Controller kommenden Funktionen
    - msg_bundle wird unter der globalen INSTANCE Variable in cb_buttons aufgerufen, da durch CB_Always der Button Callback immer, und immer als letztes aufgerufen wird
    - dies wurde gemacht um einen Thread (der wiederum irgendwo instanziert werden muss) zu sparen

#### TransportProtocol und CommunicationInterface (com.py)
- CommunicationInterface als "abstrakte" communication_protocol Klasse implementiert, von der alle CommunicationProtos erben sollen
- Sink wird als Thread aufgerufen
- send hat ping attribut um zwischen logging ping und normalen messages zu unterscheiden
- send hat ein Python Semaphor Objekt um Thread Safety und schicken aus mehreren Threads zu gewärleisten (Der Reihe nach nach Semaphor, oder so zumindest in der Theorie)

#### Logging
Logging wird durch das Python eigenes logging Modul gewärleistet, gegen Konvention (aber in ProtocolStack Konvention) wird der Root Logger für alles verwendet.
Logging Levels sind durch das logging Modul wiefolgt:

|ProtocolStack|logging|
|-|-|
|PING|logging.DEBUG|
|INFO|logging.INFO|
|SPECIAL|logging.WARNING|
|CRITICAL|logging.CRITICAL|