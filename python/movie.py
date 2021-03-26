import actor
import database_connector as DatabaseConnector

class Movie:
    def __init__(self, moviedata):
        if len(moviedata) == 7:
            self.id = moviedata[0]
            self.title = moviedata[1]
            self.startYear = moviedata[2]
            self.runtimeMinutes = moviedata[3]
            self.genres = moviedata[4].split(",")
            self.averageRating = moviedata[5]
            self.numVotes = moviedata[6]
            self.actors = []
        else:
            print("Something was wrong with the movie")

    def addActors(self, actorlist):
        if actorlist:
            for actordata in actorlist:
                self.actors.append(actor.Actor(actordata))

    def getAsString(self):
        actornames = []
        for actor in self.actors:
            actornames.append(actor.getName())
        return self.title + " (" + str(self.startYear) +") Länge: " + str(self.runtimeMinutes) + "min Genres: " + str(self.genres) + " Bewertung: " + str(self.averageRating) + " mit " + str(self.numVotes) + " Bewertungen. Mit " + str(actornames)

    def addCrewByName(self, name, role):
        db = DatabaseConnector.DataBase()
        nconst = db.get_person_id_by_name(name)
        avgrating = db.get_averagerating_by_id(nconst[0])
        if nconst[0] is None:
            print("Actor not found!")
            return
        else:
            ordering = len(self.actors) + 1
            if ordering > 10:
                print("Too many Actors in Movie " + self.title)
            else:
                actordata = [nconst[0],ordering,role,avgrating]
                self.actors.append(actor.Actor(actordata))
        db.closeConnection()

    def getAsList(self):
        actors = []
        for actor in self.actors:
            actors.append(actor.getAsList())
        return [self.id, self.title, self.startYear, self.runtimeMinutes, self.genres, self.averageRating, self.numVotes, actors]

