#!/bin/tclsh

load tclrega.so

set ise_id ""
set new_value ""

catch {
  set input $env(QUERY_STRING)
  set pairs [split $input &]
  foreach pair $pairs {
    if {0 != [regexp "^(\[^=]*)=(.*)$" $pair dummy varname val]}
      set $varname $val      
    }    
  }
}
puts {Content-Type: text/xml

<?xml version="1.0" encoding="ISO-8859-1" ?>
<result>}

array set res [rega_script "Write(dom.GetObject($ise_id).State($new_value));"]
if {$res(STDOUT) != "null"} {
  puts "<changed id=\"$ise_id\"/>";
  } else {
    puts "<not_found />";
  }
#puts "<return value=\"$res(STDOUT)\" />";
puts -nonewline {</result>}
