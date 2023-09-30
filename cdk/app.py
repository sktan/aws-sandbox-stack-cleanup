#!/usr/bin/env python3
import os

import aws_cdk as cdk
from stack.stack_timeout import StackTimeout

app = cdk.App()
StackTimeout(
    app,
    "SandboxTimeoutStack",
    env=cdk.Environment(
        account=os.getenv("CDK_DEFAULT_ACCOUNT"), region=os.getenv("CDK_DEFAULT_REGION")
    ),
    synthesizer=cdk.DefaultStackSynthesizer(generate_bootstrap_version_rule=False),
)

app.synth()
