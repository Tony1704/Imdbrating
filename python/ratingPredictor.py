from sklearn.model_selection import train_test_split
from sklearn.neural_network import MLPClassifier

from python import database_connector
from sklearn import preprocessing
import numpy as np

class ratingPredictor:

    def __init__(self, movies):
        self.movies = movies

    def learn(self):
        nnmovies = self.prepareMoviesForNN()
        ratings = self.getYValues()
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

    def getYValues(self):
        y = []
        for movie in self.movies:
            y.append(movie.averageRating)
        return y

    def getAllGenres(self):
        genres = []
        for movie in self.movies:
            for genre in movie.genres:
                if genre in genres:
                    continue
                else:
                    genres.append(genre)
        return genres

    def personIdEncoder(self):
        db = database_connector.DataBase()
        nconsts = db.get_all_person_id()
        lb = preprocessing.LabelEncoder()
        lb.fit(nconsts)
        return lb

    def getAllRoles(self):
        movies = self.movies
        roles = []
        for movie in movies:
            for actor in movie.actors:
                if actor.category in roles:
                    continue
                else:
                    roles.append(actor.category)
        return roles

    def binariseRoles(self):
        roles = self.getAllRoles()
        lb = preprocessing.LabelBinarizer()
        lb.fit(roles)
        return lb

    def binariseGenres(self):
        genres = self.getAllGenres()
        lb = preprocessing.LabelBinarizer()
        lb.fit(genres)
        return lb

    def prepareMoviesForNN(self):
        movies = self.movies
        mlmovies = []
        genresBinarizer = self.binariseGenres()
        roleBinarizer = self.binariseRoles()
        personEncoder = self.personIdEncoder()
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
                    # array = np.array([personId])
                    ordering = movie.actors[i].ordering
                    roleArray = roleBinarizer.transform([movie.actors[i].category])[0]
                    array = np.array([personId, ordering])
                    array = np.concatenate((array, roleArray))
                    actors.append(array)
                except IndexError:
                    array = np.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
                    # array = np.array([0])
                    actors.append(array)
            mlmovie = np.array([movie.startYear, movie.runtimeMinutes])
            mlmovie = np.concatenate((mlmovie, genre))
            for actor in actors:
                mlmovie = np.concatenate((mlmovie, actor))
            mlmovies.append(mlmovie)
        return mlmovies

    def printallmovies(self):
        for movie in self.movies:
            print(movie.getAsList())