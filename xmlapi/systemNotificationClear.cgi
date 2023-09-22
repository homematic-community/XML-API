#!/bin/tclsh
source session.tcl

puts "Content-Type: text/xml; charset=iso-8859-1"
puts ""
puts -nonewline "<?xml version='1.0' encoding='ISO-8859-1' ?><systemNotificationClear>"

if {[info exists sid] && [check_session $sid]} {

  set hm_script {
    string itemID;
    string address;
    object aldp_obj;

    foreach(itemID, dom.GetObject(ID_DEVICES).EnumUsedIDs()) {
      address = dom.GetObject(itemID).Address();
      aldp_obj = dom.GetObject("AL-" # address # ":0.STICKY_UNREACH");
      if (aldp_obj) {
        if (aldp_obj.Value()) {
          aldp_obj.AlReceipt();
        }
      }
    }
  }

  array set res [rega_script $hm_script]

  if { $res(STDOUT) != "" } {
    puts -nonewline $res(STDOUT)
  }
} else {
  puts -nonewline {<not_authenticated/>}
}
puts "</systemNotificationClear>"
