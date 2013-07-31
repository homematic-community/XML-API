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


array set res [rega_script "Write(dom.GetObject($ise_id).State('$new_value'));"]
if {$res(STDOUT) != "null"} {
  puts -nonewline "<changed id=\"$ise_id\" new_value=\"$new_value\" />";
  } else {
    puts -nonewline "<not_found />";
  }
#puts "<return value=\"$res(STDOUT)\" />";
puts -nonewline {</result>}

