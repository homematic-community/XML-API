#!/bin/tclsh

# Sucht in den letzten 10 Zeilen von /var/log/messages nach Homematic-Script Fehlermeldungen
# 11'2012 - hobbyquaker https://github.com/hobbyquaker
#

load tclrega.so
puts -nonewline {Content-Type: text/xml
Access-Control-Allow-Origin: *

<?xml version="1.0" encoding="ISO-8859-1" ?><scriptErrors>}

set Datei [open "|/usr/bin/tail -n 10 /var/log/messages" r]
while {[gets $Datei Zeile] >= 0} {
  if [regexp Error.*near $Zeile] {
    regexp {([a-zA-Z]+ [0-9\: ]+) \(none\) local0.err ReGaHss: Error: IseESP\:\:([a-zA-Z]+)\= Error ([0-9]+) at row ([0-9]+) col ([0-9]+)} $Zeile line time msg code row col
    puts -nonewline "<error "
    puts -nonewline "timestamp='$time' "
    puts -nonewline "row='$row' "
    puts -nonewline "col='$col' "
    puts -nonewline "code='$code' "
    puts -nonewline "msg='$msg' "
    puts "/>"
  }
}
puts {</scriptErrors>}