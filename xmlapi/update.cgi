#!/bin/tclsh
source session.tcl

puts "Content-Type: text/xml; charset=iso-8859-1"
puts ""
puts -nonewline "<?xml version='1.0' encoding='ISO-8859-1' ?><result>"

if {[info exists sid] && [check_session $sid]} {

  set checkupdate ""
  set maxdurchlaeufe 7
  catch {
    set input $env(QUERY_STRING)
    set pairs [split $input &]
    foreach pair $pairs {
      if {0 != [regexp "^checkupdate=(.*)$" $pair dummy val]} {
        set checkupdate $val
        continue
      }
      if {0 != [regexp "^maxdurchlaeufe=(.*)$" $pair dummy val]} {
        set maxdurchlaeufe $val
        continue
      }
    }
  }

  catch {
    set idlist [split [string trim $checkupdate] ";"]
    set resultids ""
    set zaehler 0
    while { ([llength $resultids] < 1) && ($zaehler < $maxdurchlaeufe) } {
      foreach pair $idlist {
        if {$pair != {} } then {
          set vp [split $pair "="]

          set id [lindex $vp 0]
          set timestamp [lindex $vp 1]

          set res [rega "dom.GetObject($id).Timestamp().ToInteger();"]

          if { $res == $timestamp } {
            continue
          }

          # unterschiedlich, also id merken
          array set res_arr [rega_script "object o=dom.GetObject($id);\nvar value=o.Value();\nvar lastupdate=o.Timestamp().ToInteger();\nvar type=o.TypeName();"]
          # puts -nonewline $res_arr(STDOUT)
          puts -nonewline "<refresh id=\"$id\" value=\"$res_arr(value)\" lastupdate=\"$res_arr(lastupdate)\" type=\"$res_arr(type)\"/>"
          lappend resultids $id
        }
      }
      if { [llength $resultids] < 1 } {
        after 500
        incr zaehler
      }
    }
  }
} else {
  puts -nonewline {<not_authenticated/>}
}
puts "</result>"


