#!/bin/tclsh
load tclrega.so
puts -nonewline {Content-Type: text/xml
Access-Control-Allow-Origin: *

<?xml version="1.0" encoding="ISO-8859-1" ?><systemNotificationClear>}

append hm_script {;

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

puts -nonewline $res(STDOUT)
puts -nonewline {</systemNotificationClear>}