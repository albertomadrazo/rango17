$( document ).ready( function (){
	// alert("cargado");
	$( "#about-btn" ).click( function (event){
		alert("You clicked the button using jQuery!");
	});
	$( "p" ).hover( function (){
		// Si cambio this por p, entonces todos los p's cambian de color
		$( this ).css( 'color', 'red' );
	},
	function (){
		$( this ).css( 'color', 'blue' );
	});

	$( '#about-btn' ).addClass( 'btn btn-primary' );

	$( "#about-btn" ).click( function (event){
		msgstr = $( "#msg" ).html();
		msgstr = msgstr + "o";
		$( "#msg" ).html( msgstr );
	});

	
});