#!/bin/tclsh
source once.tcl

array set TYPE_MAP {
    "BOOL" "bool"
    "ENUM" "int"
    "INTEGER" "int"
    "FLOAT" "double"
    "STRING" "string"
    "ACTION" "bool"
}

loadOnce tclrpc.so

proc decr {x {cnt 1}} {
       upvar $x xx
       set xx [expr { $xx - $cnt }]
}
proc max {x y} { expr { $x > $y ? $x : $y } }
proc min {x y} { expr { $x > $y ? $y : $x } }

proc cgi_cgi {args} {return $args}

proc in {list element} {expr { [lsearch -exact $list $element] >= 0 } }

proc array_clear {name} {
    upvar $name arr
    foreach key [array names arr] {
              unset arr($key)
    }
}

#Liest eine Datei ein mit dem Format
#Key=Value
#Key=Value
#...
#<.
#und speichert die Werte in einem übergebenen Array ab.
proc read_assignment_file {filename value_array} {

    upvar $value_array arr

       set ret -1

       if { ! [catch {open $filename RDONLY} f] } then {

              while {1} {

                     gets $f zeile

                     #                 Weiche EOF-Marke
                     if { [eof $f] || [string equal $zeile "<."] } break

                     set data [split $zeile =]

                     if {$zeile == "" || [lindex $data 0] == ""} then {continue}

                     set arr([lindex $data 0]) [lindex $data 1]
              }

              close $f
       }

       return $ret
}

#Schreibt ein Array in eine Datei. Format, siehe read_assignment_file
proc write_assignment_file {filename value_array {soft_eof 1}} {

    upvar $value_array arr

       set ret -1

       if { ! [catch {open $filename w} f] } then {

              foreach key [array names arr] {
                     puts $f "$key=$arr($key)"
              }

              #Weiche EOF-Marke
              if {$soft_eof} then { puts $f "<." }

              close $f

              set ret 1
       }

       return $ret
}

#Abgewandelt von http://wiki.tcl.tk/1017
#proc verbose_eval
#15.02.2007
proc eval_script {script} {

       set cmd ""
       set ret -1

       foreach line [split $script \n] {

              if {$line == ""} {continue}
              append cmd $line\n

              if { [info complete $cmd] } {
                     #puts -nonewline $cmd
                     set ret [uplevel 1 $cmd]
                     set cmd ""
              }
       }

       return $ret
}

proc putimage {img_path} {

       set in [open $img_path]

       catch {fconfigure stdout -translation binary}
       catch {fconfigure stdout -encoding binary}
       catch {fconfigure $in    -translation binary}
       catch {fconfigure $in    -encoding binary}

       puts -nonewline stdout [read $in]

       close $in
}

proc uniq {liste} {

       set u_list ""
       set last_e ""

       foreach e [lsort $liste] {
              if {$e != $last_e} then {
                     lappend u_list $e
                     set last_e $e
              }
       }

       return $u_list
}

set INTERFACES_FILE "/etc/config/InterfacesList.xml"
array set interfaces ""
array set interface_descriptions ""

proc read_interfaces {} {
  global interfaces interface_descriptions INTERFACES_FILE env
  set retval 1
  if { [ info exists env(BIDCOS_SERVICE) ] } {
    set interfaces(default) "$env(BIDCOS_SERVICE)"
    set interface_descriptions(default) "Default BidCoS Interface"
  } else {
    set fd -1
    catch {set fd [open $INTERFACES_FILE r]}
    if { $fd >=0 } {
      set contents [read $fd]
      while { [regexp -indices {</ipc[^>]*>} $contents range] } {
        set section [string range $contents 0 [lindex $range 1]]
        set contents [string range $contents [expr { [lindex $range 1] + 1 }] end]
        if {
             [regexp {<name[^>]*>([^<]+)</name} $section dummy name] &&
             [regexp {<url[^>]*>([^<]+)</url} $section dummy url] &&
             [regexp {<info[^>]*>([^<]+)</info} $section dummy description ]
           } {
             array set interfaces [list $name $url]
             array set interface_descriptions [list $name $description]
           }
      }
      close $fd
    } else {
      puts "Could not open interface file"
      set retval 0
    }
  }
  return $retval
}
