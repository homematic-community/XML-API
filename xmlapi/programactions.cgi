#!/bin/tclsh
source session.tcl

puts "Content-Type: text/xml; charset=iso-8859-1"
puts ""
puts -nonewline "<?xml version='1.0' encoding='ISO-8859-1' ?><result>"

if {[info exists sid] && [check_session $sid]} {

  set program_id "-1"
  set active ""
  set visible ""
  catch {
    set input $env(QUERY_STRING)
    set pairs [split $input &]
    foreach pair $pairs {
      if {0 != [regexp "^program_id=(.*)$" $pair dummy val]} {
        set program_id $val
        continue
      }
      if {0 != [regexp "^active=(.*)$" $pair dummy val]} {
        set active $val
        continue
      }
      if {0 != [regexp "^visible=(.*)$" $pair dummy val]} {
        set visible $val
        continue
      }
    }
  }

  array set res [rega_script {
    integer prgId = } $program_id {;
    string active = "} $active {";
    string visible = "} $visible {";
    if (prgId > 0) {
      object obj = dom.GetObject(prgId);
      if (obj && obj.IsTypeOf(OT_PROGRAM)) {
        if ((active == "false") || (active == "true")){
          obj.Active(active == "true");
        }
        if ((visible == "false") || (visible == "true")){
          obj.Visible(visible == "true");
        }
        Write(obj);
      }
    }
  }]

  if { $res(STDOUT) != "" } {
    puts -nonewline "<actions program_id=\"$res(prgId)\" active=\"$res(active)\" visible=\"$res(visible)\"/>"
  } else {
    puts -nonewline {<not_found/>}
  }
} else {
  puts -nonewline {<not_authenticated/>}
}
puts "</result>"
