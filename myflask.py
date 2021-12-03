from flask import Flask, render_template, request
import data_API
import sqlite3
from urllib.parse import unquote
import plotly.graph_objects as go
import tree
import os



app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')  # just the static HTML


@app.route('/handle_form', methods=['POST'])
def handle_the_form():
    country_id = request.form["country_id"]
    sort_type = request.form["sort_type"]
    traversal_type = request.form["traversal_type"]


    # request the API and store the result to database
    processor = data_API.DataProcessor(country_id=country_id)
    processor.generate_database('sqlite3_flask.db')

    # retrieve data from database and get the city result
    conn = sqlite3.connect('sqlite3_flask.db')
    cursor = conn.cursor()

    if(sort_type == 'distance'):
        search_str = 'SELECT country.*, city.distance FROM country, city WHERE country.wikiDateId = city.wikiDateId ORDER BY city.distance ASC;'
    else:
        search_str = 'SELECT country.*, city.distance FROM country, city WHERE country.wikiDateId = city.wikiDateId'

    cursor.execute(search_str)
    city_list = cursor.fetchall()  # a list

    # Build a tree based on the the sort_type and traversal it based on traversal_type
    name_list = [city[1] for city in city_list]
    if (sort_type =='distance'):
        data_list = [city[5] for city in city_list]
    else:
        data_list = [city[4] for city in city_list]

    root = tree.sortedArrayToBST(name_list, data_list)

    if(traversal_type == 'PreOrder'):
        traver_result = tree.preOrder(root)
    elif(traversal_type == 'PostOrder'):
        traver_result = tree.postOrder(root)
    else:
        traver_result = tree.midOrder(root)

    tree_string = tree.printTree(root)

    # save tree to json file
    tree_filePath = 'tree.json'
    if os.path.exists(tree_filePath):
        os.remove(tree_filePath)
    else:
        treeFile = open(tree_filePath, "w")
        tree.saveTree(root, treeFile)
        treeFile.close()


    # plotly a figure population
    x_vals = []
    y_vals = []
    for city in city_list:
        x_vals.append(city[1])
        y_vals.append(city[4])
    bars_data = go.Bar(x = x_vals,y = y_vals)
    fig = go.Figure(data = bars_data)
    div1 = fig.to_html(full_html = False)

    # plotly a figure distance
    x_vals = []
    y_vals = []
    for city in city_list:
        x_vals.append(city[1])
        y_vals.append(city[5])
    bars_data = go.Bar(x=x_vals, y=y_vals)
    fig = go.Figure(data=bars_data)
    div2 = fig.to_html(full_html=False)


    return render_template('result.html',
                           country_id=country_id,
                           city_list = city_list,
                           traver_result = traver_result,
                           tree_string = tree_string,
                           plot_div_population = div1,
                           plot_div_distance = div2)

@app.route('/<nm>')
def show_twitter(nm):
    nm = unquote(nm)
    print(nm)
    conn = sqlite3.connect('sqlite3_flask.db')
    cursor = conn.cursor()
    search_str = 'SELECT twitter.city_name,twitter.tweets FROM twitter WHERE twitter.city_name = ?'
    cursor.execute(search_str,(nm,))
    twitter_list = cursor.fetchall()  # a list
    return render_template('twitter.html',nm = nm,twitter_list = twitter_list)  # just the static HTML


if __name__ == "__main__":
    app.run(debug=True)