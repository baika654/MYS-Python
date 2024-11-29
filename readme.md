# Mark My Spreadsheet (MYS) application

## Setup

The first thing to do is to clone the repository:

```sh
$ git clone https://github.com/baika654/MYS-Python.git
$ cd MYS-Python
```


Then install the dependencies:

```sh
$ pip install -r requirements.txt
```
Once `pip` has finished downloading the dependencies, perform a migration:

```sh
python manage.py migrate
```

Now start the server:

```sh
$ python manage.py runserver
```

And navigate to `http://127.0.0.1:8000/`.