# XML-API CCU Addon

[![Release](https://img.shields.io/github/release/hobbyquaker/XML-API.svg)](https://github.com/hobbyquaker/XML-API/releases/latest)
[![Downloads](https://img.shields.io/github/downloads/hobbyquaker/XML-API/latest/total.svg)](https://github.com/hobbyquaker/XML-API/releases/latest)
[![Issues](https://img.shields.io/github/issues/hobbyquaker/XML-API.svg)](https://github.com/hobbyquaker/XML-API/issues)
[![License](https://img.shields.io/badge/license-GPL%203.0-green.svg)](https://opensource.org/licenses/GPL-3.0)

A HomeMatic CCU Addon implementing a xml request functionality as an interface to all homematic deviced available to a CCU device. This addon provides useful scripts that can be accessed via a HTTP request to a CCU device and allows to query and set all e.g. room- and devicetype names.
Siehe auch diesen Foren-Thread: http://homematic-forum.de/forum/viewtopic.php?f=26&t=10098&p=75959#p75959. Lizensiert unter GPL v3.

## Supported CCU models
* HomeMatic CCU1
* [HomeMatic CCU2](http://www.eq-3.de/produkt-detail-zentralen-und-gateways/items/homematic-zentrale-ccu-2.html)
* [RaspberryMatic](http://homematic-forum.de/forum/viewtopic.php?f=56&t=26917)

## Installation
This addon can be added like a usual CCU addon package via the WebUI provided functionality by selecting "System-Konfiguration » Systemsteuerung » Zusatzsoftware", to upload the addon package as a tar.gz and the use »Installieren« to actually install the addon. After a restart of the CCU the xml-api interface can then be selected from the »Zusatzsoftware« tab in the CCU settings.

## Use
After installation the XML-API should be avilable via the following URL call:
```
http://[CCU_IP]/config/xmlapi/[ScriptName]
```
where [CCU_IP] corresponds to the IP address or name of your CCU device and [ScriptName] being one of the following tool scripts:

...

All of these scripts, if called, generate a xml structured output that can then be used by third-party applications to display or modify certain information. All of these scripts rely on a `ise_id` device or channel identifier that can be, e.g. used in the following way:
```
http://192.168.178.200/config/xmlapi/statechange.cgi?ise_id=12345&new_value=0.20
```
This call, if executed with the right ise_id and IP adress would then set a dimmer to 20%.

## ChangeLog
1.12
* Workaround für Osram Lightify

1.11
* Kompatibilität zu RaspberryMatic (HM-RASPBERRYMATIC) hergestellt.

1.10
* Die XML-API kann jetzt als Addon/Zusatzsoftware über das WebUI installiert/deinstalliert werden 
* statechange.cgi - aendern eines oder mehrere Kanaele-Zustaende
* sysvar.cgi - Anpassung wegen Variablen Name "Timer>>"

1.9
* devicelist.cgi - operate und show_internal hinzugefügt

1.8
* programlist.cgi  - operate und visible hinzugefügt
* statelist.cgi - channel visible, operate und operations hinzugefügt

1.7
* statechange.cgi - encoden von Hexadezimalwerten
* protocol.cgi - Timestamp hinzugefügt
* state.cgi - einzelne Datenpunktausgabe (<state>...</state>) entfernt

1.6
* state.cgi - Abfrage Abfrage von mehreren IDs hinzugefügt (z.Bsp.: state.cgi?device_id=12796,1245789 )
* neues cgi systemNotification.cgi - Gibt die System Meldungen aus
* neues cgi systemNotificationClear.cgi -	Löcht die vorhandenen System Meldungen

1.5
* Bugfix
* Anpassung für CCU2

1.4
* Datenpunktausgabe "value_name_0 und value_name_1" in sysvar.cgi und sysvarlist.cgi hinzugefügt

1.3
* Datenpunktausgabe "unit" in state.cgi und statelist.cgi hinzugefügt
* scripterrors.cgi - Sucht in den letzten 10 Zeilen von /var/log/messages nach Homematic-Script Fehlermeldungen

1.2-hq10
* Ausgabe von version.cgi von 1.3 auf 1.2 zurück-geändert um Probleme mit Homedroid zu vermeiden
* statechange.cgi - Anführungszeichen hinzugefügt damit auch Varialben vom Typ Zeichenkette gesetzt werden können

1.2-hq9
* neues cgi scripterrors.cgi hinzugefügt. Gibt aus den letzten 10 Zeilen der /var/log/messages Homematic-Script Fehlermeldungen aus

1.2-hq8
* Fehler in sysvarlist.cgi behoben, 3 Attribute haben gefehlt. (Danke Monty)

1.2-hq7
* Datenpunktausgabe in favoritelist.cgi arbeitet nun wie erwartet (gleiches verhalten wie state.cgi, danke Monty).

1.2-hq6
* exec.cgi (von http://homematic-forum.de/forum/viewtopic.php?f=31&t=7014) hinzugefügt. Liefert zwar json und kein xml - passt aber thematisch imho trotzdem dazu
* favoritelist.cgi - Parameter show_datapoint aktiviert Ausgabe der zugehörigen Datenpunkte bzw systemvariablen (übernommen aus statelist.cgi und sysvar.cgi). Paramter show_internal siehe statelist.cgi
* statelist.cgi - Parameter show_internal=1 aktiviert nun die Ausgabe des Datenpunkt-Attributs state
* info.html aktualisiert

1.2-hq5
* version.cgi liefert nun 1.3 zurück
* protocol.cgi hinzugefügt: Gibt das Systemprotokol zurück. Parameter: start, show, clear. clear=1 löscht das Protokoll

1.2-hq4
* allow-origin Header hinzugefügt
* info.html aktualisiert

1.2-hq3
* sysvar.cgi hinzugefügt: Gibt eine einzelne Variable zurück. Liefert Wertelisten. Parameter: ise_id
* sysvarlist.cgi: neuer Parameter text um die neuen Attribute value_list and value_text zu aktivieren (text=true)
* cgi.tcl und once.tcl entfernt

## Authors
* Uwe Langhammer, Maik, dirch, Philipp, hobbyquaker, jens-maus
