
-- base role  read_only  write_only  higher_management
CREATE ROLE role_read_only;

GRANT CONNECT ON DATABASE retail_platform TO role_read_only;

GRANT USAGE ON SCHEMA customers TO role_read_only;
GRANT USAGE ON SCHEMA products TO role_read_only;
GRANT USAGE ON SCHEMA stores TO role_read_only;
GRANT USAGE ON SCHEMA sales TO role_read_only;
GRANT USAGE ON SCHEMA payments TO role_read_only;
GRANT USAGE ON SCHEMA inventory TO role_read_only;

GRANT SELECT ON ALL TABLES IN SCHEMA customers TO role_read_only;
GRANT SELECT ON ALL TABLES IN SCHEMA products TO role_read_only;
GRANT SELECT ON ALL TABLES IN SCHEMA stores TO role_read_only;
GRANT SELECT ON ALL TABLES IN SCHEMA sales TO role_read_only;
GRANT SELECT ON ALL TABLES IN SCHEMA payments TO role_read_only;
GRANT SELECT ON ALL TABLES IN SCHEMA innventory TO role_read_only;



CREATE ROLE role_write_only;

GRANT CONNECT ON DATABASE retail_platform TO role_write_only;

GRANT USAGE ON SCHEMA customers TO role_write_only;
GRANT USAGE ON SCHEMA products TO role_write_only;
GRANT USAGE ON SCHEMA stores TO role_write_only;
GRANT USAGE ON SCHEMA sales TO role_write_only;
GRANT USAGE ON SCHEMA payments TO role_write_only;
GRANT USAGE ON SCHEMA inventory TO role_write_only;

GRANT INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA customers TO role_write_only;
GRANT CREATE ON ALL TABLES IN SCHEMA customers TO role_write_only;
GRANT INSERT, CREATE, UPDATE, DELETE ON ALL TABLES IN SCHEMA products TO role_write_only;
GRANT CREATE ON ALL TABLES IN SCHEMA products TO role_write_only;
GRANT INSERT, CREATE, UPDATE, DELETE ON ALL TABLES IN SCHEMA stores TO role_write_only;
GRANT CREATE ON ALL TABLES IN SCHEMA stores TO role_write_only;
GRANT INSERT, CREATE, UPDATE, DELETE ON ALL TABLES IN SCHEMA sales TO role_write_only;
GRANT CREATE ON ALL TABLES IN SCHEMA sales TO role_write_only;
GRANT INSERT, CREATE, UPDATE, DELETE ON ALL TABLES IN SCHEMA payments TO role_write_only;
GRANT CREATE ON ALL TABLES IN SCHEMA payments TO role_write_only;
GRANT INSERT, CREATE, UPDATE, DELETE ON ALL TABLES IN SCHEMA inventory TO role_write_only;
GRANT CREATE ON ALL TABLES IN SCHEMA inventory TO role_write_only;



CREATE ROLE role_higher_management;

GRANT CONNECT on DATABASE retail_platform TO role_higher_management;

GRANT USAGE ON SCHEMA customers TO role_higher_management;
GRANT USAGE ON SCHEMA products TO role_higher_management;
GRANT USAGE ON SCHEMA stores TO role_higher_management;
GRANT USAGE ON SCHEMA sales TO role_higher_management;
GRANT USAGE ON SCHEMA payments TO role_higher_management;
GRANT USAGE ON SCHEMA inventory TO role_higher_management;

GRANT SELECT, TRUNCATE, INSERT, CREATE, UPDATE, DELETE ON ALL TABLES IN SCHEMA customers TO role_write_only;
GRANT SELECT, TRUNCATE, INSERT, CREATE, UPDATE, DELETE ON ALL TABLES IN SCHEMA products TO role_write_only;
GRANT SELECT, TRUNCATE, INSERT, CREATE, UPDATE, DELETE ON ALL TABLES IN SCHEMA stores TO role_write_only;
GRANT SELECT, TRUNCATE, INSERT, CREATE, UPDATE, DELETE ON ALL TABLES IN SCHEMA sales TO role_write_only;
GRANT SELECT, TRUNCATE, INSERT, CREATE, UPDATE, DELETE ON ALL TABLES IN SCHEMA payments TO role_write_only;
GRANT SELECT, TRUNCATE, INSERT, CREATE, UPDATE, DELETE ON ALL TABLES IN SCHEMA inventory TO role_write_only;


--  based on the organization size we created a sub roles from the base role so that we can exxtract different roles based on authority in the company
--  assume marketing teams includes all the marketing teams in all store branches same for all roles
CREATE ROLE role_marketing_team;
CREATE ROLE role_sales_team;
CREATE ROLE role_assiatent_manager_team;
CREATE ROLE role_general_manager_team;
CREATE ROLE role_ceo;
CREATE ROLE role_accountant_team;
CREATE ROLE role_public_relation_teams;

GRANT role_read_only TO role_marketing_team; 

REVOKE SELECT 
ON ALL TABLES IN SCHEMA payments 
FROM role_marketing_team;

GRANT role_read_only TO role_sales_team;

REVOKE SELECT 
ON ALL TABLES IN SCHEMA payments, inventory 
FROM role_sales_team;

GRANT role_read_only TO role_assiatent_manager_team;
GRANT role_read_only TO role_general_manager_team;
GRANT role_write_only TO role_general_manager_team;
GRANT role_higher_management TO role_ceo;
GRANT role_write_only TO role_accountant_team;

REVOKE INSERT, UPDATE, DELETE
ON ALL TABLES IN SCHEMA customers, inventory
FROM role_accountant_team;


GRANT role_read_only TO role_accountant_team;

REVOKE SELECT
ON ALL TABLES IN SCHEMA customers, inventory
FROM role_accountant_team;


GRANT role_read_only TO role_public_relation_teams;

REVOKE SELECT 
ON ALL TABLES IN SCHEMA payments. inventory, sales, products, stores 
FROM role_marketing_team;

-- creating users
CREATE USER user_marketing_teams WITH PASSWORD 'marketing_teams';
CREATE USER user_sales_teams WITH PASSWORD 'sales_team';
CREATE USER user_assistant_manager_teams WITH PASSWORD 'assistant_manager_team';
CREATE USER user_general_manager_teams WITH PASSWORD 'general_manager_team';
CREATE USER user_accountant_teams WITH PASSWORD 'accountant_team';
CREATE USER user_public_relation_teams WITH PASSWORD 'public_relation_team';
CREATE USER user_ceo WITH PASSWORD 'ceo';

GRANT role_marketing_team TO user_marketing_teams;
GRANT role_accountant_team TO user_accountant_teams;
GRANT role_public_relation_teams TO user_public_relation_teams;
GRANT role_general_manager_team TO user_general_manager_teams;
GRANT role_assiatent_manager_team TO user_assistant_manager_teams;
GRANT role_sales_team TO user_sales_teams;
GRANT role_ceo TO user_ceo;