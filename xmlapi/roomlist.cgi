#!/bin/tclsh
source session.tcl

puts "Content-Type: text/xml; charset=iso-8859-1"
puts ""
puts -nonewline "<?xml version='1.0' encoding='ISO-8859-1' ?><roomList>"

if {[info exists sid] && [check_session $sid]} {
  array set res [rega_script {

      object oRoom;
      string sRoomId;
      string sRoomName;
      string sChannelId;

      foreach (sRoomId, dom.GetObject(ID_ROOMS).EnumUsedIDs())
      {
        oRoom     = dom.GetObject(sRoomId);

        Write("<room name='");    WriteXML( oRoom.Name() );
        Write("' ise_id='" # sRoomId # "'>");

        foreach(sChannelId, oRoom.EnumUsedIDs())
        {
          Write("<channel ise_id='" # sChannelId # "'/>");
        }

        Write("</room>");
      }

  }]

  if { $res(STDOUT) != "" } {
    puts -nonewline $res(STDOUT)
  }
} else {
  puts -nonewline {<not_authenticated/>}
}
puts "</roomList>"
