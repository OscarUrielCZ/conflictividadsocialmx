-- as root user

create user confmx_user@localhost identified by 'ring0star.?';
grant all on confmx.* to confmx_user@localhost;

-- as new user

create database confmx;

use confmx;

create table sites(
    id integer primary key auto_increment,
    url varchar(150) unique not null,
    name varchar(50) not null,
    fullname varchar(80),
    enabled boolean not null default true,
    added_date datetime not null default now()
);

create table queries_sites (
    id integer auto_increment,
    site_id integer not null,
    homepage_article_links varchar(120),
    article_title varchar(120),
    article_body varchar(120),
    article_date varchar(120),
    article_time varchar(120),
    article_location varchar(120),
    article_image varchar(120),
    primary key (id, site_id),
    foreign key (site_id) references sites(id) on delete cascade
);

create table articles (
    id integer auto_increment primary key auto_increment,
    site_id integer not null,
    url varchar(255) not null,
    title varchar(255),
    body text not null,
    date datetime,
    image_link varchar(255),
    location varchar(100),
    foreign key (site_id) references sites(id)
);