#!/bin/tclsh

load tclrega.so
source once.tcl
sourceOnce cgi.tcl


cgi_eval {

	cgi_input                    
	cgi_content_type "text/xml"     
	cgi_http_head

	puts -nonewline {<?xml version="1.0" encoding="ISO-8859-1" ?><systemVariables>}

	array set res [rega_script {

		object oSysVar;
		string sSysVarId;

		foreach (sSysVarId, dom.GetObject(ID_SYSTEM_VARIABLES).EnumUsedIDs())
		{
			oSysVar     = dom.GetObject(sSysVarId);
			Write("<systemVariable");
			Write(" name='"); WriteXML( oSysVar.Name() );
			Write("' variable='"); WriteXML( oSysVar.Variable());
			Write("' value='"); WriteXML( oSysVar.Value());
			Write("' value_list='"); WriteXML( oSysVar.ValueList());
			Write("' ise_id='" # oSysVar.ID() );
			Write("' min='"); WriteXML( oSysVar.ValueMin());
			Write("' max='"); WriteXML( oSysVar.ValueMax());
			Write("' unit='"); WriteXML( oSysVar.ValueUnit());
			Write("' type='" # oSysVar.ValueType() # "' subtype='" # oSysVar.ValueSubType());
			Write("' logged='"); WriteXML( oSysVar.DPArchive());
			Write("' visible='"); WriteXML( oSysVar.Visible());
			Write("' timestamp='" # oSysVar.Timestamp().ToInteger());
			Write("'/>");
		}

	}]

	puts -nonewline $res(STDOUT)
	puts -nonewline {</systemVariables>}
}
