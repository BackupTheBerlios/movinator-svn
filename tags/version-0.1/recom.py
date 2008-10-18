import dbaccess
import math

class Recommender:
    """Objects of this class assign a score betweem 0 and 5 to a movie."""

    def __init__(self, db):
        """Creates a new object. db is the DBAcess object that returns info
        about the movies."""
        self.db = db

    def needsLearning(self):
        """Returns true if the reccomender uses a machine learning model that 
        needs a learning stage."""
        return False

    def learn(self):
        """Implements the learning stage of a recommender that uses machine 
        learning."""
        pass

    def score(self, movie):
        """Receives a movie (in the format defined in the DBAcess class), and
        returns a recomendation score. In this case, the score is the average
        of the movie ratings."""
        sum = 0.0
        if len(movie["ratings"]) == 0:
            return 0
        else:
            for i in movie["ratings"]:
                sum = sum + i[1]
            return sum/len(movie["ratings"])


class GMRecommender(Recommender):
    """Recommmender whose score is the geometric mean of the ratings. Returns 0
    if there are no ratings."""

    def score(self, movie):
        sum = 0.0
        if len(movie["ratings"]) == 0:
            return 0
        else:
            for i in movie["ratings"]:
                if i[1] == 0:
                    return 0
                sum = sum + math.log(i[1])
            return math.exp(sum/len(movie["ratings"]))




if __name__ == "__main__":
    dba = dbaccess.DBAccess("moviedb.db")
    r = Recommender(dba)
    m = dba.getMovie(50)
    print m
    print r.score(m)

    gmr = GMRecommender(dba)
    print gmr.score(m)
