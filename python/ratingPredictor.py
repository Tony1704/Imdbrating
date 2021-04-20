import sys
import time
from functools import reduce

from networkx.drawing.tests.test_pylab import plt
from sklearn.model_selection import train_test_split
from sklearn.neural_network import MLPClassifier
from sklearn import tree
from sklearn.ensemble import RandomForestClassifier
from sklearn import svm
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import MinMaxScaler
from sklearn.neighbors import KNeighborsClassifier

import database_connector
from sklearn import preprocessing
import numpy as np


class ratingPredictor:

    def __init__(self, movies):
        self.y_test = []
        self.x_test = []
        self.movies = movies
        self.clf = None
        self.scaler = StandardScaler()

    # algorithm = tree, neural oder forest
    def learn(self, algorithm='tree'):
        nnmovies = self._prepareMoviesForNN()
        ratings = self._getYValues()
        if (algorithm == 'neural'):
            clf = MLPClassifier(hidden_layer_sizes=(100,100,100,100), activation="tanh", solver="sgd", verbose=True, max_iter=3000, early_stopping=True, learning_rate='adaptive')
        elif(algorithm == 'tree'):
            clf = tree.DecisionTreeClassifier()
        elif(algorithm == 'forest'):
            clf = RandomForestClassifier()
        else:
            print("Please choose valid Algortihm: tree, neural or forest. Setting Algorithm to forest...")
            clf = RandomForestClassifier()
        x = []
        y = []
        for line in nnmovies:
            x.append(line)
        for rating in ratings:
            y.append(int(rating))
        x_train, x_test, y_train, y_test = train_test_split(x, y, random_state=1, test_size=0.3)
        self.scaler.fit(x_train)
        x_train = self.scaler.transform(x_train)
        x_test = self.scaler.transform(x_test)
        self.x_test = x_test
        self.y_test = y_test
        #scaler.fit(y_train)
        #y_train = scaler.transform(y_train)
        #y_test = scaler.transform(y_test)
        print("Training started...")
        clf.fit(x_train, y_train)
        print("Training done.")
        print("Test score is:")
        print(clf.score(x_test, y_test))
        self.clf = clf
        return clf

    def predictMovie(self, movie):
        nnmovie = self._prepareMoviesForNN([movie])
        nnmovie = self.scaler.transform(nnmovie)
        return self.clf.predict(nnmovie)

    def predictAllTestValues(self):
        y_pred = []
        y_true = []
        for i in range(len(self.x_test)):
            y_pred.append(self.clf.predict([self.x_test[i]])[0])
            y_true.append(self.y_test[i])
        return y_pred, y_true

    def _getYValues(self):
        y = []
        for movie in self.movies:
            y.append(movie.averageRating)
        return y

    def plot_ratings(self):
        y = []
        values = self._getYValues()
        x = [1,2,3,4,5,6,7,8,9]
        for i in x:
            count = 0
            for j in range(10):
                j = i + 0.1*j
                count = count + values.count(j)
            y.append(count)
        return x,y


    def _secondsToStr(self, t):
        return "%d:%02d:%02d.%03d" % reduce(lambda ll, b: divmod(ll[0], b) + ll[1:], [(t * 1000,), 1000, 60, 60])

    def _print_progress(self,p, start_time):
        sys.stdout.write("\r" + str(p) + "% \t Time elapsed: " + self._secondsToStr(time.time() - start_time) + "s")
        sys.stdout.flush()

    def getAllGenres(self):
        genres = []
        for movie in self.movies:
            for genre in movie.genres:
                if genre in genres:
                    continue
                else:
                    genres.append(genre)
        return genres

    def _personIdEncoder(self):
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

    def _binariseRoles(self):
        roles = self.getAllRoles()
        lb = preprocessing.LabelBinarizer()
        lb.fit(roles)
        return lb

    def _binariseGenres(self):
        genres = self.getAllGenres()
        lb = preprocessing.LabelBinarizer()
        lb.fit(genres)
        return lb

    def _prepareMoviesForNN(self, singlemovie=None):
        if singlemovie != None:
            movies = singlemovie
        else:
            movies = self.movies
        mlmovies = []
        genresBinarizer = self._binariseGenres()
        roleBinarizer = self._binariseRoles()
        personEncoder = self._personIdEncoder()
        start_time = time.time()
        counter = 1
        total = len(movies)
        print("Converting data...")
        for movie in movies:
            genre1 = np.zeros(genresBinarizer.classes_.shape[0])
            genre2 = np.zeros(genresBinarizer.classes_.shape[0])
            genre3 = np.zeros(genresBinarizer.classes_.shape[0])
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
                    #personId = personEncoder.transform([movie.actors[i].nconst])[0]
                    personId= movie.actors[i].rating
                    # array = np.array([personId])
                    ordering = movie.actors[i].ordering
                    roleArray = roleBinarizer.transform([movie.actors[i].category])[0]
                    array = np.array([personId, ordering])
                    array = np.concatenate((array, roleArray))
                    actors.append(array)
                except IndexError:
                    array = np.zeros(roleBinarizer.classes_.shape[0]+2)
                    # array = np.array([0])
                    actors.append(array)
            mlmovie = np.array([len(movie.title), movie.startYear, movie.runtimeMinutes, movie.numVotes])
            mlmovie = np.concatenate((mlmovie, genre))
            for actor in actors:
                mlmovie = np.concatenate((mlmovie, actor))
            mlmovies.append(mlmovie)
            percentage = (counter / total) * 100
            self._print_progress(round(percentage, 2), start_time)
            counter = counter + 1
        print("\nData converted.")
        return mlmovies





    def printallmovies(self):
        for movie in self.movies:
            print(movie.getAsList())
