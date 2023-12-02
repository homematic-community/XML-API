#!/bin/tclsh
source session.tcl

puts "Content-Type: text/xml; charset=iso-8859-1"
puts ""
puts -nonewline "<?xml version='1.0' encoding='ISO-8859-1' ?><functionList>"

if {[info exists sid] && [check_session $sid]} {

  array set res [rega_script {
    !*****************************************************************************
    ! Gibt die Gewerkeliste als XML-Datei zurück.
    !*****************************************************************************

    object oFunction;
    string sFunctionId;
    string sChannelId;

    foreach (sFunctionId, dom.GetObject(ID_FUNCTIONS).EnumUsedIDs())
    {
      oFunction = dom.GetObject(sFunctionId);

      Write("<function name='");WriteXML( oFunction.Name() );
      Write("' description='");WriteXML( oFunction.EnumInfo() );
      Write("' ise_id='" # sFunctionId # "'>");

      foreach(sChannelId, oFunction.EnumUsedIDs())
      {
        Write("<channel address='"); WriteXML( dom.GetObject(sChannelId).Address() );
        Write("' ise_id='" # sChannelId # "'/>");
      }

      Write("</function>");
    }
  }]

  if { $res(STDOUT) != "" } {
    puts -nonewline $res(STDOUT)
  }
} else {
  puts -nonewline {<not_authenticated/>}
}
puts "</functionList>"
