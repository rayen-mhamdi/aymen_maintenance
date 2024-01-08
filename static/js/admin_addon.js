function update_document() {	
	var link = location.href;
    var link_parts = link.split('/') 
    if (link_parts.indexOf('change') > -1) {
        var id = link_parts[link_parts.indexOf('change') - 1] ;
        var newlink = "/print/"+id;
        $('input[name="_continue"]').after('<a href="'+ newlink +'" target="_blank" class="deletelink" style="background:var(--admin-interface-save-button-background-color)">Imprimer</a>');
        $('#content-main > ul.object-tools').prepend('<li><a href="'+newlink+'" target="_blank" class="historylink" style="background:var(--admin-interface-save-button-background-color)">Imprimer</a></li>');
    }
    var save_btn_val = $('input[name="_save"]').val()
    $('input[name="_continue"]').val(save_btn_val)
    $('input[name="_addanother"]').hide()
    $('input[name="_save"]').hide()
    
}






// give time to jquery to load..
setTimeout("update_document();", 100);
