#!/bin/bash

npm install -g aws-cdk
pip install -r <(pipenv requirements --dev)

# A simpler way to install to authenticate via AWS SSO
tail -c1 ~/.bashrc | read -r _ || echo >>~/.bashrc
cat <<EOF >>~/.bashrc
function awscreds() {
    local TEMP_PROFILE
    if [ \$# -gt 0 ]; then
        TEMP_PROFILE="\$1"
    elif [ -z "\$AWS_PROFILE" ]; then
        echo "Login failed to AWS: One of the following needs to be specified, AWS_PROFILE environment variable or the 'awscreds <account_name>' parameter"
        return 1
    else
        TEMP_PROFILE="\$AWS_PROFILE"
    fi
    local CURRENT_ARN
    CURRENT_ARN="\$(aws sts get-caller-identity --profile="\$TEMP_PROFILE" --query "Arn" --output text 2> /dev/null)"
    if [[ "\${CURRENT_ARN}" != *"assumed-role"* ]]; then
        if ! aws sso login --profile "\$TEMP_PROFILE"; then
        echo "Login failed to AWS: \${TEMP_PROFILE}"
        return 1
        fi
    fi
    export AWS_PROFILE="\$TEMP_PROFILE"
    echo "Connected to AWS: \$TEMP_PROFILE"
}
EOF
