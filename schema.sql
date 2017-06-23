drop table if exists roomtemp;
create table roomtemp (
    id integer primary key autoincrement,
    temperature text not null,
    humidity text not null,
    timestamp text not null
);
