FROM jenkins/jenkins:lts
USER root

# Create the Docker group & add Jenkins to it
ARG DOCKER_GID=986
RUN groupadd -g ${DOCKER_GID} docker || true
RUN usermod -aG docker jenkins

# Install tools used in the pipeline
RUN apt-get update && apt-get install -y \
    python3 python3-pip python3-venv \
    curl gnupg2 lsb-release ca-certificates \
    git sudo

# Install Docker CLI
RUN curl -fsSL https://download.docker.com/linux/debian/gpg | apt-key add - && \
    echo "deb [arch=amd64] https://download.docker.com/linux/debian $(lsb_release -cs) stable" \
    > /etc/apt/sources.list.d/docker.list && \
    apt-get update && apt-get install -y docker-ce-cli

# Install gixy & trivy
RUN python3 -m venv /opt/venv && \
    /opt/venv/bin/pip install --upgrade pip && \
    /opt/venv/bin/pip install gixy && \
    curl -sfL https://raw.githubusercontent.com/aquasecurity/trivy/main/contrib/install.sh | sh -s -- -b /usr/local/bin  

ENV PATH="/opt/venv/bin:$PATH"

USER jenkins