# Development using Docker

Start a Docker container for local development.

```bash
docker build -f Dockerfile.dev -t maloja_dev .
docker run -it --rm -p 42010:42010 -v /home/$USER/git/maloja:/usr/src/app --env-file .env maloja_dev
```

Or you can use the equivalent docker-compose command.

```bash
docker-compose up
```

## Advantages

- No dependencies installed on host
- _Automatically updated content_ - TODO
