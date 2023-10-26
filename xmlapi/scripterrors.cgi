#!/bin/tclsh
# Sucht in den letzten 10 Zeilen von /var/log/messages nach Homematic-Script Fehlermeldungen
# 11'2012 - hobbyquaker https://github.com/hobbyquaker
source session.tcl

puts "Content-Type: text/xml; charset=iso-8859-1"
puts ""
puts -nonewline "<?xml version='1.0' encoding='ISO-8859-1' ?><scriptErrors>"

if {[info exists sid] && [check_session $sid]} {

  set Datei [open "|/usr/bin/tail -n 10 /var/log/messages" r]
  while {[gets $Datei Zeile] >= 0} {
    if { [regexp Error.*near $Zeile] } {
      regexp {([a-zA-Z]+ [0-9]+ [0-9\:]+) .+ local0.err ReGaHss: ERROR: SyntaxError\: Error ([0-9]+) at row ([0-9]+) col ([0-9]+)} $Zeile line time code row col
      puts -nonewline "<error "
      puts -nonewline "timestamp='$time' "
      puts -nonewline "row='$row' "
      puts -nonewline "col='$col' "
      puts -nonewline "code='$code' "
      puts "/>"
    }
  }
} else {
  puts -nonewline {<not_authenticated/>}
}
puts "</scriptErrors>"
