# Local Installation Guide

## Requirements
- Python

## Installation Steps
### Step 1
Run file `install.bat` this will execute the following statements which can be run individually instead.

- Check python is installed 
```
python --version
```
- Create virtual environment 
```
python -m venv .\venv
```
- Install requirements 
```
python -m pip install -r ./requirements.txt
```
- Create local sqlite3 database 
```
python .\lib\local_db.py
```
- Apply Django migrations to sqlite3 database 
```
python .\config_creator\manage.py migrate
```

### Step 2
Add a user, run command 
```
python .\config_creator\manage.py createsuperuser
```

You will then be prompted for your desired email address:
```
Email address: admin@example.com
```
The final step is to enter your password. You will be asked to enter your password twice, the second time as a confirmation of the first.
```
Password: **********
Password (again): *********
Superuser created successfully.
```

### Step 3
Run the app with command
```
python .\config_creator\manage.py runserver
```

## Running the development server
The application will run until you close your terminal or end the process with `ctrl-c`

To start the server, make sure the virtual environment is running
```
.\venv\Scripts\activate
```
Then run command
```
python .\config_creator\manage.py runserver
```
Navigate to the url provided
```
July 19, 2022 - 12:52:23
Django version 4.0.5, using settings 'config_creator.settings'
Starting development server at http://127.0.0.1:8000/
Quit the server with CTRL-BREAK.
```