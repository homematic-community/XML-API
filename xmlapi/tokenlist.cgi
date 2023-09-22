#!/bin/tclsh
#
# script to list all currently registred API tokens
#
# parameters: none
# return: list of currently active API tokens
#

source session.tcl

puts "Content-Type: text/xml; charset=iso-8859-1"
puts ""
puts -nonewline "<?xml version='1.0' encoding='ISO-8859-1' ?><tokens>"

if {[info exists sid] && [check_session $sid]} {

  set tokens [get_tokens]

  dict for {token desc} $tokens {
    puts "<token desc='$desc'>$token</token>"
  }

} else {
  puts -nonewline {<not_authenticated/>}
}
puts "</tokens>"
