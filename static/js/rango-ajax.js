$(document).ready( function () {

	$( '#likes' ).click( function (){
		var catid;
		catid = $( this ).attr( "data-catid" );
		$.get( '/rango/like_category/', { category_id : catid }, function ( data ){
			$( '#like_count' ).html( data );
			$( '#likes' ).hide();
		});
	});

	$('#suggestion').keyup(function(){
		var query;
		query = $(this).val();
		console.log(query);
		$.get('/rango/suggest_category/', {suggestion: query}, function ( data ){
			$('#cats').html(data);
		});
	});

	$( '.add_page' ).on( 'click', function ( event ){
		var add;
		var lista = [];
		add = $(this).val();
		//alert(add);
		$.get('/rango/add_page_ajax/', {values: add}, function ( data ){
			lista = JSON.parse(data);
			alert(lista[1]);
			$('#category_pages').append('<li><a href="'+lista[1]+'">'+lista[0]+'</a></li>')
		});
	});

});