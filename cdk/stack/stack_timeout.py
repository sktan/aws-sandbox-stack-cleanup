from aws_cdk import Stack
from aws_cdk import aws_events as events
from aws_cdk import aws_events_targets as targets
from aws_cdk import aws_iam as iam
from aws_cdk import aws_lambda as lambda_
from constructs import Construct


class StackTimeout(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        with open("lambdacode/schedule_delete.py", "r") as f:
            schedule_delete_lambda_code = f.read()

        with open("lambdacode/deleter.py", "r") as f:
            deleter_lambda_code = f.read()

        # Lambda function to delete stacks after 48 hours
        deleter_lambda = lambda_.Function(
            self,
            "deleter-lambda",
            code=lambda_.Code.from_inline(deleter_lambda_code),
            handler="index.lambda_handler",
            runtime=lambda_.Runtime.PYTHON_3_9,
        )
        deleter_lambda.add_to_role_policy(
            statement=iam.PolicyStatement(
                actions=["cloudformation:DeleteStack"], resources=["*"]
            )
        )

        # IAM role for the events bridge scheduler
        scheduler_role = iam.Role(
            self,
            "scheduler-role",
            assumed_by=iam.ServicePrincipal("scheduler.amazonaws.com"),
        )
        scheduler_role.add_to_policy(
            iam.PolicyStatement(
                actions=["lambda:InvokeFunction"],
                resources=[deleter_lambda.function_arn],
            )
        )

        # Lambda function to schedule the deletion of stacks
        schedule_delete_lambda = lambda_.Function(
            self,
            "schedule-delete-lambda",
            code=lambda_.Code.from_inline(schedule_delete_lambda_code),
            handler="index.lambda_handler",
            runtime=lambda_.Runtime.PYTHON_3_9,
            environment={
                "SCHEDULER_ROLE_ARN": scheduler_role.role_arn,
                "DELETER_LAMBDA_ARN": deleter_lambda.function_arn,
            },
        )

        schedule_delete_lambda.add_to_role_policy(
            statement=iam.PolicyStatement(
                actions=["scheduler:CreateSchedule", "iam:PassRole"], resources=["*"]
            )
        )

        events.Rule(
            self,
            "cfn-stack-create-complete-rule",
            event_pattern=events.EventPattern(
                source=["aws.cloudformation"],
                detail_type=["CloudFormation Stack Status Change"],
                detail={"status-details": {"status": ["CREATE_COMPLETE"]}},
            ),
            targets=[targets.LambdaFunction(schedule_delete_lambda)],
        )
