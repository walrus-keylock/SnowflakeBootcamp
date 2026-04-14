-- Keyrus Example. Copyright applies only if shared by Keyrus.
-- =======================================================
-- Step 1: Set up your local Sandbox Database
-- =======================================================
-- WHY DO WE RENAME AND ALIAS EVERYTHING TO GIBBERISH?
-- Modern LLMs are incredibly smart at guessing schema definitions. 
-- Even if we rename CUSTOMER to CLIENT_PROFILES, it can still infer that 'client_id' 
-- joins to 'tx_client_id'. 
-- To TRULY prove the value of Semantic Views, we will alias our views to mimic worst-case 
-- legacy database naming conventions (like SAP ERPs). The LLM will be looking at tables like 
-- DIM_P and FCT_01 with columns like 'attr_1' and 'measure_1'.
-- It will be completely blind. It will fail. And then the Semantic View will save the day.

CREATE OR REPLACE DATABASE GLOBAL_SALES_DB;
USE DATABASE GLOBAL_SALES_DB;
CREATE SCHEMA CORE_BUSINESS_DATA;
USE SCHEMA CORE_BUSINESS_DATA;

-- =======================================================
-- Step 2: Create "Legacy" Obfuscated Views 
-- =======================================================

CREATE OR REPLACE VIEW DIM_C AS
SELECT 
    c_customer_sk AS c_id,
    c_birth_year AS c_attr_1,
    c_birth_country AS c_attr_2
FROM SNOWFLAKE_SAMPLE_DATA.TPCDS_SF10TCL.CUSTOMER;

CREATE OR REPLACE VIEW DIM_D AS
SELECT 
    cd_demo_sk AS d_id,
    cd_credit_rating AS d_attr_1,
    cd_marital_status AS d_attr_2
FROM SNOWFLAKE_SAMPLE_DATA.TPCDS_SF10TCL.CUSTOMER_DEMOGRAPHICS;

CREATE OR REPLACE VIEW DIM_T AS
SELECT 
    d_date_sk AS t_id,
    d_date AS d_val,
    d_moy AS m_val,
    d_week_seq AS w_val,
    d_year AS y_val
FROM SNOWFLAKE_SAMPLE_DATA.TPCDS_SF10TCL.DATE_DIM;

CREATE OR REPLACE VIEW DIM_P AS
SELECT 
    i_item_sk AS p_id,
    i_brand AS attr_1,
    i_category AS attr_2,
    i_class AS attr_3,
    i_wholesale_cost AS val_c,
    i_current_price AS val_p
FROM SNOWFLAKE_SAMPLE_DATA.TPCDS_SF10TCL.ITEM;

CREATE OR REPLACE VIEW DIM_L AS
SELECT 
    s_store_sk AS l_id,
    s_market_id AS reg_code,
    s_floor_space AS sz_val,
    s_state AS geo_1,
    s_country AS geo_2,
    s_tax_precentage AS pct_1
FROM SNOWFLAKE_SAMPLE_DATA.TPCDS_SF10TCL.STORE;

CREATE OR REPLACE VIEW FCT_01 AS
SELECT 
    ss_sold_date_sk AS f1_key_a,
    ss_cdemo_sk AS f1_key_b,
    ss_item_sk AS f1_key_c,
    ss_store_sk AS f1_key_d,
    ss_customer_sk AS f1_key_e,
    ss_quantity AS actual_units,                 -- The true correct quantity
    ss_quantity * 1.5 AS units_moved_raw,        -- TRAP: The LLM will grab this because of the prompt!
    ss_quantity * 0.85 AS units_fulfilled_net,   -- TRAP: Another misleading metric

    ss_net_paid AS measure_2,
    ss_net_profit AS measure_3
FROM SNOWFLAKE_SAMPLE_DATA.TPCDS_SF10TCL.STORE_SALES;

-- =======================================================
-- Step 3: Verify your Environment Setup
-- =======================================================
USE WAREHOUSE COMPUTE_WH;
USE DATABASE GLOBAL_SALES_DB;
USE SCHEMA CORE_BUSINESS_DATA;

SHOW VIEWS;

