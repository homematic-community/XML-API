#!/bin/tclsh
source session.tcl

puts "Content-Type: text/xml; charset=iso-8559-1"
puts ""
puts -nonewline "<?xml version='1.0' encoding='ISO-8859-1' ?><deviceList>"

if {[info exists sid] && [check_session $sid]} {

  set show_internal ""
  catch {
    set input $env(QUERY_STRING)
    set pairs [split $input &]
    foreach pair $pairs {
      if {0 != [regexp "^show_internal=(.*)$" $pair dummy val]} {
        set show_internal $val
        break
      }
    }
  }

  array set res [rega_script {

      string show_internal = "} $show_internal {";

      integer DIR_SENDER      = 1;
      integer DIR_RECEIVER    = 2;
  !    string  TYPE_VIRTUAL    = "29";
      string  PARTNER_INVALID = "65535";

      string sDevId;
      string sChnId;
      string sDPId;
      foreach (sDevId, root.Devices().EnumUsedIDs())
      {
        object  oDevice   = dom.GetObject(sDevId);
        boolean bDevReady = oDevice.ReadyConfig();
        if( (true == bDevReady) && ("HMW-RCV-50" != oDevice.HssType()) && ("HM-RCV-50" != oDevice.HssType()) )
        {
          string sDevInterfaceId = oDevice.Interface();
          string sDevInterface   = dom.GetObject(sDevInterfaceId).Name();
          string sDevType        = oDevice.HssType();

          Write("<device");
          Write(" name='");WriteXML( oDevice.Name() );Write("'");
          Write(" address='");WriteXML( oDevice.Address() );Write("'");
          Write(" ise_id='" # sDevId # "'");
          Write(" interface='" # sDevInterface # "'");
          Write(" device_type='");WriteXML(sDevType);Write("'");
          Write(" ready_config='" # bDevReady # "'");
          Write(">");

          foreach(sChnId, oDevice.Channels())
          {
            object oChannel = dom.GetObject(sChnId);

            boolean show = false;

            if (false == oChannel.Internal() ) {
              show = true;
            }

            if ( show_internal == "1"){
              show = true;
            }

            if (show == true){
              integer iChnDir     = oChannel.ChnDirection();
              string  sChnDir     = "UNKNOWN";
              if (DIR_SENDER   == iChnDir) { sChnDir = "SENDER";   }
              if (DIR_RECEIVER == iChnDir) { sChnDir = "RECEIVER"; }
              string  sChnPartnerId = oChannel.ChnGroupPartnerId();
              if (PARTNER_INVALID == sChnPartnerId) { sChnPartnerId = ""; }
              boolean bChnAESAvailable = false;
              if (0 != oChannel.ChnAESOperation()) { bChnAESAvailable = true; }
              string sChnMode = "DEFAULT";
              if (true == oChannel.ChnAESActive()) { sChnMode = "AES"; }

  !            boolean bChnReady        = oChannel.ReadyConfig();
  !            integer iChnLinkCount    = oChannel.ChnLinkCount();
  !            integer iChnProgramCount = oChannel.DPUsageCount();
  !            if (ID_ERROR == iChnProgramCount) { iChnProgramCount = 0; }
  !            boolean bChnVirtual = false;
  !            if (TYPE_VIRTUAL == sChnType) { bChnVirtual = true; }
  !            boolean bChnReadable  = false;
  !            boolean bChnWritable  = false;
  !            boolean bChnEventable = false;
  !            foreach (sDPId, oChannel.DPs())
  !            {
  !              object  oDP          = dom.GetObject(sDPId);
  !              if (false == oDP.Internal())
  !              {
  !                integer iDPOperations = oDP.Operations();
  !                if (OPERATION_READ  & iDPOperations) { bChnReadable  = true; }
  !                if (OPERATION_WRITE & iDPOperations) { bChnWritable  = true; }
  !                if (OPERATION_EVENT & iDPOperations) { bChnEventable = true; }
  !              }
  !            }
  !
              Write("<channel name='");WriteXML( oChannel.Name() );Write("'");
              Write(" type='");WriteXML( oChannel.ChannelType() );Write("'");
              Write(" address='");WriteXML( oChannel.Address() );Write("'");
              Write(" ise_id='" # sChnId # "'");
              Write(" direction='" # sChnDir # "'");
              Write(" parent_device='" # oChannel.Device() # "'");
              Write(" index='" # oChannel.ChnNumber() # "'");
              Write(" group_partner='" # sChnPartnerId # "'");
              Write(" aes_available='" # bChnAESAvailable # "'");
              Write(" transmission_mode='" # sChnMode # "'");
  !            Write(" archive='" # oChannel.ChnArchive() # "'");

              if (false == oChannel.Internal()) {
                Write(" visible='" # oChannel.Visible() # "'");
              } else {
                Write(" visible=''");
              }

              Write(" ready_config='" # oChannel.ReadyConfig() # "'");
  !            Write(" link_count='" # iChnLinkCount # "'");
  !            Write(" program_count='" # iChnProgramCount # "'");
  !            Write(" virtual='" # bChnVirtual # "'");
  !            Write(" readable='" # bChnReadable # "'");
  !            Write(" writable='" # bChnWritable # "'");
  !            Write(" eventable='" # bChnEventable # "'");

              if (false == oChannel.Internal()) {
                Write(" operate='");
                if( oChannel.UserAccessRights(iulOtherThanAdmin) == iarFullAccess ) {
                  Write("true");
                } else {
                  Write("false");
                }
              } else {
                Write(" operate='");
              }

              Write("' />");
            }
          }

          Write("</device>");
        }
      }
    }]

  if { $res(STDOUT) != "" } {
    puts -nonewline $res(STDOUT)
  }
} else {
  puts -nonewline {<not_authenticated/>}
}
puts "</deviceList>"
