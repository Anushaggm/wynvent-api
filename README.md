#Wynvent API

* Python 3.4.3

* Django 1.11.1

* PostgreSQL 9.6.3

* Django REST 3.6.3

* Elasticsearch 2.4.1 with geopy

##Installation

1. Clone the repo `git@bitbucket.org:sambavaram/wynvent.git`.

2. Install Python 3, and create a virtual environment. `virtualenv -p python3 wynvent`

3. Activate the environment by running `source wynvent/bin/activate`

4. Create `local_settings.py`. There is a file `local_settings.py.template` for reference.

5. Run `pip install -r requirements.txt`

6. Create Postgres database, and add PostGis extension to enable spatial queries.

7. Apply database migrations. `python manage.py migrate`

8. Create superuser. `python manage.py createsuperuser`

##Execution
Run `python manage.py runserver`. The backend will then run on `http://localhost:8000/`

##Deployment

Deployment is done to servers running on AWS EC2 instance.

Staging server run on the branch `develop` and production server to be run on the branch `master`.
Do local development on a new feature branch by checking out from `develop`. Merge to `develop` after review.

1. `cd ".\wynvent"`

2. `git add .` Add everything

3. `git commit -m <message>`

4. `git push origin <branch_name>`
