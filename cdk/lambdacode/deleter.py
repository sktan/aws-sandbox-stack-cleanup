import json

import boto3

cfn_client = boto3.client("cloudformation")


def lambda_handler(event, context):
    stack_arn = event["stack_arn"]
    cfn_client.delete_stack(StackName=stack_arn)
