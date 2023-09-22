#!/bin/tclsh

set checkURL    "https://raw.githubusercontent.com/homematic-community/XML-API/master/VERSION"
set downloadURL "https://github.com/homematic-community/XML-API/releases"

catch {
  set input $env(QUERY_STRING)
  set pairs [split $input &]
  foreach pair $pairs {
    if {$pair == "cmd=download"} {
      set cmd "download"
      break
    }
  }
}

if { [info exists cmd ] && $cmd == "download"} {
  puts -nonewline "Content-Type: text/html; charset=utf-8\r\n\r\n"
  puts -nonewline "<html><head><meta http-equiv='refresh' content='0; url=$downloadURL' /></head><body></body></html>"
} else {
  puts -nonewline "Content-Type: text/plain; charset=utf-8\r\n\r\n"
  catch {
    set newversion [ exec /usr/bin/wget -qO- --no-check-certificate $checkURL ]
  }
  if { [info exists newversion] } {
    puts $newversion
  } else {
    puts "n/a"
  }
}
