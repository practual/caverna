# Caverna

## Deploying

- Build the Docker image for running the Flask app: `docker build .`
- Create a network for the docker containers to communicate to each other within: `docker network create caverna`
- Run the webapp container in the background: `docker run -d --rm --net caverna -p 5000:5000 <IMAGE>`
- Pull the memcached Docker image: `docker pull memcached`
- Run a container for the memcached image: `docker run -d --rm --net caverna --name memcached memcached`
