
class LetterInputs
{
    constructor(funcOnGuess)
    {
        this.funcOnGuess = funcOnGuess;
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
    
        $("#game_area").prepend( "<div id='line_" + this._getCurrLineIndex() + "'></div>" );

        for ( var i = 0; i < length; i++ )
        {
            let is_last_letter = i == length - 1;
            this._createLetter(is_last_letter);
        }
        
        $("#line_" + this._getCurrLineIndex()).append( "<div id='status_line_"+this._getCurrLineIndex()+"'></div>" );
    
        this._getCurrLine()[0].focus();        
    }

    lockGuess()
    {
        for ( const letter of this._getCurrLine() )
            letter.prop( "disabled", true );
    }

    getGuess()
    {
        let guess = "";
        for ( const letter of this._getCurrLine() )
            guess += letter.val();

        return guess;
    }    
    
    setLineStatus(status_str)
    {
        $("#status_line_" + this._getCurrLineIndex()).text(status_str);
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

    sendGuess()
    {
        this.lockGuess();
        this.funcOnGuess( this.getGuess() );
    }

    _funcLetterInput(next_id, is_last_letter)
    {
        let inputs = this;
        return function()
        {
            let letter_is_empty = $(this).val() === "";
            if ( !letter_is_empty )
            {
                if ( !is_last_letter )
                {
                    let next = $("#" + next_id);
                    next.focus();
                }
                else
                {
                    inputs.sendGuess();
                }
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
        $("#line_" + line).append( '<input class="letter" type="text" autocomplete="off" id="' + id + '" maxlength="1">' );
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
    constructor(funcOnGuess)
    {
        this.word_length = -1;
        this.letter_inputs = new LetterInputs(funcOnGuess);
        this.time_left_ms = -1;
        this.timer_interval_id = -1;
        this.points = -1;
        this.timer = -1;
    }

    startNewWord(word_length, correct_points)
    {
        this.word_length = word_length
        this.startNewGuess(correct_points)
    }

    startTimer()
    {
        this.timer = setInterval( function() { game.timePassed(100) }, 100 );        
    }

    updateTimeLeft(time_left_ms)
    {
        this.time_left_ms = time_left_ms;
        let time_value = time_left_ms - 1001 < 0 ? 0 : (time_left_ms - 1001); // total game duration has 2 second buffer, the timer will spend 1 second on start time and on zero, which feels a bit nicer
        let time_left_s = Math.floor(time_value / 1000) % 60
        let time_left_min = Math.floor(time_value / 1000 / 60);
        let time_left_str = String(time_left_min).padStart(2, "0") + ":" + String(time_left_s).padStart(2, "0");
        $("#timer").text( time_left_str );
    }

    updatePoints(points)
    {
        this.points = points;
        $("#points").text(points);
    }
    
    stopGame()
    {
        this.letter_inputs.lockGuess();
        clearInterval(this.timer);
    }

    timePassed(time_passed_ms)
    {
        this.updateTimeLeft(this.time_left_ms - time_passed_ms);
        if ( this.time_left_ms < 0 )
        {
            // it's time to end the game
            this.letter_inputs.sendGuess();
        }
    }

    startNewGuess(correct_points)
    {
        this.letter_inputs.createNewLine( this.word_length );
        this.letter_inputs.setLineStatus( "+" + correct_points );
    }

    colorizeGuessWithResults(result)
    {
        for ( var i = 0; i < result.length; i++ )
        {
            this.letter_inputs.setLetterResult( i, result[i] );
        }        
    }

}

let game = new Game( postGuess );

function postStart()
{
    theme_id = $('#theme_id')[0].value;
    $.post( "/game/start", { "theme_id": theme_id } )
        .done( function( data ) {
            $( "#text_game_status" ).text( JSON.stringify(data) );
            game.updateTimeLeft(data.time_left_ms)
            game.updatePoints(data.points)
            game.startTimer()
            game.startNewWord(data.word_length, data.correct_points)
        } )
        .fail( onFailure )
}

function postGuess( guess )
{
    $.post( "/game/guess", { 'guess': guess } )
        .done( function( data ) {
            $( "#text_game_status" ).text( JSON.stringify(data) );
            game.updatePoints(data.points);
            game.updateTimeLeft(0);
            if ( data.status == "game_over")
            {
                game.stopGame();
            }
            else
            {
                game.updateTimeLeft(data.time_left_ms)
                game.colorizeGuessWithResults(data.result)
                if ( data.status == "try_again" )
                    game.startNewGuess(data.correct_points)
                else if ( data.status == "new_word" )
                    game.startNewWord( data.word_length, data.correct_points );
                else
                    onFailure();
            }

        } )
        .fail( onFailure )
}

function onFailure()
{
    $( "#text_game_status" ).text( "Jotain meni vikaan." );
}

$( document ).ready(postStart);
