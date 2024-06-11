# How to create and run container

## Start docker daemon
sudo systemctl start docker.service

## Building the container
sudo docker build -t vinyl_tracker .

## Running the container
#### The container needs to be run with -ti for terminal interactivity
sudo docker run -ti vinyl_tracker

## View running containers
docker ps

## View images
docker images

## Delete everything docker related
docker system prune -a --volumes
