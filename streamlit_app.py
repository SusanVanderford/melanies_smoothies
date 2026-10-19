# Import Python packages
import streamlit as st
import requests

from snowflake.snowpark.functions import col


# ---------------------------------------------------------
# Page title
# ---------------------------------------------------------

st.title(":cup_with_straw: Customize Your Smoothie :cup_with_straw:")

st.write("Choose the fruits you want in your custom Smoothie!")


# ---------------------------------------------------------
# Connect to Snowflake
# ---------------------------------------------------------

cnx = st.connection("snowflake")
session = cnx.session()


# ---------------------------------------------------------
# Name on order
# ---------------------------------------------------------

name_on_order = st.text_input("Name on Smoothie")

if name_on_order:
    st.write("The name on your Smoothie will be:", name_on_order)


# ---------------------------------------------------------
# Get available fruit options from Snowflake
# ---------------------------------------------------------

my_dataframe = (
    session.table("SMOOTHIES.PUBLIC.FRUIT_OPTIONS")
    .select(col("FRUIT_NAME"))
)

# Convert Snowflake rows into a Python list
fruit_options = [
    row["FRUIT_NAME"]
    for row in my_dataframe.collect()
]


# ---------------------------------------------------------
# Select fruits
# ---------------------------------------------------------

ingredients_list = st.multiselect(
    "Choose up to 5 fruits:",
    fruit_options,
    max_selections=5
)


# ---------------------------------------------------------
# Map Snowflake fruit names to SmoothieFroot API names
# ---------------------------------------------------------

fruit_api_names = {
    "Apples": "apple",
    "Bananas": "banana",
    "Blueberries": "blueberry",
    "Elderberries": "elderberry",
    "Oranges": "orange",
    "Raspberries": "raspberry",
    "Strawberries": "strawberry",
    "Watermelon": "watermelon"
}


# ---------------------------------------------------------
# Get nutritional information for selected fruits
# ---------------------------------------------------------

if ingredients_list:

    st.subheader("Fruit Nutritional Information")

    for fruit_chosen in ingredients_list:

        # Look for the correct API name.
        # If no mapping exists, use the lowercase Snowflake fruit name.
        fruit_for_url = fruit_api_names.get(
            fruit_chosen,
            fruit_chosen.lower()
        )

        try:

            smoothiefroot_response = requests.get(
                f"https://my.smoothiefroot.com/api/fruit/{fruit_for_url}",
                timeout=10
            )

            smoothiefroot_response.raise_for_status()

            fruit_data = smoothiefroot_response.json()

            st.write(f"### {fruit_chosen}")

            st.dataframe(
                [fruit_data],
                use_container_width=True
            )

        except requests.exceptions.RequestException as error:

            st.warning(
                f"Nutrition information could not be retrieved "
                f"for {fruit_chosen}: {error}"
            )

        except ValueError:

            st.warning(
                f"The API did not return valid JSON for {fruit_chosen}."
            )


# ---------------------------------------------------------
# Submit order
# ---------------------------------------------------------

time_to_insert = st.button("Submit Order")


if time_to_insert:

    # Make sure a name was entered
    if not name_on_order.strip():

        st.warning("Please enter a name for the Smoothie.")

    # Make sure at least one fruit was selected
    elif not ingredients_list:

        st.warning("Please choose at least one fruit.")

    else:

        ingredients_string = " ".join(ingredients_list)

        my_insert_stmt = """
            INSERT INTO SMOOTHIES.PUBLIC.ORDERS
                (INGREDIENTS, NAME_ON_ORDER)
            VALUES (?, ?)
        """

        session.sql(
            my_insert_stmt,
            params=[ingredients_string, name_on_order]
        ).collect()

        st.success(
            "Your Smoothie is ordered!",
            icon="✅"
        )
