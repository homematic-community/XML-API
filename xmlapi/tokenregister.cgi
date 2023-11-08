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

        # replace URL encoded parts
        regsub -all {%20} $desc { } desc
        regsub -all {%21} $desc {!} desc
        regsub -all {%23} $desc {#} desc
        regsub -all {%25} $desc {%} desc
        regsub -all {%25} $desc {%} desc
        regsub -all {%2A} $desc  *  desc
        regsub -all {%2F} $desc {/} desc
        regsub -all {%3F} $desc {?} desc
        regsub -all {%5E} $desc {^} desc
        regsub -all {%3D} $desc {=} desc
        regsub -all {%2C} $desc {,} desc

        # disable certain invalid chars
        regsub -all {%3C} $desc {_} desc
        regsub -all {<}   $desc {_} desc
        regsub -all {%3E} $desc {_} desc
        regsub -all {>}   $desc {_} desc
        regsub -all {%27} $desc {_} desc
        regsub -all {'}   $desc {_} desc
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
