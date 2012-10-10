#!/bin/tclsh

load tclrega.so
source once.tcl
sourceOnce cgi.tcl


cgi_eval {

#  cgi_input

  cgi_content_type "text/xml"
  cgi_http_head
  puts -nonewline {<?xml version="1.0" encoding="ISO-8859-1" ?>}
  puts -nonewline {<roomList>}

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
  puts -nonewline $res(STDOUT)
  puts -nonewline {</roomList>}
}
