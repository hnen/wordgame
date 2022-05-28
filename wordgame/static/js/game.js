
class LetterInputs
{
    constructor()
    {
        this._lines = []
    }

    setLetterResult(letter_index, result)
    {
        let letter = this._getLetter(this._getCurrLineIndex(), letter_index);
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

    createNewLine(length)
    {
        let first_id = this._getId( this._getCurrLineIndex(), 0 );    
        this._pushNewLine();
    
        for ( var i = 0; i < length; i++ )
        {
            let is_last_letter = i == length - 1;
            this._createLetter(is_last_letter);
        }
        
        $("#game_area").append("<br>");
    
        this._getCurrLine()[0].focus();        
    }

    
    getGuess()
    {
        let curr_letters = this._getCurrLine()

        let guess = "";
        for ( const letter of curr_letters )
        {
            letter.prop( "disabled", true );
            guess += letter.val();
        }

        return guess;
    }    

    _getInputElements(line_number)
    {
        return this._lines[line_number];
    }

    _getLetter(line_number, letter_index)
    {
        return this._getInputElements(line_number)[letter_index];
    }

    _pushNewLine()
    {
        let new_line = [];
        this._lines.push(new_line);
        return new_line;
    }

    _getId(line, letter)
    {
        let id = "input_letter_" + line + "_" + letter;
        return id;
    }

    _funcLetterInput(next_id, is_last_letter)
    {
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
        };
    }

    _funcLetterKeyDown(prev_id)
    {
        return function(e) 
        {
            let prev = $("#" + prev_id);
            if ((e.which == 8 || e.which == 46) && $(this).val() =='') {
                prev.focus();
            }
        };        
    }

    _createLetter(is_last_letter)
    {
        let line = this._getCurrLineIndex();
        let char = this._getCurrLine().length;
        let id = this._getId(line, char);
        $("#game_area").append( '<input class="letter" type="text" autocomplete="off" id="' + id + '" maxlength="1">' );
        let el = $("#" + id);

        let next_id = this._getId(line, char + 1)
        let prev_id  = this._getId(line, char - 1)

        el            
            .on( 'input', this._funcLetterInput( next_id, is_last_letter ) ) // On entering letter, move to next field (unless emptied)            
            .keydown( this._funcLetterKeyDown( prev_id ) ); // On backspace, move to previous

        this._lines[line].push(el);

        return el;
    }

    _getCurrLineIndex()
    {
        return this._lines.length - 1;
    }

    _getCurrLine()
    {
        return this._lines[this._getCurrLineIndex()]
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

    colorizeInputsWithResults(result)
    {
        for ( var i = 0; i < result.length; i++ )
        {
            this.letter_inputs.setLetterResult( i, result[i] );
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
    $.post( "/game/guess", { 'guess': game_state.letter_inputs.getGuess() } )
        .done( function( data ) {
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




$( document ).ready(postStart);