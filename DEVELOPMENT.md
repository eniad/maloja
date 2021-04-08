# Development using Docker

Once prepped, the local development container can be run using this docker run command.

```bash
docker run -it --rm -p 42010:42010 \
  -v /home/$USER/git/maloja:/usr/src/app \
  -v /home/$USER/git/maloja/.local:/data \
  --env-file .env \
  maloja_dev
```

<!-- Or you can use the equivalent docker-compose command.

```bash
docker-compose up
``` -->

**But... There are some steps to prepare for using the above command.**

## Prep for local development

Maloja requires the data directory to be setup before local development can be done easily.

1. Copy and populate `.env`.

    1. Copy `./development/.env.sample` to `.env`
    1. Populate the variables with your API keys. See [README.md](./README.md) for links to get API keys. Note: This is optional, but you won't have images.
    1. Leave other variables as they are. They're needed for Docker to run Maloja correctly!

1. Optional: Export your scrobbles into an `scrobbles.csv`. See Maloja [Data](./README.md#data) for how to export your list from last.fm. You can also use the examples in `example_scrobbles.csv` or use that file to create your own test data. Importing scrobbles may take a long time depending on how many you have. If your `.local/data_files` already has scrobbles, Maloja will ask you if you want to override the existing scrobbles. You can rename the `scrobbles.csv` file to avoid the interaction, or just answer.

1. Setup local files for local development. Assume Maloja repo was cloned to `/home/$USER/git/maloja`. Persistent volumes are used to allow development.

    ```bash
    ./development/setup_local_directories.sh
    ```

    note: `Building wheel for lxml (setup.py)` during pip install of requirements takes a long time.

    This will create a `.local` folder as a persistent volume for Maloja data files during local development. The Docker entrypoint `--target dev_setup` is [`./development/maloja_install.sh`](./development/maloja_install.sh) which installs, starts, and stops the server to setup local files. This can't be done in Dockerfiles because the persistent volumes are mounted after build.

    The docker container is re-built to change the entry point.

1. Run the container for development.  The server is started directly using python to allow changes to be reflected by the server.

    ```bash
    docker run -it --rm -p 42010:42010 \
      -v /home/$USER/git/maloja:/usr/src/app \
      -v /home/$USER/git/maloja/.local:/data \
      --env-file .env \
      maloja_dev
    ```

    note: Build will be much faster this time because of Docker cacheing.

## Advantages

- Isolates dev environment with no dependencies installed on host. Only dependency is Docker.
- Same base docker image as production Maloja.
- Persistent storage and mounted volume allow for development on the host while server is running in a container.

## Future imporovements

- Elevate to docker-compose files.
- Squash commits.
- Omit writing build artifacts instead of removing them after the fact.
- Run build as non-root user instead of changing ownership of local data_files after they are written.
- Consider a better test of success instead of checking for log entry that gets

## Done

- [x] Copy maloja/data_files to default location in container using Dockerfile commands
- [x] Run using maloja.server directly, i.e. `python -m maloja.server`
- [x] ~~... without setup.py build/install~~ The setup script is working fine.
   - python module can be used _after_ `python setup.py install && maloja start && maloja stop`
- [x] Automatically updated content on edits. See these resources:
  - [Bottle Tutorial Auto Reloading](https://bottlepy.org/docs/dev/tutorial.html#auto-reloading)
  - [How to change and reload python code in waitress without restarting the server?](https://stackoverflow.com/questions/36817604/how-to-change-and-reload-python-code-in-waitress-without-restarting-the-server)
  - Works by simply using `python -m maloja.server`. Maybe read more about waitress to understand why that works.
- [x] Read about Doreah and understand how Maloja uses it for local dev
  - Doreah is a personal util for the main Majola dev.
- [x] Figure out CSV import using dev server
- [x] See if there is a way to
    1. not write dist/, build/, and malojaserver.egg-info OR
    1. write them into .local OR
    1. just `rm` them after setup
- [x] Set up user for Docker container to avoid `root` owning files
  - Just changing the ownership after the fact achieves the same result, but it would be better to run as the user in the first place.
- [x] Reference DEVELOPMENT.md in README.md Docker section
