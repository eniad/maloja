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

## TODO:

- Run using maloja.server directly, i.e. `python -m maloja.server` instead of pip install or setup.py build/install
- Automatically updated content on edits. See these resources:
  - [Bottle Tutorial Auto Reloading](https://bottlepy.org/docs/dev/tutorial.html#auto-reloading)
  - [How to change and reload python code in waitress without restarting the server?](https://stackoverflow.com/questions/36817604/how-to-change-and-reload-python-code-in-waitress-without-restarting-the-server)
- Allow CSV import using dev server
