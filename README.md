# Brawlclub

This repository contains the source code of the Brawlclub.app website.

This web app allows you to find clubs that match your criteria in Brawl Stars, a Supercell game.
It also shows you statistics about yourself or clubs!

## Table of content
* [Requirements](#Requirements)
* [Django setup](#Django-setup)
* [React setup](#react-setup)
* [Running tests](#tests)

## Requirements 
Please install all these:
- [Python](https://www.python.org/downloads/) > = 3.8
- [Git](https://git-scm.com/downloads)
- [Redis](https://redis.io/download/)
- [PostgreSQL](https://www.postgresql.org/download/)
- [Node Package Manager](https://docs.npmjs.com/downloading-and-installing-node-js-and-npm)
- [React JS](https://reactjs.org/tutorial/tutorial.html#setup-option-2-local-development-environment)

## Django setup

### 1. Change current directory to be where you want the project to be
    cd <future project folder> 
 
### 2. Clone the github project
    git clone git@github.com:Shriukan33/OC-P13-BrawlClub.git

### 3. Get into the project's folder
    cd OC-P13-BrawlClub

### 4. Create a virtual environment (recommended)
    python -m venv venv

### 5. Activate your virtual environment (if you went through step 4)
#### Windows
    venv/Scripts/activate
#### Linux / MacOS
    . venv/bin/activate

### 6. Install project's dependencies
    pip install -r requirements.txt

### 7. Set proper env variable in .env files
There are two environment variables files: 
* In BrawlClub/.env.template
* In BrawlClub/bc_frontend/dotenv.template
Fill in the different fields as necessary, instructions are in the file.
Note that brawl stars API keys are free, if you want to use several, you may create several and make a single string with several keys, separated by a '#'.
Example: `BRAWLSTARS_API_KEY = "thisIsKey1#thisIsKey2"`


### 8. Start the redis server
Redis server is used to cache leaderboard pages, as they are computation heavy.
Use the command `redis-server` to start the cache server and keep the terminal open.
You should see something that looks like this:
![image](https://user-images.githubusercontent.com/70256364/206862566-ff3201fe-58ac-41b2-b985-8ce8869fb5aa.png)


### 9. Create the PostgreSQL database
Create the database using pgSQL:
```
psql -d postgres
CREATE DATABASE brawlclub;
grant all privileges on database brawlclub to <user you want to give the privileges>;
alter database brawlclub owner to <user you want to give the privileges> ;
quit;
```
You don't have to create a specific user, the default `postgres` can do the work.

### 10. Create tables in the database using `manage.py migrate`
* If you have your [virtual environment activated](#4-create-a-virtual-environment-recommended),
move your working directory to the same directory as `manage.py` (P13_BS_API/BrawlClub/) and use this command: 
`python manage.py migrate` to create the tables in the database.

* You may also create a superuser using `python manage.py createsuperuser`,
this will allow you to login into the admin panel in http://127.0.0.1:8000/admin

### 11. Start the server
Use the following command 
`python manage.py runserver`


## React setup

### 1. Rename dotenv.template
Fill Django's address (by default, 127.0.0.1:8000)

### 2. Install react dependencies
```
cd bc_frontend/
npm install
```

### 2. Start the react server
```
npm start
```

## Tests

To launch the tests, first activate the redis server

`redis-server`

then, while having your venv activated, move to migrate.py directory and use: 

`python manage.py test`



You're done! You may now head to localhost:3000 to see the landing page!
