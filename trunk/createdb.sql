drop table movie;
drop table critic;
drop table rates;

create table movie (
       mid integer primary key autoincrement,
       title text not null,
       year integer,
       director text,
       original_title text,
       rating integer,
       status integer not null,
       unique (original_title, year),
       check (rating >= 0 and rating <= 5),
       check (status >= 1 and status <= 4)
);

create table critic (
       cid integer primary key autoincrement,
       initials text unique not null,
       name text
);

create table rates (
       cid integer,
       mid integer,
       rating integer not null,
       primary key (cid,mid),
       --foreign key cid references critic,
       --foreign key mid references movie,
       check (rating >= 0 and rating <= 5)       
);
