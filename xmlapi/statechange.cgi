#!/bin/tclsh
source session.tcl

puts "Content-Type: text/xml; charset=iso-8859-1"
puts ""
puts -nonewline "<?xml version='1.0' encoding='ISO-8859-1' ?><result>"

if {[info exists sid] && [check_session $sid]} {

  set ise_id ""
  set new_value ""
  catch {
    set input $env(QUERY_STRING)
    set pairs [split $input &]
    foreach pair $pairs {
      if {0 != [regexp "^ise_id=(.*)$" $pair dummy val]} {
        set ise_id $val
        continue
      }
      if {0 != [regexp "^new_value=(.*)$" $pair dummy val]} {
        set new_value $val
        continue
      }
    }
  }

  regsub -all {%20} $new_value { } new_value
  regsub -all {%21} $new_value {!} new_value
  regsub -all {%23} $new_value {#} new_value
  regsub -all {%25} $new_value {%} new_value
  regsub -all {%2A} $new_value  *  new_value
  regsub -all {%2F} $new_value {/} new_value
  regsub -all {%3C} $new_value {<} new_value
  regsub -all {%3E} $new_value {>} new_value
  regsub -all {%3F} $new_value {?} new_value
  regsub -all {%5E} $new_value {^} new_value
  regsub -all {%3D} $new_value {=} new_value
  regsub -all {%2C} $new_value {,} new_value

  if { [string match "rgb*" $new_value ] || [string match "*=*" $new_value ] } {
    array set res [rega_script "Write(dom.GetObject($ise_id).State('$new_value'));"]

    if {$res(STDOUT) != "null"} {
      if {$res(STDOUT) == "true"} {
        set success "true"
      } else {
        set success "false"
      }
      puts -nonewline "<changed id=\"$ise_id\" new_value=\"$new_value\" success=\"$success\" />";
    } else {
      puts -nonewline "<not_found />";
    }

  } else {

    set rec_ise_id [split $ise_id "\,"]

    # only split new_value in case we have more ise_id
    if { [llength $rec_ise_id] > 1 } {
      set rec_new_value [split $new_value "\,"]
    } else {
      set rec_new_value [list $new_value]
    }

    for {set x 0} {$x<[llength $rec_ise_id]} {incr x} {

      array set res [rega_script "Write(dom.GetObject([lindex $rec_ise_id $x]).State('[lindex $rec_new_value $x]'));"]

      if {$res(STDOUT) != "null"} {
        if {$res(STDOUT) == "true"} {
          set success "true"
        } else {
          set success "false"
        }
        puts -nonewline "<changed id=\"[lindex $rec_ise_id $x]\" new_value=\"[lindex $rec_new_value $x]\" success=\"$success\" />";
      } else {
        puts -nonewline "<not_found />";
      }
    }
  }
} else {
  puts -nonewline {<not_authenticated/>}
}
puts "</result>"
