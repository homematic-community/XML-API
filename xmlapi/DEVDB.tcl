#!/bin/tclsh

################################################################################
# Ressourcen                                                                   #
################################################################################

source once.tcl

################################################################################
# Konstanten                                                                   #
################################################################################

set DEVDB_DIRECTORY "/www/config/devdescr"
set DEVDB_FILE      "$DEVDB_DIRECTORY/DEVDB.tcl"

################################################################################
# Globale Variablen                                                            #
################################################################################

set DEV_LIST ""

array set DEV_DESCRIPTION ""
array set DEV_PATHS       ""
array set DEV_HIGHLIGHT   ""

################################################################################
# Hilfsfunktionen                                                              #
################################################################################

proc devdb_saveToFile { file_name content } {
  upvar $content file_content

  if { ![catch { open $file_name w } fd] } then {
    puts $fd $file_content
    close $fd
  }
}

proc devdb_loadFromFile { file_name } {
  set content ""
  set fd -1

  catch { set fd [open $file_name r] }
  if { 0 <= $fd } then {
    set content [read $fd]
    close $fd
  }
  return $content
}

################################################################################
# Set-Prozeduren                                                               #
################################################################################

proc AddUIDescription {key} {
  global DEV_LIST

  lappend DEV_LIST $key
}

proc AddDescription {key desc} {
  global DEV_DESCRIPTION

  set DEV_DESCRIPTION($key) $desc
}

proc AddPaths {key p_PATHS} {
  global DEV_PATHS
  upvar $p_PATHS PATHS

  set DEV_PATHS($key) $PATHS
}

proc AddCoordinates {key p_P} {
  global DEV_HIGHLIGHT
  upvar $p_P P

  set DEV_HIGHLIGHT($key) $P
}

################################################################################
# Get- Funktionen                                                              #
################################################################################

proc DEV_getImagePath {key size} {
  global DEV_PATHS DEV_LIST

  if { [lsearch $DEV_LIST $key] < 0 } then { return "" }

  set pathlist $DEV_PATHS($key)
  set path ""

  foreach px $pathlist {

    set asize [lindex $px 0]
    set apath [lindex $px 1]

    if {$asize == $size} then {
      set path $apath
      break
    }
  }


  return $path
}

################################################################################
# Funktionen und Prozeduren für Debug-Ausgaben                                 #
################################################################################

proc PrintCoordinates {} {

  global DEV_HIGHLIGHT
  foreach descr [array names DEV_HIGHLIGHT] {

    puts "Type: $descr -- Coordinates: $DEV_HIGHLIGHT($descr)"
  }
}

proc PrintPaths {} {

  global DEV_PATHS
  foreach descr [array names DEV_PATHS] {
    puts "Type: $descr -- Path: $DEV_PATHS($descr)"
  }
}

proc PrintDescriptions {} {

  global DEV_DESCRIPTION
  foreach descr [array names DEV_DESCRIPTION] {
      puts "Type: $descr -- Description: $DEV_DESCRIPTION($descr)"
  }
}

proc PrintList {} {

  global DEV_LIST
  puts "List: $DEV_LIST"
}

proc Print {} {
  PrintList
  PrintDescriptions
  PrintPaths
  PrintCoordinates
}

################################################################################
# Laden- und erzeugen der Device Datenbank                                     #
################################################################################

proc DEVDB_create { } {
  global DEVDB_DIRECTORY

  set filelist [glob -nocomplain "$DEVDB_DIRECTORY/*.tcl"]

  foreach file $filelist {

    if {[file tail $file] == "DEVDB.tcl"} then { continue }

    set TYPE        ""
    set DESCRIPTION ""
    set PATHLIST    ""
    set P           ""

    sourceOnce $file

    catch {
      AddUIDescription $TYPE
      AddDescription   $TYPE $DESCRIPTION
      AddPaths         $TYPE PATHLIST
      AddCoordinates   $TYPE P
    }
  }
}

proc DEVDB_save { } {
  global DEVDB_FILE
  global DEV_LIST DEV_DESCRIPTION DEV_PATHS DEV_HIGHLIGHT

  array set debdb ""
  set devdb(DEV_LIST)        $DEV_LIST
  set devdb(DEV_DESCRIPTION) [array get DEV_DESCRIPTION]
  set devdb(DEV_PATHS)       [array get DEV_PATHS]
  set devdb(DEV_HIGHLIGHT)   [array get DEV_HIGHLIGHT]

  set content [array get devdb]

  devdb_saveToFile $DEVDB_FILE content
}

proc DEVDB_load { } {
  global DEVDB_FILE
  global DEV_LIST DEV_DESCRIPTION DEV_PATHS DEV_HIGHLIGHT

  unset DEV_LIST
  unset DEV_DESCRIPTION
  unset DEV_PATHS
  unset DEV_HIGHLIGHT

  array set devdb [devdb_loadFromFile $DEVDB_FILE]
  catch {
    set       DEV_LIST        $devdb(DEV_LIST)
    array set DEV_DESCRIPTION $devdb(DEV_DESCRIPTION)
    array set DEV_PATHS       $devdb(DEV_PATHS)
    array set DEV_HIGHLIGHT   $devdb(DEV_HIGHLIGHT)
  }

}

################################################################################
# Obsolute Funktionen und Prozeduren                                           #
################################################################################

#proc Clear {} {
#
#   global DEV_LIST DEV_DESCRIPTION DEV_PATHS DEV_HIGHLIGHT
#
#   set DEV_LIST ""
#   array_clear DEV_DESCRIPTION ""
#   array_clear DEV_PATHS       ""
#   array_clear DEV_HIGHLIGHT   ""
#}

################################################################################
# Einsprungpunkt                                                               #
################################################################################

#if { ![file exists $DEVDB_FILE] } then {
#  DEVDB_create
#  DEVDB_save
#} else {
  DEVDB_load
#}
