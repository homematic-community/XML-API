#!/bin/tclsh

load tclrega.so

set program_id ""

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

array set res [rega_script "object obj = dom.GetObject($program_id); if (obj) { obj.ProgramExecute(); Write(obj); }"]

if { $res(STDOUT) != "" } {
 puts -nonewline "<started program_id=\"$program_id\"/>"
} else {
 puts -nonewline {<not_found/>}
}

puts -nonewline {</result>}


