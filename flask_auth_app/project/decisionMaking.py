import sqlite3
import secrets

def get_next_question(cur, table, user_response=None, prev_characteristic=None):
    # Start with an empty WHERE clause
    # where_clause = "1"

    # if user_response is not None and prev_characteristic is not None:
    #     if user_response == "yes":
    #         where_clause += f" AND {prev_characteristic} = 1"
    #     else:  # handle 'no' response
    #         where_clause += f" AND {prev_characteristic} = 0"

    countries = get_all_country(cur, table)
    # If we're down to 3 or fewer countries, start guessing
    # if len(countries) <= 3:
    #     return {
    #         'next_question_text': "I am now guessing your country",
    #         'countries_left': len(countries),
    #         'countries_to_guess': countries,
    #         'next_characteristic': None,
    #     }

    # Pick the next characteristic to ask about
    next_question_text, next_characteristic = getQuestion(cur, table)

    return {
        'next_question_text': next_question_text,
        'next_characteristic': next_characteristic,
        'countries_left': len(countries),
        'countries': countries,
    }

def get_all_country(cur, table):
     # Execute a SQL query to get the current list of possible countries
    q = "SELECT countrycode FROM %s" % table
    cur.execute(q)
    countries = [row[0] for row in cur.fetchall()]
    return countries

def get_country_name(code):
    conn = sqlite3.connect('countries.db')
    cur = conn.cursor()
    query = "SELECT countryname FROM countrycode WHERE countrycode.countrycode = '%s'" % code
    cur.execute(query)
    name = cur.fetchall()[0][0]
    cur.close()
    conn.close()
    return name

def guess_country(cur, table): #3 countries or less left
    # query = "SELECT COUNT(*) FROM %s" % table
    # cur.execute(query)
    # r = secrets.randbelow(cur.fetchone()[0])

    # query = "SELECT countryname FROM countrycode JOIN %s ON countrycode.countrycode = %s.countrycode" % (table, table)
    # cur.execute(query)
    # country = cur.fetchall()[r][0]
    column = getColumnNames(cur, table)
    countries = get_all_country(cur, table)
    random_guess = True
    next_q = ""
    t_q= "SELECT COUNT (*) FROM %s" % table
    cur.execute(t_q)
    coun_left = cur.fetchone()[0]
    if coun_left == 1:
        query = "SELECT countrycode FROM %s" % table
        cur.execute(query)
        code = cur.fetchone()[0]
        name = get_country_name(code)
        Qu = "You are in " + name + "!"
    else:
        for c in column:
            q = "SELECT COUNT(distinct %s) FROM %s WHERE %s = 1" % (c, table, c)
            cur.execute(q)
            count = cur.fetchone()[0]
            if count != 1:
                random_guess = False
                next_q = c
        if random_guess:
            query = "SELECT countrycode FROM %s" % table
            cur.execute(query)
            code = cur.fetchone()[0]
            Qu = "Are you in " + get_country_name(code) + "?"
        else:
            formatQ = next_q.replace("_"," ") + "?"
            Qu = "Is your country " + formatQ
    
    return {
            'next_question_text': Qu,
            'countries_left': len(countries),
            'countries_to_guess': countries,
            'next_characteristic': None,
        }


    # while True:
    #     # ask the user if this is their country
    #     print(f"Are you in {country}? (yes/no)")
        
    #     # get the user's response
    #     user_response = input().strip().lower()

    #     # check if the response is valid
    #     if user_response in ('yes', 'no'):
    #         break
    #     else:
    #         print("Invalid input. Please respond with 'yes' or 'no'.")

    # # if the user said 'yes', return True
    # if user_response == 'yes':
    #     return True
    # # if the user said 'no', return False
    # elif user_response == 'no':
    #     return False
    

def getQuestion(cur, table):
    countQuery = "SELECT COUNT(*) FROM %s" % table
    cur.execute(countQuery)
    rowCount = cur.fetchone()[0]

    if rowCount > 200:
        r = secrets.randbelow(3)
        c = percentage(cur, table, rowCount)[r][0]
    else:
        
        c = percentage(cur, table, rowCount)[0][0]
    formatC = c.replace("_"," ") + "?"
    question = "Is your country " + formatC

    return question, c


def percentage(cur, table, rowCount=217):
    # get column names
    columnNames = getColumnNames(cur, table)
    pList = []
    for c in columnNames:
        count = countOne(cur,table,c)
        p = round(count/rowCount, 4)
        pList.append((c, p))
    sortedP = sorted(pList, key=lambda tup: abs(0.5 - tup[1]), reverse=False)
    print(sortedP)
    return sortedP

def getColumnNames(cur, table):
    query = "SELECT * FROM %s" % table
    cur.execute(query)
    names = [i[0] for i in cur.description[2:]]
    return names

def countOne(cur, table, column):
    query = "SELECT COUNT(*) FROM %s WHERE %s=1" % (table, column)
    cur.execute(query)
    count = cur.fetchone()[0]
    return count


# # define all the characteristics/column names
# characteristics = [
#     'in_oceania', 
#     'in_north_america', 
#     'in_south_america', 
#     'in_caribbean', 
#     'in_atlantic_ocean', 
#     'in_europe_or_mediterranean', 
#     'in_antarctica', 
#     'in_africa', 
#     'in_middle_east', 
#     'in_indian_ocean', 
#     'in_asia', 
#     'with_less_than_100000_people', 
#     'with_more_than_100000_people_but_less_than_1000000', 
#     'with_more_than_1000000_people_but_less_than_10000000', 
#     'with_more_than_10000000_people_but_less_than_100000000', 
#     'with_more_than_100000000_people', 
#     'low_income', 
#     'lower_middle_income', 
#     'upper_middle_income_', 
#     'high_income', 
#     'smaller_than_1000_sq_km', 
#     'greater_than_1000_sq_km_but_smaller_than_100000_sq_km', 
#     'greater_than_100000_sq_km_but_smaller_than_1000000_sq_km', 
#     'greater_than_1000000_sq_km', 
#     'landlocked', 
#     'an_island'
# ]
# characteristic_questions = {
#     'in_oceania': 'Is your country in Oceania?', 
#     'in_north_america': 'Is your country in North America?', 
#     'in_south_america': 'Is your country in South America?', 
#     'in_caribbean': 'Is your country in the Caribbean?', 
#     'in_atlantic_ocean': 'Is your country in the Atlantic Ocean?', 
#     'in_europe_or_mediterranean': 'Is your country in Europe or the Mediterranean?', 
#     'in_antarctica': 'Is your country in Antarctica?', 
#     'in_africa': 'Is your country in Africa?', 
#     'in_middle_east': 'Is your country in the Middle East?', 
#     'in_indian_ocean': 'Is your country in the Indian Ocean?', 
#     'in_asia': 'Is your country in Asia?', 
#     'with_less_than_100000_people': 'Does your country have less than 100,000 people?', 
#     'with_more_than_100000_people_but_less_than_1000000': 'Does your country have more than 100,000 people but less than 1,000,000?', 
#     'with_more_than_1000000_people_but_less_than_10000000': 'Does your country have more than 1,000,000 people but less than 10,000,000?', 
#     'with_more_than_10000000_people_but_less_than_100000000': 'Does your country have more than 10,000,000 people but less than 100,000,000?', 
#     'with_more_than_100000000_people': 'Does your country have more than 100,000,000 people?', 
#     'low_income': 'Is your country considered low income?', 
#     'lower_middle_income': 'Is your country considered lower-middle income?', 
#     'upper_middle_income_': 'Is your country considered upper-middle income?', 
#     'high_income': 'Is your country considered high income?', 
#     'smaller_than_1000_sq_km': 'Is your country smaller than 1000 square kilometers?', 
#     'greater_than_1000_sq_km_but_smaller_than_100000_sq_km': 'Is your country greater than 1000 square kilometers but smaller than 100,000 square kilometers?', 
#     'greater_than_100000_sq_km_but_smaller_than_1000000_sq_km': 'Is your country greater than 100,000 square kilometers but smaller than 1,000,000 square kilometers?', 
#     'greater_than_1000000_sq_km': 'Is your country greater than 1,000,000 square kilometers?', 
#     'landlocked': 'Is your country landlocked?', 
#     'an_island': 'Is your country an island?'
# }

# def get_next_question(user_response=None, prev_characteristic=None):
#     # Connect to the SQLite database
#     conn = sqlite3.connect('countries.db')
#     cur = conn.cursor()

#     # Start with an empty WHERE clause
#     where_clause = "1"

#     if user_response is not None and prev_characteristic is not None:
#         if user_response == "yes":
#             where_clause += f" AND {prev_characteristic} = 1"
#         else:  # handle 'no' response
#             where_clause += f" AND {prev_characteristic} = 0"

#     # Execute a SQL query to get the current list of possible countries
#     cur.execute(f"SELECT countrycode FROM completedata WHERE {where_clause}")
#     rows = cur.fetchall()
#     countries = [row[0] for row in rows]

#     # If we're down to 5 or fewer countries, start guessing
#     if len(countries) <= 5:
#         return {
#             'next_question_text': "I am now guessing your country",
#             'countries_left': len(countries),
#             'countries_to_guess': countries,
#             'next_characteristic': None
#         }

#     # Pick the next characteristic to ask about
#     next_characteristic = characteristics.pop(0)
#     next_question_text = characteristic_questions.get(next_characteristic, 'Unknown question')

#     return {
#         'next_question_text': next_question_text,
#         'next_characteristic': next_characteristic,
#         'countries_left': len(countries),
#         'countries': countries
#     }

# def guess_country(country_code):
#     # convert the country code to a country name
#     country = pycountry.countries.get(alpha_2=country_code.upper())
#     country_name = country.name if country else country_code

#     while True:
#         # ask the user if this is their country
#         print(f"Is your country {country_name}? (yes/no)")
        
#         # get the user's response
#         user_response = input().strip().lower()

#         # check if the response is valid
#         if user_response in ('yes', 'no'):
#             break
#         else:
#             print("Invalid input. Please respond with 'yes' or 'no'.")

#     # if the user said 'yes', return True
#     if user_response == 'yes':
#         return True
#     # if the user said 'no', return False
#     elif user_response == 'no':
#         return False



# # connect to the SQLite database
# conn = sqlite3.connect('countries.db')
# cur = conn.cursor()

# # start with an empty WHERE clause
# where_clause = ""

# # loop over all the characteristics
# for characteristic in characteristics:
#     # ask the user the question related to this characteristic
#     user_response = ask_question(characteristic)
    
#     # update the WHERE clause based on the user's response
#     if user_response:
#         if where_clause:
#             where_clause += " AND "
#         where_clause += f"{characteristic} = 1"

#     # execute a SQL query to get the current list of possible countries
#     cur.execute(f"SELECT countrycode FROM YourTableName WHERE {where_clause}")
#     rows = cur.fetchall()
#     countries = [row[0] for row in rows]

#     # if we're down to 5 or fewer countries, start guessing
#     if len(countries) <= 5:
#         for country in countries:
#             if guess_country(country):
#                 print(f"Your country is {country}!")
#                 return
#         print("I couldn't guess your country. Let's try again.")
#         return

# print("I couldn't guess your country. Let's try again.")

#Below is some code for connecting to the frontned via flask 
# @app.route('/game/next_question', methods=['GET'])
# def next_question():
#     # get the current game state
#     # choose the next question to ask
#     # return the question as JSON


#Description of the Connection 
# User Authentication: Since you already have user authentication set up, you could potentially keep track of each user's progress through the game. 
# This would allow users to stop and resume games. 
# This can be done using sessions or storing game progress in your database.

# Game State: The current state of the game (i.e., which questions have been asked and answered, which countries are still possible, etc.) needs to be stored between requests. 
# You could store this in the user's session, or in the database if you want it to persist across multiple devices or sessions.

# API Endpoints: You'll need at least one API endpoint that the front end can call to get the next question, submit an answer, and get the current guessed country. 
# This might look like this in Flask:
# @app.route('/game/submit_answer', methods=['POST'])
# def submit_answer():
#     # get the answer from the request
#     # update the game state based on the answer
#     # return a success status

# @app.route('/game/current_guess', methods=['GET'])
# def current_guess():
#     # get the current game state
#     # guess a country based on the current state
#     # return the guessed country as JSON
