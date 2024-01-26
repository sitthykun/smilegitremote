"""
Author: masakokh
Year: 2024
Package: project
Note:
Version: 0.1.1
"""
# built-in
import os
## set
os.environ['GIT_PYTHON_REFRESH']        = 'quiet'
os.environ['GIT_PYTHON_GIT_EXECUTABLE'] = '/usr/bin/git'
from typing import Any
# external
from flask import Flask
from smilelog.Logger import Logger
# internal
from help.Help import Help
from vamp.Action import Action
from vamp.Validation import Validation


# instance
app = Flask(__name__)
log = Logger(
    path        = 'log'
    , enableLog = True
)


@app.route('/', methods= ['GET'])
def home() -> Any:
    #
    return 'Miss Mom', 200

@app.route('/checkout/<string:projectId>', methods= ['POST'])
def checkoutProjectPost(projectId: str) -> Any:
    #
    return Validation(log).fail(message= 'checkout project post') if not Validation(log).checkoutPost() else Action(log).checkoutPost(projectId= projectId)

@app.route('/checkout/help', methods= ['GET'])
def checkoutProjectHelp() -> Any:
    #
    return Help().checkout()

@app.route('/pull/<string:projectId>', methods= ['POST'])
def pullProjectPost(projectId: str) -> Any:
    #
    return Validation(log).fail(message= 'pull project post') if not Validation(log).pullPost() else Action(log).pullPost(projectId= projectId)

@app.route('/pull/help', methods= ['GET'])
def pullProjectHelp() -> Any:
    #
    return Help().pull()


# run server
if __name__ == '__main__':
    #
    app.run(
        host    = '127.0.0.1'
        , port  = 6060
        , debug = True
    )
