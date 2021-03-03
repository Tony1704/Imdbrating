import database_connector
import movie

def databasetesting():
    db = database_connector.DataBase()
    movies = []
    print(db.get_person_by_id("nm0001877"))
    print(db.get_person_by_name("Zac Efron"))
    for line in db.get_valid_movies():
        newMovie = movie.Movie(line)
        newMovie.addActors(db.get_crew_of_movie(newMovie.id))
        movies.append(newMovie)
    print(len(movies))
    print(movies[3000].actors[0].nconst)

if __name__ == '__main__':
    databasetesting()
