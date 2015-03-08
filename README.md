# LemonNotes Web (aka `lemonnotes_web`)

A web app version of LemonNotes! Made mostly for educational purposes. Use at your own risk!

## Setting up a development server
**(Work in progress; not guaranteed to work!)**
Clone the repo, set up a `virtualenv` if that's your thing, and install the required packages from `requirements.txt`:
```python
pip install -r requirements.txt
```

`lemonnotes_web` uses Postgres. On Mac OS X, [`Postgres.app`](http://postgresapp.com/) is probably the simplest way to get a Postgres installation. You may also use homebrew to install Postgres:
```shell
brew install postgresql
```

`lemonnotes_web` also depends on Redis as a message broker for Celery. Download and installation instructions can be found at [http://redis.io/](http://redis.io/). On Mac OS X, Redis can be installed using homebrew:
```shell
brew install redis
```

Start the Redis server with `redis-server`. Next, start the Celery worker process and the Celery scheduler:
```python
celery -A lemonnotes_web worker --loglevel=info
celery -A lemonnotes_web beat
```

Run the server with ```python manage.py runserver```.
