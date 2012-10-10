#!/bin/tclsh

load tclrega.so
source once.tcl
sourceOnce cgi.tcl
sourceOnce xml.tcl


cgi_eval {

  cgi_input

  set ise_id ""
  set new_value ""

  catch { import ise_id }
  catch { import new_value }

  cgi_content_type "text/xml"
  cgi_http_head

  puts -nonewline {<?xml version="1.0" ?>}  
  puts -nonewline {<result>} 

  set res [rega "dom.GetObject($ise_id).State($new_value);"]
  puts "<changed id=\"$ise_id\"/>"

  puts -nonewline {</result>} 

}

