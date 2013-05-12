#!/bin/tclsh
load tclrega.so
puts -nonewline {Content-Type: text/xml
Access-Control-Allow-Origin: *

<?xml version="1.0" encoding="ISO-8859-1" ?><systemVariables>}

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
                if (oSysVar.ValueType() == 16) {
                        Write("' value_list='"); WriteXML( oSysVar.ValueList());
                } else {
                        Write("' value_list='");
                }
                Write("' ise_id='"); WriteXML( oSysVar.ID());
                if (sShowText == "true") {
                        Write("' value_text='"); WriteXML( oSysVar.ValueList().StrValueByIndex(';', oSysVar.Value()));
                }
                Write("' min='"); WriteXML( oSysVar.ValueMin());
                Write("' max='"); WriteXML( oSysVar.ValueMax());
                Write("' unit='"); WriteXML( oSysVar.ValueUnit());
                Write("' type='"); WriteXML( oSysVar.ValueType());
                Write("' subtype='"); WriteXML( oSysVar.ValueSubType());
                Write("' logged='"); WriteXML( oSysVar.DPArchive());
                Write("' visible='"); WriteXML( oSysVar.Visible());
                Write("' timestamp='"); WriteXML( oSysVar.Timestamp().ToInteger());
                if (oSysVar.ValueType() == 2) {
                        Write("' value_name_0='"); WriteXML( oSysVar.ValueName0());
                        Write("' value_name_1='"); WriteXML( oSysVar.ValueName1());
                } else {
                        Write("' value_name_0='");
                        Write("' value_name_1='");
                }
                Write("'/>");
	}

}

array set res [rega_script $hm_script]

puts -nonewline $res(STDOUT)
puts -nonewline {</systemVariables>}
