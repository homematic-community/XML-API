#!/bin/tclsh
load tclrega.so
puts -nonewline {Content-Type: text/xml
Access-Control-Allow-Origin: *

<?xml version="1.0" encoding="ISO-8859-1" ?>}

puts -nonewline {<programList>}

array set res [rega_script {

string sProgramId;
object oProgram; 
foreach (sProgramId, dom.GetObject(ID_PROGRAMS).EnumUsedIDs())
{
	oProgram = dom.GetObject(sProgramId);
	if(oProgram != null)
	{
		Write("<program id='" # sProgramId #"' active='" # oProgram.Active() # "'")
		Write(" timestamp='" # oProgram.ProgramLastExecuteTime().ToInteger() #"' name='");
		WriteXML( oProgram.Name() );
		Write("' description='");
		WriteXML(oProgram.PrgInfo());
		Write("'/>");
	}
}

}]

puts -nonewline $res(STDOUT)
puts -nonewline {</programList>}
