import sqlite3


class DBAccess:
    """Class that provides access to the movie database.
       Uses SQLLite to store the data."""

    def __init__(self, data):
        """Creates a new object and opens a connection to the database."""
        self.con = sqlite3.connect(data)
        self.con.isolation_level = None
        self.cur = self.con.cursor()

    def closeDB(self):
        """Closes the connection."""
        self.con.close()

    def getMovie(self, mid):
        """Given an ID, returns all informationo about a movie. This is a
        dictionary containing: title, year, director, original_title, rating,
        status, list of ratings (ratings). Each rating in the list is a pair
        (critic id, rating)."""
        self.cur.execute(
            """select title, year, director, original_title,
                      rating, status
               from movie m
               where mid = ?""", (mid, ))
        i = self.cur.fetchone()
        if i is None:
            return None
        movie = {}
        for j, k in zip(self.cur.description, i):
            movie[j[0]] = k
        movie["ratings"] = self.getRatings(mid) # outer join does not work on sqlite3
        return movie

    def getRatings(self, mid):
        """Given an ID, returns all ratings given to a movie. Each rating in
        the list is a pair (critic id, rating)"""
        self.cur.execute(
            """select cid, rating
               from rates
               where mid = ?""", (mid, ))
        return list(self.cur)

    def listMovies(self):
        """Generator that lists all the movies in the database. Information is
        returned as in the getMovie funtion."""
        self.cur.execute(
            """select m.mid, m.title, m.year, m.director, m.original_title,
                      m.rating, m.status, r.cid, r.rating
               from movie m, rates r
               where m.mid = r.mid
               order by m.mid""")
        m = self.cur.fetchone()
        while m != None:
            m_ant = m[0]

            movie = {}
            for j, k in zip(self.cur.description[:7], m[:7]):
                movie[j[0]] = k

            ratings = []
            while m!= None and m_ant == m[0]:
                ratings.append(m[7:])
                m = self.cur.fetchone()

            movie["ratings"] = ratings

            yield movie

    def getCriticRatings(self, critic):
        """Generator that returns a list of ratings for a given critic. The list
        contains mid,rating pairs."""
        self.cur.execute("select mid,rating from rates where cid = ?",
                         (critic, ))
        for i in self.cur:
            yield i        

    def getCritics(self):
        """Returns the contents of the critics table, i.e., a list of tuples
        (cid,initials,name)."""
        self.cur.execute("select * from critic")
        return list(self.cur)

    def getMaxMID(self):
        """Returns the maximum id of the movies in the database."""
        self.cur.execute("select max(mid) from movie")
        return self.cur.fetchone()[0]

    def updateMovie(self, mid, field, value):
        """Updates a field in a movie in the database."""
        self.cur.execute(
            """update movie
               set """ + field + """ = ?
               where mid = ?""", (value, mid))

    def updateRating(self, mid, cid, rating):
        """Updates a rating given by critic cid to movie mid. If the movie did
        not have a rating from that critic, adds it."""
        self.cur.execute(
            """select rating
               from rates
               where mid = ? and cid = ?""", (mid, cid))
        if len(self.cur.fetchall()) > 0:
            self.cur.execute(
                """update rates
                   set rating = ?
                   where mid = ? and cid = ?""", (rating, mid, cid))
        else:
            self.cur.execute(
                """insert into rates(mid, cid, rating)
                   values (?, ?, ?)""", (mid, cid, rating))

    def delMovie(self, mid):
        """Removes a movie and all related info from the database."""
        self.cur.execute("delete from movie where mid = ?", (mid,))
        self.cur.execute("delete from rates where mid = ?", (mid,))

    def insMovie(self, title, year, director, original_title, rating, status):
        """Inserts a new movie in the database. Returns the mid of the inserted
        movie."""
        mid = self.getMaxMID() + 1
        self.cur.execute(
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

#    for i in dba.listMovies():
#        print i
#    print

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

    dba.delMovie(mid)
