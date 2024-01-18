# Smile Git Remote
Use a web service(microservice) to remote git's command
## Version 0.1.0
- This project lets us pull a repo via website that installed and 
set configure
- Using OOP and make a simple structure in Python 3.x
- Project structure
  - main.py is a startup and route collection
  - core directory: where we write code the most, there are Action as Controller class, Model, ReqValidity as Validation class, Git as Git Library
  - data directory: contains git profiles, others json file
  - entity directory: stores the data mapping of the json file and others
- Framework
  - Flask 3.0.0: To create a service, this project implements Flask 3.0.0 and tried 3.0.1(not yet official)
- Libraries
  - Gitpython: In the early idea of my code, I wrote all by integrating git command. This library is still alive until now, that is why, I decide to use and do not want to write my own code. It's the core library which run behind the Git class
  - SmileError: To catch the error in better way
  - SmileLogger: For tracking every process
  - SmileValidation: Did not implement yet, but it will use for data validation for the next version


## Update data
Find data/project.json
```
{
  "projects": {
	"123": {
	  "auth": [
		{
		  "password": "123456"
		  , "username": "kara"
		}
		, {
		  "password": "123456"
		  , "username": "jojo"
		}
	  ]
	  , "datetime_format": "%Y-%m-%d %H:%M:%S"
	  , "env": "pro"
	  , "force_clone": "true"
	  , "force_pull": "true"
	  , "git_branch": "master"
	  , "git_dir": "/var/www/test/aabb"
	  , "git_remote_origin": "origin"
	  , "git_remote_url": "https://github.com/sitthykun/smileerror.git"
	  , "git_token": ""
	  , "git_username": ""
	  , "name": "test website"
	  , "note": "test project website"
	  , "trigger": {
		"before": [""]
		, "after": [""]
	  }
	  , "white_ip": ["192.168.2.3","192.168.2.4"]
	}
	, "345": {
	}
  }
  , "version": "1.0.0"
}
```
Above the project.json has only a valid project is '123'

## Create a post route:
Check out in main.py along root directory
```
# built-in
from typing import Any
# external
from flask import Flask
from smilelog.Logger import Logger
# internal
from core.Action import Action


# instance
app = Flask(__name__)
log = Logger(
    path        = 'log'
    , enableLog = True
)

@app.route('/pull/<string:projectId>', methods= ['POST'])
def pullProjectPost(projectId: str) -> Any:
    #
    return Action(log).pullPost(
        projectId   = projectId
    )

# run server
if __name__ == '__main__':
    #
    app.run(
        host    = '127.0.0.1'
        , port  = 6060
        , debug = True
    )
```

## Request a service
Start a terminal with CURL command
```
$ curl -X POST -H "Content-type: application/json" -d "{\"username\" : \"kara\", \"password\" : \"123456\"}" "http://127.0.0.1:6060/pull/123"
```

## GUnicorn
If you need to configure with Linux server, I recommend to run wsgi instead.
Example:
```
$ gunicorn --bind 127.0.0.1:5000 wsgi:app
```

Hopefully, you will enjoy it

To Support my work, please donate me via <a class="bmc-button" target="_blank" href="https://www.buymeacoffee.com/sitthykun"><img src="https://cdn.buymeacoffee.com/buttons/bmc-new-btn-logo.svg" alt="Buy me a Pizza"><span style="margin-left:5px;font-size:28px !important;">Buy me a Coffee</span></a>
