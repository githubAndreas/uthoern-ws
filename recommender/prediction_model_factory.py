from sklearn.linear_model import Ridge, LinearRegression, Lasso
from sklearn.neighbors import KNeighborsRegressor


class PredictionModelFactory:

    @staticmethod
    def get(model: str):
        if model == 'neighbors.KNeighborsRegressor':
            return KNeighborsRegressor(n_neighbors=3)

        if model == 'linear_model.LinearRegression':
            return LinearRegression()

        if model == 'linear_model.Ridge':
            return Ridge()

        if model == 'linear_model.Lasso':
            return Lasso(alpha=0.1)

        return None
