import streamlit
import pandas
import requests
import snowflake.connector
from urllib.error import URLError

streamlit.title('My Parents New Healthy Diner')

streamlit.header('Breakfast Favorites')
streamlit.text('🥣 Omaga 3 & Blueberry Oatmeal')
streamlit.text('🥗 Kale, Spinach & Rocket Smoothie')
streamlit.text('🐔 Hard-Boiled Free-Range Egg')
streamlit.text('🥑🍞 Avocado Toast')

streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')

# import pandas
my_fruit_list = pandas.read_csv("http://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
# streamlit.dataframe(my_fruit_list)

# pick by fruit name
my_fruit_list = my_fruit_list.set_index('Fruit')

# let's put a pick list here so they can pick the fruit they want to include
streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index))

#display the table on the page
streamlit.dataframe(my_fruit_list)

# #let's put a pick list here so they can pick the fruit they want to include
# streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index),['Avocado','Strawberries'])
                                                                      
# Let's put a pick list here so they can pick the fruit they want to include
fruits_selected = streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index),['Avocado','Strawberries'])
fruits_to_show = my_fruit_list.loc[fruits_selected]

#display the table on the page
streamlit.dataframe(fruits_to_show)



# import requests
#fruityvice_response = requests.get("https://fruityvice.com/api/fruit/watermelon")
#streamlit.text(fruityvice_response)

#streamlit.header("Fruityvice Fruit Advice!")

# import requests
#fruityvice_response = requests.get("https://fruityvice.com/api/fruit/watermelon")
#streamlit.text(fruityvice_response.json()) # just writes the data to the screen

# import requests
# fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + "kiwi")

#take the json version of the response and normalize it
# fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
#output it the screen as a table
# streamlit.dataframe(fruityvice_normalized)

# #new section to dispaly fruityvice api response
# streamlit.header('Fruityvice Fruit Advice!')
# fruit_choice = streamlit.text_input('What fruit would you like information about?','Kiwi')
# streamlit.write('The user entered ', fruit_choice)
# # import requests
# fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + fruit_choice)
# # fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + "kiwi")

# #take the json version of the response and normalize it
# fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
# #output it the screen as a table
# streamlit.dataframe(fruityvice_normalized)

#create the repeatable code block (called a function)
def get_fruityvice_data(this_fruit_choice): #this_fruit_choice It actually is used to pass the value into the function... 
    fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + this_fruit_choice)
    fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
    return fruityvice_normalized

#new section to dispaly fruityvice api response
streamlit.header('Fruityvice Fruit Advice!')
try:
  fruit_choice = streamlit.text_input('What fruit would you like information about?')
  if not fruit_choice:
    streamlit.error("Please select a fruit to get information.")
  else:
    back_from_function = get_fruityvice_data(fruit_choice) #get kiwi go to function, data available for kiwi from the fuction get_fruityvice_data then go to the next to display
    streamlit.dataframe(back_from_function)

except URLError as e:
  streamlit.error()





# my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
# my_cur = my_cnx.cursor()
# my_cur.execute("SELECT * from fruit_load_list")
# my_data_rows = my_cur.fetchall()
# streamlit.header("The fruit load list contains:")
# streamlit.dataframe(my_data_rows)

streamlit.header("The fruit load list contains:")
#snowflake - related functions
def get_fruit_load_list():
    with my_cnx.cursor() as my_cur:
         my_cur.execute("SELECT * from fruit_load_list")
         return my_cur.fetchall()
      
#add a button to load the fruit
if streamlit.button('Get Fruit Load List'):
    my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
    my_data_rows = get_fruit_load_list()
    streamlit.dataframe(my_data_rows)

# # don't run anything past here while we troubleshoot
# streamlit.stop()

# #allow the end user to add a fruit to the list
# add_my_fruit = streamlit.text_input('What fruit would you like to add?','Kiwi')
# streamlit.write('Thanks for adding ', add_my_fruit)


# #this will not work correctly, but just go with it for now
# my_cur.execute("insert into fruit_load_list values ('from streamlit')")

#allow the end user to add a fruit to the list
def insert_row_snowflake(new_fruit):
   with my_cnx.cursor() as my_cur:
        my_cur.execute("insert into fruit_load_list values ('from streamlit')")
        return "Thanks for adding " + new_fruit
      
add_my_fruit = streamlit.text_input('What fruit would you like to add?')
if streamlit.button('Add a Fruit to the List'):
    my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
    back_from_function = insert_row_snowflake(add_my_fruit)
    streamlit.text(back_from_function)

# don't run anything past here while we troubleshoot
streamlit.stop()
#this will not work correctly, but just go with it for now
my_cur.execute("insert into fruit_load_list values ('from streamlit')")
