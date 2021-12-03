# SI507_Final_Project

This is my final project for SI 507 at University of Michigan. This project can search the top 5 cities in population in the selected country and get real-time Twitter related to the cities. The user would select a country they are interested in and choose the sort types. Then you would get a table containing the information about the cities, including WikiData Id, Latitude, Longitude, Population, and Distance from Ann Arbor. You can choose to sort the table
by population or by the distance from Ann Arbor.

## Requisite Packages

This project requires requests, tabulate, pandas, sqlite3, urllib, flask, plotly (please use requirements.txt for installation)

```
pip install -r requirements.txt
```

## Supplying API Keys
Please create a "mysecrets.py" file at the root level of the project (at same level of myflask.py), and supply your API keys in it. You can copy the following code and fill in your keys. For GeoDB Cities API, please refer to https://rapidapi.com/wirefreethought/api/geodb-cities/. For Twitter API, please refer to https://developer.twitter.com/en.
```
# key of GeoDB Cities API
COUNTRY_KEY = ""
CITY_KEY = ""

# key of Twitter API
TWITTER_API_KEY = ""
TWITTER_API_SECRET = ""
TWITTER_ACCESS_TOKEN = ""
TWITTER_ACCESS_TOKEN_SECRET = ""
TWITTER_ACCESS_BEARER_TOKEN = ""
```
## How to use
After supplying API keys, please run "myflask.py" file. You'll see the server is up; click on the localhost http://127.0.0.1:5000/ to view the index page. There you can select a country you interested and find the top 5 cities in population in this country. You can choose sort the cities by their population or by the distance from Ann Arbor. 
A tree structure of the cities would be shown to you and you can choose to traversal the tree by pre-order, mid-order and post-order. After selecting all options, you hit search and you'll see all information in a table. There is a link attached to each city, by clicking it you can get the recent twitter related to the city. Note you can easily return back by clicking on top left "Michigan" icon.

## Data Structure
I build a Balanced Binary Search Tree (BST) for the cities and countries based on their population and have that be part of my selection in tree.py. You can choose to see the traversal result of tree in three different ways, including pre-order, mid-order and post-order traversal. I also provide the printTree method which can print out the tree in string. After getting the tree, you can choose to save the tree in the json file. The format of the json file is as follows. An internal node starts with the line "Internal Node" or "Leaf". There is the city name after the line. You can load the tree using loadTree.py.


