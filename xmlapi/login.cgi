#!/bin/tclsh
source session.tcl
package require http

puts "Content-Type: text/xml; charset=iso-8859-1"
puts ""
puts -nonewline "<?xml version='1.0' encoding='ISO-8859-1' ?><login>"

# get username+password from query string
set username ""
set password ""
catch {
  set input $env(QUERY_STRING)
  set pairs [split $input &]
  foreach pair $pairs {
    if {0 != [regexp "^username=(.*)$" $pair dummy val]} {
      set username $val
      continue
    }
    if {0 != [regexp "^password=(.*)$" $pair dummy val]} {
      set password $val
      continue
    }
  }
}

# returns value of http header or "" if it does not exist
proc getHttpHeader { pRequest headerName } {
  upvar $pRequest request

  set headerName [string toupper $headerName]
  array set meta $request(meta)
  foreach header [array names meta] {
    if {$headerName == [string toupper $header] } then {
      return $meta($header)
    }
  }

  return ""
}

# perform login and create of session
set LOGIN_URL http://127.0.0.1/login.htm
set request  [::http::geturl $LOGIN_URL -query [::http::formatQuery tbUsername $username tbPassword $password]]
set location [getHttpHeader $request location]
set code     [::http::code $request]
::http::cleanup $request

set sid ""
if { -1 == [string first 503 $code] &&
      0 != [regexp {sid=(@[^@]*@)} $location dummy sid]}  then {

  # check if sid is really valid
  if {[check_session $sid]} {
    # output sid to allow to be reused for other requests
    puts -nonewline "<session id='$sid' />"
  } else {
    puts -nonewline {<not_authenticated/>}
  }
} else {
  puts -nonewline {<not_authenticated/>}
}
puts "</login>"
