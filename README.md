# Description

Table builder API is a simple REST API which allows clients to create tables in database and to fill up them with data. The project uses `Django` framework to run server and `django-ninja` to expose REST API. It stores data in `PostgreSql` database.

# Installation

## Requirements

Project is hosted inside docker container so only requirement is to has `docker` and `docker-compose` already installed.
If you do not have it please follow:
* official docker installation guide: https://docs.docker.com/engine/install/
* officail docker-compose installation guide: https://docs.docker.com/compose/

## Installation steps

1. Pull git repository: `git clone https://github.com/PitterRup/table-builder-api.git`
2. Go in to root project directory: `cd table-builder-api`
3. Run `make init` command to create your local `.env` file
4. Run `make build` command to build docker images for database and web application.
5. Run `make start` command to start application. API should be available on `http://localhost:32321`
6. To stop application run `make stop` command.

# Usage

Table builder REST API exposes 4 endpoints.

* POST `/api/table/` - allows to create new table in database. Accepts table name and table fields declaration.
* PUT `/api/table/{table_id}` - allows to update table structure. Accepts new table fields declaration.
* POST `/api/table/{table_id}/row` - allows to add new table record. Payload validation is based on fields declaration.
* GET `/api/table/{table_id}/rows` - allows to fetch all table records.

# Documentation

Project is created with `django-ninja` so automatically generated documenation is available on `http://localhost:32321/api/docs`. You can also do test requests using provided interactive client available on documentation site.
