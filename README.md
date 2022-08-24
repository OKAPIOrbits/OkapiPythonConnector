# OkapiPythonConnector
Some routines to connect OKAPI:Orbits software with python.

## Dependencies:
* python 3.8+
* requests
* python-dotenv

## Installation walk-through

1. Clone connector

> git clone https://github.com/OKAPIOrbits/OkapiPythonConnector.git python-connector-git<br>
> cd python-connector-git

2. Python environment 

2.1 Linux/WSL

> sudo apt install python3-pytest<br>
> sudo apt-get --assume-yes install python3.8 python3.8-dev python3-pip<br>
> python3.8 -m pip install python-dotenv

2.2 Windows

Install Python3.8 e.g. from Windows Store. Next, install required packages:<br>
> python3.8.exe -m pip install -r requirements.txt

3. Running an example

See `tryout.py` for example calls. To get started create a `.env` file and add your username and password:
```buildoutcfg
OKAPI_TEST_URL=https://api.okapiorbits.com/
OKAPI_TEST_USERNAME=your_username
OKAPI_TEST_PASSWORD=your_password
```
Make sure that the username and password itentifiers are identical to those used in the python script.

Execute script:
> python3.8 -m pytest

# Creating an account
Contact us at contact@okapiorbits.com

For more information, go to https://www.okapiorbits.space/documentation

Checkout the API at https://okapiorbits.space/api-redoc/
