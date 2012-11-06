#!/bin/tclsh

#  !*****************************************************************************
#  !* statelist.cgi
#  !* Stati aller kanaele und timestamp der letzten aktualisierung
#  !*
#  !* Autor      : Dirk Szymanski
#  !* Erstellt am: gleich, kleinen moment noch
#  !* 
#  !* 11.2012 hobbyquaker: cgi.tcl rausgeworfen, Allow-Origin Header
#  !* 	hinzugefügt. Parameter show_internal=1 aktiviert ausgabe des
#  !*   datenpunkt-attributs state.
#  !*
#  !*****************************************************************************

load tclrega.so
puts -nonewline {Content-Type: text/xml
Access-Control-Allow-Origin: *

<?xml version="1.0" encoding="ISO-8859-1" ?><stateList>}

set ise_id 0
set show_internal 0

catch {
  set input $env(QUERY_STRING)
  set pairs [split $input &]
  foreach pair $pairs {
    if {0 != [regexp "^(\[^=]*)=(.*)$" $pair dummy varname val]} {
      set $varname $val      
    }    
  }
}

set comm "var ise_id=$ise_id;\n"
set comm "var show_internal=$show_internal;\n"


if { $ise_id != 0 } then {

  append comm {
        object obj = dom.GetObject(ise_id);
        if(obj.TypeName() == "HSSDP")
        {
            object oDP = obj;
            string dp = oDP.Name().StrValueByIndex(".", 2);

            Write("<datapoint");
            Write(" name='");WriteXML(oDP.Name());Write("'");
            Write(" type='");WriteXML(oDP.Name().StrValueByIndex(".", 2));Write("'");
            Write(" ise_id='");WriteXML(ise_id);Write("'");
            ! state fragt den aktuellen status des sensors/aktors ab, dauert lange
            if (show_internal == 1) {
                Write(" state='");WriteXML(oDP.State());Write("'");
            }
            ! value nimmt den von der ccu gecachten wert, moeglicherweise nicht korrekt. Ggf. bei einigen geraeten immer abfragen
            Write(" value='");WriteXML(oDP.Value());Write("'");
            Write(" valuetype='");WriteXML(oDP.ValueType());Write("'");
            Write(" timestamp='");WriteXML(oDP.Timestamp().ToInteger());Write("'");
            Write(" />");
        }
    }

} else {





append comm {

string sDevId;
string sChnId;
string sDPId;

	foreach (sDevId, root.Devices().EnumUsedIDs())
	{
		object oDevice   = dom.GetObject(sDevId);

		if( oDevice.ReadyConfig() && (oDevice.Name() != "Zentrale") && (oDevice.Name() != "HMW-RCV-50 BidCoS-Wir") )
		{
			Write("<device");
			Write(" name='" # oDevice.Name() # "'");
			Write(" ise_id='" # sDevId # "'");

			string interfaceid = oDevice.Interface();
			string servicechan = "" # dom.GetObject(interfaceid).Name() #"."#oDevice.Address()#":0";
			object schan = dom.GetObject(servicechan#".UNREACH");
			if(schan) { Write(" unreach='" # schan.Value() #"'"); }
			object schan = dom.GetObject(servicechan#".STICKY_UNREACH");
			if(schan) { Write(" sticky_unreach='" # schan.Value() #"'"); }
			object schan = dom.GetObject(servicechan#".CONFIG_PENDING");
			if(schan) { Write(" config_pending='" # schan.Value() #"'"); }
			
			Write(" >");  ! device tag schliessen

			foreach(sChnId, oDevice.Channels())
			{
				object oChannel = dom.GetObject(sChnId);
				if ( (! oChannel.Internal()) ||  oChannel.Internal()  )
				{

					Write("<channel name='");
					WriteXML( oChannel.Name() );
					Write("' ise_id='" # sChnId # "'>");

					foreach(sDPId, oChannel.DPs().EnumUsedIDs())
					{
						object oDP = dom.GetObject(sDPId);
						if(oDP)
						{
							string dp = oDP.Name().StrValueByIndex(".", 2);

							if( (dp != "ON_TIME") && (dp != "INHIBIT") )
							{
								Write("<datapoint");
								Write(" name='"); WriteXML(oDP.Name());
								Write("' type='"); WriteXML(oDP.Name().StrValueByIndex(".", 2))
								Write("' ise_id='" # sDPId );
                                ! state fragt den aktuellen status des sensors/aktors ab, dauert lange
								if (show_internal == 1) {
                                        Write("' state='"); WriteXML(oDP.State());
                                }
                                ! value nimmt den von der ccu gecachten wert, moeglicherweise nicht korrekt. Ggf. bei einigen geraeten immer abfragen
								Write("' value='"); WriteXML(oDP.Value());
								Write("' valuetype='" # oDP.ValueType());
								Write("' timestamp='" # oDP.Timestamp().ToInteger());
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

  array set res [rega_script $comm]

  puts -nonewline $res(STDOUT)
}
puts -nonewline {</stateList>}


