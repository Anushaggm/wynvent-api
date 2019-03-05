#!/bin/bash

PROJECT_DIR_PATH='/home/ubuntu/wynvent'
PROJECT_VIRTUAL_ENV_PATH='/home/ubuntu/virtual'

echo 'Activating virtual enviroment...'
. $PROJECT_VIRTUAL_ENV_PATH/bin/activate

echo 'Activating environment variables...'
. /home/ubuntu/envs/server.env

cd $PROJECT_DIR_PATH

python manage.py crunch_data