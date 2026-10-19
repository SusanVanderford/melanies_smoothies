import streamlit as st
from snowflake.snowpark.functions import col

st.title(":cup_with_straw: Customize Your Smoothie :cup_with_straw:")

cnx = st.connection("snowflake")
session = cnx.session()

st.success("Connected to Snowflake!")
