#!/bin/tclsh
load tclrega.so
puts -nonewline {Content-Type: text/xml
Access-Control-Allow-Origin: *

<?xml version="1.0" encoding="ISO-8859-1" ?><systemVariables>}

set text "true"
set ise_id "-1"

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
	string iSysVarId=}
append hm_script $ise_id
append hm_script {;

	foreach (sSysVarId, dom.GetObject(ID_SYSTEM_VARIABLES).EnumUsedIDs()){

		oSysVar = dom.GetObject(sSysVarId);
		
		if (oSysVar.ID() == iSysVarId) {					   
			
		    Write("<systemVariable");
		    Write(" name='"); WriteXML( oSysVar.Name() );
                    Write("' variable='");
                    if (oSysVar.ValueSubType() == 6) {
                      WriteXML( oSysVar.AlType());
                    } else {
                      WriteXML( oSysVar.Variable());
                    }
                    Write("' value='"); WriteXML( oSysVar.Value());
	
    		    if (sShowText == "true") {
                  Write("' value_list='");
        	        if (oSysVar.ValueType() == 16) {
                 		WriteXML( oSysVar.ValueList());
                        }
        	        Write("' value_text='"); WriteXML( oSysVar.ValueList().StrValueByIndex(';', oSysVar.Value()));
                    }
	
                    Write("' ise_id='"); WriteXML( oSysVar.ID());
                    Write("' min='"); WriteXML( oSysVar.ValueMin());
                    Write("' max='"); WriteXML( oSysVar.ValueMax());
                    Write("' unit='"); WriteXML( oSysVar.ValueUnit());
                    Write("' type='"); WriteXML( oSysVar.ValueType());
                    Write("' subtype='"); WriteXML( oSysVar.ValueSubType());
                    Write("' timestamp='"); WriteXML( oSysVar.Timestamp().ToInteger());
	
                    Write("' value_name_0='");
                    if (oSysVar.ValueType() == 2) {
    			            WriteXML( oSysVar.ValueName0());
                    }
                    Write("' value_name_1='");
                    if (oSysVar.ValueType() == 2) {
    			            WriteXML( oSysVar.ValueName1());
                    }
    		    Write("'/>");
		}
	}
}

array set res [rega_script $hm_script]

puts -nonewline $res(STDOUT)
puts -nonewline {</systemVariables>}
