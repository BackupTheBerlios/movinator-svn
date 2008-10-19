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
from recom import Recommender

import os.path
import math
import pickle

class FreqRecommender(Recommender):
    """The score produced by this recommender is the weighted average of the critic
    ratings given to the movie. The weights are the inverse frequency of the
    score for each critic. I.e.:

       score = \sum_{i \in C} r_i * w_{ri} / \sum_{i \in C} w_{ri}

    where C is the set of critics that rated the movie, r_i is the rating of
    critic i, and w_{ri} is defined as:

       w_{ri} = \log(N_i / n_{ri})

    where N_i is the number of ratings given by critic i and n_{ri} is the
    number of ratings with value r given by critic i."""

    def __init__(self, db, file):
        """Initializes the recommender. file is the name of the file where the
        statistics will be stored, so that they do not have to be recomputed
        every time."""
        Recommender.__init__(self, db)
        self.file = file
        self.wri = {}
        if os.path.isfile(file):
            self.__readStats(self.file)

    def needsLearning(self):
        return True

    def learn(self):
        """Computes the statistics w_{ri} for each critic and saves them in the
        statistics file. The w_{ri} are normalized such that the sum is 1."""
        for c in self.db.getCritics():
            count = [0, 0, 0, 0, 0, 0]
            n = 0.0
            for r in self.db.getCriticRatings(c[0]):
                count[r[1]] = count[r[1]] + 1
                n = n + 1
            if n == 0:
                continue

            self.wri[c[0]] = {}
            for i in range(6):
                if count[i] == 0:
                    count[i] = 1
                self.wri[c[0]][i] = math.log(n / count[i], 2)

        self.__saveStats(self.file)

    def score(self, movie):
        score = 0.0
        sum = 0.0
        for i in movie["ratings"]:
            score = score + i[1] * self.wri[i[0]][i[1]]
            sum = sum + self.wri[i[0]][i[1]]
        return score / sum

    def __readStats(self, file):
        f = open(file, "r")
        self.wri = pickle.load(f)
        f.close()

    def __saveStats(self, file):
        f = open(file, "w")
        pickle.dump(self.wri, f)
        f.close()




if __name__ == "__main__":
    dba = dbaccess.DBAccess("moviedb.db")
    r = FreqRecommender(dba, "freqs.stat")
    r.learn()
    print r.wri
    print

    m = dba.getMovie(50)
    print m
    print r.score(m)
    print

    del r

    r2 = FreqRecommender(dba, "freqs.stat")
    print r2.wri
    print r2.score(m)
