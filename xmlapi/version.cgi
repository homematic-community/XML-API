#!/bin/tclsh
set filename "/www/addons/xmlapi/VERSION"
set fd [open $filename r]
set version ""
if { $fd >=0 } {
  gets $fd version
  close $fd
}

puts "Content-Type: text/xml; charset=iso-8859-1"
puts ""
puts -nonewline "<?xml version='1.0' encoding='ISO-8859-1' ?><version>"

puts -nonewline $version

puts "</version>"
