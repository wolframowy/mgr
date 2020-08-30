
# MRM Table

Jakub Kierejsza's master thesis and django based program for finding registration parameters of human metabolite spectra.

## Installing / Getting started

For application to work it requires metabolite data from [hmdb.ca](https://www.hmdb.ca "HMDB") in MongoDB database in form presented in /django_test/hmdb/submodels/.
For processing look into /HMDB/pymongo_workspace.py for initial data load and processing and for /HMDB/mongo_scripts_to_run.js for second data processing.

You can run dev server with following commands executed in /django_test/ folder.

```shell
pip install req.txt
py manage.py runserver
```

Above code installs all required packages and start a server at address localhost:8000. If you want to use different name (ex. 127.0.0.1) you will need to add it in /django_test/django_test/settings.py.


### Deploying / Publishing

Application as it is is not ready to be published. This project is designed to be behind proxy-server. You'll need to configure it using nginx or gunicorn and run it as generic wsgi project from /django_test/ folder.

Example
```shell
gunicorn django_test.wsgi
```

## Features

* Table visualization of metabolite registration parameters
* Simple search through metabolite data
* Processing of hmdb metabolite data to calculate metabolite registration parameters

## Contributing

If you'd like to contribute or, please fork the repository and use a feature
branch. Pull requests are warmly welcome.

## Licensing

The code in this project is licensed under MIT license.