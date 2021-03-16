import database_connector as DataBase


class Actor:
    def __init__(self,actordata):
        if len(actordata) == 3:
            self.nconst = actordata[0]
            self.ordering = actordata[1]
            self.category = actordata[2]
        else:
            print("Something was wrong with the Actor")

    def getName(self):
        db = DataBase.DataBase()
        person = db.get_person_by_id(self.nconst)
        db.closeConnection()
        return person[1]

    def getAsList(self):
        return [self.nconst, self.ordering, self.category]
