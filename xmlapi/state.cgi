#!/bin/tclsh
source session.tcl

puts "Content-Type: text/xml; charset=iso-8859-1"
puts ""
puts -nonewline "<?xml version='1.0' encoding='ISO-8859-1' ?><state>"

if {[info exists sid] && [check_session $sid]} {

  set device_id ""
  set channel_id ""
  set datapoint_id ""
  catch {
    set input $env(QUERY_STRING)
    set pairs [split $input &]
    foreach pair $pairs {
      if {0 != [regexp "^device_id=(.*)$" $pair dummy val]} {
        set device_id $val
        continue
      }
      if {0 != [regexp "^channel_id=(.*)$" $pair dummy val]} {
        set channel_id $val
        continue
      }
      if {0 != [regexp "^datapoint_id=(.*)$" $pair dummy val]} {
        set datapoint_id $val
        continue
      }
    }
  }

  array set res [rega_script {

    string sDevIds = "} $device_id {";
    string sChannelIds = "} $channel_id {";
    string sDatapointIds = "} $datapoint_id {";
    string sChnId;
    string sDPId;

    if (sDatapointIds.Length() > 0 ) {

      string sDatapointId;
      foreach(sDatapointId, sDatapointIds.Split(",")) {

        object oDatapoint = dom.GetObject(sDatapointId);
        if (oDatapoint.IsTypeOf(OT_DP)) {
          Write("<datapoint ise_id='");
          WriteXML(sDatapointId);
          Write("' value='");
          WriteXML(oDatapoint.Value());
          Write("'/>");
        }
      }

    } else {

      if (sChannelIds.Length() > 0 ) {

        string sChannelId;
        foreach(sChannelId, sChannelIds.Split(",")) {
          object oChannel2 = dom.GetObject(sChannelId);

          if (sDevIds.Length() > 0 ) {
            sDevIds = sDevIds # "," # oChannel2.Device().ToString();
          } else {
            sDevIds = oChannel2.Device().ToString();
          }
        }
      }

      string sDevId;
      foreach(sDevId, sDevIds.Split(",")) {

        object oDevice = dom.GetObject(sDevId);
        integer iDevInterfaceId = oDevice.Interface();
        object oDeviceInterface = dom.GetObject(iDevInterfaceId);

        if( (oDeviceInterface) && (oDevice.ReadyConfig()) && (oDevice.Name() != "Zentrale") && (oDevice.Name() != "HMW-RCV-50 BidCoS-Wir") && (oDevice.IsTypeOf(OT_DEVICE)) ) {
          Write("<device");
          Write(" name='" # oDevice.Name() # "'");
          Write(" ise_id='" # sDevId # "'");

          string servicechan = "" # oDeviceInterface.Name() #"."#oDevice.Address()#":0";
          object schan = dom.GetObject(servicechan#".UNREACH");
          if(schan) { Write(" unreach='" # schan.Value() #"'"); }
          object schan = dom.GetObject(servicechan#".STICKY_UNREACH");
          if(schan) { Write(" sticky_unreach='" # schan.Value() #"'"); }
          object schan = dom.GetObject(servicechan#".CONFIG_PENDING");
          if(schan) { Write(" config_pending='" # schan.Value() #"'"); }

          Write(" >");  ! device tag schliessen

          foreach(sChnId, oDevice.Channels()) {
            object oChannel = dom.GetObject(sChnId);
            if ((!oChannel.Internal()) || oChannel.Internal()) {

              Write("<channel name='");
              WriteXML( oChannel.Name() );
              Write("' ise_id='" # sChnId);
              Write("' lastdpactiontime='" # oChannel.LastDPActionTime().ToInteger());
              Write("'>");


              foreach(sDPId, oChannel.DPs().EnumUsedIDs()) {
                object oDP = dom.GetObject(sDPId);
                if(oDP) {
                  string dp = oDP.Name().StrValueByIndex(".", 2);

                  if( (dp != "ON_TIME") && (dp != "INHIBIT") && (dp != "CMD_RETS") && (dp != "CMD_RETL") && (dp != "CMD_SETS") && (dp != "CMD_SETL") ) {
                    Write("<datapoint");
                    Write(" name='"); WriteXML(oDP.Name());
                    Write("' type='"); WriteXML(oDP.Name().StrValueByIndex(".", 2));
                    Write("' ise_id='" # sDPId );
                    ! state fragt den aktuellen status des sensors/aktors ab, dauert lange
                    !Write("' state='"); WriteXML(oDP.State());
                    ! value nimmt den von der ccu gecachten wert, moeglicherweise nicht korrekt. Ggf. bei einigen geraeten immer abfragen
                    Write("' value='"); WriteXML(oDP.Value());
                    Write("' valuetype='" # oDP.ValueType());
                    Write("' valueunit='" # oDP.ValueUnit());
                    Write("' timestamp='" # oDP.Timestamp().ToInteger());
                    Write("' lasttimestamp='" # oDP.LastTimestamp().ToInteger());
                    Write("' />");
                  }
                }
              }
              Write("</channel>");
            }
          }
          Write("</device>");
        }
      }
    }
  }]

  if { $res(STDOUT) != "" } {
    puts -nonewline $res(STDOUT)
  }
} else {
  puts -nonewline {<not_authenticated/>}
}
puts "</state>"
