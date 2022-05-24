$( document ).ready(function() {

    $.post( "/action_game_start" )
        .done( function( data ) {
            $( "#text_game_status" ).text( "(TODO) Started: " + data.word );
        } )
        .fail( function() {
            $( "#text_game_status" ).text( "Jotain meni vikaan." );
        } )

});