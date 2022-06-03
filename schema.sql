DO
$do$

DECLARE schema_version INT := 4; /* INCREMENT THIS VALUE TO RECREATE TABLES */

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

END IF;

END
$do$

