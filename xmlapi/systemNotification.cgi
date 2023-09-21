#!/bin/tclsh
source session.tcl

puts "Content-Type: text/xml; charset=iso-8859-1"
puts ""
puts -nonewline "<?xml version='1.0' encoding='ISO-8859-1' ?><systemNotification>"

if {[info exists sid] && [check_session $sid]} {

  set hm_script {
    object oTmpArray = dom.GetObject(ID_SERVICES);

    if( oTmpArray ) {
      string sTmp;

      foreach(sTmp, oTmpArray.EnumIDs()){

        object oTmp = dom.GetObject( sTmp );

        if( oTmp ){
          if( oTmp.IsTypeOf( OT_ALARMDP ) && ( oTmp.AlState() == asOncoming ) ){

            var trigDP = dom.GetObject(oTmp.AlTriggerDP());
            if( trigDP ) {
              Write("<notification ise_id='");
              !WriteXML( oTmp.ID());
              WriteXML( oTmp.AlTriggerDP());
              Write("' name='");
              WriteXML( trigDP.Name());
              Write("' type='");
              WriteXML(trigDP.HssType());
              Write("' timestamp='");
              WriteXML(trigDP.Timestamp().ToInteger());
              Write("'/>");
            }
          }
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
puts "</systemNotification>"
