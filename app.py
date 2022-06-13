import os
import sys
import json

for root, sub_dir, file in os.walk(os.getcwd()):
    sys.path.insert(0, root)

file_name = os.path.splitext(os.path.basename(__file__))[0]


def lambda_handler(event, context):
    """
    This is the only one Lambda function we use.
    It is triggered by SNS Topic with the event details.
    Lambda has to be subscribed manually.
    :param event:
        {
          "env": "dev",
          "create_or_update_ses": "true",
          "app_name": "demo_app",
          "app_data": {
            "date": "2022-06-03",
            "env": "dev"
          },
          "log_debug": "false"
        }
            :param context: None
    :return: None
    """
    os.environ['log_debug'] = event.get("log_debug", "false")
    os.environ['env'] = event.get("env", "dev")

    from src.config import get_logger
    from src.ses_api import create_or_update_ses_template, send_email

    log = get_logger(f"{file_name}.{lambda_handler.__name__}")
    log.info('=' * 30 + " Init " + '=' * 30)
    log.info(f"[*] event - {event}")
    log.info(f"[*] context - {context}")

    app_name = event.get('app_name', None)
    if not app_name:
        log.info("[-] event json has no app_name key & value.")
        return None

    create_or_update_ses = event.get('create_or_update_ses', "false")
    if create_or_update_ses == "true":
        create_or_update_ses_template(app_name)

    app_data = event.get("app_data", "{}")
    send_email(app_name, str(json.dumps(app_data)))
    log.info('=' * 30 + " Exit " + '=' * 30)
