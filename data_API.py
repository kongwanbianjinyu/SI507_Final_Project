import requests
from utilities import *
from mysecrets import *
import sqlite3
import time
import os
from tabulate import tabulate
import pandas as pd

class DataProcessor():
    def __init__(self,country_id):
        self.country_id = country_id


    def get_country_data(self, cache_filename = "country_cache.json"):
        '''

        :param country_id: "US"/"CN"
        :return: dictionary of cities in this country more than 1000000 people. {[],[],[],[],[]}
        '''

        url = "https://wft-geo-db.p.rapidapi.com/v1/geo/cities"


        querystring = {"countryIds": self.country_id, "sort": "-population"}#"minPopulation": "1000000"

        headers = {
            'x-rapidapi-host': "wft-geo-db.p.rapidapi.com",
            'x-rapidapi-key': COUNTRY_KEY
        }
        cache = open_cache(cache_filename)
        unique_key = construct_unique_key(url, querystring)
        output_dict = {}
        if unique_key in cache:
            print("fetching from cache...")
            response = cache[unique_key]
            output_dict = response['data']
        else:
            print("making new request...")

            response = requests.request("GET", url, headers=headers, params=querystring).json()

            print(response)
            if('data' in response.keys()):
                cache[unique_key] = response
                save_cache(cache, cache_filename)
                output_dict = response['data']
            else:
                output_dict = {}

        return output_dict

    def get_city_data(self, city_wikiDataId, cache_filename = "city_cache.json"):
        '''

        :param city_wikiDataId: e.g."Q104994" id represent for Los Angeles
        :return: city_distance Get the distance from Ann Arbor to target city.
        '''

        url = f"https://wft-geo-db.p.rapidapi.com/v1/geo/cities/{city_wikiDataId}/distance"


        headers = {
            'x-rapidapi-host': "wft-geo-db.p.rapidapi.com",
            'x-rapidapi-key': CITY_KEY
        }
        querystring = {"fromCityId": "Q485172"}

        cache = open_cache(cache_filename)
        unique_key = construct_unique_key(url, querystring)
        output_dict = {}
        if unique_key in cache:
            print("fetching from cache...")
            response = cache[unique_key]
        else:
            print("making new request...")
            time.sleep(1.5)
            response = requests.request("GET", url, headers=headers, params=querystring).json()

            print(response)
            cache[unique_key] = response
            save_cache(cache, cache_filename)

        output_dict['wikiDataId'] = city_wikiDataId
        output_dict['distance'] = response['data']
        return output_dict

    def bearer_oauth(self,r):
        """
        Method required by bearer token authentication.
        """

        r.headers["Authorization"] = f"Bearer {TWITTER_ACCESS_BEARER_TOKEN}"
        r.headers["User-Agent"] = "v2RecentSearchPython"
        return r

    def get_twitter_data(self, city_name, cache_filename = "twitter_cache.json"):
        '''

        :param city_name: cities' name
        :param cache_filename: cache_file of twitter
        :return: list of tweets related to the city. Should not use cache, since the recent twitter is updated in real time.
        '''

        bearer_token = TWITTER_ACCESS_BEARER_TOKEN
        url = "https://api.twitter.com/2/tweets/search/recent"
        querystring = {'query': f'#{city_name}'}

        #cache = open_cache(cache_filename)
        #unique_key = construct_unique_key(url, querystring)
        output_dict = {}
        # if unique_key in cache:
        #     print("fetching from cache...")
        #     response = cache[unique_key]
        #     output_dict = response['data']
        # else:
        print("making new request...")
        response = requests.get(url, auth=self.bearer_oauth, params=querystring).json()
        print(response)
        if ('data' in response.keys()):
            #cache[unique_key] = response
            #save_cache(cache, cache_filename)
            output_dict = response['data']
        else:
            output_dict = {}

        return output_dict

    def generate_database(self, database_name):

        if os.path.exists(database_name):
            os.remove(database_name)
        conn = sqlite3.connect(database_name)
        cursor = conn.cursor()

        # country table
        print('generating country table')
        cursor.execute('create table country (wikiDateId varchar(50) primary key, name varchar(20), latitude REAL, longitude REAL, population INT)')
        cities_information = self.get_country_data()
        if cities_information:
            for city in cities_information:
                insert_str = 'insert into country (wikiDateId, name, latitude, longitude, population) values (?,?,?,?,?)'
                cursor.execute(insert_str,[city["wikiDataId"], city["name"] ,city["latitude"], city["longitude"], city["population"]])
                # print(cursor.rowcount)
                # print(city)

        # city table
        print('generating city table')
        cursor.execute('create table city (wikiDateId varchar(50) primary key, name varchar(20), distance REAL)')
        if cities_information:
            for city in cities_information:

                distance = self.get_city_data(city["wikiDataId"])['distance']
                insert_str = 'insert into city (wikiDateId, name, distance) values (?,?,?)'
                cursor.execute(insert_str,[city["wikiDataId"], city["name"],distance])

        # twitter table
        print('generating twitter table')
        cursor.execute('create table twitter (twitterId varchar(50) primary key, wikiDateId varchar(20), city_name varchar(20) , tweets TEXT)')
        if cities_information:
            for city in cities_information:
                print(city)
                city_name = city['name']
                print(city_name)
                if(city_name.split()[-1] in ['City', 'County','Shi','Community','Region']):
                    new_city_name = ' '.join(city['name'].split()[:-1])
                else:
                    new_city_name = city['name']
                print('looking up for tweets of ',new_city_name)
                tweets = self.get_twitter_data(new_city_name)
                if tweets:
                    for tweet in tweets:
                        insert_str = 'insert into twitter (twitterId, wikiDateId, city_name, tweets) values (?,?,?,?)'
                        cursor.execute(insert_str, [tweet['id']+city["wikiDataId"], city["wikiDataId"], city["name"], tweet['text']])
        # close
        cursor.close()
        conn.commit()
        conn.close()
        print('Successfully generated database: ',database_name)

if __name__ == '__main__':
    processor = DataProcessor(country_id="CN")
    processor.generate_database('sqlite3_1.db')


    # output_dict = get_country_data(country_id="US", cache_filename = "country_cache.json")
    # print(output_dict)

    # output_dict = get_city_data(city_wikiDataId = "Q104994", cache_filename = "city_cache.json") #
    # print(output_dict)

    # output_dict = get_twitter_data('Ann Arbor', cache_filename = "twitter_cache.json") #
    # print(output_dict)

    # conn = sqlite3.connect('test1.db')
    # cursor = conn.cursor()
    #
    # cursor.execute('create table country (wikiDateId varchar(20) primary key, name varchar(20), latitude REAL, longitude REAL, population INT)')
    # for country in output_dict:
    #     insert_str = 'insert into country (wikiDateId, name, latitude, longitude, population) values (?,?,?,?,?)'
    #     cursor.execute(insert_str,[country["wikiDataId"], country["name"] ,country["latitude"], country["longitude"], country["population"]])
    #     #print(cursor.rowcount)
    #
    # cursor.close()
    # conn.commit()
    # conn.close()

    conn = sqlite3.connect('sqlite3_1.db')
    cursor = conn.cursor()

    cursor.execute('select * from country')
    values = cursor.fetchall() # a list
    df = pd.DataFrame(values)
    print(tabulate(df, tablefmt='psql', showindex='False'))

    cursor.execute('select * from city')
    values = cursor.fetchall() # a list
    df = pd.DataFrame(values)
    print(tabulate(df, tablefmt='psql', showindex='False'))

    cursor.execute('select * from twitter')
    values = cursor.fetchall() # a list
    df = pd.DataFrame(values)
    print(tabulate(df, tablefmt='psql', showindex='False'))

    cursor.close()
    conn.close()


