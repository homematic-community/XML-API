#!/bin/tclsh

load tclrega.so
source once.tcl
sourceOnce cgi.tcl


cgi_eval {

  cgi_input

  set checkupdate ""
  catch { import checkupdate }

  set maxdurchlaeufe 7
  catch { import maxdurchlaeufe }

  cgi_content_type "text/xml"
  cgi_http_head

  puts -nonewline {<?xml version="1.0" ?>}  
  puts -nonewline {<result>} 

	catch {
		set idlist [split [string trim $checkupdate] ";"]
		set resultids ""
		set zaehler 0
		while { ([llength $resultids] < 1) && ($zaehler < $maxdurchlaeufe) } {
			foreach pair $idlist {
				if {$pair != {} } then {
					set vp [split $pair "="]

					set id [lindex $vp 0]
					set timestamp [lindex $vp 1]

					set res [rega "dom.GetObject($id).Timestamp().ToInteger();"]

					if { $res == $timestamp } {
						continue
					}
			# unterschiedlich, also id merken
					array set res_arr [rega_script "object o=dom.GetObject($id);\nvar value=o.Value();\nvar lastupdate=o.Timestamp().ToInteger();\nvar type=o.TypeName();"]
			#		puts -nonewline $res_arr(STDOUT)
					puts -nonewline "<refresh id=\"$id\" value=\"$res_arr(value)\" lastupdate=\"$res_arr(lastupdate)\" type=\"$res_arr(type)\"/>"
					lappend resultids $id
				}
	    	}
		    if { [llength $resultids] < 1 } {
				after 500
				incr zaehler
		    }
		}
	}
  	puts -nonewline {</result>} 
}

