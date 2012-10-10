#!/bin/tclsh

load tclrega.so
source once.tcl
sourceOnce cgi.tcl
sourceOnce xml.tcl


cgi_eval {

  cgi_input

  set SysVarId 0
  set SysVarCount 0
  set SysVarLastupdate 0
  set DeviceId 0
  set DeviceCount 0
  set DeviceTypeCount 0
  set FirstRequest 0

  catch { import DeviceId    }
  catch { import DeviceCount }
  catch { import SysVarId    }
  catch { import SysVarCount }
  catch { import SysVarLastupdate }
  catch { import DeviceTypeCount  }
  catch { import FirstRequest  }
  

  cgi_content_type "text/xml"
  cgi_http_head

  puts -nonewline {<?xml version="1.0" ?>}  
  puts -nonewline {<result>} 

  set script "string DeviceId=\"$DeviceId\";\nstring DeviceCount=\"$DeviceCount\";\n"
  append script "string SysVarId=\"$SysVarId\";\nstring SysVarCount=\"$SysVarCount\";\n"
  append script "string SysVarLastupdate=\"$SysVarLastupdate\";\nstring DeviceTypeCount=\"$DeviceTypeCount\";\n"

  append script {

  string sDeviceId;
  string sSysVarId;

  boolean refreshDevices = false;
  boolean refreshSysVars = false;

  if ( (DeviceId.ToInteger() == 0) || (DeviceCount.ToInteger() == 0) ) 
  { refreshDevices = true; }
  else
  {
    if((DeviceCount.ToInteger()+3) != dom.GetObject(ID_DEVICES).Count().ToInteger())
    { refreshDevices = true; }
    else {
      foreach (sDeviceId, dom.GetObject(ID_DEVICES).EnumUsedIDs()) {
	  if(sDeviceId.ToInteger() > DeviceId.ToInteger()) { refreshDevices = true; }
      }
    }
  }

  if ( (SysVarId.ToInteger() == 0) || (SysVarCount.ToInteger() == 0) || (SysVarLastupdate.ToInteger() == 0) )
  { refreshSysVars = true; }
  else
  {
    if((SysVarCount.ToInteger()+2) != dom.GetObject(ID_SYSTEM_VARIABLES).Count().ToInteger())
    { refreshSysVars = true; }
    else {
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

#	puts $script

array set res [rega_script $script ]
  puts -nonewline $res(STDOUT)
  puts -nonewline {<refreshRssi/><refreshStatelist/>}
  puts -nonewline {</result>}
}
