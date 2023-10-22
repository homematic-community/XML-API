#!/bin/tclsh
source session.tcl

puts "Content-Type: text/xml; charset=iso-8859-1"
puts ""
puts -nonewline "<?xml version='1.0' encoding='ISO-8859-1' ?><systemProtocol>"

if {[info exists sid] && [check_session $sid]} {

  set start "0"
  set show "0"
  set clear "0"
  catch {
    set input $env(QUERY_STRING)
    set pairs [split $input &]
    foreach pair $pairs {
      if {0 != [regexp "^start=(.*)$" $pair dummy val]} {
        set start $val
        continue
      }
      if {0 != [regexp "^show=(.*)$" $pair dummy val]} {
        set show $val
        continue
      }
      if {0 != [regexp "^clear=(.*)$" $pair dummy val]} {
        set clear $val
        continue
      }
    }
  }

  set hm_script {
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
      Write("<records");
      Write(" start='"); WriteXML(iStart);
      Write("' show='"); WriteXML(iCount);
      Write("' count='"); WriteXML(eCount);
      Write("' />");
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
              Write("<row");
              Write(" datetime='"); WriteXML(sCollectedDateTimes);
              Write("' names='"); WriteXML(sCollectedNames);
              Write("' values='"); WriteXML(sCollectedValues);
              Write("' timestamp='"); WriteXML(sCollectedTimestamp);
              Write("' />");
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
        Write("<row");
        Write(" datetime='"); WriteXML(sCollectedDateTimes);
        Write("' names='"); WriteXML(sCollectedNames);
        Write("' values='"); WriteXML(sCollectedValues);
        Write("' timestamp='"); WriteXML(sCollectedTimestamp);
        Write("' />");
      }
    }
  }

  array set res [rega_script $hm_script]

  if { $res(STDOUT) != "" } {
    puts -nonewline $res(STDOUT)
  }
} else {
  puts -nonewline {<not_authenticated/>}
}
puts "</systemProtocol>"
