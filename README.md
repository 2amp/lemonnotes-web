# LemonNotes Web (aka `lemonnotes_web`)

A web app version of LemonNotes! Made mostly for educational purposes. Use at your own risk!

## Setting up a development server
**(Work in progress; not guaranteed to work!)**
Clone the repo, set up a `virtualenv` if that's your thing, and install the required packages from `requirements.txt`:
```python
pip install -r requirements.txt
```

`lemonnotes_web` also depends on RabbitMQ as a message broker for Celery. Download and installation instructions can be found at [https://www.rabbitmq.com/download.html](https://www.rabbitmq.com/download.html). On Mac OS X, RabbitMQ can be installed using homebrew:
```shell
brew install rabbitmq
```

Start the RabbitMQ server with `rabbitmq-server`. If you installed RabbitMQ using homebrew, you may need to add `/usr/local/sbin` to your `PATH`. Next, start the Celery worker process and the Celery scheduler:
```python
celery -A lemonnotes_web worker --loglevel=info
celery -A lemonnotes_web beat
```

Run the server with ```python manage.py runserver```.
