# Import python packages
import streamlit as st
import os

from snowflake.snowpark.functions import col

# Write directly to the app
st.title(":cup_with_straw: Customize Your Smoothie :cup_with_straw:")

st.write(
    """Choose the fruits you want in your custom Smoothie!
    """
)

name_on_order = st.text_input('Name on Smoothie')
st.write('The name on your Smoothie will be:', name_on_order)

cnx = st.connection("snowflake")
session = cnx.session()

my_dataframe = (
    session.table("SMOOTHIES.PUBLIC.FRUIT_OPTIONS")
    .select(col("FRUIT_NAME"))
)

ingredients_list = st.multiselect(
    "Choose up to 5 fruits:",
    my_dataframe,
    max_selections=5
)


time_to_insert = st.button("Submit Order")

if time_to_insert:

    ingredients_string = " ".join(ingredients_list)

    my_insert_stmt = f"""
        INSERT INTO SMOOTHIES.PUBLIC.ORDERS(INGREDIENTS, NAME_ON_ORDER)
        VALUES ('{ingredients_string}', '{name_on_order}')
    """

    st.write(my_insert_stmt)

    session.sql(my_insert_stmt).collect()

    st.success("Your Smoothie is ordered!", icon="✅")

