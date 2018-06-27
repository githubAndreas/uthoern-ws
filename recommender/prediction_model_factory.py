from sklearn.linear_model import Ridge
from sklearn.neighbors import KNeighborsRegressor


class PredictionModelFactory:

    @staticmethod
    def get(model: str):
        if model == 'linear_model.Ridge':
            return Ridge()

        if model == 'neighbors.KNeighborsRegressor':
            return KNeighborsRegressor()

        # reg = KNeighborsRegressor(n_neighbors=2,n_jobs=-1)
        # reg = LinearRegression(n_jobs=-1)
        # reg = Lasso
        # reg = BayesianRidge()
        # reg = SVR(C=1.0, epsilon=0.2)
        return None
