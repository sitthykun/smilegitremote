# Smile Git Remote
Use a web service (microservice) to remote git's command
## Version 0.1.0
- This project lets us pull a repo via a website that installed and set configuration
- Using OOP and make a simple structure in Python 3.x
- Project structure
  - main.py is a startup and route collecting
  - core directory: where we write code the most, there are Action as Controller class, Model, ReqValidity as Validation class, Git as Git Library
  - data directory: contains git profiles, others json file
  - entity directory: stores the data mapping of the json file and others
- Framework
  - Flask 3.0.0: To create a service, this project implements Flask 3.0.0 and upgraded to Flask 3.0.1
- Libraries
  - Gitpython: In the early idea of my code, I wrote all by integrating git command. This library is still alive until now, that is why, I decide to use and do not want to write my own code. It's the core library which runs behind the Git class
  - SmileError: To catch the error in a better way
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
Check out main.py in alongside root directory
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

## Server Deployment
### GUnicorn
If service needs running on Linux/Unix server, it should point the service path to wsgi.py instead of main.py.
This wsgi.py was designed for the OS system service purpose, and recommends guincorn or uvicorn\
Example:
```
$ gunicorn --bind 127.0.0.1:5000 wsgi:app
```

### Bash profile
Some systems are not yet ready with git command, it will raise a common error message or any kind of unrecognised git command or not found the file or directory.
```
Cmd('git') not found due to: FileNotFoundError('[Errno 2] No such file or directory: 'git'')
```

Calm down and try adding these lines to your current theme profile such as .bashrc
```
# gitpython
export PATH=$PATH:/usr/bin/git
export GIT_PYTHON_GIT_EXECUTABLE="/usr/bin/git"
export GIT_PYTHON_REFRESH="quiet"
```
or add directly these lines before importing git namespace inside the code
```
# built-in
import os
# set
os.environ['GIT_PYTHON_REFRESH']        = 'quiet'
os.environ['GIT_PYTHON_GIT_EXECUTABLE'] = '/usr/bin/git'
...
import git
from git import Repo, Remote
from git.exc import GitError, GitCommandError, ...
```
or extend a Git package by applying the OOPs' inherit concept. Enhance the appearance of our Python code.

In case you're uncertain about the location of git, give the command a try.
```
$ which git
/usr/bin/git
```

### Roadmap

| Version | Status  | Description                                          |
|---------|---------|------------------------------------------------------|
| 0.1.0   | current | Clone, checkout a branch and pull function           |
| 0.2.0   | dev     | Enable trigger (before and after)                    |
| 0.3.0   | dev     | Validating implementation for the request parameters |


Hopefully, you will enjoy on Linux and MacOS

To Support my work, please donate me via <a class="bmc-button" target="_blank" href="https://www.buymeacoffee.com/sitthykun"><img src="https://cdn.buymeacoffee.com/buttons/bmc-new-btn-logo.svg" alt="Buy me a Pizza"><span style="margin-left:5px;font-size:28px !important;">Buy me a Coffee</span></a>
