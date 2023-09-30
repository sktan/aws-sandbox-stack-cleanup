# AWS Sandbox Stack Cleanup

I'm sure everyone working with AWS has a similar story to tell. You spin up a few resources, go away for lunch or for the weekend and then completely forget about it. The only reminder of your forgotten experiment is the bill you receive after the first few days of the following month. What was supposed to be a small couple-dollar exercise has now turned into a double-digit or triple-digit bill. This story is commonly told in sandbox environments, where users are encouraged to experiment with AWS services.

This repository contains a CloudFormation template that will help you clean up your AWS sandbox account 48 hours after a stack has been created.

## Architecture

![Architecture](https://cdn.sktan.com/content/blog_post_10/1-architecture-diagram.webp)

## How to Deploy

You can use CDK to deploy the stack directly from the `cdk` directory:

```bash
cd cdk
cdk deploy
```

Or you can deploy the pre-built CloudFormation template from the `cloudformation` directory via the CloudFormation UI.
