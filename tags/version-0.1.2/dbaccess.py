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


import sqlite3

class DBAccess:
    """Class that provides access to the movie database.
       Uses SQLLite to store the data."""

    def __init__(self, data):
        """Creates a new object and opens a connection to the database."""
        self.con = sqlite3.connect(data)
        self.con.isolation_level = None

    def closeDB(self):
        """Closes the connection."""
        self.con.close()

    def getMovie(self, mid):
        """Given an ID, returns all informationo about a movie. This is a
        dictionary containing: title, year, director, original_title, rating,
        status, list of ratings (ratings). Each rating in the list is a pair
        (critic id, rating)."""
        cur = self.con.cursor()
        cur.execute(
            """select title, year, director, original_title,
                      rating, status
               from movie m
               where mid = ?""", (mid, ))
        i = cur.fetchone()
        if i is None:
            return None
        movie = {}
        for j, k in zip(cur.description, i):
            movie[j[0]] = k
        movie["ratings"] = self.getRatings(mid) # outer join does not work on sqlite3
        return movie

    def getRatings(self, mid):
        """Given an ID, returns all ratings given to a movie. Each rating in
        the list is a pair (critic id, rating)"""
        cur = self.con.cursor()
        cur.execute(
            """select cid, rating
               from rates
               where mid = ?""", (mid, ))
        return list(cur)

    def listMovies(self):
        """Generator that lists all the movies in the database. Information is
        returned as in the getMovie funtion."""
        cur = self.con.cursor()
        cur.execute(
            """select mid, title, year, director, original_title, rating, status
               from movie m
               order by m.mid""")
        m = cur.fetchone()
        while m != None:
            movie = {}
            for j, k in zip(cur.description, m):
                movie[j[0]] = k
            movie["ratings"] = self.getRatings(m[0]) # outer join does not work on sqlite3
            m = cur.fetchone()
            yield movie

    def getCriticRatings(self, critic):
        """Generator that returns a list of ratings for a given critic. The list
        contains mid,rating pairs."""
        cur = self.con.cursor()
        cur.execute("select mid,rating from rates where cid = ?",
                         (critic, ))
        for i in cur:
            yield i        

    def getCritics(self):
        """Returns the contents of the critics table, i.e., a list of tuples
        (cid,initials,name)."""
        cur = self.con.cursor()
        cur.execute("select * from critic")
        return list(cur)

    def getMaxMID(self):
        """Returns the maximum id of the movies in the database."""
        cur = self.con.cursor()
        cur.execute("select max(mid) from movie")
        mid = cur.fetchone()[0]
        if mid == None:
            return 0
        else:
            return mid

    def updateMovie(self, mid, field, value):
        """Updates a field in a movie in the database."""
        cur = self.con.cursor()
        cur.execute(
            """update movie
               set """ + field + """ = ?
               where mid = ?""", (value, mid))

    def updateRating(self, mid, cid, rating):
        """Updates a rating given by critic cid to movie mid. If the movie did
        not have a rating from that critic, adds it."""
        cur = self.con.cursor()
        cur.execute(
            """select rating
               from rates
               where mid = ? and cid = ?""", (mid, cid))
        if len(cur.fetchall()) > 0:
            cur.execute(
                """update rates
                   set rating = ?
                   where mid = ? and cid = ?""", (rating, mid, cid))
        else:
            cur.execute(
                """insert into rates(mid, cid, rating)
                   values (?, ?, ?)""", (mid, cid, rating))

    def delRating(self, mid, cid):
        """Deletes a rating given by critic cid to movie mid."""
        cur = self.con.cursor()
        cur.execute(
            """delete from rates
               where mid = ? and cid = ?""", (mid, cid))

    def delMovie(self, mid):
        """Removes a movie and all related info from the database."""
        cur = self.con.cursor()
        cur.execute("delete from movie where mid = ?", (mid,))
        cur.execute("delete from rates where mid = ?", (mid,))

    def insMovie(self, title, year, director, original_title, rating, status):
        """Inserts a new movie in the database. Returns the mid of the inserted
        movie."""
        cur = self.con.cursor()
        mid = self.getMaxMID() + 1
        cur.execute(
            """insert into movie(mid, title, year, director, original_title, 
                                 rating, status)
               values (?, ?, ?, ?, ?, ?, ?)""",
            (mid, title, year, director, original_title, rating, status))
        return mid




if __name__ == "__main__":
    dba = DBAccess("moviedb.db");
    print dba.getMovie(9)
    print dba.getRatings(9)
    m = dba.listMovies()
    print

    print m.next()
    print m.next()
    print m.next()
    print

    for i in dba.getCriticRatings(5):
        print "5: ", i

    print dba.getCritics()

    print dba.getMaxMID()

    print dba.getMovie(9)
    dba.updateMovie(9, "status", 3)
    print dba.getMovie(9)

    dba.updateRating(9, 1, 0)
    dba.updateRating(9, 4, 0)
    print dba.getRatings(9)


    mid = dba.insMovie("xpto", 1997, "ze", "optx", 3, 1)
    dba.updateRating(mid, 1, 0)
    dba.updateRating(mid, 2, 5)
    dba.updateRating(mid, 3, 3)
    print mid, dba.getMovie(mid)

    dba.delRating(mid, 3)
    print dba.getMovie(mid)

    dba.delMovie(mid)

#    print "----"
#    for m in dba.listMovies():
#        print m
