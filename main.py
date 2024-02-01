"""
Author: masakokh
Year: 2024
Package: project
Note:
Version: 0.1.2
"""
# built-in
import os
# # set these lines to prevent any error happen on linux
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
    return 'Love Mom', 200

@app.route('/checkout/<string:projectId>', methods= ['POST'])
def checkoutProjectPost(projectId: str) -> Any:
    #
    return Action(log).checkoutPost(projectId= projectId) if Validation(log).checkoutPost() else Validation(log).fail(message= 'checkout project post')

@app.route('/checkout/help', methods= ['GET'])
def checkoutProjectHelp() -> Any:
    #
    return Help().checkout()

@app.route('/pull/<string:projectId>', methods= ['POST'])
def pullProjectPost(projectId: str) -> Any:
    #
    return Action(log).pullPost(projectId= projectId) if Validation(log).pullPost() else Validation(log).fail(message= 'pull project post')

@app.route('/pull/help', methods= ['GET'])
def pullProjectHelp() -> Any:
    #
    return Help().pull()


@app.route('/token/help', methods= ['GET'])
def tokenProjectHelp() -> Any:
    #
    return Help().tokenRequest()

@app.route('/token/', methods= ['POST'])
def tokenProjectPost() -> Any:
    #
    return Action(log).tokenPost() if Validation(log).tokenPost() else Validation(log).fail(message= 'token project post')


# run server
if __name__ == '__main__':
    #
    app.run(
        host    = '127.0.0.1'
        , port  = 6060
        , debug = True
    )
