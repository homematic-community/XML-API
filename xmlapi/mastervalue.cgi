#!/bin/tclsh
load tclrpc.so
source session.tcl
source common.tcl

puts "Content-Type: text/xml; charset=iso-8559-1"
puts ""
puts -nonewline "<?xml version='1.0' encoding='ISO-8859-1' ?><mastervalue>"

if {[info exists sid] && [check_session $sid]} {

  set device_id ""
  set requested_names ""
  catch {
    set input $env(QUERY_STRING)
    set pairs [split $input &]
    foreach pair $pairs {
      if {0 != [regexp "^device_id=(.*)$" $pair dummy val]} {
        set device_id $val
        continue
      }
      if {0 != [regexp "^requested_names=(.*)$" $pair dummy val]} {
        set requested_names $val
        continue
      }
    }
  }

  read_interfaces

  set devids [split $device_id ,]
  if { $requested_names == "" } {
    set allMasterValues "*"
  } else {
    set allMasterValues ""
    set requestedNames [split $requested_names ,]
  }

  foreach devid $devids {
    array set values [rega_script {
      integer iseId = "} $devid {";
      var oDevice = dom.GetObject(iseId);
      var address = oDevice.Address();
      var deviceType = oDevice.HssType();
      Write("<device");
      Write(" name='");
      WriteXML(oDevice.Name());
      Write("'");
      Write(" ise_id='" # iseId # "'");
      Write(" device_type='");
      WriteXML(deviceType);
      Write("'");
      Write(" >");
    }]
    set deviceAddress $values(address)
    set deviceType $values(deviceType)

    puts -nonewline $values(STDOUT)

    # simple check against unknown device id
    if { $deviceType == "null" } {
      puts -nonewline {<device ise_id="}
      puts -nonewline $devid
      puts -nonewline {" error="true">DEVICE NOT FOUND</device>}
    } else {
      # initialize variable, could fail in catch block below
      set ausgabe ""
      if {[string compare -nocase -length 9 "HM-CC-VG-" $deviceType] == 0} {
        catch {set ausgabe [xmlrpc $interfaces(VirtualDevices) getParamset [list string $deviceAddress] [list string "MASTER"] ] }
      } elseif {[string compare -nocase -length 5 "HMIP-" $deviceType] == 0} {
        catch {set ausgabe [xmlrpc $interfaces(HmIP-RF) getParamset [list string $deviceAddress] [list string "MASTER"] ] }
      } else {
        catch {set ausgabe [xmlrpc $interfaces(BidCos-RF) getParamset [list string $deviceAddress] [list string "MASTER"] ] }
      }

      foreach { bezeichnung wert } $ausgabe {
        if { ($allMasterValues == "*" || [lsearch $requestedNames $bezeichnung] >= 0) } {
          puts -nonewline {<mastervalue name='}
          puts -nonewline $bezeichnung
          puts -nonewline {' value='}
          puts -nonewline $wert
          puts -nonewline {'/>}
        }
      }

      puts -nonewline {</device>}
    }
  }
} else {
  puts -nonewline {<not_authenticated/>}
}
puts "</mastervalue>"