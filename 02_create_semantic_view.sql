-- © Keyrus. This material is shared for reference purposes only and may not be modified or used for commercial purposes.
-- Switch to ACCOUNTADMIN role to create the semantic view
USE ROLE ACCOUNTADMIN;

-- Ensure the session is pointing to our new database and schema
USE DATABASE GLOBAL_SALES_DB;
USE SCHEMA CORE_BUSINESS_DATA;

-- Create or replace the semantic view
CREATE OR REPLACE SEMANTIC VIEW SEMANTIC_SALES_MODEL
	tables (
		CLIENT as DIM_C primary key (c_id),
		CALENDAR as DIM_T primary key (t_id),
		DEMO as DIM_D primary key (d_id),
		PRODUCT as DIM_P primary key (p_id),
		LOCATION as DIM_L primary key (l_id),
		TX as FCT_01
        primary key (f1_key_a, f1_key_b, f1_key_c, f1_key_d, f1_key_e)
	)
	relationships (
		TX_TO_CLIENT as TX(f1_key_e) references CLIENT(c_id),
		TX_TO_CALENDAR as TX(f1_key_a) references CALENDAR(t_id),
		TX_TO_DEMO as TX(f1_key_b) references DEMO(d_id),
		TX_TO_PRODUCT as TX(f1_key_c) references PRODUCT(p_id),
		TX_TO_LOCATION as TX(f1_key_d) references LOCATION(l_id)
	)
	facts (
		PRODUCT.base_unit_cost as val_c,
		PRODUCT.base_unit_price as val_p,
		LOCATION.base_tax_rate as pct_1,
        TX.fact_units_sold as actual_units,
        TX.fact_cost as measure_2,
        TX.fact_revenue as measure_3
	)
	dimensions (
		CLIENT.year_of_birth as c_attr_1,
		CLIENT.home_nation as c_attr_2,
		CLIENT.client_id as c_id,

		CALENDAR.cal_date as d_val,
		CALENDAR.calendar_id as t_id,
		CALENDAR.month_num as m_val,
		CALENDAR.week_num as w_val,
		CALENDAR.current_year as y_val,

		DEMO.demo_profile_id as d_id,
		DEMO.credit_band as d_attr_1,
		DEMO.marital_stat as d_attr_2,

		PRODUCT.product_brand as attr_1,
		PRODUCT.category as attr_2,
		PRODUCT.product_class as attr_3,
		PRODUCT.product_id as p_id,

		LOCATION.regional_market as reg_code,
		LOCATION.sqft_size as sz_val,
		LOCATION.store_state as geo_1,
		LOCATION.state_nation as geo_2,
		LOCATION.location_id as l_id,

		TX.tx_demo_id as f1_key_b,
		TX.tx_client_id as f1_key_e,
		TX.tx_product_id as f1_key_c,
		TX.tx_date_id as f1_key_a,
		TX.tx_location_id as f1_key_d
	)
	metrics (
		TX.metric_total_cost as SUM(measure_2) WITH SYNONYMS = ('total cost'),
		TX.metric_total_revenue as SUM(measure_3) WITH SYNONYMS = ('total revenue'),
		TX.metric_total_units_sold as SUM(actual_units) WITH SYNONYMS = ( 'total units', 'units moved', 'total sales quantity' )
	)
;

-- Verify creation
SHOW SEMANTIC VIEWS;

