# Import python packages

import streamlit as st

import os

from snowflake.snowpark.functions import col, when_matched

 

# Write directly to the app

st.title(f"Customize Your Smoothie: {st.__version__}")

st.write(

  """Replace this example with your own code!

  **And if you're new to Streamlit,** check

  out our easy-to-follow guides at

  [docs.streamlit.io](https://docs.streamlit.io).

  """

)

 

st.markdown("""

- :page_with_curl: [Streamlit open source documentation](https://docs.streamlit.io)

- :snowflake: [Streamlit in Snowflake documentation](https://docs.snowflake.com/en/developer-guide/streamlit/about-streamlit)

- :books: [Demo repo with templates](https://github.com/Snowflake-Labs/snowflake-demo-streamlit)

- :memo: [Streamlit in Snowflake release notes](https://docs.snowflake.com/en/release-notes/streamlit-in-snowflake)

""")

 

# Create a database connection to Snowflake

conn = st.connection("snowflake", ttl=os.getenv("SNOWFLAKE_CONNECTION_TTL"))

session = conn.session()

 

 

my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))

st.dataframe(data=my_dataframe, use_container_width=True)

 

name_on_order = st.text_input('Name on Smoothie')

st.write('The name on the smoothie will be', name_on_order)

 

ingredients_list = st.multiselect(

    'Choose up to 5 ingredients:',

    my_dataframe,

    max_selections = 5

)

if ingredients_list:

 

    ingredients_string = ''

    for fruits_chosen in ingredients_list:

        ingredients_string += fruits_chosen + ' '

 

    st.write(ingredients_string)

 

    my_insert_stmt = """

    INSERT INTO smoothies.public.orders(ingredients, name_on_order)

    VALUES ('""" + ingredients_string + """','""" + name_on_order + """')

"""

 


    st.write(my_insert_stmt)

    time_to_insert = st.button('Submit Order')

   

    if time_to_insert:

        session.sql(my_insert_stmt).collect()

        st.success('Your Smoothie is ordered, ' + name_on_order + '!', icon="✅")
