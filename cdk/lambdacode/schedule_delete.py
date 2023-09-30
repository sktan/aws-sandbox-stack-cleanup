import os
from datetime import datetime, timedelta, timezone

import boto3

scheduler_client = boto3.client("scheduler")


def lambda_handler(event, context):
    stack_id = event["detail"]["stack-id"]

    flex_window = {"Mode": "OFF"}
    lambda_target = {
        "RoleArn": os.environ["SCHEDULER_ROLE_ARN"],
        "Arn": os.environ["DELETER_LAMBDA_ARN"],
        "Input": f"{ 'stack_arn': '{stack_id}' }",
    }

    dt = datetime.now(timezone.utc) + timedelta(hours=48)

    scheduler_client.create_schedule(
        Name=f"cfn-{stack_id.split('/')[-1]}",
        ScheduleExpression=f"at({dt.strftime('%Y-%m-%dT%H:%M:%S')})",
        Target=lambda_target,
        ScheduleExpressionTimezone="Etc/UTC",
        FlexibleTimeWindow=flex_window,
    )
