Homematic XML-API
=================

Fork von http://www.homematic-inside.de/software/download/item/xmlapi-addon - kompatibel zur Version 1.2

siehe auch diesen Forums-Thread: http://homematic-forum.de/forum/viewtopic.php?f=26&t=10098&p=75959#p75959

Lizensiert unter GPL v3

**Download:** https://github.com/downloads/hobbyquaker/hq-xmlapi/hq-xmlapi.img

Changelog
=========

* added protocol.cgi, returns the system history. parameter: start, show, clear. Set clear=1 to clear the Log
* updated info.html
* sysvar.cgi: new, returns a single variable. parameter: ise_id, gives value_list and value_text on default
* sysvarlist.cgi: removed cgi.tcl, added attributes value_list and value_text, added parameter text.
* programlist.cgi: removed cgi.tcl
* runprogram.cgi: removed cgi.tcl
* statechange.cgi: removed cgi.tcl
* state.cgi: removed cgi.tcl

