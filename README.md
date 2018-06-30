# Uthoern WS

Playlist continuation recommender webservice.


### Installing

The first step is to install [Anaconda](https://anaconda.org/anaconda/python). Uthoern WS needs libaries like Pandas or scikit-learn and there are included in the Anaconda package.

Open the Anaconda prompt, navigate into the project and execute the following statement:
```
pip install -r requirements.txt
```

### Execution

1. Go into the project where you can find the manage.py.
2. Run following statement:

```
python manage.py migrate
```
3. Create a folder named 'storage' and inside there create following folders: 'challenge_set', 'columns', 'decomposition_alg', 'mdp_set', 'ml_alg', 'recommendation_export'

4. Now you will find inside the project a file called 'db.sqlite3'. Open there with the SQL manager of your decision and execute following SQL Statements:

```
INSERT INTO recommender_decomposition (id, name) VALUES (1, 'LatentDirichletAllocation');
INSERT INTO recommender_decomposition (id, name) VALUES (2, 'NMF');
INSERT INTO recommender_decomposition (id, name) VALUES (3, 'TruncatedSVD');

INSERT INTO recommender_environment (id, name, challenge_set_dir_path, recommendation_dir_path, columns_dir_path, decomposition_alg_dir_path, ml_alg_dir_path, mdp_set_dir_path) VALUES (1, 'testing', 'storage/challenge_set', 'storage/recommendation_export', 'storage/columns', 'storage/decomposition_alg', 'storage/ml_alg', 'storage/mdp_set');

INSERT INTO recommender_model_algorithm (id, name) VALUES (1, 'linear_model.Ridge');
INSERT INTO recommender_model_algorithm (id, name) VALUES (2, 'neighbors.KNeighborsRegressor');
```



5. Run following statement:
```
python manage.py runserver
```
8. Open your favorit browser and navigato to:
```
http://127.0.0.1:8000/dataset
```