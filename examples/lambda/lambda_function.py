import os
import sys
import traceback
import json
import logging
from datetime import datetime as dt, timezone
import boto3

# custom imports
from config import config

# VARIABLES
file_name = os.path.splitext(os.path.basename(__file__))[0]
job_name = file_name
project_name = config['project_name']
# AWS
region_name = config['region_name']
lambda_log_url_fmt = config['lambda_log_url']
topic_arn = config['sns']['topic_arn']
sns_message = config['sns']['publish_message']
message_limit = config['sns']['message_limit']
status_failed = config['status']['failed']
status_success = config['status']['success']
status_running = config['status']['running']
status_started = config['status']['started']
# Lambda
lambda_name = os.environ.get('AWS_LAMBDA_FUNCTION_NAME', 'Alert-Test-Lambda').replace(' ', '%20')
lambda_log_id = (os.environ.get('AWS_LAMBDA_LOG_STREAM_NAME', '')
                 .replace('$', '$2524')
                 .replace('/', '$252F')
                 .replace('[', '$255B')
                 .replace(']', '$255D')
                 )

root = logging.getLogger()

if root.handlers:
    for handler in root.handlers:
        root.removeHandler(handler)

stream_handler = logging.StreamHandler(sys.stdout)

log_args = {
    "level": logging.DEBUG if config['log_debug'] else logging.INFO,
    "format": "%(asctime)s [%(levelname)s] %(name)s - %(message)s",
    "datefmt": config['dates']['log_fmt'],
    "handlers": [stream_handler]
}

logging.basicConfig(**log_args)


def publish_sns(topic_arn, message: dict):
    client = boto3.client('sns')
    response = client.publish(
        TargetArn=topic_arn,
        Message=json.dumps({'default': json.dumps(message)}),
        MessageStructure='json')
    return response


def lambda_handler(event: dict = None, context: dict = None):
    logger = logging.getLogger(f"{file_name}.__main__")
    lambda_log_url = lambda_log_url_fmt.format(region_name=region_name, lambda_name=lambda_name,
                                               lambda_log_id=lambda_log_id)
    logger.info('=' * 30 + " Start " + '=' * 30)
    logger.info(f"event - {event}")
    logger.info(f"context - {context}")

    try:
        logger.info(str(os.environ.items()))
        # TODO implement
        print(1 / 0)

    except Exception as error:
        err_msg = ''.join(traceback.format_exception(None, error, error.__traceback__))
        sns_message['app_data']['env'] = os.environ.get('env', None) if os.environ.get('env', None) else config['env']
        sns_message['app_data']['cloud_watch_url'] = lambda_log_url
        sns_message['app_data']['cloud_service'] = '[Lambda] - ' + job_name
        sns_message['app_data']['date'] = str(dt.now(timezone.utc))
        sns_message['app_data']['project_name'] = project_name
        sns_message['app_data']['status'] = status_failed
        sns_message['app_data']['error_message'] = err_msg[:message_limit]
        publish_sns(topic_arn=topic_arn, message=sns_message)
        traceback.print_exception(type(error), error, error.__traceback__)
        logger.exception(err_msg)
        raise

    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }
