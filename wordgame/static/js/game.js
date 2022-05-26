
class Game
{
    constructor()
    {
        this.word_length = -1;
        this.line_number = 0;
        this.letter_inputs = [];
    }

    getCurrentInputs()
    {
        return this.letter_inputs[this.line_number];
    }

    colorizeInputsWithResults(result)
    {
        curr_letters = this.getCurrentInputs();
        for ( var i = 0; i < curr_letters.length; i++ )
        {
            let letter = curr_letters[i]
            if ( result[i] === "WRONG" )
            {
                letter.addClass( "letter_wrong" )
            }
            else if ( result[i] === "HINT" )
            {
                letter.addClass( "letter_hint" )
            }
            else if ( result[i] === "CORRECT" )
            {
                letter.addClass( "letter_correct" )
            }                
        }        
    }

}

let game_state = new Game();

function postStart()
{
    $.post( "/game/start" )
        .done( function( data ) {
            $( "#text_game_status" ).text( JSON.stringify(data) );
            startNewWord(data.word_length)
        } )
        .fail( onFailure )
}

function postGuess()
{
    $.post( "/game/guess", { 'guess': getGuess() } )
        .done( function( data ) {
            curr_letters = game_state.getCurrentInputs();
            game_state.colorizeInputsWithResults(data.result)
            game_state.line_number++;
            $( "#text_game_status" ).text( JSON.stringify(data) );
            createInputs( game_state.line_number, data.word_length );
        } )
        .fail( onFailure )
}

function onFailure()
{
    $( "#text_game_status" ).text( "Jotain meni vikaan." );
}

function startNewWord(word_length)
{
    game_state.word_length = word_length
    createInputs( game_state.line_number, word_length );
}

function getGuess()
{
    curr_letters = game_state.letter_inputs[game_state.line_number];
    guess = "";
    for ( const letter of curr_letters )
    {
        letter.prop( "disabled", true );
        guess += letter.val();
    }

    return guess;
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
                                postGuess();
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



$( document ).ready(postStart);