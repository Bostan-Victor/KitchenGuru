#!/bin/bash

# uwsgi --chdir=/Users/doschinescud/Documents/GitHub/KitchenGuru/Backend
#     --module=KitchenGuru.wsgi:application \
#     --env DJANGO_SETTINGS_MODULE=mysite.settings \
#     --master --pidfile=/tmp/project-master.pid \
#     --socket=127.0.0.1:49152 \      # can also be a file
#     --processes=5 \                 # number of worker processes
#     --uid=1000 --gid=2000 \         # if root, uwsgi can drop privileges
#     --harakiri=20 \                 # respawn processes taking more than 20 seconds
#     --max-requests=5000 \           # respawn processes after serving 5000 requests
#     --vacuum \                      # clear environment on exit
#     --home=/path/to/virtual/env \   # optional path to a virtual environment
#     --daemonize=/var/log/uwsgi/yourproject.log      # background the process

python3 manage.py makemigrations

sleep .10

python3 manage.py migrate

sleep .5

python3 manage.py collectstatic --no-imput

sleep .5 

python3 manage.py loaddata recipes.json

sleep .5

python3 manage.py loaddata recipe_images.json

sleep .5 

python3 manage.py loaddata ingredients.json

sleep .5

gunicorn KitchenGuru.wsgi:application -b 0.0.0.0:8000