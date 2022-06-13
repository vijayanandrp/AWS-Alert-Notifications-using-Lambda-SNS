import os
import boto3
import json

from config import config_dir, config_format, get_logger

file_name = os.path.splitext(os.path.basename(__file__))[0]


def get_app_config(app_name: str = None):
    log = get_logger(f"{file_name}.{get_app_config.__name__}")

    log.info(f'[+] App name - {app_name}')

    if not app_name:
        log.info("[-] Oops. App name cannot be empty.")
        return None

    app_name = app_name.lower()

    if not app_name.endswith(config_format):
        app_name += config_format

    existing_config = [file for file in os.listdir(config_dir)
                       if file.lower().endswith(config_format)]

    if app_name not in existing_config:
        log.info(f"[-] App config named {app_name} not found in existing_config")
        return None

    project_config_file = os.path.join(config_dir, app_name)
    project = json.load(open(project_config_file))
    return project


def create_or_update_ses_template(app_name: str = None):
    log = get_logger(f"{file_name}.{create_or_update_ses_template.__name__}")

    app_config = get_app_config(app_name)
    if not app_config:
        return None

    ses = boto3.client('ses', app_config['aws_region'])

    # get list of email templates
    ses_existing_templates = ses.list_templates()
    log.info(f"[+] ses_existing_templates - {ses_existing_templates}")

    ses_existing_template_names = [_.get('Name', None)
                                   for _ in ses_existing_templates['TemplatesMetadata']
                                   if _ and isinstance(_, dict)]
    log.info(f"[+] ses_existing_template_names - {ses_existing_template_names}")

    template_name = app_config['template_name']
    subject_part = app_config['email']['subject_part']
    text_part = app_config['email']['text_part']
    html_part = app_config['email']['html_part']

    if template_name not in ses_existing_template_names:
        response = ses.create_template(
            Template={
                'TemplateName': template_name,
                'SubjectPart': subject_part,
                'TextPart': text_part,
                'HtmlPart': html_part
            })
        log.info(
            f"[+] created the email template ({template_name}) for the App = {app_name} with response - {response}")
        return response
    else:
        response = ses.update_template(
            Template={
                'TemplateName': template_name,
                'SubjectPart': subject_part,
                'TextPart': text_part,
                'HtmlPart': html_part
            })
        log.info(
            f"[+] updated the email template ({template_name}) for the App = {app_name} with response - {response}")
        return response


def send_email(app_name: str = None, app_data: str = None):
    log = get_logger(f"{file_name}.{send_email.__name__}")
    app_config = get_app_config(app_name)
    ses = boto3.client('ses', app_config['aws_region'])
    log.info(f"[*] app_data - {app_data}")
    response = ses.send_templated_email(
        Source=app_config['email']['sender'],
        Destination={
            'ToAddresses': app_config['email']['to_recipient']
            ,
            'CcAddresses': app_config['email']['cc_recipient']
        },
        ReplyToAddresses=[
        ],
        Template=app_config['template_name'],
        TemplateData=app_data
    )
    log.info(f"[+] Sent an email for the App Name = {app_name}; Response - {response}")
    return response
