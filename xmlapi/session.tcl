#!/bin/tclsh
load tclrega.so

catch {
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

  set tokens ""
  if {! [catch {set fd [open $filename r] } errmsg]} {
    set tokens [read $fd]
    close $fd
  }

  return $tokens
}

proc register_token desc {
  set filename "/etc/config/addons/xmlapi/token.list"

  set tokens ""
  if {! [catch {set fd [open $filename r] } errmsg]} {
    set tokens [read $fd]
    close $fd
  }

  # function to generate a random string of 16 characters
  # cf. https://wiki.tcl-lang.org/page/Generating+random+strings
  set newToken [subst [string repeat {[format %c [expr {int(rand() * 26) + (rand() > .5 ? 97 : 65)}]]} 16]]

  # add token to dict
  dict append tokens $newToken $desc

  if {! [catch {set fd [open $filename w] } errmsg]} {
    puts $fd $tokens
  }

  return $newToken
}

proc revoke_token token {
  set filename "/etc/config/addons/xmlapi/token.list"

  set tokens ""
  if {! [catch {set fd [open $filename r] } errmsg]} {
    set tokens [read $fd]
    close $fd
  }

  if {[dict exists $tokens $token]} {
    # remove token from dict
    dict unset tokens $token

    if {! [catch {set fd [open $filename w] } errmsg]} {
      puts $fd $tokens
      return 1
    }
  }

  return 0
}

proc check_session sid {
  # check for api tokens first and then check
  # for webui session ids as well as a fallback
  if {[regexp {^([0-9a-zA-Z]{16})$} $sid all sidnr]} {
    set tokens [get_tokens]

    # check if sid exists in token dict
    if {[dict exists $tokens $sid]} {
      return 1
    }
  } elseif {[regexp {^@([0-9a-zA-Z]{10})@$} $sid all sidnr]} {
    set res [lindex [rega_script "Write(system.GetSessionVarStr('$sidnr'));"] 1]
    if {$res != ""} {
      return 1
    }
  }
  return 0
}
