#!/bin/tclsh
load tclrega.so
puts -nonewline {Content-Type: text/xml
Access-Control-Allow-Origin: *

<?xml version="1.0" encoding="ISO-8859-1" ?>}

set start "0"
set show "0"
set clear "0"

catch {
 set input $env(QUERY_STRING)
 set pairs [split $input &]
 foreach pair $pairs {
  if {0 != [regexp "^(\[^=]*)=(.*)$" $pair dummy varname val]} {
   set $varname $val
  }
 }
}

puts -nonewline {<systemProtocol>}

append hm_script {
    string drop = "";
    integer iLastGroupIndex = 1;
    string sCollectedNames = "";
    string sCollectedValues = "";
    string sCollectedDateTimes = "";
    string sCollectedTimestamp = "";
    string s;
    integer iStart = }
append hm_script $start
append hm_script {;
    integer iCount = }
append hm_script $show
append hm_script {; 
    integer eCount = dom.GetHistoryDataCount();
    integer clear = }
append hm_script $clear
append hm_script {;
    integer rCount;
    if (iCount == "0") {
      iCount = eCount;
    }
    Write("<records start=\"" # iStart # "\" show=\"" # iCount # "\" count=\"" # eCount # "\"/>");
}

append hm_script {

    if (clear == "1") {
      var clearHistory = dom.ClearHistoryData();
      WriteLine("<cleared_protocol/>");
    } else {

    foreach( s, dom.GetHistoryData( iStart, iCount, &rCount ) )
    {
      integer iGroupIndex = s.StrValueByIndex(";",0).ToInteger();
      string sDatapointId = s.StrValueByIndex(";",1);
      string sRecordedValue = s.StrValueByIndex(";",2);
      string sDateTime = s.StrValueByIndex(";",3);
      string sTimestamp = s.StrValueByIndex(";",3).ToTime().ToInteger();
	    
      string sDatapointName = "";
      object oHistDP = dom.GetObject( sDatapointId );
      if( oHistDP )
      {
        object oDP = dom.GetObject( oHistDP.ArchiveDP() );
        if( oDP )
        {
          sDatapointName = oDP.Name();
          boolean bSysVar = (oDP.IsTypeOf(OT_VARDP) || oDP.IsTypeOf(OT_ALARMDP));
          if( !bSysVar )
          {
            object oCH = dom.GetObject( oDP.Channel() );
            if( oCH )
            {
              sDatapointName = oCH.Name();
            }           
          }
         
          if( iLastGroupIndex != iGroupIndex )
          {
              drop = drop # "<row datetime=\"" # sCollectedDateTimes # "\" names=\"" # sCollectedNames # "\" values=\"" # sCollectedValues # "\" timestamp=\"" # sCollectedTimestamp # "\" />\n";
            sCollectedNames = "";
            sCollectedValues = "";
            iLastGroupIndex = iGroupIndex;
          }
         
          string id = oDP.ID();
          string sRet = "";
          string sValue = sRecordedValue;
          Call("/esp/functions.fn::WriteDPText()");
          sRecordedValue = system.GetVar("sRet");
         
          sCollectedNames = sDatapointName;
          sCollectedDateTimes = sDateTime;
	  sCollectedTimestamp = sTimestamp;
		
          if( !sCollectedValues.Length() )
          {
            sCollectedValues = sRecordedValue;
          }
          else
          {
            sCollectedValues = sCollectedValues#", "#sRecordedValue;
          }
         
        }
      }
     
    }
    if( sCollectedValues.Length() )
    {
      drop = drop # "<row datetime=\"" # sCollectedDateTimes # "\" names=\"" # sCollectedNames # "\" values=\"" # sCollectedValues # "\" timestamp=\"" # sCollectedTimestamp # "\" />";

    }

    Write(drop);
    }
}

array set res [rega_script $hm_script]

puts -nonewline $res(STDOUT)
puts -nonewline {</systemProtocol>}


