import actor


class Movie:
    id = ""
    title = ""
    startYear = 0
    runtimeMinutes = 0
    genres = []
    numVotes = 0
    averageRating = 0
    actors = []

    def __init__(self, moviedata):
        if len(moviedata) == 7:
            self.id = moviedata[0]
            self.title = moviedata[1]
            self.startYear = moviedata[2]
            self.runtimeMinutes = moviedata[3]
            self.genres = moviedata[4].split(",")
            self.averageRating = moviedata[5]
            self.numVotes = moviedata[6]
        else:
            print("Something was wrong with the movie")

    def addActors(self, actorlist):
        if actorlist:
            for actordata in actorlist:
                self.actors.append(actor.Actor(actordata))
