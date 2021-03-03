import database_connector
import movie


def databasetesting(movies):
    for line in movies:
        print(line.getAsString())


def loadDataBase():
    db = database_connector.DataBase()
    movies = []
    for line in db.get_valid_movies():
        newMovie = movie.Movie(line)
        newMovie.addActors(db.get_crew_of_movie(newMovie.id))
        movies.append(newMovie)
    return movies


if __name__ == '__main__':
    databasetesting(loadDataBase())
