#!/bin/tclsh
set filename "/www/addons/xmlapi/VERSION"
set fd [open $filename r]
set version ""
if { $fd >=0 } {
  gets $fd version
  close $fd
}

set output "Content-Type: text/xml
Access-Control-Allow-Origin: *

<?xml version='1.0' encoding='ISO-8859-1' ?><version>$version</version>"

puts -nonewline $output
