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

## Create a post route:
```
@app.route('/pull/<string:projectId>', methods= ['POST'])
def pullProjectPost(projectId: str) -> Any:
    #
    return Action(log).pullPost(
        projectId   = projectId
    )
```

To Support my work, please donate me via <a class="bmc-button" target="_blank" href="https://www.buymeacoffee.com/sitthykun"><img src="https://cdn.buymeacoffee.com/buttons/bmc-new-btn-logo.svg" alt="Buy me a Pizza"><span style="margin-left:5px;font-size:28px !important;">Buy me a Coffee</span></a>
