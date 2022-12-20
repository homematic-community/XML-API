#!/bin/tclsh

load tclrega.so

catch {
  set input $env(QUERY_STRING)
  set pairs [split $input &]
  set sid ""
  foreach pair $pairs {
    if {0 != [regexp "^sid=(@.*@)$" $pair dummy val]} {
      set sid $val
      break
    }
  }
}

proc check_session sid {
  if {[regexp {@([0-9a-zA-Z]{10})@} $sid all sidnr]} {
    set res [lindex [rega_script "Write(system.GetSessionVarStr('$sidnr'));"] 1]
    if {$res != ""} {
      return 1
    }
  }
  return 0
}
