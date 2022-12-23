#!/bin/tclsh
source session.tcl

puts "Content-Type: text/xml; charset=iso-8859-1"
puts ""
puts -nonewline "<?xml version='1.0' encoding='ISO-8859-1' ?><logout>"

if {[info exists sid] && [check_session $sid]} {
  if {[regexp {@([0-9a-zA-Z]{10})@} $sid all sidnr]} {
    array set res [rega_script "Write(system.ClearSessionID(\"$sidnr\"));"]
    if {$res(STDOUT) == "true"} {
      puts -nonewline {<session_cleared/>}
      puts "</logout>"
      return
    }
  }
}

puts -nonewline {<not_authenticated/>}
puts "</logout>"
