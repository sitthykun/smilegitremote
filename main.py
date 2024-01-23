"""
Author: masakokh
Year: 2024
Package: project
Note:
Version: 0.1.0
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
from vamp.Action import Action


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
    return Action(log).pullPost(
        projectId   = projectId
    )

@app.route('/pull/<string:projectId>', methods= ['POST'])
def pullProjectPost(projectId: str) -> Any:
    #
    return Action(log).pullPost(
        projectId   = projectId
    )


# route
# @app.route('/pull/<string:projectId>/<string:username>/<string:password>', methods= ['GET'])
# def pullProjectGet(projectId: str, username: str, password: str) -> Any:
#     #
#     return Action(log).pullGet(
#         projectId   = projectId
#         , username  = username
#         , password  = password
#     )


@app.route('/pull/help', methods= ['GET'])
def pullProjectHelp() -> Any:
    #
    return Action(log).pullHelp()


# run server
if __name__ == '__main__':
    #
    app.run(
        host    = '127.0.0.1'
        , port  = 6060
        , debug = True
    )
