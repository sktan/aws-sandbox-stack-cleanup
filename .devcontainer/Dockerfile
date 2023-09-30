FROM mcr.microsoft.com/vscode/devcontainers/python:3.10
ENV EDITOR=vim

# This is disabling the "pin versions for apt / pip" warnings
# hadolint ignore=DL3008,DL3042,DL3013
RUN apt-get update && export DEBIAN_FRONTEND=noninteractive && \
    apt-get install -y vim gnupg2 ripgrep
