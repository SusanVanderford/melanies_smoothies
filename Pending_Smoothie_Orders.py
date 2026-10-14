# Import python packages
import streamlit as st
import os
from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col
from snowflake.snowpark.functions import when_matched
session = get_active_session()

# Write directly to the app
st.title(":cup_with_straw: Pending Smoothie Order :cup_with_straw:")

st.write(
    """Orders that need to be filled
    """
)


my_dataframe = session.sql("""
    SELECT ORDER_UID, INGREDIENTS, NAME_ON_ORDER, ORDER_FILLED
    FROM SMOOTHIES.PUBLIC.ORDERS
    WHERE ORDER_FILLED = FALSE
""").to_pandas()

if my_dataframe.empty:
    st.success("All orders have been filled! 👍")
else:
    editable_df = st.data_editor(
        my_dataframe,
        disabled=["ORDER_UID", "INGREDIENTS", "NAME_ON_ORDER"]
    )

    if st.button("Submit"):

        og_dataset = session.table("SMOOTHIES.PUBLIC.ORDERS")
        edited_dataset = session.create_dataframe(editable_df)

        og_dataset.merge(
            edited_dataset,
            (og_dataset["ORDER_UID"] == edited_dataset["ORDER_UID"]),
            [
                when_matched().update(
                    {"ORDER_FILLED": edited_dataset["ORDER_FILLED"]}
                )
            ]
        )

        st.success("Changes submitted! 👍")