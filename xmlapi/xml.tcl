#!/bin/tclsh

#*******************************************************************************
# xml.tcl
# Hilffunktionen f�r den Umgang mit XML.
#
# Autor      : Falk Werner
# Erstellt am: 28.04.2008
#*******************************************************************************

################################################################################
# Funktionen und Prozeduren                                                    #
################################################################################

#*******************************************************************************
# xml_escape
# Ersetzt spezielle Sonderzeichen durch die g�ngigen XML-Umschreibungen.
#
# Neben den XML-spezifischen Zeichen <, > und & werden auch die deutschen
# Umlauter �, �, �, �, � und � sowie das scharfe S (�) ersetzt.
#*******************************************************************************
proc xml_escape { value } {
  set     xml_map ""

  lappend xml_map "<" "&lt;"
  lappend xml_map ">" "&gt;"
  lappend xml_map "&" "&amp;"

  lappend xml_map "�" "&#196;"
  lappend xml_map "�" "&#214;"
  lappend xml_map "�" "&#220;"

  lappend xml_map "�" "&#228;"
  lappend xml_map "�" "&#246;"
  lappend xml_map "�" "&#252;"
  lappend xml_map "�" "&#223;"

  return [string map $xml_map $value]
}
