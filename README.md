# Marco Polo
An akinator-esque website which allows users to pick a country and our program will guess your country by asking you some simple questions.

## How To Start Game
1. Clone this repo to your desired destination:
```
$ git clone https://github.com/N0nameleft/Marco-Polo.git
```

2. Navigate to the top directory:
```$ cd ./Marco-Polo```

3. Check if you are running Python ver3.11.3:
```$ python3 --version```

3. Navigate to the project directory:
```$ cd ./application```

4. If Python version is lower than 3.11.3, [ install Python](https://www.python.org/downloads/release/python-3113/)

5. Install python virtual environment:
```$ pip3 install virtualenv```

6. Create a python virtual environment named as "venv":
```$ python3 -m venv venv```

7. Activate the venv:
```$ source ./venv/bin/activate```

8. Install prerequisites:
```$ python3 -m pip install -r requirements.txt```

9. Export project:
```$ export FLASK_APP=project```
```$ export FLASK_DEBUG=1```

10. Run the app in local host:
```$ flask run```

To exit:
```$ ^C```

To close the environment:
```$ deactivate```

After you open the local host link, click Sign up from menu, or simply just click sign up button to register an account.
Once you have an account, log in, and start the game!

Noted that a supported country list is available at the bottom of home page. Our app is still under development, more countries coming soon.


## Required packages

Python 3.11.3  <br/>[Python requirements](./application/requirements.txt)

## Testing

## Authors
Thomas Rigby (22973756)
Xinze Feng (23163302)
Laurel Chow (23387082)
Jessica Lovensia Christy (23042584)

## Contribution

## License
See the [ LICENSE ](./LICENSE.txt) file for license rights and limitations (MIT).


