#!/bin/tclsh
load tclrega.so
puts  {Content-Type: text/xml

<?xml version="1.0" encoding="ISO-8859-1" ?><systemVariables>}

set ise_id ""
set text "false"

catch {
 set input $env(QUERY_STRING)
 set pairs [split $input &]
 foreach pair $pairs {
  if {0 != [regexp "^(\[^=]*)=(.*)$" $pair dummy varname val]} {
   set $varname $val
  }
 }
}

append hm_script {

	object oSysVar;
	string sSysVarId;
	string sShowText=
} 

append hm_script $text

append hm_script {;

	foreach (sSysVarId, dom.GetObject(ID_SYSTEM_VARIABLES).EnumUsedIDs()) {
		oSysVar     = dom.GetObject(sSysVarId);
		Write("<systemVariable");
		Write(" name='"); WriteXML( oSysVar.Name() );
		Write("' variable='"); WriteXML( oSysVar.Variable());
		Write("' value='"); WriteXML( oSysVar.Value());
		if (sShowText == "true") {
			Write("' value_list='"); WriteXML( oSysVar.ValueList());
			Write("' value_text='"); WriteXML( oSysVar.ValueList().StrValueByIndex(';', oSysVar.Value()));
		}
		Write("' ise_id='" # oSysVar.ID() );
		Write("' min='"); WriteXML( oSysVar.ValueMin());
		Write("' max='"); WriteXML( oSysVar.ValueMax());
		Write("' unit='"); WriteXML( oSysVar.ValueUnit());
		Write("' type='" # oSysVar.ValueType() # "' subtype='" # oSysVar.ValueSubType());
		Write("' timestamp='" # oSysVar.Timestamp().ToInteger());
		Write("'/>");
	}

}

array set res [rega_script $hm_script]

puts -nonewline $res(STDOUT)
puts -nonewline {</systemVariables>}