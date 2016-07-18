create table foo (id serial primary key, geo geography(POINT, 4326));

insert into foo (geo) values
(ST_GeographyFromText('SRID=4326;POINT(-110 30)'));
insert into foo (geo) values
(ST_GeographyFromText('POINT(-111 30)'));
insert into foo (geo) values
(ST_GeographyFromText('POINT(-110 30)'));
insert into foo (geo) values
(ST_GeographyFromText('POINT(-111.2 30)'));
insert into foo (geo) values
(ST_GeographyFromText('POINT(-112 30)'));
insert into foo (geo) values
(ST_GeographyFromText('POINT(-113 30)'));
insert into foo (geo) values
(ST_GeographyFromText('POINT(-111.001 30)'));

create index foo_geo_gix on foo using gist (geo);

-- distance between two points
select ST_Distance(
    ST_GeographyFromText('POINT(-110 30)'),
    ST_GeographyFromText('POINT(-111 30)'));

-- things within distance
select id, ST_AsText(geo), ST_Distance(ST_GeographyFromText('POINT(-111 30.01)'), geo) from foo where ST_DWithin(
    ST_GeographyFromText('POINT(-111 30.01)'),
    geo,
    100000);
