#!/bin/tclsh

#*******************************************************************************
# xml.tcl
# Hilffunktionen für den Umgang mit XML.
#
# Autor      : Falk Werner
# Erstellt am: 28.04.2008
#*******************************************************************************

################################################################################
# Funktionen und Prozeduren                                                    #
################################################################################

#*******************************************************************************
# xml_escape
# Ersetzt spezielle Sonderzeichen durch die gängigen XML-Umschreibungen.
#
# Neben den XML-spezifischen Zeichen <, > und & werden auch die deutschen
# Umlauter Ä, Ö, Ü, ä, ö und ü sowie das scharfe S (ß) ersetzt.
#*******************************************************************************
proc xml_escape { value } {
  set     xml_map ""

  lappend xml_map "<" "&lt;"
  lappend xml_map ">" "&gt;"
  lappend xml_map "&" "&amp;"

  lappend xml_map "Ä" "&#196;"
  lappend xml_map "Ö" "&#214;"
  lappend xml_map "Ü" "&#220;"

  lappend xml_map "ä" "&#228;"
  lappend xml_map "ö" "&#246;"
  lappend xml_map "ü" "&#252;"
  lappend xml_map "ß" "&#223;"

  return [string map $xml_map $value]
}
