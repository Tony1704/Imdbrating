import sys
import time
from functools import reduce

import database_connector
import movie
import numpy as np
from sklearn.neural_network import MLPRegressor
from sklearn.model_selection import train_test_split
import ratingPredictor


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

def printallmovies(movies):
    for movie in movies:
        print(movie.getAsList())

# Gibt zeit und prozent aus
def _secondsToStr(t):
    return "%d:%02d:%02d.%03d" % reduce(lambda ll, b: divmod(ll[0], b) + ll[1:], [(t * 1000,), 1000, 60, 60])

def _print_progress(p, start_time):
    sys.stdout.write("\r" + str(p) + "% \t Time elapsed: " + _secondsToStr(time.time() - start_time) + "s")
    sys.stdout.flush()

#Lädt die Filme aus der Datenbank ins Python Programm, befüllt das array movies
def loadDataBase():
    start_time = time.time()
    counter = 1
    odd = True
    db = database_connector.DataBase()
    movies = []
    print("Loading Database...")
    query = db.get_valid_movies()
    total = len(query)
    for line in query:
        newMovie = movie.Movie(line)
        newMovie.addActors(db.get_crew_of_movie(newMovie.id))
        movies.append(newMovie)
        percentage = (counter / total) * 100
        if (odd == True):
            _print_progress(round(percentage, 2), start_time)
            counter = counter + 1
            odd = False
        else:
            odd = True
            counter = counter + 1
    db.closeConnection()
    print("\nDatabase loaded.")
    return movies


def createMovie(title,startYear, runtime, genre1, genre2, genre3, numVotes):
    genres = "" + genre1
    if genre2 != "":
        genres = genres + "," + genre2
    if genre3 != "":
        genres = genres + "," + genre3
    array = [0,title,startYear, runtime,genres,0,numVotes]
    newMovie = movie.Movie(array)
    return newMovie

def updateAvgRatings():
    start_time = time.time()
    counter = 1
    db = database_connector.DataBase()
    personids = db.get_all_person_id()
    print(personids)
    total = len(personids)
    for person, averageR in personids:
        if averageR is None:
            avgRating = db.get_averagerating_by_id(person)
            db.update_avg_rating(person,avgRating)
        percentage = (counter / total) * 100
        _print_progress(round(percentage, 2), start_time)
        counter = counter + 1


if __name__ == '__main__':
    ratingPredictor = ratingPredictor.ratingPredictor(loadDataBase())
    ratingPredictor.learn(algorithm='neural')
    #print(ratingPredictor.plot_ratings())
    #loadDataBase()
    ourMovie = createMovie("Wolf ;)",1994,125,"Drama","Horror","Romance",49989)
    ourMovie.addCrewByName("Jack Nicholson", "actor")
    ourMovie.addCrewByName("Michelle Pfeiffer", "actress")
    ourMovie.addCrewByName("James Spader", "actor")
    ourMovie.addCrewByName("Ennio Morricone", "composer")
    ourMovie.addCrewByName("Mike Nichols", "director")
    #ourMovie.addCrewByName("Giuseppe Rotunno", "cinematographer")
    ourMovie.addCrewByName("Jim Harrison", "writer")
    #ourMovie.addCrewByName("Kate Nelligan", "actress")
    ourMovie.addCrewByName("Wesley Strick", "writer")
    ourMovie.addCrewByName("Douglas Wick", "producer")
    print(ourMovie.getAsString())
    print(ratingPredictor.predictMovie(ourMovie))






