#!/bin/tclsh
source session.tcl

puts "Content-Type: text/xml; charset=iso-8859-1"
puts ""
puts -nonewline "<?xml version='1.0' encoding='ISO-8859-1' ?><result>"

if {[info exists sid] && [check_session $sid]} {

  set program_id "-1"
  set cond_check 0
  catch {
    set input $env(QUERY_STRING)
    set pairs [split $input &]
    foreach pair $pairs {
      if {0 != [regexp "^program_id=(.*)$" $pair dummy val]} {
        set program_id $val
        continue
      }
      if {0 != [regexp "^cond_check=(.*)$" $pair dummy val]} {
        set cond_check $val
        continue
      }
    }
  }

  # execut with condition check or without
  if { $cond_check == 1 } {
    array set res [rega_script "if ($program_id > 0) { object obj = dom.GetObject($program_id); if (obj && obj.IsTypeOf(OT_PROGRAM)) { obj.State(1); Write(obj); }}"]
  } else {
    array set res [rega_script "if ($program_id > 0) { object obj = dom.GetObject($program_id); if (obj && obj.IsTypeOf(OT_PROGRAM)) { obj.ProgramExecute(); Write(obj); }}"]
  }

  if { $res(STDOUT) != "" } {
    puts -nonewline "<started program_id=\"$program_id\"/>"
  } else {
    puts -nonewline {<not_found/>}
  }
} else {
  puts -nonewline {<not_authenticated/>}
}
puts "</result>"
