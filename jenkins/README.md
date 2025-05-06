# Jenkins Pipeline
## Info
- Dockerfile uses group ID 986 to match the host's Docker group ID. (So jenkins user in the container can access the Docker socket on the host.)
- Jenkins pipeline requires NodeJS tool with retire.js as global npm package

## Build Jenkins Docker Image
```
cd /home/user/TempNote/prod/jenkins
docker build -t jenkins-with-tools .
```
## Run the Jenkins Container
```
docker run -d \
  --name jenkins \
  -p 8080:8080 \
  -p 50000:50000 \
  -v jenkins_home:/var/jenkins_home \
  -v /home/user/TempNote:/workspace \
  -v /var/run/docker.sock:/var/run/docker.sock \
  jenkins-with-tools
``` 



