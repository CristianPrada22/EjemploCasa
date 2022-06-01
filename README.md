# project_name

Django 3.1.1 + Postgres 11 + Dokku config (Production Ready)

## Documentation ##

The project has a requirements document which is hosted at the following link:
https://docs.google.com/document/d/1sPXStBqmgArgUppvDD705n8iP_wjbgbnHtVZsB5MZwA

### Kanban ###
```
The visualization and assignment of tasks and project requirements is handled on a Kanban board 
located in the Projects tab called "Base CMS E-Commerce". In the board there are 5 columns.
- To Do (pending tasks) 
- In progress (Tasks in progress)
- Review in progress
- Reviewer approved
- Done (tasks/requirements completed)

The Issues and notes are created in the To Do column. 
Notes are requirements to work in later.
issues are next or in progress requirements to develop.
```
### Steps to change the name of an application in Django: ###
```
-An application with the target name must be created.
-Copy the contents of the application to be renamed into the application with the target name.
-Delete the content of the application to be renamed. (delete the url in project_name)
-Execute the migration commands (makegrations and migrate), this is done to delete the DB tables.
-Delete the folder of the application to rename and delete the application record in the settings(common.py).
-Ready, you have renamed the app.

```
### Directory Tree ###
```

├── main (Main application of the project, use it to add main templates, statics and root routes)
│   ├── fixtures
│   │   ├── dev.json (Useful dev fixtures, by default it creates an `admin` user with password `admin`)
│   │   └── initial.json (Initial fixture loaded on each startup of the project)
│   ├── migrations
│   ├── static (Add here the main statics of the app)
│   ├── templates (Add here the main templates of the app)
│   ├── admin.py
│   ├── apps.py
│   ├── models.py (Main models like City, Config)
│   ├── tests.py (We hope you will put some tests here :D)
│   ├── urls.py (Main urls, place the home page here)
│   └── views.py
├── media
├── project_name
│   ├── settings
│   │   ├── partials
│   │   │   └── util.py (Useful functions to be used in settings)
│   │   ├── common.py (Common settings for different environments)
│   │   ├── development.py (Settings for the development environment)
│   │   └── production.py (Settings for production)
│   ├── urls.py
│   └── wsgi.py
├── scripts
│   ├── command-dev.sh (Commands executed after the development containers are ready)
│   └── wait-for-it.sh (Dev script to wait for the database to be ready before starting the django app)
├── static
├── Dockerfile (Instructions to create the project image with docker)
├── Makefile (Useful commands)
├── Procfile (Dokku or Heroku file with startup command)
├── README.md (This file)
├── app.json (Dokku deployment configuration)
├── docker-compose.yml (Config to easily deploy the project in development with docker)
├── manage.py (Utility to run most django commands)
└── requirements.txt (Python dependencies to be installed)
```

### How to install the template ###

Clone the repository, and update your origin url: 
```
git clone https://github.com/altixco/django-postgres-dokku project_name
cd project_name
```

Merge the addons required by your project (Optional):
```
git merge origin/rest
git merge origin/webpack
git merge origin/push-notifications
```

Rename your project files and directorys:
```
make name=project_name init
```
> Info: Make is required, for mac run `brew install make`

> After this command you can already delete the init command inside the `Makefile` 

The command before will remove the `.git` folder so you will have to initialize it again:
```
git init
git remote add origin <repository-url>
```

### How to run the project ###

The project use docker, so just run:

```
docker-compose up
```

> If it's first time, the images will be created. Sometimes the project doesn't run at first time because the init of postgres, just run again `docker-compose up` and it will work.

*Your app will run in url `localhost:8000`*

To recreate the docker images after dependencies changes run:

```
docker-compose up --build
```

To remove the docker containers including database (Useful sometimes when dealing with migrations):

```
docker-compose down
```

### Accessing Administration

The django admin site of the project can be accessed at `localhost:8000/admin`

By default the development configuration creates a superuser with the following credentials:

```
Username: admin
Password: admin
```

## Production Deployment: ##

The project is dokku ready, this are the steps to deploy it in your dokku server:

#### Server Side: ####

> This docs does not cover dokku setup, you should already have configured the initial dokku config including ssh keys

Create app and configure postgres:
```
dokku apps:create project_name
dokku postgres:create project_name
dokku postgres:link project_name project_name
```

> If you don't have dokku postgres installed, run this before:
> `sudo dokku plugin:install https://github.com/dokku/dokku-postgres.git`

Create the required environment variables:
```
dokku config:set project_name ENVIRONMENT=production DJANGO_SECRET_KEY=....
```

Current required environment variables are:

* ENVIRONMENT
* DJANGO_SECRET_KEY
* EMAIL_PASSWORD

Use the same command to configure secret credentials for the app

#### Local Side: ####

Configure the dokku remote:

```
git remote add dokku dokku@<my-dokku-server.com>:project_name
```

Push your changes and just wait for the magic to happens :D:

```
git push dokku master
```

Optional: To add SSL to the app check:
https://github.com/dokku/dokku-letsencrypt

Optional: Additional nginx configuration (like client_max_body_size) should be placed server side in:
```
/home/dokku/<app>/nginx.conf.d/<app>.conf
```

> Further dokku configuration can be found here: http://dokku.viewdocs.io/dokku/
