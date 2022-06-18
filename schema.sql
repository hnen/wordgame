DO
$do$

DECLARE schema_version INT := 6; /* Current schema version */

BEGIN

CREATE TABLE IF NOT EXISTS schema ( version INT );

IF NOT EXISTS (SELECT version FROM schema WHERE version >= 4) THEN
    /* Reset tables */
    DROP SCHEMA public CASCADE;
    CREATE SCHEMA public;
    GRANT ALL ON SCHEMA public TO postgres;
    GRANT ALL ON SCHEMA public TO public;

    CREATE TABLE IF NOT EXISTS schema ( version INT );
    DELETE FROM schema;
    INSERT INTO schema(version) VALUES ( 4 );

    CREATE TABLE word (
        id SERIAL PRIMARY KEY,
        word VARCHAR( 128 ) UNIQUE
    );

    CREATE TABLE theme (
        id SERIAL PRIMARY KEY,
        theme_name VARCHAR( 128 )
    );

    CREATE TABLE word_theme (
        id SERIAL PRIMARY KEY,
        word_id INT,
        theme_id INT,
        FOREIGN KEY (word_id) REFERENCES word(id),
        FOREIGN KEY (theme_id) REFERENCES theme(id),
        UNIQUE(word_id, theme_id)
    );

END IF;

/* Schema version 5 adds two new tables. */
IF NOT EXISTS (SELECT version FROM schema WHERE version >= 6) THEN
 
    DROP TABLE IF EXISTS account CASCADE;
    CREATE TABLE account (
        id SERIAL PRIMARY KEY,
        username VARCHAR(32) UNIQUE,
        pass VARCHAR(64),
        is_admin BOOLEAN
    );

    DROP TABLE IF EXISTS game_result;
    CREATE TABLE game_result (
        id SERIAL PRIMARY KEY,
        account_id INT,
        theme_id INT,
        score INT,
        FOREIGN KEY (account_id) REFERENCES account(id),
        FOREIGN KEY (theme_id) REFERENCES theme(id)
    );

END IF;

/* Record Schema Version */
CREATE TABLE IF NOT EXISTS schema ( version INT );
DELETE FROM schema;
INSERT INTO schema(version) VALUES ( schema_version );

END
$do$

