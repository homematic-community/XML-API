#!/bin/tclsh

load tclrega.so
source once.tcl
sourceOnce cgi.tcl

puts -nonewline {<?xml version="1.0" encoding="ISO-8859-1" ?>}
puts -nonewline {<version>1.2}
puts -nonewline {</version>}
}
