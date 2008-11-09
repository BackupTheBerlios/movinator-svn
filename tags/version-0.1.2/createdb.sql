drop table if exists movie;
drop table if exists critic;
drop table if exists rates;

create table movie (
       mid integer primary key,
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

-- 1 = c
-- 2 = f
-- 3 = v
-- 4 = a

create table critic (
       cid integer primary key,
       initials text unique not null,
       name text
);

insert into critic values(1, "C1", "Critic 1");
insert into critic values(2, "C2", "Critic 2");
insert into critic values(3, "C3", "Critic 3");
insert into critic values(4, "C4", "Critic 4");
insert into critic values(5, "C5", "Critic 5");

create table rates (
       cid integer,
       mid integer,
       rating integer not null,
       primary key (cid,mid),
       --foreign key cid references critic,
       --foreign key mid references movie,
       check (rating >= 0 and rating <= 5)       
);
