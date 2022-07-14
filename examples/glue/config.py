config = {
    # Project
    'project_name': 'Alert Glue Testing',
    'log_debug': False,
    "env": "Development",
    # AWS
    'region_name': 'eu-west-1',

    # LOG
    "status": {
        "success": "SUCCESS",
        "failed": "FAILED",
        "running": "RUNNING",
        "started": "STARTED",
    },

    # Log URLs
    'glue_log_url': 'https://{region_name}.console.aws.amazon.com/gluestudio/home?region={region_name}#/job/{job_name}/run/{run_id}',
    'lambda_log_url': 'https://{region_name}.console.aws.amazon.com/cloudwatch/home?region={region_name}#logsV2:log-groups/log-group/$252Faws$252Flambda$252F{lambda_name}/log-events/{lambda_log_id}',

    # SNS
    'sns': {
        'topic_arn': 'arn:aws:sns:eu-west-1:250045325250:alert_notifications_sns',
        'message_limit': 1500,
        'publish_message': {
            "create_or_update_ses": "false",  # Should be used only if we add new email templates for custom project
            "app_name": "generic_bi_project",  # templates file we created for SES found in data/config
            "email": {
                "sender": "vpandian@email.com",
                "to_recipient": ["vpandian@email.com"],
                "cc_recipient": ["vpandian@email.com"]
            },
            "app_data": {
                "project_name": "",
                "cloud_service": "",
                "env": "",
                "status": "",
                "date": "",
                "error_message": "",
                "cloud_watch_url": ""
            }
        }
    },
    'dates': {
        'default_fmt': "%Y-%m-%d",
        'partition_fmt': "%Y%m%d",
        'log_fmt': '%d-%b-%y %H:%M'
    }
}
