import streamlit
import pandas
import requests
import snowflake.connector
from urllib.error import URLError


streamlit.title('My Moms New Healthy Diner')

streamlit.header('Breakfast Favorites')
streamlit.text('🥣 Omega 3 & Blueberry Oatmeal')
streamlit.text('🥗 Kale, Spinach & Rocket Smoothie')
streamlit.text('🐔 Hard-Boiled Free-Range Egg')
streamlit.text('🥑🍞 Avocado Toast')

streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')

# import pandas
my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list = my_fruit_list.set_index('Fruit')

# Let's put a pick list here so they can pick the fruit they want to include
fruits_selected = streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index),['Avocado','Strawberries'])
fruits_to_show = my_fruit_list.loc[fruits_selected]

#display the table on the page
streamlit.dataframe(fruits_to_show)

#create the repeatable code block (called a function)
def get_fruityvice_data(this_fruit_choice):
        fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + this_fruit_choice)
        fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
        return fruityvice_normalized

#New Section to display fruityvice api response
streamlit.header('Fruityvice Fruit Advice!')
try:
    fruit_choice = streamlit.text_input('What fruit would you like the information about?')
    if not fruit_choice:
        streamlit.error("Please select a fruit to get information.")
    else:
        back_from_function = get_fruityvice_data(fruit_choice)
        streamlit.dataframe(back_from_function)
#streamlit.write('The user entered', fruit_choice)
# import requests
        #fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + this_fruit_choice)
        #fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
# write your own comment - what does this do?
        #streamlit.dataframe(fruityvice_normalized)

except  URLError as e:
# don't run anything past here while we troubleshoot
    streamlit.error()
# streamlit.stop()

# import snowflake.connector

my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
my_cur = my_cnx.cursor()
my_cur.execute("select * from fruit_load_list") # ("SELECT CURRENT_USER(), CURRENT_ACCOUNT(), CURRENT_REGION()")
my_data_rows = my_cur.fetchall()
# my_data_row = my_cur.fetchone()


streamlit.header("The fruit load list contains:")
#Snowflake-related functions
def get_fruit_load_list():
                with my_cnx.cursor() as my_cur:
                        my_cur.execute("select * from fruit_load_list")
                        return my_cur.fetchall()

# Add a button to load the fruit ***********************************************************************
if streamlit.button('Get Fruit Load List'):
        my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
        my_data_rows = get_fruit_load_list()
        my.cnx.close() 
        streamlit.dataframe(my_data_rows)

# Using a Function and Button to Add the Fruit Name Submissions
# Allow the end user to add a fruit to the list
def insert_row_snowflake(new_fruit):
    with my_cnx.cursor() as my_cur:
             my_cur.execute("insert into fruit_load_list values ('" + new_fruit +"')")  #('from streamlit')")
             return "Thanks for adding " + new_fruit

# Button ***********************************************************************
add_my_fruit = streamlit.text_input('What fruit would you like to add?')
if streamlit.button('Add a Fruit to the List'):
    my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
    back_from_function = insert_row_snowflake(add_my_fruit)
    streamlit.text(back_from_function)

# streamlit.text("The fruit load list contains:")  # ("Hello from Snowflake:")
# streamlit.text(my_data_row)
