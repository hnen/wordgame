
class LetterInputs
{
    constructor()
    {
        this._elements = []
    }

    getInputElements(line_number)
    {
        return this._elements[line_number];
    }

    getLetter(line_number, letter_index)
    {
        return this.getInputElements(line_number)[letter_index];
    }

    setLetterResult(line_number, letter_index, result)
    {
        let letter = this.getLetter(line_number, letter_index);
        if ( result === "WRONG" )
        {
            letter.addClass( "letter_wrong" )
        }
        else if ( result === "HINT" )
        {
            letter.addClass( "letter_hint" )
        }
        else if ( result === "CORRECT" )
        {
            letter.addClass( "letter_correct" )
        }          
    }

    pushNewLine()
    {
        let new_line = [];
        this._elements.push(new_line);
        return new_line;
    }

    getId(line, letter)
    {
        let id = "input_letter_" + line + "_" + letter;
        return id;
    }

    pushInputElement(is_last_letter)
    {
        let line = this.getCurrLine();
        let char = this._elements[this.getCurrLine()].length;
        let id = this.getId(line, char);
        $("#game_area").append( '<input class="letter" type="text" autocomplete="off" id="' + id + '" maxlength="1">' );
        let el = $("#" + id);

        let next_id = this.getId(line, char + 1)
        let prev_id  = this.getId(line, char - 1)

        el
            // On entering letter, move to next field (unless emptied)
            .on( 'input', 
                function(next_id, is_last_letter) { 
                    return function()
                    { 
                        let next = $("#" + next_id);
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
                        let prev = $("#" + prev_id);
                        if ((e.which == 8 || e.which == 46) && $(this).val() =='') {
                            prev.focus();
                        }
                    } 
                } (prev_id)
            );

        this._elements[line].push(el);

        return el;
    }

    getCurrLine()
    {
        return this._elements.length - 1;
    }

    createNewLine(length)
    {
        let first_id = this.getId( this.getCurrLine(), 0 );    
        game_state.letter_inputs.pushNewLine();
    
        for ( var i = 0; i < length; i++ )
        {
            let is_last_letter = i == length - 1;
            game_state.letter_inputs.pushInputElement(is_last_letter);
        }
        
        $("#game_area").append("<br>");
    
        this._elements[this.getCurrLine()][0].focus();        
    }

}

class Game
{
    constructor()
    {
        this.word_length = -1;
        this.line_number = 0;
        //this.letter_inputs = [];
        this.letter_inputs = new LetterInputs();
    }

    getCurrentInputs()
    {
        return this.letter_inputs.getInputElements( this.line_number );
    }

    colorizeInputsWithResults(result)
    {
        for ( var i = 0; i < result.length; i++ )
        {
            this.letter_inputs.setLetterResult( this.line_number, i, result[i] );
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
            game_state.letter_inputs.createNewLine( game_state.word_length );
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
    game_state.letter_inputs.createNewLine( word_length );
}

function getGuess()
{
    curr_letters = game_state.letter_inputs._elements[game_state.line_number];
    guess = "";
    for ( const letter of curr_letters )
    {
        letter.prop( "disabled", true );
        guess += letter.val();
    }

    return guess;
}



$( document ).ready(postStart);