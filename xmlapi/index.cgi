#!/bin/tclsh
source session.tcl

puts "Content-Type: text/html; charset=iso-8859-1"
puts ""
puts "<!DOCTYPE HTML PUBLIC '-//W3C//DTD HTML 4.01 Transitional//EN' 'http://www.w3.org/TR/REC-html40/loose.dtd'>"
puts "<html>"
puts "<head>"
puts "<title>XML-API</title>"
puts "<meta http-equiv='Content-Type' content='text/html; charset=iso-8859-1'/>"
puts "<style type='text/css'>"
puts "a {color: blue;}"
puts "table { width:100%; }"
puts "td, th { border: 1px solid;}"
puts "</style>"
puts "</head>"
puts "<body>"

if {[info exists sid] && [check_session $sid]} {
  puts "<table cellpadding=5 cellspacing=5>"

  set filename "/www/addons/xmlapi/VERSION"
  set fd [open $filename r]
  set version ""
  if { $fd >=0 } {
    gets $fd version
    close $fd
  }

  puts [subst {
    <tr><th colspan=2>XML-API $version</th></tr>
    <tr><td><a href=./checkuptodate.cgi?sid=$sid>checkuptodate.cgi</a></td><td>????</td></tr>
    <tr><td><a href=./devicelist.cgi?sid=$sid>devicelist.cgi</a></td><td><b>Lists all devices with channels. Contain names, serial number, device type and ids.</b><br/>
      <i>sid=string</i> - security access token id<br/>
      <i>device_id=list</i> - returns values of specified devices (e.g. "1234,5678") (optional)<br/>
      <i>show_internal=0/1</i> - adds internal channels also (default=0)<br/>
      <i>show_remote=0/1</i> - adds output of virtual remote channels (default=0)
    </td></tr>
    <tr><td><a href=./devicetypelist.cgi?sid=$sid>devicetypelist.cgi</a></td><td><b>Lists all possible device types with their possible meta data.</b><br/>
      <i>sid=string</i> - security access token id<br/>
    </td></tr>
    <tr><td><a href=./exec.cgi?sid=$sid>exec.cgi</a></td><td><b>Allows to execute arbitrary ReGaHss script commands (as POST data).</b><br/>
      <i>sid=string</i> - security access token id<br/>
    </td></tr>
    <tr><td><a href=./favoritelist.cgi?sid=$sid>favoritelist.cgi</a></td><td><b>Lists all favorites and users.</b><br/>
      <i>sid=string</i> - security access token id<br/>
      <i>show_datapoint=0/1</i> - outputs datapoint_id and datapoint_type also (default=0)<br/>
      <i>show_internal=0/1</i> - adds internal channels also (default=0)
    </td></tr>
    <tr><td><a href=./functionlist.cgi?sid=$sid>functionlist.cgi</a></td><td><b>Lists all functions including channels.</b><br/>
      <i>sid=string</i> - security access token id<br/>
    </td></tr>
    <tr><td><a href=./mastervalue.cgi?sid=$sid>mastervalue.cgi</a></td><td><b>Outputs a single or several '1234,5678' devices with their names and master values.</b><br/>
      <i>sid=string</i> - security access token id<br/>
      <i>device_id=list</i> - returns master values of specified devices (e.g. "1234,5678")<br/>
      <i>requested_names=list</i> - returns only master values of selected types (e.g. "TEMPERATURE_COMFORT,TEMPERATURE_LOWERING")
    </td></tr>
    <tr><td><a href=./mastervaluechange.cgi?sid=$sid>mastervaluechange.cgi</a></td><td><b>Sets one or more master values for a list of devices.</b><br/>
      <i>sid=string</i> - security access token id<br/>
      <i>device_id=list</i> - sets master values of specified devices (e.g. "1234,5678")<br/>
      <i>name=list</i> - sets only master values of selected types (e.g. "TEMPERATURE_LOWERING,TEMPERATURE_COMFORT")<br/>
      <i>value=list</i> - sets master values to specified values (e.g. "17.0,22.5")
    </td></tr>
    <tr><td><a href=./programactions.cgi?sid=$sid>programactions.cgi</a></td><td><b>Allows to change active and visible program options.</b><br/>
      <i>sid=string</i> - security access token id<br/>
      <i>program_id=int</i> - id of program to modify (e.g. "1234")<br/>
      <i>active=true/false</i> - sets active status of program to true/false<br/>
      <i>visible=true/false</i> - sets visible status of program to true/false
    </td></tr>
    <tr><td><a href=./programlist.cgi?sid=$sid>programlist.cgi</a></td><td><b>Lists all programs.</b><br/>
      <i>sid=string</i> - security access token id<br/>
    </td></tr>
    <tr><td><a href=./protocol.cgi?sid=$sid>protocol.cgi</a></td><td><b>Outputs the system protocol.</b><br/>
      <i>sid=string</i> - security access token id<br/>
      <i>start=int</i> - start of the protocol<br/>
      <i>show=int</i> - number of entries to output<br/>
      <i>clear=0/1</i> - allows to clear the system protocol
    </td></tr>
    <tr><td><a href=./roomlist.cgi?sid=$sid>roomlist.cgi</a></td><td><b>Lists all configured rooms including channels.</b><br/>
      <i>sid=string</i> - security access token id<br/>
    </td></tr>
    <tr><td><a href=./rssilist.cgi?sid=$sid>rssilist.cgi</a></td><td><b>Lists RSSI values of all RF devices.</b><br/>
      <i>sid=string</i> - security access token id<br/>
    </td></tr>
    <tr><td><a href=./runprogram.cgi?sid=$sid>runprogram.cgi</a></td><td><b>Starts a program with the specified id.</b><br/>
      <i>sid=string</i> - security access token id<br/>
      <i>program_id=int</i> - id of program to modify (e.g. "1234")<br/>
      <i>cond_check=0/1</i> - execute program with normal condition checks or not (only first "then" is executed) (default=0)
    </td></tr>
    <tr><td><a href=./scripterrors.cgi?sid=$sid>scripterrors.cgi</a></td><td><b>Searches for the last 10 lines in /var/log/messages containing script runtime errors and outputs them.</b><br/>
      <i>sid=string</i> - security access token id<br/>
    </td></tr>
    <tr><td><a href=./state.cgi?sid=$sid>state.cgi</a></td><td><b>Outputs one or more devices with their channels and current values.</b><br/>
      <i>sid=string</i> - security access token id<br/>
      <i>device_id=list</i> - returns values of specified devices (e.g. "1234,5678")<br/>
      <i>channel_id=list</i> - returns values of specified channels (e.g. "1234,5678")<br/>
      <i>datapoint_id=list</i> - returns Value() for datapoint with id (e.g. "1234,5678")
    </td></tr>
    <tr><td><a href=./statechange.cgi?sid=$sid>statechange.cgi</a></td><td><b>Allows to change the state of one or more devices.</b><br/>
      <i>sid=string</i> - security access token id<br/>
      <i>ise_id=list</i> - selects the devices with the specified ids (e.g. "1234,5678")<br/>
      <i>new_value=list</i> - new values for device states (e.g. "0.20,1.45")
    </td></tr>
    <tr><td><a href=./statelist.cgi?sid=$sid>statelist.cgi</a></td><td><b>Outputs all devices with channels and their current values.</b><br/>
      <i>sid=string</i> - security access token id<br/>
      <i>ise_id=int</i> - output only channels and values of device with specified id (e.g. "1234")<br/>
      <i>show_internal=0/1</i> - adds internal channels also (default=0)<br/>
      <i>show_remote=0/1</i> - adds output of virtual remote channels (default=0)
    </td></tr>
    <tr><td><a href=./systemNotification.cgi?sid=$sid>systemNotification.cgi</a></td><td><b>Outputs the currently existing system notifications.</b><br/>
      <i>sid=string</i> - security access token id<br/>
    </td></tr>
    <tr><td><a href=./systemNotificationClear.cgi?sid=$sid>systemNotificationClear.cgi</a></td><td><b>Clears the current active system notifications (if not sticky).</b><br/>
      <i>sid=string</i> - security access token id<br/>
    </td></tr>
    <tr><td><a href=./sysvar.cgi?sid=$sid>sysvar.cgi</a></td><td><b>Outputs a single system variable with its corresponding values.</b><br/>
      <i>sid=string</i> - security access token id<br/>
      <i>ise_id=int</i> - the id of the system variable to output (e.g. "1234")<br/>
      <i>text=true/false</i> - outputs or suppressed the text for string variables (default=true)<br/>
    </td></tr>
    <tr><td><a href=./sysvarlist.cgi?sid=$sid>sysvarlist.cgi</a></td><td><b>Outputs all system variables with their corresponding values.</b><br/>
      <i>sid=string</i> - security access token id<br/>
      <i>text=true/false</i> - outputs or suppressed the text for string variables (default=false)<br/>
    </td></tr>
    <tr><td><a href=./tokenlist.cgi?sid=$sid>tokenlist.cgi</a></td><td><b>Lists all registered security access tokens</b><br/>
      <i>sid=string</i> - security access token id<br/>
    </td></tr>
    <tr><td><a href=./tokenregister.cgi?sid=$sid>tokenregister.cgi</a></td><td><b>Registers a new security access token</b><br/>
      <i>sid=string</i> - security access token id<br/>
      <i>desc=string</i> - description for new token id<br/>
    </td></tr>
    <tr><td><a href=./tokenrevoke.cgi?sid=$sid>tokenrevoke.cgi</a></td><td><b>Revokes an existing security access token</b><br/>
      <i>sid=string</i> - security access token id<br/>
    </td></tr>
    <tr><td><a href=./update.cgi?sid=$sid>update.cgi</a></td><td><b>???</b><br/>
      <i>sid=string</i> - security access token id<br/>
      <i>checkupdate=list</i> - ???<br/>
      <i>maxdurchlaeufe=int</i> - ??? (default=7)<br/>
    </td></tr>
    <tr><td><a href=./version.cgi?sid=$sid>version.cgi</a></td><td><b>Outputs version of XML-API.</b><br/>
    </td></tr>
  }]
} else {
  puts "not authenticated"
}
puts "</body>"
puts "</html>"
