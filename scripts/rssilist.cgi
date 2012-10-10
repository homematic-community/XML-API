#!/bin/tclsh

source once.tcl
sourceOnce cgi.tcl
sourceOnce xml.tcl
sourceOnce common.tcl

loadOnce tclrpc.so

set RSSI_BAD -120.0
set RSSI_MEDIUM -100.0
set RSSI_GOOD -20.0



#  !*****************************************************************************
#  !* rssilist.cgi
#  !* Signalqualitaet aller funk komponenten
#  !*
#  !* Autor      : Dirk Szymanski
#  !* Erstellt am: gleich, kleinen moment noch
#  !*
#  !*****************************************************************************



cgi_eval {

	set url "xmlrpc_bin://127.0.0.1:2001"

	cgi_input
	cgi_content_type "text/xml"
	cgi_http_head

	puts -nonewline {<?xml version="1.0" ?>}
	puts -nonewline {<rssiList>}

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
	puts -nonewline {</rssiList>}
}
