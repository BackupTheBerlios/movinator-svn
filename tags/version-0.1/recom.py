# Copyright 2008 Pavel Calado

# This file is part of Movinator. Movinator is free software: you can
# redistribute it and/or modify it under the terms of the GNU General Public
# License as published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.

# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more
# details.

# You should have received a copy of the GNU General Public License along with
# this program.  If not, see <http://www.gnu.org/licenses/>.


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
