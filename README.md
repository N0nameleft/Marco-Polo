# Marco Polo
An akinator-esque website which allows users to pick a country and our program will guess your country by asking you some simple questions.

## How To Start Game
1. Clone this repo to your desired destination:
```
$ git clone https://github.com/N0nameleft/Marco-Polo.git
```

2. Navigate to the top directory:
```
$ cd ./Marco-Polo
```

3. Check if you are running Python ver3.11.3:
```
$ python3 --version
```

4. If Python version is lower than 3.11.3, [ install Python](https://www.python.org/downloads/release/python-3113/)

5. Install python virtual environment:
```
$ pip3 install virtualenv
```

6. Create a python virtual environment named as "venv":
```
$ python3 -m venv venv
```

7. Activate the venv:
```
$ source ./venv/bin/activate
```

8. Install prerequisites:
```
$ python3 -m pip install -r requirements.txt
```

9. Export project:
```
$ export FLASK_APP=app
$ export FLASK_DEBUG=1
```

10. Run the app in local host:
```
flask run
```

To exit:
```
$ ^C
```

To close the environment:
```
$ deactivate
```

After you open the local host link, click Sign up from menu, or simply just click sign up button to register an account.
Once you have an account, log in, and start the game!

Noted that a supported country list is available at the bottom of home page. Our app is still under development, more countries coming soon.


## Required packages

Python 3.11.3  <br/>[Python requirements](./requirements.txt)

## Testing
### Unit test
To run unit test, please ensure [coverage.py](https://coverage.readthedocs.io/en/coverage-5.5/) is installed, it is also included in [requirement.txt](./requirements.txt). 

1. Ensure you are running python virtual environment from the top level of the repo (Marco-Polo)
```
$ python3 -m venv venv
$ source ./venv/bin/activate
```

2. Run the unittest.py using coverage, and read the generate a coverage report.
```
$ coverage run -m test.unittest
$ coverage report -m
```

3. Expected output will be:
```
test_password_hashing (__main__.UserModelCase.test_password_hashing) ... /Users/zach/Desktop/Aus/UWA/CITS3403/Project/Project 2/Marco-Polo/test/unittest.py:15: UserWarning: The 'sha256' password method is deprecated and will be removed in Werkzeug 3.0. Migrate to the 'scrypt' method.
  cur.execute("INSERT INTO user VALUES(1001,'test1@mail.com','%s','Test1')" % generate_password_hash("test1", method="sha256"))
/Users/zach/Desktop/Aus/UWA/CITS3403/Project/Project 2/Marco-Polo/test/unittest.py:16: UserWarning: The 'sha256' password method is deprecated and will be removed in Werkzeug 3.0. Migrate to the 'scrypt' method.
  cur.execute("INSERT INTO user VALUES(1002,'test2@mail.com','%s','Test2')" % generate_password_hash("test2", method="sha256"))
/Users/zach/Desktop/Aus/UWA/CITS3403/Project/Project 2/Marco-Polo/test/unittest.py:44: UserWarning: The 'sha256' password method is deprecated and will be removed in Werkzeug 3.0. Migrate to the 'scrypt' method.
  self.assertFalse(check_password_hash(p1, 'test2'))
/Users/zach/Desktop/Aus/UWA/CITS3403/Project/Project 2/Marco-Polo/test/unittest.py:45: UserWarning: The 'sha256' password method is deprecated and will be removed in Werkzeug 3.0. Migrate to the 'scrypt' method.
  self.assertTrue(check_password_hash(p1, 'test1'))
/Users/zach/Desktop/Aus/UWA/CITS3403/Project/Project 2/Marco-Polo/test/unittest.py:47: UserWarning: The 'sha256' password method is deprecated and will be removed in Werkzeug 3.0. Migrate to the 'scrypt' method.
  self.assertFalse(check_password_hash(p2, 'test1'))
/Users/zach/Desktop/Aus/UWA/CITS3403/Project/Project 2/Marco-Polo/test/unittest.py:48: UserWarning: The 'sha256' password method is deprecated and will be removed in Werkzeug 3.0. Migrate to the 'scrypt' method.
  self.assertTrue(check_password_hash(p2, 'test2'))
ok
test_username (__main__.UserModelCase.test_username) ... ok
test_code_convert (__main__.algoCase.test_code_convert) ... ok
test_finish_message (__main__.algoCase.test_finish_message) ... ok
test_get_country_list (__main__.algoCase.test_get_country_list) ... ok
test_guess (__main__.algoCase.test_guess) ... ok
test_percentage (__main__.algoCase.test_percentage) ... ok
test_question (__main__.algoCase.test_question) ... ok
test_time (__main__.algoCase.test_time) ... ok

----------------------------------------------------------------------
Ran 9 tests in 0.011s

OK
```
Warning is ignored as this app uses 'sha256' to hash users password.

4. Expected coverage report will be 
```
Name                    Stmts   Miss  Cover   Missing
-----------------------------------------------------
app/__init__.py            22      1    95%   27
app/auth.py                41     24    41%   12, 18-29, 34, 40-56, 62-63
app/database.py            86     75    13%   12-13, 17-41, 44-46, 51-72, 77-90, 94-104, 110-126
app/decisionMaking.py     124     26    79%   9-12, 57-62, 72-76, 102, 149, 151, 153, 155, 157, 159, 161, 163, 165, 167, 171
app/main.py                96     69    28%   12, 18, 23-27, 32, 39-59, 67-101, 107-122, 129-141, 147
app/models.py               7      0   100%
test/__init__.py            1      0   100%
test/unittest.py          101      0   100%
-----------------------------------------------------
TOTAL                     478    195    59%

```

Noted that root(main, auth) and database is not tested in the unit test, as it can easily be tested by other methods.

Main focus of this test is desicionMaking.py.

### System test (Selenium test)

## Authors
Thomas Rigby (22973756)<br/>
Xinze Feng (23163302)<br/>
Laurel Chow (23387082)<br/>
Jessica Lovensia Christy (23042584)

## Contribution

## License
See the [ LICENSE ](./LICENSE.txt) file for license rights and limitations (MIT).


