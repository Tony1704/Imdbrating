import database_connector
import movie
import numpy as np
from sklearn.neural_network import MLPRegressor, MLPClassifier
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


def learn(nnmovies, ratings):
    nn = MLPClassifier(hidden_layer_sizes=200, activation="tanh", solver="sgd", verbose=True, max_iter=3000)
    x = []
    y = []
    for line in nnmovies:
        x.append(line)
    for rating in ratings:
        y.append(int(rating))
    x_train, x_test, y_train, y_test = train_test_split(x, y, random_state=1, test_size=0.3)
    print(x_test, y_test)
    nn.fit(x_train, y_train)
    print(nn.out_activation_)
    print(nn.score(x_test, y_test))
    return nn


def testing(movies):
    for line in movies:
        print(line.getAsList())


def personIdEncoder():
    db = database_connector.DataBase()
    nconsts = db.get_all_person_id()
    lb = preprocessing.LabelEncoder()
    lb.fit(nconsts)
    return lb


def printallmovies(movies):
    for movie in movies:
        print(movie.getAsList())


def getAllGenres(movies):
    genres = []
    for movie in movies:
        for genre in movie.genres:
            if genre in genres:
                continue
            else:
                genres.append(genre)
    return genres


def getYValues(movies):
    y = []
    for movie in movies:
        y.append(movie.averageRating)
    return y


def getAllRoles():
    movies = loadDataBase()
    roles = []
    for movie in movies:
        for actor in movie.actors:
            if actor.category in roles:
                continue
            else:
                roles.append(actor.category)
    return roles


def binariseRoles():
    roles= getAllRoles()
    lb = preprocessing.LabelBinarizer()
    lb.fit(roles)
    return lb


def binariseGenres():
    genres = getAllGenres(loadDataBase())
    lb = preprocessing.LabelBinarizer()
    lb.fit(genres)
    return lb


def loadDataBase():
    db = database_connector.DataBase()
    movies = []
    for line in db.get_valid_movies():
        newMovie = movie.Movie(line)
        newMovie.addActors(db.get_crew_of_movie(newMovie.id))
        movies.append(newMovie)
    db.closeConnection()
    return movies


def prepareMoviesForNN(movies):
    mlmovies = []
    genresBinarizer = binariseGenres()
    roleBinarizer = binariseRoles()
    personEncoder = personIdEncoder()
    for movie in movies:
        genre1 = np.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
        genre2 = np.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
        genre3 = np.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
        if movie.genres is not None:
            genre1 = np.array(genresBinarizer.transform([movie.genres[0]])[0])
            if len(movie.genres) >= 2:
                genre2 = np.array(genresBinarizer.transform([movie.genres[1]])[0])
            if len(movie.genres) >= 3:
                genre3 = np.array(genresBinarizer.transform([movie.genres[2]])[0])
        genre = np.add(genre1, genre2)
        genre = np.add(genre, genre3)
        actors = []
        for i in range(10):
            try:
                personId = personEncoder.transform([movie.actors[i].nconst])[0]
                #array = np.array([personId])
                ordering = movie.actors[i].ordering
                roleArray = roleBinarizer.transform([movie.actors[i].category])[0]
                array = np.array([personId, ordering])
                array = np.concatenate((array, roleArray))
                actors.append(array)
            except IndexError:
                array = np.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
               #array = np.array([0])
                actors.append(array)
        mlmovie = np.array([movie.startYear, movie.runtimeMinutes])
        mlmovie = np.concatenate((mlmovie, genre))
        for actor in actors:
            mlmovie = np.concatenate((mlmovie, actor))
        mlmovies.append(mlmovie)
    return mlmovies


def createMovie(startYear, runtime, genre1, genre2, genre3):
    genres = "" + genre1
    if genre2 != "":
        genres = genres + "," + genre2
    if genre3 != "":
        genres = genres + "," + genre3
    array = [0,"",startYear, runtime,genres,0,0]
    newMovie = movie.Movie(array)
    return newMovie

if __name__ == '__main__':
    moviePredictor = learn(prepareMoviesForNN(loadDataBase()), getYValues(loadDataBase()))
    ourMovie = createMovie(1995,142,"Drama","","")
    ourMovie.addCrewByName("Frank Darabont","director")
    ourMovie.addCrewByName("Morgan Freeman", "actor")
    ourMovie.addCrewByName("Tim Robbins", "actor")
    print(ourMovie.genres)
    ournnMovie = prepareMoviesForNN([ourMovie])
    print(ournnMovie[0])
    print(moviePredictor.predict(ournnMovie))




