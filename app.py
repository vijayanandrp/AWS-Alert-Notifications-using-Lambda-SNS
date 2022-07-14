import os
import sys
import json

for root, sub_dir, file in os.walk(os.getcwd()):
    sys.path.insert(0, root)

file_name = os.path.splitext(os.path.basename(__file__))[0]

from src.config import get_logger
from src.ses_api import create_or_update_ses_template, send_email


# s3://aws-c4-bdap-prod-artefacts/alert_notifications/code.zip

def send_email_to_ses(event: dict):
    log = get_logger(f"{file_name}.{send_email_to_ses.__name__}")
    log.info(f"[*] event - {event}")
    app_name = event.get('app_name', None)
    if not app_name:
        log.info("[-] event json has no app_name key & value.")
        return None
    # Create or Update the Email templates
    create_or_update_ses = event.get('create_or_update_ses', "false")
    if create_or_update_ses == "true":
        create_or_update_ses_template(app_name)

    app_data = event.get("app_data", "{}")
    email_data = event.get("email", dict())
    return send_email(app_name=app_name,
                      app_data=str(json.dumps(app_data)),
                      email_data=email_data)


def lambda_handler(event, context):
    """
    This is the only one Lambda function we use.
    It is triggered by SNS Topic with the event details.
    Lambda has to be subscribed manually.
    :param event: Dict Check ReadMe.md
    :param context: None
    :return: None
    """

    log = get_logger(f"{file_name}.{lambda_handler.__name__}")
    log.info('=' * 30 + " Init " + '=' * 30)
    log.info(f"[*] event - {event}")
    log.info(f"[*] context - {context}")

    records = event.get('Records', None)
    if records:
        events = [x['Sns'].get('Message', '{}') for x in records if 'Message' in x['Sns'].keys()]
        for event in events:
            response = send_email_to_ses(json.loads(event))
            log.info(f'{response}')
    else:
        response = send_email_to_ses(event)
        log.info(f'{response}')

    log.info('=' * 30 + " Exit " + '=' * 30)
