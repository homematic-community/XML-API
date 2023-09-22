#!/bin/tclsh
#  !*****************************************************************************
#  !* rssilist.cgi
#  !* Signalqualitaet aller funk komponenten
#  !* Autor: Dirk Szymanski
#  !*****************************************************************************
source session.tcl

puts "Content-Type: text/xml; charset=iso-8859-1"
puts ""
puts -nonewline "<?xml version='1.0' encoding='ISO-8859-1' ?><rssiList>"

if {[info exists sid] && [check_session $sid]} {

  load tclrpc.so
  source common.tcl

  set RSSI_BAD -120.0
  set RSSI_MEDIUM -100.0
  set RSSI_GOOD -20.0

  read_interfaces

  set url $interfaces(BidCos-RF)

  if { [ catch {
    #check if the interface supports rssi
    #failure of this call will throw us out of here
    xmlrpc $url system.methodHelp rssiInfo
  } ] } { continue }

  array_clear rssi_map
  set rssi_list [xmlrpc $url rssiInfo ]
  array set rssi_map $rssi_list

  foreach dev [lsort [array names rssi_map]] {
    puts -nonewline "<rssi device='$dev' rx='[lindex [lindex $rssi_map($dev) 1] 0]' tx='[lindex [lindex $rssi_map($dev) 1] 1]'/>"
  }

} else {
  puts -nonewline {<not_authenticated/>}
}
puts "</rssiList>"
