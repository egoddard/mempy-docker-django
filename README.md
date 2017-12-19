# Django Development with Docker and Docker Compose

This is the repo for the December 2017 MemPy talk on using Docker Compose for Django development. We'll run through an overview of Docker, Docker Compose, and look at some basic examples. After that, we'll start setting up our Django project, starting with a basic Dockerfile and working our way up to using Docker Compose to spin up three containers: one for our app, one for Redis, and one for Postgres.

This example is based on the [Docker Compose Django Quickstart](https://docs.docker.com/compose/django/), but with some changes. The changes are primarily to fix permissions issues caused by the root user running inside of the container.

## Overview
  * What is Docker?
  * What is Docker Compose?
  * Setup
  * Creating the Django project Dockerfile
  * Enabling docker-compose
    * Django app, postgres app, redis

## What is Docker

Docker is a tool for running isolated processes or code. It is kind of like a
virtual machine, but Docker virtualizes the OS instead of the hardware. It uses
your OS's kernel space and isn't seperated from the host by the hypervisor.
This allows Docker containers to start up a lot faster (and put a lot less
strain on your battery!). Using Docker helps keep your environments consistent
across development and production.

### Installing docker

https://docs.docker.com/compose/install/

* Don't use the version that is in your distribution's package manager; it is probably old. Add the official Docker repo for your distro so you're up to date.

## Some basic examples

### __Example 1__: Docker processes 

This example shows how Docker is different from a traditional VM. The command
below starts a container named mongo, removes it when it is stopped and runs it
in the background:

`$ docker container run -d --rm --name mongo mongo`

View the running containers on your system:

`$ docker container ls`

Execute the command `ps aux` in the running container named mongo:

`$ docker container exec mongo ps aux`

We can see the same process running on the host machine:
`$ ps aux | grep mongod`

### __example 2__: SciPy up and running with the SciPy stack with one command

https://github.com/jupyter/docker-stacks/tree/master/scipy-notebook

__WARNING__: SciPy is not a small project. The container created by the
following command is several gigabytes in size.

`$ docker run -it --rm -p 8888:8888 -v $(pwd):/home/jovyan/work jupyter/scipy-notebook`

In example 1, the container we run is just `mongo`, while in example 2
it is `jupyter/scipy-notebook`. The containers are fetched from
[Docker Hub](https://hub.docker.com), the official Docker container registry.
Docker Hub contains many images, some contributed by Docker (official images)
and others added by the community. You can differentiate official images from
community images based on the name: official images won't have a prefix.
Containers from other organizations or individuals will include their name as
part of the container name.

## Dockerizing a Django app

### Basic Dockerfile

So far we've been running containers from Docker Hub, unmodified. We can also
use the container images on Docker Hub as a base for creating our own
containers. To do this, we create a `Dockerfile` that specifies the Docker Hub
image to use as a base, and then we provide some additional commands. Once our
Dockerfile is ready, we can build it.

[Basic Dockerfile](./1-basic-dockerfile/Dockerfile)

Build the container and then run it with the following commands:

`$ docker build -t django-basic .`

`$ docker container run -it --rm django-basic`

You should have a shell inside the container. Try creating a Django project:

`$ django-admin startproject docker .`

You can also start up the development server with `$ python manage.py runserver`

Use `ctrl+c` to kill the server and typ `exit` to leave the container.

### Problems with the basic config

1. We can't access the server from our host machine
1. Our project disappeared when we killed the container 
1. Files created inside the container are owned by root (_may not apply_
   _to Windows and Linux environments_)

The first two issues can be corrected by passing some additional parameters in
to our `docker container run` command:

`docker container run -it -p 8000:8000 -v $(pwd):/app django-basic`

This command:

  * binds ports (-p) 8000 in the container to 8000 on the host
  * creates a volume (-v) for persistent storage. Our current working directory
    on the host will be mapped to `/app` in the container.


### Dockerfile permissions fix

If you're using Docker for Windows/Mac, you may not have this problem. On
linux, we need our container user to run as a normal user, which requires
a few additions to our Dockerfile. First, we need to include 
[gosu](https://github.com/tianon/gosu) in our container, then we configure an
`ENTRYPOINT` script that sets up our non-root user. Any commands we specify in
the Dockerfile (via `CMD`) or that we pass in to the container during the
`docker container run` command will be run after the `ENTRYPOINT` script.

[2-dockerfile-with-entrypoint/Dockerfile](./2-dockerfile-ith-entrypoint/Dockerfile)

Build the container and then run `bash` in the container, overriding the default command:

`$ docker build -t django-permissions .`

`$ docker container run -it --rm -p 8000:8000 -v $(pwd):/app django-permissions bash`

You should have a shell inside the container. Try creating a Django project:

`$ django-admin startproject docker .`

Now type `exit` to leave the container and run the `django-permissions`
container with no command. The development server should start:

`docker container run --rm -p 8000:8000: -v $(pwd):/app django-permissions`

Visiting `localhost:8000` in your host's browser should show the Django 2.0 start page. It works! That's a lot of command to run and parameters to remember everytime you want to development though. we can simplify this setup and make it more reproducible with Docker Compose.


### Docker Compose Basics

Docker compose is a tool for defining and running multiple containers. It is
used primarily for local development and CI workflows, however recent versions
can also be used in production with Docker Swarm. Just like Docker and the
`Dockerfile`, `docker-compose` allows you to create a `docker-compose.yml`
file that defines a number of services (containers) to be used together, set
environment variables, and configure other container options you would normally pass into the `docker container run` command. 

Take a look at 
[3-docker-compose/docker-compose.yml](./3-docker-compose/docker-compose.yml).
You can see that there are several parameters that map to some of the options
we passed to `docker container run`. With the `docker-compose.yml` file
configured, running `docker-compuse up` starts up both our django (serving code
from the current directory) and postgres database containers defined in the
compose file:

`$ docker-compose up`

Arbitrary commands can be run in the container with `docker-compose run <service> <cmd>`:

`$ docker-compose run django bash`

`docker-compose` automatically creates a network for the services listed in a `docker-compose.yml` file. The network is configured to use the service name for DNS. From the bash prompt in the `django` container, we can ping the postgres container using `$ ping postgres`.

Use `exit` to leave the container bash prompt. Run `docker-compose down` to shut down all of the services specified in the compose file.

We can take advantage of this setup and some environment variables to use
`docker-compose` to closely mimic our production environment. For our final project we'll setup a Django Rest Framework API to serve some spatial data using `docker-compose`.

### Final Project
The app in this project is a dockerized version of
https://github.com/egoddard/mempy-drf-gis. For more info about that project,
visit the repo. You should be able to follow along in that repo if you want
more info about that project, just skip any steps that mention `vagrant`,
`pip`, `mkvirtualenv` or steps involving database creation; all of that is
handled by Docker. Unlike the other examples so far, this example has a
complete Django project that we'll walk through to see how it is configured for
Docker.

#### [Direnv](https://direnv.net/)

In the last example's `docker-compose.yml`, you may have noticed we had
passwords and database urls, etc. in our compose file, which isn't good because
we want to commit that to version control. A better option is to load those
values from the environment. We can use `direnv` to automatically load/unload
environment variables when we enter directories, which we can reference in our `docker-compose.yml`

To make sure your environment variables are never committed to version control,
create a global `gitignore` file that contains `.envrc`, the file `direnv`
looks for in a directory:

```
$ touch ~/.gitignore_global
$ git config --global core.excludesfile ~/.gitignore_global
$ echo ".envrc" >> ~/.gitignore_global
```

After creating a `.envrc` file in a directory, any time you make changes to the file
you need to run `direnv allow` before the file will be reloaded.

Your `.envrc` should look something like this:

```
export POSTGRES_DB=osm
export POSTGRES_USER=osm
export POSTGRES_PASSWORD=mysecretpassword
export DATABASE_URL=postgis://osm:mysecretpassword@postgres:5432/osm
export SECRET_KEY='super_secret_key'
export DEBUG=True
```

We can reference these variables directly in our
[docker-compose.yml](./4-final-project/docker-compose.yml) file.

With the variables in the container, we can update
[settings.py](./4-final-project/gis/settings.py) to use
[djang-environ](https://github.com/joke2k/django-environ) to configure our 
database, secret key, and debug settings from environment varibales.

Run `$ docker-compose up` to start the containers and run the development
server.

Run `$ docker-compose run django python manage.py makemigrations osm` to
generate the migration for the `osm` app.

Run `$ docker-compose run django python manage.py migrate` to apply all migrations.

Finally, to load the data from the `osm_amenities.json` fixtures, run:

`$ docker-compose run django python manage.py loaddata osm_amenities.json`


### Additional Resources

* Getting started with Docker: https://docs.docker.com/get-started/
* Quickstart with Compose and Django: https://docs.docker.com/compose/django/
* Dockerfile Documentation:
* Compose Documentation: https://docs.docker.com/compose/