FROM jenkins/jenkins:lts
USER root

# Create the Docker group (ID 986) & add Jenkins to it
RUN groupadd -g 986 docker || true
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
    curl -sfL https://github.com/aquasecurity/trivy/releases/latest/download/trivy_0.48.4_Linux-64bit.deb -o trivy.deb && \
    dpkg -i trivy.deb

ENV PATH="/opt/venv/bin:$PATH"

USER jenkins