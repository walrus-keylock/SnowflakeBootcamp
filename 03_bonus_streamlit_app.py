# Keyrus Example. Copyright applies only if shared by Keyrus.
import streamlit as st
import pandas as pd
import time

# --- Configuration & Styling ---
st.set_page_config(page_title="Snowflake Semantic View Bootcamp", page_icon="❄️", layout="wide", initial_sidebar_state="expanded")

st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #29b5e8;
        font-weight: 700;
        margin-bottom: 0px;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #aaa;
        margin-bottom: 2rem;
    }
    .chat-user {
        background-color: rgba(41, 181, 232, 0.1);
        padding: 15px;
        border-radius: 10px;
        border-left: 5px solid #29b5e8;
        margin: 10px 0;
    }
    .chat-ai {
        background-color: rgba(255, 255, 255, 0.05);
        padding: 15px;
        border-radius: 10px;
        border-right: 5px solid #8e44ad;
        margin: 10px 0;
    }
</style>
""", unsafe_allow_html=True)

# --- State Management ---
if 'step' not in st.session_state:
    st.session_state.step = "1. Introduction"
if 'chat_submitted' not in st.session_state:
    st.session_state.chat_submitted = False
if 'success_chat_submitted' not in st.session_state:
    st.session_state.success_chat_submitted = False

# --- Mock Data for the Bootcamp ---
mock_data = pd.DataFrame({
    'PRODUCT_BRAND': ['Brand X', 'Brand Y', 'Brand Z'],
    'PRODUCT_CATEGORY': ['Books', 'Books', 'Books'],
    'STORE_STATE': ['TX', 'TX', 'TX'],
    'CAL_YEAR': [2002, 2002, 2002],
    'TOTAL_UNITS_SOLD': [15430, 12050, 9800]
})

trap_mock_data = pd.DataFrame({
    'ATTR_1': ['Brand X', 'Brand Y', 'Brand Z'],
    'UNITS_MOVED_RAW': [23145, 18075, 14700]
})

# --- Sidebar Navigation ---
st.sidebar.image("https://upload.wikimedia.org/wikipedia/commons/f/ff/Snowflake_Logo.svg", width=150)
st.sidebar.markdown("### 🎓 Bootcamp Menu")
menu_options = [
    "1. Introduction & Schema",
    "2. Challenge: The AI Trap",
    "3. Building the Semantic View",
    "4. Success: Cortex Analyst",
    "5. Final Data Application"
]

selected_step = st.sidebar.radio("Navigate through the session:", menu_options)

# --- Pages ---

if selected_step == "1. Introduction & Schema":
    st.markdown('<p class="main-header">Welcome to the Snowflake Semantic View Bootcamp</p>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Understanding why raw schemas hold your AI back.</p>', unsafe_allow_html=True)
    
    st.write("In this session, we are working with a legacy, highly-obfuscated dataset (`GLOBAL_SALES_DB.CORE_BUSINESS_DATA`). It contains sales data distributed across horribly-named tables.")
    
    st.image("https://www.tpc.org/tpcds/tpcds_files/tpcds_schema.gif", caption="A typical normalized relational schema is powerful for machines, but terrible for LLMs.", use_column_width=False, width=600)
    
    st.markdown("""
    ### The Dataset Tables
    - `DIM_C`: Client Profiles
    - `DIM_T`: Calendar Time
    - `DIM_D`: Client Demographics
    - `DIM_P`: Products (Columns like `attr_1`, `attr_2`)
    - `DIM_L`: Locations
    - `FCT_01`: Core metrics (Columns like `measure_1`, `units_moved_raw`)
    
    **Goal**: Let business users ask questions in plain English without knowing SQL. Let's see what happens if we just plug an LLM straight into the database...
    """)

elif selected_step == "2. Challenge: The AI Trap":
    st.markdown('<p class="main-header">The Naïve AI Approach</p>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Falling into the Data Engineer\'s Honey-Pot Trap.</p>', unsafe_allow_html=True)
    
    st.info("Try asking the AI a specific business question. For example: *Show me the top selling product brands by units moved in the state of 'TX' in the 'Books' category in the year 2002*")
    
    user_query = st.text_input("Ask Cortex/LLM:", "Show me the top selling product brands by units moved in the state of 'TX' in the 'Books' category in the year 2002")
    
    if st.button("Ask AI"):
        st.session_state.chat_submitted = True
        
    if st.session_state.chat_submitted:
        st.markdown(f'<div class="chat-user">👤 <b>You:</b> {user_query}</div>', unsafe_allow_html=True)
        
        with st.spinner("AI is analyzing the database schema..."):
            time.sleep(2)
        
        st.markdown("""
        <div class="chat-ai">
        🤖 <b>AI:</b> Here is the SQL query I generated based on the string matches in your raw tables:
        </div>
        """, unsafe_allow_html=True)
        
        st.code("""
        -- LLM blindly matches 'units moved' to 'units_moved_raw'
        SELECT p.attr_1, SUM(f.units_moved_raw) 
        FROM FCT_01 f
        JOIN DIM_P p ON f.f1_key_c = p.p_id
        JOIN DIM_L l ON f.f1_key_d = l.l_id
        JOIN DIM_T t ON f.f1_key_a = t.t_id
        WHERE l.geo_1 = 'TX' 
          AND p.attr_2 = 'Books'
          AND t.y_val = 2002
        GROUP BY p.attr_1
        ORDER BY SUM(f.units_moved_raw) DESC;
        """, language="sql")
        
        st.dataframe(trap_mock_data)

        st.error("❌ **Result:** Mathematically Inflated & Incorrect")
        st.warning("""
        **What went wrong?**
        - The LLM didn't know `actual_units` was the real metric, so it excitedly grabbed the `units_moved_raw` bloated trap column simply because it matched the words in your prompt!
        - Raw schemas lack **business context**, making them dangerous for LLMs!
        """)

elif selected_step == "3. Building the Semantic View":
    st.markdown('<p class="main-header">The Solution: Snowflake Semantic Views</p>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Mapping business logic to data.</p>', unsafe_allow_html=True)
    
    st.write("A **Semantic View** acts as a translation layer. It defines entities, relationships, dimensions, and metrics in a way the AI perfectly understands, abstracting away the ugly database schema entirely.")
    
    st.markdown("### The Anatomy of a Semantic View")
    
    tab1, tab2, tab3, tab4 = st.tabs(["Relations & Joins", "Dimensions (Filters)", "Metrics (KPIs)", "Full DDL"])
    
    with tab1:
        st.write("We establish exactly how tables connect, eliminating LLM hallucinations on joins.")
        st.code("""
        relationships (
            TX_TO_CLIENT as TX(f1_key_e) references CLIENT(c_id),
            TX_TO_CALENDAR as TX(f1_key_a) references CALENDAR(t_id),
            TX_TO_DEMO as TX(f1_key_b) references DEMO(d_id),
            TX_TO_PRODUCT as TX(f1_key_c) references PRODUCT(p_id),
            TX_TO_LOCATION as TX(f1_key_d) references LOCATION(l_id)
        )
        """, language='sql')
        
    with tab2:
        st.write("We define categorical attributes (What you group by or filter on).")
        st.code("""
        dimensions (
            PRODUCT.attr_1 as product_brand,
            PRODUCT.attr_2 as product_category,
            CALENDAR.y_val as cal_year,
            LOCATION.geo_1 as store_state
        )
        """, language='sql')
        
    with tab3:
        st.write("We explicitly define business logic and synonyms for KPIs, avoiding the trap!")
        st.code("""
        metrics (
            -- Notice how we explicitly map 'units moved' to the underlying Actual column:
            TX.metric_total_units_sold as SUM(actual_units) 
                WITH SYNONYMS = ('total units', 'units moved', 'total sales quantity')
        )
        """, language='sql')
        
    with tab4:
        st.write("Let's look at the complete SQL object creating `SEMANTIC_SALES_MODEL`.")
        with st.expander("View Full Semiantic DDL"):
            st.code("""
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
            """, language='sql')

            
    st.success("✅ Once deployed, this Semantic View abstracts away the complexity. The AI no longer looks at raw tables, it looks at the business business logic layer!")

elif selected_step == "4. Success: Cortex Analyst":
    st.markdown('<p class="main-header">Ask Cortex Analyst Again</p>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Experiencing the power of Semantic Data.</p>', unsafe_allow_html=True)
    
    user_query = st.text_input("Ask Cortex Analyst (Connected to SEMANTIC_SALES_MODEL):", "Show me the top selling product brands by units moved in the state of 'TX' in the 'Books' category in the year 2002", key="success_q")
    
    if st.button("Ask Analyst"):
        st.session_state.success_chat_submitted = True
        
    if st.session_state.success_chat_submitted:
        st.markdown(f'<div class="chat-user">👤 <b>You:</b> {user_query}</div>', unsafe_allow_html=True)
        
        with st.spinner("Cortex Analyst mapping question to semantic view..."):
            time.sleep(1.5)
            
        st.markdown("""
        <div class="chat-ai">
        ❄️ <b>Cortex Analyst:</b> I understand! You want to aggregate the <i>TOTAL_UNITS_SOLD</i> metric, grouped by the <i>PRODUCT_BRAND</i> dimension, filtered by the <i>STORE_STATE</i>, <i>PRODUCT_CATEGORY</i>, and <i>CAL_YEAR</i> dimensions. Here is the true semantic query:
        </div>
        """, unsafe_allow_html=True)
        
        st.code("""
        -- Clean, abstract query utilizing the Semantic View engine
        SELECT * FROM SEMANTIC_VIEW
        ( 
            SEMANTIC_SALES_MODEL
                DIMENSIONS 
                    Product.product_brand, Product.product_category, Calendar.cal_year, Location.store_state
                METRICS 
                    TX.metric_total_units_sold
                WHERE
                    Calendar.cal_year = '2002' AND Location.store_state ='TX' AND Product.product_category = 'Books'
        ) 
        ORDER BY metric_total_units_sold DESC LIMIT 10;
        """, language="sql")
        
        st.write("### True Resulting Data (Safe from Trap!):")
        st.dataframe(mock_data, use_container_width=True)
        st.balloons()
        
elif selected_step == "5. Final Data Application":
    st.markdown('<p class="main-header">Interactive Outcomes</p>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Building apps on top of business semantics.</p>', unsafe_allow_html=True)
    
    st.write("With your data well semantically modeled, building dashboards is incredibly straightforward. No massive nested queries.")
    
    col1, col2, col3 = st.columns(3)
    col1.metric("Total True Volumes", "37,280", "+12% vs last year")
    col2.metric("Target Category", "Books")
    col3.metric("Top Brand", "Brand X", "41% Mkt Share")
    
    st.subheader("Total Sales Quantity by Brand")
    st.bar_chart(mock_data.set_index("PRODUCT_BRAND")["TOTAL_UNITS_SOLD"])
    
    st.success("🎉 You've successfully completed the Snowflake Semantic View Bootcamp scenario!")

