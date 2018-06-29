# Uthoern WS

Playlist continuation recommender webservice.


### Installing

The first step is to install [Anaconda](https://anaconda.org/anaconda/python). Uthoern WS needs libaries like Pandas or scikit-learn and there are included in the Anaconda package.

Open the Anaconda Prompt, navigate into the project and execute the following statement:
```
pip install -r requirements.txt
```

### Execution

1. Go into the project where you can find the manage.py.
2. Run following statements:

```
python manage.py migrate
```

```
python manage.py runserver
```
3. Open your favorit browser and navigato to:
```
http://127.0.0.1:8000/dataset
```