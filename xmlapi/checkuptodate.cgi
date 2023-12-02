#!/bin/tclsh
source session.tcl

puts "Content-Type: text/xml; charset=iso-8859-1"
puts ""
puts -nonewline "<?xml version='1.0' encoding='ISO-8859-1' ?><result>"

if {[info exists sid] && [check_session $sid]} {

  set SysVarId 0
  set SysVarCount 0
  set SysVarLastupdate 0
  set DeviceId 0
  set DeviceCount 0
  set DeviceTypeCount 0
  catch {
    set input $env(QUERY_STRING)
    set pairs [split $input &]
    foreach pair $pairs {
      if {0 != [regexp "^SysVarId=(.*)$" $pair dummy val]} {
        set SysVarId $val
        continue
      }
      if {0 != [regexp "^SysVarCount=(.*)$" $pair dummy val]} {
        set SysVarCount $val
        continue
      }
      if {0 != [regexp "^SysVarLastupdate=(.*)$" $pair dummy val]} {
        set SysVarLastupdate $val
        continue
      }
      if {0 != [regexp "^DeviceId=(.*)$" $pair dummy val]} {
        set DeviceId $val
        continue
      }
      if {0 != [regexp "^DeviceCount=(.*)$" $pair dummy val]} {
        set DeviceCount $val
        continue
      }
      if {0 != [regexp "^DeviceTypeCount=(.*)$" $pair dummy val]} {
        set DeviceTypeCount $val
        continue
      }
    }
  }

  set script "string DeviceId=\"$DeviceId\";\nstring DeviceCount=\"$DeviceCount\";\n"
  append script "string SysVarId=\"$SysVarId\";\nstring SysVarCount=\"$SysVarCount\";\n"
  append script "string SysVarLastupdate=\"$SysVarLastupdate\";\nstring DeviceTypeCount=\"$DeviceTypeCount\";\n"

  append script {

    string sDeviceId;
    string sSysVarId;

    boolean refreshDevices = false;
    boolean refreshSysVars = false;

    if ( (DeviceId.ToInteger() == 0) || (DeviceCount.ToInteger() == 0) ) {
      refreshDevices = true;
    } else {
      if((DeviceCount.ToInteger()+3) != dom.GetObject(ID_DEVICES).Count().ToInteger()) {
        refreshDevices = true;
      } else {
        foreach (sDeviceId, dom.GetObject(ID_DEVICES).EnumUsedIDs()) {
          if(sDeviceId.ToInteger() > DeviceId.ToInteger()) { refreshDevices = true; }
        }
      }
    }

    if ( (SysVarId.ToInteger() == 0) || (SysVarCount.ToInteger() == 0) || (SysVarLastupdate.ToInteger() == 0) ) {
      refreshSysVars = true;
    } else {
      if((SysVarCount.ToInteger()+2) != dom.GetObject(ID_SYSTEM_VARIABLES).Count().ToInteger()) {
        refreshSysVars = true;
      } else {
        foreach (sSysVarId, dom.GetObject(ID_SYSTEM_VARIABLES).EnumUsedIDs()) {
          if(sSysVarId.ToInteger() > SysVarId.ToInteger()) { refreshSysVars = true; }
          if(dom.GetObject(sSysVarId).Timestamp().ToInteger() > SysVarLastupdate.ToInteger()) { refreshSysVars = true; }
        }
      }
    }
    if( refreshDevices ) { Write("<refreshDevices/>"); }
    if( refreshSysVars ) { Write("<refreshSysVars/>"); }
    if( DeviceTypeCount < 20 ) { Write("<refreshDeviceTypes/>"); }
  }

  array set res [rega_script $script]

  if { $res(STDOUT) != "" } {
    puts -nonewline $res(STDOUT)
    puts -nonewline {<refreshRssi/><refreshStatelist/>}
  }
} else {
  puts -nonewline {<not_authenticated/>}
}
puts "</result>"
