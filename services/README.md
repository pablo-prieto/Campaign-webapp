# Backend
This repo is just the backend portion of this project.  

## Prerequisites
### You might need to have the following softwares:
* Python 3.6
* PostgreSQL

### You might need to install the following packages:
* virtualenv
* flask
* psycopg2
* requests

## Getting Started
Download necessary softwares and packages first.  
If you activate virtualenv called "venv" you won't need the libraries below. Instructions are below so keep reading.

### Remote host and database
Make sure in ```./base_cmd/db_commands.py``` the code:
```
def connect(remote = False):
```
Is modified to:
```
def connect(remote = True):
```
In order to use remote database.  
  
All backend APIs does not currently have a remote host.  
The following callable links can be found at:
```
./api_list.txt
```

### Local host and database
If you want to set up in local database follow the steps below.
  
#### Modify Database
Setup your PostgreSQL database.  
You must first edit the code so that it matches your SQL credentials in this file:
```
./base_cmd/db_commands.py
```
Then you should modify line 29 to match your own variables.
  
#### Modify Flask Call
To run in a local host, you must make sure that the file at:
```
$ ./call_flask.sh
```
  
#### Getting the Data
In order to match python version and libraries you must run the following bash command:
```
$ source ./venv/Scripts/activate
``` 
Or if you are in cmd-prompt, you can run:
```
"venv/Scripts/activate.bat"
```

Finally we can create the database with the following command:
```
py ./base_cmd/create_db.py
```
  
#### Running the localhost
Then run the localhost using the bash command:
```
$ ./call_flask.sh
```
Make sure it says:
```
(venv) C:\path-to-your-directory\Campaign-webapp\services>
```
  
Then on your command prompt, we can first create a user.
Here is an example:
```
curl http://localhost:3000/user/create-user -d "{\"usertype\": \"influencer\", "\"first_name\": \"banana\", "\"last_name\": \"banana\", \"borough\":\"Manhattan\", \"state\": \"NY\", \"phone\":\"718-239-4738\", \"email\":\"banana@b.\", \"password\":\"bananahana\"}" -H "Content-Type: application/json"
```

Then activate the account using the following command (make sure the user id matches):
```
curl http://localhost:3000/user/update -X PUT -d "{\"user_id\": \"1\", \"status\": \"active\"}" -H "Content-Type: application/json"
```

Then we can login to that user using the following command:
```
curl http://localhost:3000/user/login -d "{\"email\": \"banana@b.\", \"password\": \"bananahana\"}" -H "Content-Type: application/json"
```