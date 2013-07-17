#!/bin/tclsh
load tclrega.so
puts -nonewline {Content-Type: text/xml
Access-Control-Allow-Origin: *

<?xml version="1.0" encoding="ISO-8859-1" ?><systemNotification>}

catch {
  set input $env(QUERY_STRING)
	set pairs [split $input &]
	foreach pair $pairs {
		if {0 != [regexp "^(\[^=]*)=(.*)$" $pair dummy varname val]} {
			set $varname $val
		}
	}
}

append hm_script {;
  object oTmpArray = dom.GetObject(ID_SERVICES);
    
	if( oTmpArray ) {
		string sTmp;
    
		foreach(sTmp, oTmpArray.EnumIDs()){
    	
			object oTmp = dom.GetObject( sTmp );
        
			if( oTmp ){
  			if( oTmp.IsTypeOf( OT_ALARMDP ) && ( oTmp.AlState() == asOncoming ) ){
  				
  			  var trigDP = dom.GetObject(oTmp.AlTriggerDP());
  					
  				Write("<notification ise_id='");
  				!WriteXML( oTmp.ID());
  				WriteXML( oTmp.AlTriggerDP());
  				Write("' name='");
  				WriteXML( trigDP.AlDestMapDP().Name());
  				Write("' type='");
          WriteXML(trigDP.AlDestMapDP().Name().StrValueByIndex(".", 2));
          Write("' timestamp='");
          WriteXML(trigDP.AlDestMapDP().Timestamp().ToInteger());
  				Write("'/>");
  		  }
      }
		}
  }	
}

array set res [rega_script $hm_script]

puts -nonewline $res(STDOUT)
puts -nonewline {</systemNotification>}
