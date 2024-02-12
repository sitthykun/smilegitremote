![template-sgr](https://github.com/sitthykun/smilevalidation/assets/227092/dfbbdff9-dae7-4d50-b354-8c741703060f)
# Smile Git Remote
Use a web service (microservice) to remote git's command. 
To avoid various external software installations such as Redis, RDMS, NoSQL, all the permanent and temporary data is using a file for storage.
Additionally, among of those files are json and plain text.

## Version 0.3.0
On pull request, this function allows checkout any available branch instead of the default git_branch's setting value in project.json. And
Implement a plug feature via reading file which stored in the plugin directory. The batch command inside the plugin file execution is lower priority than the trigger.
```
Pull > 
// optional
"plugin": {
  // optional
  "before": "flask.init"
  // optional
  , "after": "flask.clean"
}

Checkout >
// optional
"plugin": {
  // optional
  "after": 'flask.clean'
}
```

## Version 0.2.0
The trigger is implemented with two events are the before and after.
- before: contains a list of commands
- after: is the same as before event but it will execute after complete the main process

```
"trigger": {
  "before": []
  , "after": []
}
```

## Version 0.1.0
- This project lets us pull a repo via a website that installed
- Using OOP and make a simple structure in Python 3.x
- Project structure
  - main.py is a startup and route collecting
  - core directory: where we write code the most, there are Action as Controller class, Model, ReqValidity as Validation class, Git as Git Library
  - data directory: contains git profiles, others json file
  - entity directory: stores the data mapping of the json file and others
- Framework
  - Flask 3.0.0: To create a service, this project implements Flask 3.0.1
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
		  "username": "kara"
		}
		, {
		  "username": "jojo"
		}
	  ]
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
		"before": ["echo 'Start'"]
		, "after": ["echo 'Finish'"]
	  }
	  , "white_ip": ["192.168.2.3","192.168.2.4"]
	}
	, "345": {
	}
  }
  , "version": "1.0.1"
}
```
Above the project.json has only a valid project is '123'
The previous commit, the token concept was implemented and stored in 'token' subdirectory of the 'data'.
Furthermore, if github's repo is a private, the configuration required 'git_username' and 'git_token'.

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

## In main.py file now
There are a couple route samples such as
- Request token
- Checkout
- Pull

Before request the git command, these commands need a token to access
```
@app.route('/token/', methods= ['POST'])
def tokenProjectPost() -> Any:
    return Action(log).tokenPost() if Validation(log).tokenPost() else Validation(log).fail(message= 'token project post')
```

## API Document
To get the requirement of each api, please follow the format '/token/help' for a new route.
Let checkout exist in the main.py
```
@app.route('/token/help', methods= ['GET'])
def tokenProjectHelp() -> Any:
    #
    return Help().tokenRequest()
```
The right output should be like this
```
{
  "token_document": {
    "body": {
      "password*": "xxx",
      "username*": "xxx"
    },
    "method": "post",
    "url": "https://domain/token/"
  }
}
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
The git command is not yet compatible with some systems, which may result in a common error message, an unrecognized git command, or a failure to locate the file or directory.
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
# # set these lines to prevent any error happen on linux
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

| Version | Status   | Description                                                                                                  |
|---------|----------|--------------------------------------------------------------------------------------------------------------|
| 0.1.0   | released | Clone, checkout a branch and pull function                                                                   |
| 0.2.0   | current  | Enable trigger (before and after)                                                                            |
| 0.3.0   | dev      | Allow pulling with any branch on the request and implement plugin which allows executing a batch of commands |
| 0.4.0   | dev      | Validating implementation for the request parameters                                                         |


Hopefully, you will enjoy on Linux and MacOS

To Support my work, please donate me via <a class="bmc-button" target="_blank" href="https://www.buymeacoffee.com/sitthykun"><img src="https://cdn.buymeacoffee.com/buttons/bmc-new-btn-logo.svg" alt="Buy me a Pizza"><span style="margin-left:5px;font-size:28px !important;">Buy me a Coffee</span></a>
