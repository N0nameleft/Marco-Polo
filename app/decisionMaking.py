# this is the file contain all the function related to guessing which country user is in
import sqlite3
import secrets

# takes cursor and table name as parameter
# get the list of countries left to return
# get what to ask for next question and return
def get_next_question(cur, table):
    countries = get_all_country(cur, table)
    next_question_text, next_characteristic = getQuestion(cur, table)

    return {
        'next_question_text': next_question_text,
        'next_characteristic': next_characteristic,
        'countries': countries,
    }

# takes cursor and table as parameter
# return a list contain all the countrycode in the conn that cursor is pointing to
# return the list
def get_all_country(cur, table):
     # Execute a SQL query to get the current list of possible countries
    q = "SELECT countrycode FROM %s" % table
    cur.execute(q)
    countries = [row[0] for row in cur.fetchall()]
    return countries

# takes the 3 letter country code 
# read from the completedata table
# use code to get name from countrycode table which is in countries.db
# and return the converted country name for the given code
def get_country_name(code):
    conn = sqlite3.connect('./data/countries.db')
    cur = conn.cursor()
    query = "SELECT countryname FROM countrycode WHERE countrycode.countrycode = '%s'" % code
    cur.execute(query)
    name = cur.fetchall()[0][0]
    cur.close()
    conn.close()
    return name

# takes cursor and table as parameter
# get how many country is left
# if only one country left in table, or there is no characteristic left and will ask if user is in that country/ the first country
# else, it will check if all column only have one "1", if not then its not going to random guess, it will ask the question with more than one country have 1 as value
# if random guess, it will ask the first country returned by sqlite query
def guess_country(cur, table): 
    column = getColumnNames(cur, table)
    countries = get_all_country(cur, table)
    random_guess = True
    next_q = ""
    t_q= "SELECT COUNT (*) FROM %s" % table
    cur.execute(t_q)
    coun_left = cur.fetchone()[0]

    if coun_left == 1 or len(column) == 0:
        query = "SELECT countrycode FROM %s" % table
        cur.execute(query)
        code = cur.fetchone()[0]
        name = get_country_name(code)
        Qu = "Are you in " + name + "?"
        Ch = None
    else:
        for c in column:
            q = "SELECT COUNT(distinct %s) FROM %s WHERE %s = 1" % (c, table, c)
            cur.execute(q)
            count = cur.fetchone()[0]
            if count >= 1:
                random_guess = False
                next_q = c
        if random_guess:
            query = "SELECT countrycode FROM %s" % table
            cur.execute(query)
            code = cur.fetchone()[0]
            Qu = "Are you in " + get_country_name(code) + "?"
            Ch = None
        else:
            formatQ = next_q.replace("_"," ")
            Qu = "Is your country " + formatQ + "?"
            Ch = next_q
    
    return {
            'next_question_text': Qu,
            'countries_to_guess': countries,
            'next_characteristic': Ch,
        }

# takes cursor and table as parameter
# get how many row is left
# if row count greater than 200, it will randomise from the first 3 country
# if lower than 200, it will ask the first question returned by percentage
# finally it will format the column name and return it and the original column name
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

# takes cursor, table, and rowcount as parameter
# get all column names in table
# iterate thru column names, count how many country have 1 as value
# divided by row count, and round to 4 decimal places
# add column name, percentage to the list
# sort the list by which percentage is closest to 0.5
# return the sorted list
def percentage(cur, table, rowCount):
    # get column names
    columnNames = getColumnNames(cur, table)
    pList = []
    for c in columnNames:
        count = countOne(cur,table,c)
        p = round(count/rowCount, 4)
        pList.append((c, p))
    sortedP = sorted(pList, key=lambda tup: abs(0.5 - tup[1]), reverse=False)
    return sortedP

# grab all column names from description and return it
def getColumnNames(cur, table):
    query = "SELECT * FROM %s" % table
    cur.execute(query)
    names = [i[0] for i in cur.description[2:]]
    return names

# count how many country have 1 as value in the given column, given table
def countOne(cur, table, column):
    query = "SELECT COUNT(*) FROM %s WHERE %s=1" % (table, column)
    cur.execute(query)
    count = cur.fetchone()[0]
    return count

# convert number 01,02...12, to Jan, Feb...Dec and return it
def format_time(time):
    s = str(time)
    year = s[:4]
    date = s[6:8]
    m = s[4:6]
    if m == '01':
        month = 'Jan'
    elif m == '02':
        month = 'Feb'
    elif m == '03':
        month = 'Mar'
    elif m == '04':
        month = 'Apr'
    elif m == '05':
        month = 'May'
    elif m == '06':
        month = 'Jun'
    elif m == '07':
        month = 'Jul'
    elif m == '08':
        month = 'Aug'
    elif m == '09':
        month = 'Sep'
    elif m == '10':
        month = 'Oct'
    elif m == '11':
        month = 'Nov'
    elif m == '12':
        month = 'Dec'
    else:
        month = m
    hour = s[8:10]
    min = s[10:12]
    sec = s[-2:]
    time = "%s %s %s, %s:%s:%s" % (date, month, year, hour, min,  sec)
    return time

# return win/lose message after "are you in ...." asked and user has answered
def game_finish(answer):
    message = ""
    if answer == "yes":
        message = "Found ya! Do you want to start a new game?"
    if answer == "no":
        message = "You win! Sorry I can't find you.\nDo you want to start a new game?"

    return {
        'next_question_text': message,
        'countries_to_guess': None,
        'next_characteristic': None,
    }
