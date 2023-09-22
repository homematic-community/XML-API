#!/bin/tclsh
source session.tcl

puts "Content-Type: text/xml; charset=iso-8859-1"
puts ""
puts -nonewline "<?xml version='1.0' encoding='ISO-8859-1' ?><programList>"

if {[info exists sid] && [check_session $sid]} {

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
        Write("' visible='");
        WriteXML(oProgram.Visible());
        Write("' operate='");

        object o_sysVar = dom.GetObject(sProgramId);

        if( o_sysVar.UserAccessRights(iulOtherThanAdmin) == iarFullAccess ) {
          Write("true");
        } else {
          Write("false");
        }

        Write("'/>");
      }
    }

  }]

  if { $res(STDOUT) != "" } {
    puts -nonewline $res(STDOUT)
  }
} else {
  puts -nonewline {<not_authenticated/>}
}
puts "</programList>"
