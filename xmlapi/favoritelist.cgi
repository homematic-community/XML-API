#!/bin/tclsh
load tclrega.so
puts -nonewline {Content-Type: text/xml
Access-Control-Allow-Origin: *

<?xml version="1.0" encoding="ISO-8859-1" ?><favoriteList>}

array set res [rega_script {


    object oFavorite;
    string sFavoriteId;
    string sFavoriteName;
    string sChannelId;

    foreach (sFavoriteId, dom.GetObject(ID_FAVORITES).EnumUsedIDs())
    {
      oFavorite     = dom.GetObject(sFavoriteId);

      Write("<favorite name='"); WriteXML( oFavorite.Name() );
      Write("' ise_id='" # sFavoriteId # "'>");
  
      foreach(sChannelId, oFavorite.EnumUsedIDs())
      {
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
	foreach (id, oFavorite.FavControlIDs().EnumIDs()){
         if (id == sChannelId) { canUse = "true"; }
      }
      Write( "' not_can_use='" # canUse);
      Write("'/>"); 
      }

      Write("</favorite>");
    }

}]
puts -nonewline $res(STDOUT)
puts -nonewline {</favoriteList>}

