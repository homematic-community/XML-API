#!/bin/tclsh
source session.tcl

puts "Content-Type: text/xml; charset=iso-8859-1"
puts ""
puts -nonewline "<?xml version='1.0' encoding='ISO-8859-1' ?><tokenregister>"

if {[info exists sid] && [check_session $sid]} {

  set desc ""
  set ise_id "-1"
  catch {
    set input $env(QUERY_STRING)
    set pairs [split $input &]
    foreach pair $pairs {
      if {0 != [regexp "^desc=(.*)$" $pair dummy val]} {
        set desc $val
        break
      }
    }
  }

  set newToken [register_token $desc]
  if { $newToken != "" } {
    puts "<token desc='$desc'>$newToken</token>"
  } else {
    puts "<error/>"
  }

} else {
  puts -nonewline {<not_authenticated/>}
}
puts "</tokenregister>"
