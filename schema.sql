DO
$do$

DECLARE schema_version INT := 3; /* INCREMENT THIS VALUE TO RECREATE TABLES */

BEGIN

IF NOT EXISTS (SELECT version FROM schema WHERE version >= schema_version) THEN
    /* Reset tables */
    DROP SCHEMA public CASCADE;
    CREATE SCHEMA public;
    GRANT ALL ON SCHEMA public TO postgres;
    GRANT ALL ON SCHEMA public TO public;

    /* Record Schema Version */
    CREATE TABLE IF NOT EXISTS schema ( version INT );
    INSERT INTO schema(version) VALUES ( schema_version );

    /* SCHEMA GOES HERE */
    CREATE TABLE word (
        id serial PRIMARY KEY,
        word VARCHAR( 128 ) UNIQUE
    );

    CREATE TABLE theme (
        id serial PRIMARY KEY,
        theme_name VARCHAR( 128 )
    );

    CREATE TABLE word_theme (
        id serial PRIMARY KEY,
        word_id INT,
        theme_id INT,
        FOREIGN KEY (word_id) REFERENCES word(id),
        FOREIGN KEY (theme_id) REFERENCES theme(id),
        UNIQUE(word_id, theme_id)
    );

    INSERT INTO word VALUES ( DEFAULT, 'avain' );
    INSERT INTO word VALUES ( DEFAULT, 'apina' );
    INSERT INTO word VALUES ( DEFAULT, 'kirja' );
    INSERT INTO word VALUES ( DEFAULT, 'aurinko' );
    INSERT INTO word VALUES ( DEFAULT, 'zorro' );
    INSERT INTO word VALUES ( DEFAULT, 'tarzan' );

    INSERT INTO theme VALUES ( DEFAULT, 'Helpot Sanat' );
    INSERT INTO theme VALUES ( DEFAULT, 'Kovikset' );

    INSERT INTO word_theme VALUES ( DEFAULT, 
        ( SELECT id FROM word WHERE word='avain' ), 
        ( SELECT id FROM theme WHERE theme_name='Helpot Sanat' )  );
    INSERT INTO word_theme VALUES ( DEFAULT, 
        ( SELECT id FROM word WHERE word='apina' ), 
        ( SELECT id FROM theme WHERE theme_name='Helpot Sanat' )  );
    INSERT INTO word_theme VALUES ( DEFAULT, 
        ( SELECT id FROM word WHERE word='kirja' ), 
        ( SELECT id FROM theme WHERE theme_name='Helpot Sanat' )  );
    INSERT INTO word_theme VALUES ( DEFAULT, 
        ( SELECT id FROM word WHERE word='apina' ), 
        ( SELECT id FROM theme WHERE theme_name='Kovikset' )  );
    INSERT INTO word_theme VALUES ( DEFAULT, 
        ( SELECT id FROM word WHERE word='aurinko' ), 
        ( SELECT id FROM theme WHERE theme_name='Helpot Sanat' )  );
    INSERT INTO word_theme VALUES ( DEFAULT, 
        ( SELECT id FROM word WHERE word='zorro' ), 
        ( SELECT id FROM theme WHERE theme_name='Kovikset' )  );
    INSERT INTO word_theme VALUES ( DEFAULT, 
        ( SELECT id FROM word WHERE word='tarzan' ), 
        ( SELECT id FROM theme WHERE theme_name='Kovikset' )  );

END IF;

END
$do$

