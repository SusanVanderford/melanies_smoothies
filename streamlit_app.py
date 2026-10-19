# Import Python packages
import streamlit as st
import pandas as pd
import requests

from urllib.parse import quote
from snowflake.snowpark.functions import col


# ---------------------------------------------------------
# Page heading
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
# Get fruit options from Snowflake
# ---------------------------------------------------------

# Get fruit options from Snowflake
my_dataframe = (
    session.table("SMOOTHIES.PUBLIC.FRUIT_OPTIONS")
    .select(
        col("FRUIT_NAME"),
        col("SEARCH_ON")
    )
    .sort(col("FRUIT_NAME"))
)

# Convert the Snowpark dataframe to a Pandas dataframe
pd_df = my_dataframe.to_pandas()


# Create the list of fruit names for the multiselect
fruit_options = pd_df["FRUIT_NAME"].tolist()


# Multiselect
ingredients_list = st.multiselect(
    "Choose up to 5 fruits:",
    fruit_options,
    max_selections=5
)


# Get nutritional information for selected fruits
if ingredients_list:

    for fruit_chosen in ingredients_list:

        # Find SEARCH_ON value in the Pandas dataframe
        search_on = pd_df.loc[
            pd_df["FRUIT_NAME"] == fruit_chosen,
            "SEARCH_ON"
        ].iloc[0]

        st.write(
            "The search value for ",
            fruit_chosen,
            " is ",
            search_on,
            "."
        )

        try:
            smoothiefroot_response = requests.get(
                f"https://my.smoothiefroot.com/api/fruit/{search_on}",
                timeout=10
            )

            smoothiefroot_response.raise_for_status()

            fruit_data = smoothiefroot_response.json()

            nutrition = fruit_data.get("nutritions", {})

            nutrition_data = [
                {
                    "Nutrient": "Carbs",
                    "Family": fruit_data.get("family"),
                    "Genus": fruit_data.get("genus"),
                    "ID": fruit_data.get("id"),
                    "Name": fruit_data.get("name"),
                    "Nutrition": nutrition.get("carbohydrates"),
                    "Order": fruit_data.get("order")
                },
                {
                    "Nutrient": "Fat",
                    "Family": fruit_data.get("family"),
                    "Genus": fruit_data.get("genus"),
                    "ID": fruit_data.get("id"),
                    "Name": fruit_data.get("name"),
                    "Nutrition": nutrition.get("fat"),
                    "Order": fruit_data.get("order")
                },
                {
                    "Nutrient": "Protein",
                    "Family": fruit_data.get("family"),
                    "Genus": fruit_data.get("genus"),
                    "ID": fruit_data.get("id"),
                    "Name": fruit_data.get("name"),
                    "Nutrition": nutrition.get("protein"),
                    "Order": fruit_data.get("order")
                },
                {
                    "Nutrient": "Sugar",
                    "Family": fruit_data.get("family"),
                    "Genus": fruit_data.get("genus"),
                    "ID": fruit_data.get("id"),
                    "Name": fruit_data.get("name"),
                    "Nutrition": nutrition.get("sugar"),
                    "Order": fruit_data.get("order")
                }
            ]

            st.subheader(
                f"{fruit_chosen} Nutritional Information"
            )

            st.dataframe(
                nutrition_data,
                use_container_width=True,
                hide_index=True,
                column_order=[
                    "Nutrient",
                    "Family",
                    "Genus",
                    "ID",
                    "Name",
                    "Nutrition",
                    "Order"
                ]
            )

        except requests.exceptions.RequestException as error:

            st.warning(
                f"Nutrition information could not be retrieved "
                f"for {fruit_chosen}: {error}"
            )


# ---------------------------------------------------------
# Select fruits
# ---------------------------------------------------------

ingredients_list = st.multiselect(
    "Choose up to 5 fruits:",
    fruit_options,
    max_selections=5
)


# ---------------------------------------------------------
# Display nutritional information
# ---------------------------------------------------------

if ingredients_list:

    for fruit_chosen in ingredients_list:

        # Retrieve SEARCH_ON using the selected FRUIT_NAME
        search_on = fruit_search_lookup.get(fruit_chosen)

        if not search_on:

            st.warning(
                f"No SEARCH_ON value has been configured for "
                f"{fruit_chosen}."
            )

            # Skip this fruit and continue to the next selection
            continue


        # Make the SEARCH_ON value safe for use in the URL
        fruit_for_url = quote(
            str(search_on).strip().lower(),
            safe=""
        )


        try:

            smoothiefroot_response = requests.get(
                f"https://my.smoothiefroot.com/api/fruit/{fruit_for_url}",
                timeout=10
            )

            smoothiefroot_response.raise_for_status()

            fruit_data = smoothiefroot_response.json()


            # Get the nested nutrition information
            nutrition = fruit_data.get("nutritions", {})


            # Build a separate set of rows for this fruit
            nutrition_data = [
                {
                    "Nutrient": "Carbs",
                    "Family": fruit_data.get("family"),
                    "Genus": fruit_data.get("genus"),
                    "ID": fruit_data.get("id"),
                    "Name": fruit_data.get("name"),
                    "Nutrition": nutrition.get("carbohydrates"),
                    "Order": fruit_data.get("order")
                },
                {
                    "Nutrient": "Fat",
                    "Family": fruit_data.get("family"),
                    "Genus": fruit_data.get("genus"),
                    "ID": fruit_data.get("id"),
                    "Name": fruit_data.get("name"),
                    "Nutrition": nutrition.get("fat"),
                    "Order": fruit_data.get("order")
                },
                {
                    "Nutrient": "Protein",
                    "Family": fruit_data.get("family"),
                    "Genus": fruit_data.get("genus"),
                    "ID": fruit_data.get("id"),
                    "Name": fruit_data.get("name"),
                    "Nutrition": nutrition.get("protein"),
                    "Order": fruit_data.get("order")
                },
                {
                    "Nutrient": "Sugar",
                    "Family": fruit_data.get("family"),
                    "Genus": fruit_data.get("genus"),
                    "ID": fruit_data.get("id"),
                    "Name": fruit_data.get("name"),
                    "Nutrition": nutrition.get("sugar"),
                    "Order": fruit_data.get("order")
                }
            ]


            # Display a heading and table for this fruit
            st.subheader(
                f"{fruit_chosen} Nutritional Information"
            )

            st.dataframe(
                nutrition_data,
                use_container_width=True,
                hide_index=True,
                column_order=[
                    "Nutrient",
                    "Family",
                    "Genus",
                    "ID",
                    "Name",
                    "Nutrition",
                    "Order"
                ]
            )


        except requests.exceptions.HTTPError:

            st.warning(
                f"Nutrition information was not found for "
                f"{fruit_chosen}. SEARCH_ON is currently "
                f"set to '{search_on}'."
            )


        except requests.exceptions.RequestException as error:

            st.warning(
                f"Nutrition information could not be retrieved "
                f"for {fruit_chosen}: {error}"
            )


        except ValueError:

            st.warning(
                f"The API did not return valid JSON for "
                f"{fruit_chosen}."
            )


# ---------------------------------------------------------
# Submit the smoothie order
# ---------------------------------------------------------

time_to_insert = st.button("Submit Order")


if time_to_insert:

    # Validate name
    if not name_on_order.strip():

        st.warning("Please enter a name for the Smoothie.")


    # Validate fruit selection
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
            params=[
                ingredients_string,
                name_on_order.strip()
            ]
        ).collect()

        st.success(
            "Your Smoothie is ordered!",
            icon="✅"
        )
