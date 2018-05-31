from logger import Logger
from playlist_parser import PlaylistParser
from playlist_slice_converter import PlaylistSliceConverter
from ranging_matrix_factory import RangingMatrixFactory
from sklearn.neighbors import KNeighborsRegressor
from sklearn.linear_model import LinearRegression, Ridge, Lasso, BayesianRidge
from sklearn.svm import SVR
import numpy as np
from sklearn.model_selection import train_test_split
import math

if __name__ == '__main__':
    Logger.log_info('Start uthoern')
    file_collection = PlaylistParser.parse_folder('E:/Development/uthoern/test')
    # files = PlaylistParser.parse_folder('E:/Development/_data/mpd.v1/data')

    slices = PlaylistSliceConverter.from_json_files(file_collection)

    ranging_df = RangingMatrixFactory.create_data_frame(slices)
    template_ranging_matrix = RangingMatrixFactory.create_template_ranging_matrix(ranging_df)

    for column_index, target_column in enumerate(ranging_df.columns):
        Logger.log_info(
            'Model[' + str(column_index + 1) + '/' + str(len(ranging_df.columns)) + '] Name:' + target_column)

        # Testdaten
        # y = ranging_df[target_column]
		y = ranging_df.loc[:, target_column].as_matrix()
        X = ranging_df.drop(target_column, 'columns').as_matrix()

        X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=42)

        # Modele
        # reg = KNeighborsRegressor(n_neighbors=2,n_jobs=-1)
        # reg = LinearRegression(n_jobs=-1)
        reg = Ridge()
        # reg = Lasso
        # reg = BayesianRidge()
        # reg = SVR(C=1.0, epsilon=0.2)

        # Trainieren
        reg.fit(X_train, y_train)
        print("Score Trainingsdatensatz: {:.2f}".format(reg.score(X_train, y_train)))

        # vorhersage
        predicted_column = reg.predict(X_test)

        new_column = np.append(y_train, predicted_column)

        for row_index, row in ranging_df.iterrows():
            cell_value = row[target_column]
            #if cell_value < 1.0:
			if(not math.isclose(cell_value, 1.0, abs_tol=0.00000001))
                #ranging_df.at[target_column, row_index] = 
				ranging_df = ranging_df.set_value(row_index, target_column, new_column[row_index])

        print("Score Testdatensatz: {:.2f}".format(reg.score(X_test, y_test)))

    Logger.log_info('Stop uthoern')
