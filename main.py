"""
Author: masakokh
Year: 2024
Package: project
Note:
Version: 0.1.3
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

## error ###########################
@app.errorhandler(403)
def page_forbidden(e) -> Any:
    """

	:return:
	"""
    return 'Page forbidden', 403


@app.errorhandler(404)
def page_not_found(e) -> Any:
    """

	:return:
	"""
    return 'Page not found', 404


@app.route('/', methods= ['GET'])
def home() -> Any:
    #
    return 'Love Mom', 200

@app.route('/checkout/<string:projectId>', methods= ['POST'])
def checkoutProjectPost(projectId: str) -> Any:
    #
    return Action(log).checkoutPost(project= projectId) if Validation(log).checkoutPost(projectId) else Validation(log).fail(message= 'checkout project post')

@app.route('/checkout/help', methods= ['GET'])
def checkoutProjectHelp() -> Any:
    #
    return Help().checkout()

@app.route('/pull/<string:projectId>', methods= ['POST'])
def pullProjectPost(projectId: str) -> Any:
    #
    return Action(log).pullPost(project= projectId) if Validation(log).pullPost(projectId) else Validation(log).fail(message= 'pull project post')

@app.route('/pull/help', methods= ['GET'])
def pullProjectHelp() -> Any:
    #
    return Help().pull()


@app.route('/token/help', methods= ['GET'])
def tokenProjectHelp() -> Any:
    #
    return Help().tokenRequest()

@app.route('/token/<string:projectId>', methods= ['POST'])
def tokenProjectPost(projectId: str) -> Any:
    #
    return Action(log).tokenPost(project= projectId) if Validation(log).tokenPost(projectId) else Validation(log).fail(message= 'token project post')


# run server
if __name__ == '__main__':
    #
    app.run(
        host    = '127.0.0.1'
        , port  = 6060
        , debug = True
    )
