#!/bin/tclsh
source session.tcl

puts "Content-Type: text/xml; charset=iso-8859-1"
puts ""
puts -nonewline "<?xml version='1.0' encoding='ISO-8859-1' ?><tokenregister>"

if {[info exists sid] && [check_session $sid]} {

  set result [revoke_token $sid]
  if { $result == 1 } {
    puts "<ok/>"
  } else {
    puts "<error/>"
  }

} else {
  puts -nonewline {<not_authenticated/>}
}
puts "</tokenregister>"
