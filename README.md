Homematic XML-API
=================

Fork von http://www.homematic-inside.de/software/download/item/xmlapi-addon - kompatibel zur Version 1.2

siehe auch diesen Foren-Thread: http://homematic-forum.de/forum/viewtopic.php?f=26&t=10098&p=75959#p75959

Lizensiert unter GPL v3

Changelog
=========

1.2-hq7
* Fehler in favoritelist.cgi behoben - es werden nun alle Datenpunk-Typen ausser ON_TIME und INHIBIT zurückgegeben.

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


