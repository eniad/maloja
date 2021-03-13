# Development using Docker

Once prepped, the local development container can be run using the same docker run command.

```bash
docker run -it --rm -p 42010:42010 -v /home/$USER/git/maloja:/usr/src/app -v /home/$USER/git/maloja/.local:/data --env-file .env maloja_dev
```

Or you can use the equivalent docker-compose command.

```bash
docker-compose up
```

**But... There are some steps to prepare for using the above command.**

## Prep for local development

Maloja requires the data directory to be setup before local development can be done easily.

1. Set up local files in a persistent local directory. This gets wierd.

    ```bash
    mkdir -p .local/data_files
    cp -r maloja/data_files .local/data_files
    ```

1. Edit the Dockerfile to switch the `dev` stage ENTRYPOINT to `/bin/bash/`. The Dockerfile should contain these lines:

    ```Dockerfile
    ENTRYPOINT /bin/bash
    # ENTRYPOINT python -m maloja.server
    ```

1. Start a Docker container for local development. Assume maloja repo was cloned to `/home/$USER/git/maloja`. Persistent volumes are used to allow development.

    ```bash
    docker build -f Dockerfile --target dev -t maloja_dev .
    docker run -it --rm -p 42010:42010 -v /home/$USER/git/maloja:/usr/src/app -v /home/$USER/git/maloja/.local:/data --env-file .env maloja_dev
    ```

    note: `Building wheel for lxml (setup.py)` during pip install of requirements takes a long time.

1. Inside the container, install maloja. This can't be done in Dockerfiles because the persistent volumes are mounted after build.

    The setup script will add `dist/`, `build` and `malojaserver.egg-info` directories in your local directory. Those can be deleted.

    ```bash
    python setup.py install
    maloja start
    maloja stop
    ```

    The maloja data directory is not setup correctly for subsequent runs.

1. Re-edit the Dockerfile to switch the `dev` stage ENTRYPOINT to `python -m maloja.server`. The Dockerfile should contain these lines:

    ```Dockerfile
    # ENTRYPOINT /bin/bash
    ENTRYPOINT python -m maloja.server
    ```

1. Re-build and run Docker container. The server is now started directly using python.

    ```bash
    docker build -f Dockerfile --target dev -t maloja_dev .
    docker run -it --rm -p 42010:42010 -v /home/$USER/git/maloja:/usr/src/app -v /home/$USER/git/maloja/.local:/data --env-file .env maloja_dev
    ```

    note: Build will be much faster this time because of Docker cacheing.

## Advantages

- Isolated dev environment with no dependencies installed on host
- Same base image a production maloja

## TODO:

- [x] Copy maloja/data_files to default locaton in container using Dockerfile commands
- [x] Run using maloja.server directly, i.e. `python -m maloja.server`
- [ ] ... without setup.py build/install
   - python module can be used _after_ `python setup.py install && maloja start && maloja stop`
- [x] Automatically updated content on edits. See these resources:
  - [Bottle Tutorial Auto Reloading](https://bottlepy.org/docs/dev/tutorial.html#auto-reloading)
  - [How to change and reload python code in waitress without restarting the server?](https://stackoverflow.com/questions/36817604/how-to-change-and-reload-python-code-in-waitress-without-restarting-the-server)
  - Works by simply using `python -m maloja.server`. Maybe read more about waitress to understand why that works.
- Read about Doreah and understand how maloja uses it for local dev
- Figure out CSV import using dev server
- Set up user for Docker container following the ansible-nas convention to avoid `root` owning files
- Reference DEVELOPMENT.md in README.md Docker section
- Squash commits
