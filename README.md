# Programmable-Web-2019
REST API project repository for the course Programmable Web Summer Course 2019

# Overview

A Python program to make a database to track users spending.
User can manage database with Flask API.

### What you can do:

- Create different users

- Create a wallet for the user and add money to it!

- Add money to different spending categories in your wallet to follow your spending habits

# Project

**Project title**
Spending Tracker

**Authors**
Markus H


# Installation

### Project requires: 

- Python 3.x for pip installation

### Make virtual environment

#### Windows

```
$ python -m pip venv tracker_venv
```

#### Linux

```
$ virtualenv tracker_venv
```


### Install project from git

#### Windows

```
$ python -m pip install git+https://github.com/Ruutimies/programmable-web-2019.git
```

#### Linux

```
$ pip install git+https://github.com/Ruutimies/programmable-web-2019.git
```

# Running the Spending Tracker

```
$ tracker --help
```

Run Flake8 to check errors

```
python setup.py flake8
```

Run tests

To run tests you need to clone the repo.

```
python setup.py test
```
DeprecationWarnings are suppressed at the moment. Still in works how to ignore 3rd party modules.




