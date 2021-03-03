import database_connector as DataBase


class Actor:
    nconst = ""
    ordering = 0
    category = ""

    def __init__(self,actordata):
        if len(actordata) == 3:
            self.nconst = actordata[0]
            self.ordering = actordata[1]
            self.category = actordata[2]

    def getName(self):
        db = DataBase.DataBase()
        person = db.get_person_by_id(self.nconst)
        return person[1]
