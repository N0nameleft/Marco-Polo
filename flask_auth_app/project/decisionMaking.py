import sqlite3

# define all the characteristics/column names
characteristics = [
    'in_oceania', 
    'in_north_america', 
    'in_south_america', 
    'in_caribbean', 
    'in_atlantic_ocean', 
    'in_europe_or_mediterranean', 
    'in_antarctica', 
    'in_africa', 
    'in_middle_east', 
    'in_indian_ocean', 
    'in_asia', 
    'with_less_than_100000_people', 
    'with_more_than_100000_people_but_less_than_1000000', 
    'with_more_than_1000000_people_but_less_than_10000000', 
    'with_more_than_10000000_people_but_less_than_100000000', 
    'with_more_than_100000000_people', 
    'low_income', 
    'lower_middle_income', 
    'upper_middle_income_', 
    'high_income', 
    'smaller_than_1000_sq_km', 
    'greater_than_1000_sq_km_but_smaller_than_100000_sq_km', 
    'greater_than_100000_sq_km_but_smaller_than_1000000_sq_km', 
    'greater_than_1000000_sq_km', 
    'landlocked', 
    'an_island'
]

def ask_question(characteristic):
    # replace this with your own function to ask the user a question
    # this function should return True or False based on the user's answer
    return user_response

def guess_country(countries):
    # replace this with your own function to guess a country
    # this function should take a list of countries as input
    # it should select one country and ask the user if that's their country
    # if the user says yes, it should return True. Otherwise, it should return False.
    return guess_response

# connect to the SQLite database
conn = sqlite3.connect('countries.db')
cur = conn.cursor()

# start with an empty WHERE clause
where_clause = ""

# loop over all the characteristics
for characteristic in characteristics:
    # ask the user the question related to this characteristic
    user_response = ask_question(characteristic)
    
    # update the WHERE clause based on the user's response
    if user_response:
        if where_clause:
            where_clause += " AND "
        where_clause += f"{characteristic} = 1"

    # execute a SQL query to get the current list of possible countries
    cur.execute(f"SELECT countrycode FROM YourTableName WHERE {where_clause}")
    rows = cur.fetchall()
    countries = [row[0] for row in rows]

    # if we're down to 5 or fewer countries, start guessing
    if len(countries) <= 5:
        for country in countries:
            if guess_country(country):
                print(f"Your country is {country}!")
                return
        print("I couldn't guess your country. Let's try again.")
        return

print("I couldn't guess your country. Let's try again.")

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
