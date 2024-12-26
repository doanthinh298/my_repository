import os
import time
import warnings

from sanic import json, Request
from sanic_ext import openapi
from bson import ObjectId
from App.api import api
from App import create_app
from App.database.mongodb.database_store import Database
from App.misc.log import log
from App.utils.logger_utils import get_logger
from config import Config , LocalDBConfig


warnings.filterwarnings('ignore')

logger = get_logger('Main')

app = create_app(Config, LocalDBConfig)

app.blueprint(api)

@app.before_server_start
async def setup_db(_):
    app.ctx.db = Database()
    log(f'Connected to Database {app.ctx.db.connection_url}')

@app.middleware('request')
async def add_start_time(request: Request):
    request.headers['start_time'] = time.time()

@app.middleware('response')
async def add_spent_time(request: Request, response):
    try:
        if 'start_time' in request.headers:
            timestamp = request.headers['start_time']
            spend_time = round((time.time() - timestamp), 3)
            response.headers['latency'] = spend_time

            msg = "{status} {method} {path} {query} {latency}s".format(
                status=response.status,
                method=request.method,
                path=request.path,
                query=request.query_string,
                latency=spend_time
            )
            if response.status >= 400:
                logger.error(msg)
            elif response.status >= 300:
                logger.warning(msg)
            else:
                logger.info(msg)
    except Exception as ex:
        logger.exception(ex)


@app.route("/ping", methods={'GET'})
@openapi.tag("Ping")
@openapi.summary("Ping server !")
async def hello_world(request: Request):
    response = json({
        "description": "Success",
        "status": 200,
        "message": f"App {request.app.name}: Hello, World !!!"
    })
    return response


if __name__ == '__main__':
    if 'SECRET_KEY' not in os.environ:
        log(message='SECRET KEY is not set in the environment variable.',
            keyword='WARN')

    try:
        app.run(**app.config['RUN_SETTING'])
    except (KeyError, OSError):
        log('End Server...')
