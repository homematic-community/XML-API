# XML-API CCU Addon

[![Release](https://img.shields.io/github/release/homematic-community/XML-API.svg)](https://github.com/homematic-community/XML-API/releases/latest)
[![Downloads](https://img.shields.io/github/downloads/homematic-community/XML-API/latest/total.svg)](https://github.com/homematic-community/XML-API/releases/latest)
[![Issues](https://img.shields.io/github/issues/homematic-community/XML-API.svg)](https://github.com/homematic-community/XML-API/issues)
[![License](https://img.shields.io/badge/license-GPL%203.0-green.svg)](https://opensource.org/licenses/GPL-3.0)

A HomeMatic CCU Addon implementing a xml request functionality as an interface to all homematic deviced available to a CCU device. This addon provides useful scripts that can be accessed via a HTTP request to a CCU device and allows to query and set all e.g. room- and devicetype names.

## Supported CCU models
* [HomeMatic CCU3](https://www.eq-3.de/produkte/homematic/zentralen-und-gateways/smart-home-zentrale-ccu3.html) / [RaspberryMatic](https://raspberrymatic.de/)
* [HomeMatic CCU2](https://www.eq-3.de/produkt-detail-zentralen-und-gateways/items/homematic-zentrale-ccu-2.html)
* HomeMatic CCU1

## Installation
This addon can be added like a usual CCU addon package via the WebUI provided functionality by selecting "System-Konfiguration » Systemsteuerung » Zusatzsoftware", to upload the addon package as a tar.gz and the use »Installieren« to actually install the addon. After a restart of the CCU the xml-api interface can then be selected from the »Zusatzsoftware« tab in the CCU settings.

## Use
After installation the XML-API should be avilable via the following URL call:
```
https://[CCU_IP]/addons/xmlapi/[ScriptName]?sid=[TOKEN_ID]
```
where [TOKEN_ID] corresponds to a stateless token-based authentication id a user can register using the `tokenregister.cgi` script listed below. In addition, [CCU_IP] corresponds to the IP address or hostname of your CCU device and [ScriptName] being one of the following scripts:

| ScriptName                    | Description / Parameters  
| ----------------------------- |-------------------------
| `checkuptodate.cgi`           | ???
| `devicelist.cgi`              | Lists all devices with channels. Contain names, serial number, device type and ids.<br>`device_id=list` - returns values of specified devices (e.g. "1234,5678") (optional)<br>`show_internal=0/1` - adds internal channels also (default=0)<br>`show_remote=0/1` - adds output of virtual remote channels (default=0)
| `devicetypelist.cgi`          | Lists all possible device types with their possible meta data.
| `exec.cgi`                    | Allows to execute arbitrary ReGaHss script commands (as POST data).
| `favoritelist.cgi`            | Lists all favorites and users.<br>`show_datapoint=0/1` - outputs datapoint_id and datapoint_type also (default=0)<br>`show_internal=0/1` - adds internal channels also (default=0)
| `functionlist.cgi`            | Lists all functions including channels.
| `mastervalue.cgi`             | Outputs a single or several '1234,5678' devices with their names and master values.<br>`device_id=list` - returns master values of specified devices (e.g. "1234,5678")<br>`requested_names=list` - returns only master values of selected types (e.g. "TEMPERATURE_COMFORT,TEMPERATURE_LOWERING")
| `mastervaluechange.cgi`       | Sets one or more master values for a list of devices.<br>`device_id=list` - sets master values of specified devices (e.g. "1234,5678")<br>`name=list` - sets only master values of selected types (e.g. "TEMPERATURE_LOWERING,TEMPERATURE_COMFORT")<br>`value=list` - sets master values to specified values (e.g. "17.0,22.5")
| `programactions.cgi`          | Allows to change active and visible program options.<br>`program_id=int` - id of program to modify (e.g. "1234")<br>`active=true/false` - sets active status of program to true/false<br>`visible=true/false` - sets visible status of program to true/false
| `programlist.cgi`             | Lists all programs.
| `protocol.cgi`                | Outputs the system protocol.<br>`start=int` - start of the protocol<br>`show=int` - number of entries to output<br>`clear=0/1` - allows to clear the system protocol
| `roomlist.cgi`                | Lists all configured rooms including channels.
| `rssilist.cgi`                | Lists RSSI values of all RF devices.
| `runprogram.cgi`              | Starts a program with the specified id.<br>`program_id=int` - id of program to modify (e.g. "1234")<br>`cond_check=0/1` - execute program with normal condition checks or not (only first "then" is executed) (default=0)
| `scripterrors.cgi`            | Searches for the last 10 lines in `/var/log/messages` containing script runtime errors and outputs them.
| `state.cgi`                   | Outputs one or more devices with their channels and current values.<br>`device_id=list` - returns values of specified devices (e.g. "1234,5678")<br>`channel_id=list` - returns values of specified channels (e.g. "1234,5678")<br>`datapoint_id=list` - returns Value() for datapoint with id (e.g. "1234,5678")
| `statechange.cgi`             | Allows to change the state of one or more devices.<br>`ise_id=list` - selects the devices with the specified ids (e.g. "1234,5678")<br>`new_value=list` - new values for device states (e.g. "0.20,1.45")
| `statelist.cgi`               | Outputs all devices with channels and their current values.<br>`ise_id=int` - output only channels and values of device with specified id (e.g. "1234")<br>`show_internal=0/1` - adds internal channels also (default=0)<br>`show_remote=0/1` - adds output of virtual remote channels (default=0)
| `systemNotification.cgi`      | Outputs the currently existing system notifications.
| `systemNotificationClear.cgi` | Clears the current active system notifications (if not sticky).
| `sysvar.cgi`                  | Outputs a single system variable with its corresponding values.<br>`ise_id=int` - the id of the system variable to output (e.g. "1234")<br>`text=true/false` - outputs or suppressed the text for string variables (default=true)
| `sysvarlist.cgi`              | Outputs all system variables with their corresponding values.<br>`text=true/false` - outputs or suppressed the text for string variables (default=false)
| `tokenlist.cgi`               | Lists all registered security access tokens.
| `tokenregister.cgi`           | Registers a new security access token.<br>`desc=string` - description for new token id
| `tokenrevoke.cgi`             | Revokes an existing security access token.<br>`sid=string` - security access token id
| `update.cgi`                  | ????<br>`checkupdate=list` - ???<br>`maxdurchlaeufe=int` - ??? (default=7)
| `version.cgi`                 | Outputs version of XML-API.

All of these scripts, in addition to the listed parameters require a security access token id to be specified via a mandatory `?sid=[TOKEN_ID]` URL parameter with an adequate token ID specified. Such a security token can be generated using `tokenregister.cgi` from within the standard CCU addon webui page (`Settings -> Control panel -> Additional software -> XML-API -> Set`) or by using an already registered security token. Furthermore, already registered tokens can be listed via `tokenlist.cgi` and revoked via `tokenrevoke.cgi` with the token id supplied.

If a script will be correctly called, it generates a xml structured output that can then be used by third-party applications to display or modify certain information. 

In addition many of these scripts rely on additional URL parameter to be specifeid (e.g. `ise_id` device or channel identifier). And example of such script executing URL can be seen here:
```
https://<CCU-IP>/addons/xmlapi/statechange.cgi?sid=[TOKEN_ID]&ise_id=12345&new_value=0.20
```
This call, if executed with a registered [TOKEN_ID] and the right ise_id and IP address would then e.g. set a dimmer to 20%.

## Support
https://homematic-forum.de/forum/viewtopic.php?f=26&t=10098&p=75959#p75959

## Authors
* jens-maus, Maik (Monty1979), Philipp (ultrah), hobbyquaker, dirch, Uwe (uwe111)
