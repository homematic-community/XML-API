#!/bin/tclsh
source session.tcl

puts "Content-Type: text/xml; charset=iso-8859-1"
puts ""
puts -nonewline "<?xml version='1.0' encoding='ISO-8859-1' ?><favoriteList>"

if {[info exists sid] && [check_session $sid]} {

  set show_datapoint 0
  set show_internal 0
  catch {
    set input $env(QUERY_STRING)
    set pairs [split $input &]
    foreach pair $pairs {
      if {0 != [regexp "^show_datapoint=(.*)$" $pair dummy val]} {
        set show_datapoint $val
        continue
      }
      if {0 != [regexp "^show_internal=(.*)$" $pair dummy val]} {
        set show_internal $val
        continue
      }
    }
  }

  set hm_script "var show_datapoint=$show_datapoint;\n"
  append hm_script "var show_internal=$show_internal;\n"

  append hm_script {

      object oFavorite;
      string sFavoriteId;
      string sFavoriteName;
      string sChannelId;

      foreach (sFavoriteId, dom.GetObject(ID_FAVORITES).EnumUsedIDs()) {
          oFavorite     = dom.GetObject(sFavoriteId);

          Write("<favorite name='"); WriteXML( oFavorite.Name() );
          Write("' ise_id='" # sFavoriteId # "'>");

          foreach(sChannelId, oFavorite.EnumUsedIDs()) {
              object fav = dom.GetObject(sChannelId);
              Write("<channel ise_id='" # sChannelId # "' name='"); WriteXML(fav.Name());
              !Write( "' column_count='"); WriteXML(fav.FavColumnCount());
              !Write( "' column_count='"); WriteXML(fav.FavControls());

              var favType = "UNKNOWN";
              if (fav.IsTypeOf(OT_PROGRAM)) { favType = "PROGRAM"; }
              if (fav.IsTypeOf(OT_DP))      { favType = "SYSVAR";  }
              if (fav.IsTypeOf(OT_CHANNEL)) { favType = "CHANNEL"; }
              Write( "' type='" # favType);

              string canUse = "false";
              string id;

              foreach (id, oFavorite.FavControlIDs().EnumIDs()) {
                   if (id == sChannelId) { canUse = "true"; }
              }
              Write( "' not_can_use='" # canUse);

              if (show_datapoint == 1) {
                  Write ("'>");
                  if (favType == "CHANNEL") {
                      string sDPId;
                      foreach (sDPId, fav.DPs().EnumUsedIDs()) {
              object oDP = dom.GetObject(sDPId);
              if (oDP) {
                string dp = oDP.Name().StrValueByIndex(".", 2);

                if ((dp != "ON_TIME") && (dp != "INHIBIT")) {
                  Write("<datapoint");
                  Write(" name='"); WriteXML(oDP.Name());
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


                  }

                  if (favType == "SYSVAR") {
                    Write("<systemVariable");
                      Write(" name='"); WriteXML( fav.Name() );
                      Write("' variable='");
                      if (fav.ValueSubType() == 6) {
                        WriteXML( fav.AlType());
                      } else {
                        WriteXML( fav.Variable());
                      }
                      Write("' value='"); WriteXML( fav.Value());
                      Write("' value_list='");
                      if (fav.ValueType() == 16) {
                        WriteXML( fav.ValueList());
                      }
                      Write("' value_text='"); WriteXML( fav.ValueList().StrValueByIndex(';', fav.Value()));
                      Write("' ise_id='" # fav.ID() );
                      Write("' min='"); WriteXML( fav.ValueMin());
                      Write("' max='"); WriteXML( fav.ValueMax());
                      Write("' unit='"); WriteXML( fav.ValueUnit());
                      Write("' type='" # fav.ValueType() # "' subtype='" # fav.ValueSubType());
                      Write("' timestamp='" # fav.Timestamp().ToInteger());
                      Write("' value_name_0='");
                      if (fav.ValueType() == 2) {
                        WriteXML( fav.ValueName0());
                      }
                      Write("' value_name_1='");
                      if (fav.ValueType() == 2) {
                        WriteXML( fav.ValueName1());
                      }
                    Write("'/>");
                  }
                  Write("</channel>");
              } else {
                  Write ("'/>");
              }
          }
          Write("</favorite>");
      }
  }

  array set res [rega_script "$hm_script"]

  if { $res(STDOUT) != "" } {
    puts -nonewline $res(STDOUT)
  }
} else {
  puts -nonewline {<not_authenticated/>}
}
puts "</favoriteList>"
