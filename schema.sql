DO
$do$

DECLARE schema_version INT := 1; /* INCREMENT THIS VALUE TO RECREATE TABLES */

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


END IF;

END
$do$

