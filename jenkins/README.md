# Jenkins Pipeline
## Info
- To access Docker socket, pass host's Docker group ID as build argument.
- Jenkins pipeline requires NodeJS plugin with retire as global npm package

## Build Jenkins Docker Image
```
cd /home/user/temp-note/jenkins

# Get the Docker GID from the host
DOCKER_GID=$(getent group docker | cut -d: -f3)

# Build the image and pass the host's Docker GID
docker build --build-arg DOCKER_GID=$DOCKER_GID -t jenkins-with-tools .
```
## Run the Jenkins Container
```
docker run -d \
  --name jenkins \
  -p 8080:8080 \
  -p 50000:50000 \
  -v jenkins_home:/var/jenkins_home \
  -v /home/user/temp-note:/workspace \
  -v /var/run/docker.sock:/var/run/docker.sock \
  jenkins-with-tools
``` 



