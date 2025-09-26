ARG VARIANT=3.11-bookworm
FROM mcr.microsoft.com/vscode/devcontainers/python:${VARIANT}

# Install dependencies
RUN apt-get update && apt-get install -y \
    curl \
    unzip \
    gnupg \
    software-properties-common \
    apt-transport-https \
    ca-certificates \
    lsb-release
