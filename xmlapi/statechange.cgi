#!/bin/tclsh

load tclrega.so

set ise_id ""
set new_value ""

catch {
  set input $env(QUERY_STRING)
  set pairs [split $input &]
  foreach pair $pairs {
    if {0 != [regexp "^(\[^=]*)=(.*)$" $pair dummy varname val]} {
      set $varname $val      
    }    
  }
}
puts -nonewline {Content-Type: text/xml
Access-Control-Allow-Origin: *

<?xml version="1.0" encoding="ISO-8859-1" ?><result>}

regsub -all {%20} $new_value { } new_value
regsub -all {%21} $new_value {!} new_value
regsub -all {%23} $new_value {#} new_value
regsub -all {%25} $new_value {%} new_value
regsub -all {%2A} $new_value {*} new_value
regsub -all {%2F} $new_value {/} new_value
regsub -all {%3C} $new_value {<} new_value
regsub -all {%3E} $new_value {>} new_value
regsub -all {%3F} $new_value {?} new_value
regsub -all {%3D} $new_value {=} new_value
regsub -all {%2C} $new_value {,} new_value

if { [string match "rgb*" $new_value ] || ![string match "ise_id=*" $new_value ]} {
	array set res [rega_script "Write(dom.GetObject($ise_id).State('$new_value'));"]

	if {$res(STDOUT) != "null"} {
		puts -nonewline "<changed id=\"$ise_id\" new_value=\"$new_value\" />";
	} else {
		puts -nonewline "<not_found />";
	}
	
} else {

	set rec_new_value [split $new_value "\,"]
	set rec_ise_id [split $ise_id "\,"]

	for {set x 0} {$x<[llength $rec_ise_id]} {incr x} {

	array set res [rega_script "Write(dom.GetObject([lindex $rec_ise_id $x]).State('[lindex $rec_new_value $x]'));"]

		if {$res(STDOUT) != "null"} {
		  puts -nonewline "<changed id=\"[lindex $rec_ise_id $x]\" new_value=\"[lindex $rec_new_value $x]\" />";
		  } else {
			puts -nonewline "<not_found />";
		  }
	}
}

puts -nonewline {</result>}

