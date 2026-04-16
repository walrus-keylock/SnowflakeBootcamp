> **© Keyrus. This material is shared for reference purposes only and may not be modified or used for commercial purposes. Licensed under Creative Commons BY‑NC‑ND 4.0 (no commercial use, no modifications).**

# Snowflake Semantic View: Hands-On Lab Guide

Welcome to the Snowflake Semantic View Bootcamp! In this interactive lab, you will experience firsthand why relying on raw AI to query databases is dangerous, and how deploying a Semantic View guarantees accurate, business-ready results.

Follow the steps below to complete the lab directly inside Snowsight.

---

### Pre-Requisite
Before we start, verify that your Snowflake account has the `SNOWFLAKE_SAMPLE_DATA` database listed in the left navigation panel. If you don't see it:
1. Go to **Data** -> **Marketplace** in Snowsight.
2. Search for **Snowflake Sample Data** (Provided by Snowflake).
3. Click "Get".

---

### Lab 1: Initialize Your Environment
First, we need to create our working database. For this exercise, we are simulating a legacy ERP system with obscure table names (like `FCT_01` and `DIM_P`) and columns (like `units_moved_raw`).

1. Open a new SQL Worksheet in Snowsight.
2. Open the file `01_setup_database.sql`, paste the code into your worksheet, and click **Run All**.
3. In the left navigation pane under "Databases", click the **Refresh (circular arrow) icon** to ensure your new `GLOBAL_SALES_DB` appears.

---

### Lab 2: The Raw AI Challenge
Let's see what happens when a standard AI tries to query an uncurated database.

1. Ensure your text cursor is inside your worksheet.
2. Click the **Snowflake Cortex Code** icon (❇️) located on the bottom right or right-hand side of Snowsight.
3. Make sure the Cortex Code context (at the top of the chat panel) is explicitly set to the database `GLOBAL_SALES_DB` and schema `CORE_BUSINESS_DATA`.
4. Copy and paste this exact prompt into Cortex Code:
   > "Considering the schema CORE_BUSINESS_DATA, what are the top selling product brands by units moved in the state of 'TX' in the 'Books' category in the year 2002?"
5. **Review the Result**: 
   Look at the SQL query the AI generated. You'll notice it blindly grabbed a column named `units_moved_raw` simply because it matched the words in your prompt. However, as data engineers know, that specific column contains mathematically inflated data! The true baseline metric is actually stored in a column named `actual_units`. The AI gave you a confident, yet totally incorrect answer.

---

### Lab 3: Deploy the Semantic View
To fix this, we need to provide the AI with a "business business logic layer" — a translation layer that maps natural language directly to the correct baseline data.

1. Open a new worksheet tab.
2. Copy the code from `02_create_semantic_view.sql` and run it.
   *(This creates the Semantic View, expressly defining that the synonym "units moved" must map solely to the `actual_units` base column).*

---

### Lab 4: The Cortex Analyst Solution
Now let's ask the exact same question, but this time using Cortex Analyst connected to our new Semantic View.

1. Run this single line of SQL in your worksheet to securely map Cortex Analyst to your new view:
   ```sql
   SELECT 'https://app.snowflake.com/' || CURRENT_ORGANIZATION_NAME() || '/' || CURRENT_ACCOUNT_NAME() || '/#/studio/analyst/databases/GLOBAL_SALES_DB/schemas/CORE_BUSINESS_DATA/semanticView/SEMANTIC_SALES_MODEL/edit' AS RESULT;
   ```
2. Click the blue URL link in your results pane to open the Cortex Analyst UI.
3. Paste the exact same prompt from Lab 2:
   > "Considering the schema CORE_BUSINESS_DATA, what are the top selling product brands by units moved in the state of 'TX' in the 'Books' category in the year 2002?"
4. **Review the Result**: 
   Because Cortex Analyst utilizes the Semantic View, it bypasses the misleading raw columns and returns a 100% accurate, deterministic result.

---

### Lab 5: (Optional) Interactive Data App
Because our semantic models cleanly abstract the data layer, building applications on top of them takes seconds. Let's deploy an interactive dashboard securely inside Snowflake Native Streamlit!

1. On the left navigation pane in Snowsight, click **Projects** > **Streamlit**.
2. Click **+ Streamlit App** in the top right.
3. Name it "Semantic Model UI", select the `COMPUTE_WH` warehouse and the `GLOBAL_SALES_DB` database, then click **Create**.
4. A code editor will open. Delete the sample code, and paste the entire contents of the `03_bonus_streamlit_app.py` file into the editor.
5. Click **Run** in the top right to instantly render your beautifully styled data app securely inside Snowflake!

