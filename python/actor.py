class Actor:
    nconst = ""
    ordering = 0
    category = ""

    def __init__(self,actordata):
        if len(actordata) == 3:
            self.nconst = actordata[0]
            self.ordering = actordata[1]
            self.category = actordata[2]

