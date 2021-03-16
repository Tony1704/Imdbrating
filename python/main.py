import database_connector
import movie
import numpy as np
from sklearn.neural_network import MLPRegressor
from sklearn.datasets import make_regression
from sklearn.model_selection import train_test_split
from sklearn import preprocessing

def mltesting(movies):
    nn = MLPRegressor(hidden_layer_sizes=100, activation="logistic", solver="adam", verbose=True, max_iter=3000)
    x = []
    y = []
    for line in movies:
        mlmovie = [line.runtimeMinutes, line.startYear, line.numVotes]
        for i in range(10):
            try:
                mlmovie.append(line.actors[i].nconst[2:])
                mlmovie.append(line.actors[i].ordering)
            except IndexError:
                mlmovie.append(0)
                mlmovie.append(0)
        print(mlmovie)
        x.append(mlmovie)
        y.append(line.averageRating)
    x_train, x_test, y_train, y_test = train_test_split(x, y, random_state=1, test_size=0.3)
    x_train = np.array(x_train)
    x_test = np.array(x_test)
    nn.fit(x_train.astype(np.float64), y_train)
    print(nn.score(x_test.astype(np.float64), y_test))
    # print(nn.predict([[120, 2005, 60000]]))


def testing(movies):
    for line in movies:
        print(line.getAsList())

def labelBinariser(movies):
    db = database_connector.DataBase()
    nconsts = db.get_all_person_id()
    print(nconsts)
    lb = preprocessing.LabelBinarizer()
    print(lb.fit_transform(nconsts))
    print(lb.transform(['nm0051659, nm2860379']))

def printallmovies(movies):
    for movie in movies:
        print(movie.getAsList())


def loadDataBase():
    db = database_connector.DataBase()
    movies = []
    for line in db.get_valid_movies():
        newMovie = movie.Movie(line)
        newMovie.addActors(db.get_crew_of_movie(newMovie.id))
        movies.append(newMovie)
    db.closeConnection()
    return movies


if __name__ == '__main__':
    printallmovies(loadDataBase())
