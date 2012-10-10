#!/bin/tclsh

load tclrega.so
source once.tcl
sourceOnce cgi.tcl
sourceOnce xml.tcl


cgi_eval {

  cgi_input

  set ise_id ""

  catch { import program_id }

  cgi_content_type "text/xml"
  cgi_http_head

  puts -nonewline {<?xml version="1.0" ?>}  
  puts -nonewline {<result>} 

  array set res_arr [rega_script "object obj = dom.GetObject($program_id); if (obj) { obj.ProgramExecute(); }"]
  if { $res_arr(obj) != "" } { 
  	puts "<started program_id=\"$program_id\"/>"
  } else {
  	puts "<not_found/>"
  }  
  puts -nonewline {</result>} 

}

