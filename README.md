Homematic XML-API
=================

Fork von http://www.homematic-inside.de/software/download/item/xmlapi-addon - kompatibel zur Version 1.2

siehe auch diesen Foren-Thread: http://homematic-forum.de/forum/viewtopic.php?f=26&t=10098&p=75959#p75959

Lizensiert unter GPL v3

Changelog
=========
1.12
* Workaround für Osram Lightify

1.11
* Kompatibilität zu RaspberryMatic (HM-RASPBERRYMATIC) hergestellt.

1.10 als Addon
* Die XML-API kann jetzt als Addon/Zusatzsoftware über das WebUI installiert/deinstalliert werden 

1.10
* statechange.cgi - aendern eines oder mehrere Kanaele-Zustaende
* sysvar.cgi - Anpassung wegen Variablen Name "Timer>>"

1.9
* devicelist.cgi - operate und show_internal hinzugefÃ¼gt

1.8
* programlist.cgi  - operate und visible hinzugefÃ¼gt
* statelist.cgi - channel visible, operate und operations hinzugefÃ¼gt

1.7
* statechange.cgi - encoden von Hexadezimalwerten
* protocol.cgi - Timestamp hinzugefÃ¼gt
* state.cgi - einzelne Datenpunktausgabe (<state>...</state>) entfernt

1.6
* state.cgi - Abfrage Abfrage von mehreren IDs hinzugefÃ¼gt (z.Bsp.: state.cgi?device_id=12796,1245789 )
* neues cgi systemNotification.cgi - Gibt die System Meldungen aus
* neues cgi systemNotificationClear.cgi -	LÃ¶scht die vorhandenen System Meldungen

1.5
* Bugfix
* Anpassung fÃ¼r CCU2

1.4
* Datenpunktausgabe "value_name_0 und value_name_1" in sysvar.cgi und sysvarlist.cgi hinzugefÃ¼gt

1.3
* Datenpunktausgabe "unit" in state.cgi und statelist.cgi hinzugefÃ¼gt
* scripterrors.cgi - Sucht in den letzten 10 Zeilen von /var/log/messages nach Homematic-Script Fehlermeldungen

1.2-hq10
* Ausgabe von version.cgi von 1.3 auf 1.2 zurÃ¼ck-geÃ¤ndert um Probleme mit Homedroid zu vermeiden
* statechange.cgi - AnfÃ¼hrungszeichen hinzugefÃ¼gt damit auch Varialben vom Typ Zeichenkette gesetzt werden kÃ¶nnen

1.2-hq9
* neues cgi scripterrors.cgi hinzugefÃ¼gt. Gibt aus den letzten 10 Zeilen der /var/log/messages Homematic-Script Fehlermeldungen aus

1.2-hq8
* Fehler in sysvarlist.cgi behoben, 3 Attribute haben gefehlt. (Danke Monty)

1.2-hq7
* Datenpunktausgabe in favoritelist.cgi arbeitet nun wie erwartet (gleiches verhalten wie state.cgi, danke Monty).

1.2-hq6
* exec.cgi (von http://homematic-forum.de/forum/viewtopic.php?f=31&t=7014) hinzugefÃ¼gt. Liefert zwar json und kein xml - passt aber thematisch imho trotzdem dazu
* favoritelist.cgi - Parameter show_datapoint aktiviert Ausgabe der zugehÃ¶rigen Datenpunkte bzw systemvariablen (Ã¼bernommen aus statelist.cgi und sysvar.cgi). Paramter show_internal siehe statelist.cgi
* statelist.cgi - Parameter show_internal=1 aktiviert nun die Ausgabe des Datenpunkt-Attributs state
* info.html aktualisiert

1.2-hq5
* version.cgi liefert nun 1.3 zurÃ¼ck
* protocol.cgi hinzugefÃ¼gt: Gibt das Systemprotokol zurÃ¼ck. Parameter: start, show, clear. clear=1 lÃ¶scht das Protokoll

1.2-hq4
* allow-origin Header hinzugefÃ¼gt
* info.html aktualisiert

1.2-hq3
* sysvar.cgi hinzugefÃ¼gt: Gibt eine einzelne Variable zurÃ¼ck. Liefert Wertelisten. Parameter: ise_id
* sysvarlist.cgi: neuer Parameter text um die neuen Attribute value_list and value_text zu aktivieren (text=true)
* cgi.tcl und once.tcl entfernt
