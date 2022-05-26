
var game_state =
{
    'word_length': -1,
    'line_number': 0,
    'letter_inputs': []
};

function submitWord()
{
    curr_letters = game_state.letter_inputs[game_state.line_number];

    guess = "";

    for ( const letter of curr_letters )
    {
        letter.prop( "disabled", true );
        guess += letter.val();
    }
    
    $.post( "/game/guess", { 'guess': guess } )
        .done( function( data ) {
            game_state.line_number++;
            $( "#text_game_status" ).text( JSON.stringify(data) );
            createInputs( game_state.line_number, data.word_length );
        } )
        .fail( function() {
            $( "#text_game_status" ).text( "Jotain meni vikaan." );
        } )
}

function createInputs(line)
{
    first_id = "input_letter_" + line + "_" + 0;
    
    letter_inputs = [];
    game_state.letter_inputs.push(letter_inputs);

    length = game_state.word_length

    for ( var i = 0; i < length; i++ )
    {
        id = "input_letter_" + line + "_" + i;
        next_id ="input_letter_" + line + "_" + (i + 1);
        prev_id ="input_letter_" + line + "_" + (i - 1);
        is_last_letter = i == length - 1;
        $("#game_area").append( '<input class="letter" type="text" autocomplete="off" id="' + id + '" maxlength="1">' );

        $("#" + id)
            // On entering letter, move to next field (unless emptied)
            .on( 'input', 
                function(next_id, is_last_letter) { 
                    return function()
                    { 
                        next = $("#" + next_id);
                        if ( !($(this).val() === "") )
                        {
                            if ( !is_last_letter )
                                next.focus();
                            else
                                submitWord();
                        }
                    } 
                } ( next_id, is_last_letter ) 
            )
            // On backspace, move to previous
            .keydown(
                function(prev_id) {
                    return function(e) 
                    {
                        prev = $("#" + prev_id);
                        if ((e.which == 8 || e.which == 46) && $(this).val() =='') {
                            prev.focus();
                        }
                    } 
                } (prev_id)
            );

        letter_inputs.push( $("#" + id ) );
    }
    
    $("#game_area").append("<br>");

    letter_inputs[0].focus();

}

function startGame()
{
    $.post( "/game/start" )
        .done( function( data ) {
            $( "#text_game_status" ).text( JSON.stringify(data) );
            game_state.word_length = data.word_length
            createInputs( game_state.line_number, data.word_length );
        } )
        .fail( function() {
            $( "#text_game_status" ).text( "Jotain meni vikaan." );
        } )

}

$( document ).ready(startGame);