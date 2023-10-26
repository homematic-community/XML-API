#!/bin/tclsh
load tclrega.so

catch {
  set raddr $env(REMOTE_ADDR)
  set input $env(QUERY_STRING)
  set pairs [split $input &]
  set sid ""
  foreach pair $pairs {
    if {0 != [regexp "^sid=(.*)$" $pair dummy val]} {
      set sid $val
      break
    }
  }
}

proc get_tokens {} {
  set filename "/etc/config/addons/xmlapi/token.list"

  array set tokens {}
  if {! [catch {set fd [open $filename r] } errmsg]} {
    array set tokens [read $fd]
    close $fd
  }

  return [array get tokens]
}

proc save_tokens tokenlist {
  set filename "/etc/config/addons/xmlapi/token.list"

  array set tokens $tokenlist
  if {! [catch {set fd [open $filename w] } errmsg]} {
    puts $fd [array get tokens]
    close $fd
  }
}

proc register_token descr {
  # get tokens
  array set tokens [get_tokens]

  # function to generate a random string of 16 characters
  # cf. https://wiki.tcl-lang.org/page/Generating+random+strings
  set newToken [subst [string repeat {[format %c [expr {int(rand() * 26) + (rand() > .5 ? 97 : 65)}]]} 16]]

  # add token to array
  set tokens($newToken) $descr

  # save tokens
  save_tokens [array get tokens]

  return $newToken
}

proc revoke_token tid {
  # get tokens
  array set tokens [get_tokens]

  if {[info exists tokens($tid)]} {
    # remove token from array
    unset tokens($tid)

    # write out new token list
    save_tokens [array get tokens]
    return 1
  }

  return 0
}

proc check_session session_id {
  global raddr
  # check for api tokens first and then check
  # for webui session ids as well as a fallback
  if {[regexp {^([0-9a-zA-Z]{16})$} $session_id all sidnr]} {
    # get tokens
    array set tokens [get_tokens]

    # check if sid exists in token array
    if {[info exists tokens($session_id)]} {
      return 1
    }
  } elseif {[regexp {^@([0-9a-zA-Z]{10})@$} $session_id all sidnr]} {
    set res [lindex [rega_script "Write(system.GetSessionVarStr('$sidnr'));"] 1]
    if {$res != ""} {
      return 1
    }
  } elseif {$raddr == "127.0.0.1"} {
    # allow all xmlapi requests from localhost without
    # any sid
    return 1
  }
  return 0
}
