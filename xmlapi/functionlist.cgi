#!/bin/tclsh
load tclrega.so
puts -nonewline {Content-Type: text/xml
Access-Control-Allow-Origin: *

<?xml version="1.0" encoding="ISO-8859-1" ?><functionList>}

array set res [rega_script {
  !*****************************************************************************
  ! Gibt die Gewerkeliste als XML-Datei zurück.
  !*****************************************************************************

	object oFunction;
	string sFunctionId;
	string sChannelId;

	foreach (sFunctionId, dom.GetObject(ID_FUNCTIONS).EnumUsedIDs())
	{
		oFunction     = dom.GetObject(sFunctionId);

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
puts -nonewline $res(STDOUT)
puts -nonewline {</functionList>}

