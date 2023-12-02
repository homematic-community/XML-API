#!/bin/tclsh
load tclrpc.so
source session.tcl
source common.tcl

puts "Content-Type: text/xml; charset=iso-8859-1"
puts ""
puts -nonewline "<?xml version='1.0' encoding='ISO-8859-1' ?><mastervalue>"

if {[info exists sid] && [check_session $sid]} {

  set device_id ""
  set name ""
  set value ""
  catch {
    set input $env(QUERY_STRING)
    set pairs [split $input &]
    foreach pair $pairs {
      if {0 != [regexp "^device_id=(.*)$" $pair dummy val]} {
        set device_id $val
        continue
      }
      if {0 != [regexp "^name=(.*)$" $pair dummy val]} {
        set name $val
        continue
      }
      if {0 != [regexp "^value=(.*)$" $pair dummy val]} {
        set value $val
        continue
      }
    }
  }

  read_interfaces

  set rec_devids [split $device_id "\,"]
  set rec_mvaluename [split $name "\,"]
  set rec_mvaluevalue [split $value "\,"]

  for {set counter 0} {$counter<[llength $rec_devids]} {incr counter} {
    set devid [lindex $rec_devids $counter]

    set item [lindex $rec_mvaluename $counter]
    set val [lindex $rec_mvaluevalue $counter]
    set cmd "{$item {string $val}}"

    array set values [rega_script {
      integer iseId = "} $devid {";
      var oDevice = dom.GetObject(iseId);
      var address = oDevice.Address();
      integer ifId = oDevice.Interface();
      object oDeviceInterface = dom.GetObject(ifId);
      if(oDeviceInterface)
      {
        string deviceInterface = oDeviceInterface.Name();
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
      }
    }]
    set deviceAddress $values(address)
    set deviceType $values(deviceType)
    set deviceInterface $values(deviceInterface)

    puts -nonewline $values(STDOUT)

    # simple check against unknown device id
    if { $deviceType == "null" } {
      puts -nonewline {<device ise_id="}
      puts -nonewline $devid
      puts -nonewline {" error="true">DEVICE NOT FOUND</device>}
    } else {
      # initialize variable, could fail in catch block below
      set channel ""
      if {[string compare -nocase -length 4 "HmIP" "$deviceInterface"] == 0 ||
          [string compare -nocase -length 4 "HmIP" "$deviceType"] == 0 } {
        # HmIP requires to add :0 to deviceAddress
        set channel ":0"
      }

      # call xmlrpc to set the MASTER paramset
      set ausgabe ""
      catch {set ausgabe [xmlrpc $interfaces($deviceInterface) putParamset [list string "$deviceAddress$channel"] [list string "MASTER"] [list struct $cmd] ] }

      puts -nonewline {<mastervalue name='}
      puts -nonewline $item
      puts -nonewline {' value='}
      puts -nonewline $val
      puts -nonewline {'/>}
      puts -nonewline {</device>}
    }
  }
} else {
  puts -nonewline {<not_authenticated/>}
}
puts "</mastervalue>"
