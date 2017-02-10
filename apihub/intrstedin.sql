---BLOGDEMO sql

insert into basic_auth.users (email,pass,name,role,verified) values
('ranjanprj@gmail.com','ranjanprj', 'Ranjan Prj', 'author','TRUE'),
('mayank13@gmail.com','mayank13', 'Mayank', 'author','TRUE');

drop table if exists public.email_interest_areas;
drop table if exists public.interest_areas;
create table if not exists public.interest_areas(
	id BIGSERIAL primary key , 
	area_type text,
	area_name text unique
	
);
insert into public.interest_areas(area_type,area_name) values 
('Technology','Programming'),('Technology','Computer'),('Technology','AI'),
('News','International'),('News','Local'),('News','Event');


create table if not exists public.email_interest_areas(
	email text,
	area_name_id INTEGER references interest_areas(id) 
);



grant select on table public.interest_areas,email_interest_areas to author;
grant insert on table public.interest_areas,email_interest_areas to author;

grant delete on table public.email_interest_areas to author;

ALTER TABLE public.email_interest_areas ENABLE ROW LEVEL SECURITY;
drop policy if exists authors_eigenedit on public.email_interest_areas;
create policy authors_eigenedit on public.email_interest_areas
  using (true)
  with check (
    email = basic_auth.current_email()
  );
  
  insert into public.email_interest_areas values('ranjanprj@gmail.com',1);
  insert into public.email_interest_areas values('ranjanprj@gmail.com',2);
  
  select * from public.interest_areas;
  
  
  select * from public.email_interest_areas;
  
  
  ---------------------------------------------
  -- INTEREST range
  -------------------------------
drop policy if exists authors_for_view on public.intrst_range;
drop policy if exists authors_eigenedit on public.intrst_range;
drop table if exists public.intrst_range;  
create table if not exists public.intrst_range(email text UNIQUE, intrst_range text check (intrst_range in ('city','state','country','beyond')) default 'city');
ALTER TABLE public.intrst_range ENABLE ROW LEVEL SECURITY;
grant select on table public.intrst_range to author;
grant insert on table public.intrst_range to author;
grant update on table public.intrst_range to author;

drop policy if exists authors_eigenedit on public.intrst_range;
create policy authors_eigenedit on public.intrst_range
  using (email = basic_auth.current_email())
  with check (
    email = basic_auth.current_email()
);

drop policy if exists authors_for_view on public.intrst_range;
create policy authors_for_view on public.intrst_range FOR SELECT 
  using (email = basic_auth.current_email() );
  

insert into public.intrst_range values('mayank13@gmail.com','city');
insert into public.intrst_range values('jaydeep@gmail.com','city');
select * from intrst_range;
delete  from intrst_range;  
  

--- GEOLOCATION

drop policy if exists authors_for_view on public.geo_location;
drop policy if exists authors_eigenedit on public.geo_location;


drop table if exists public.geo_location;
create table if not exists public.geo_location(
	email text UNIQUE,
	latitude numeric,
	longitude numeric,
	altitude numeric,
	altitude_accuracy numeric,
	heading numeric,
	speed numeric,
	time_stamp timestamp,
	address text,
	city text,
	state text,
	country text,
	full_address json
	
);

ALTER TABLE public.geo_location ENABLE ROW LEVEL SECURITY;
grant select on table public.geo_location to author;
grant insert on table public.geo_location to author;
grant update on table public.geo_location to author;

drop policy if exists authors_eigenedit on geo_location;
create policy authors_eigenedit on public.geo_location
  using (email = basic_auth.current_email())
  with check (
    email = basic_auth.current_email()
);

drop policy if exists authors_for_view on public.geo_location;
create policy authors_for_view on public.geo_location FOR SELECT 
  using (email = basic_auth.current_email() );
  
 
 insert into public.geo_location values('ranjanprj@gmail.com',12.12,12.12,12.12,12.12,12.12,12.12,now(),'address');
 delete from public.geo_location; 
 select * from public.geo_location;
 -- Actual parameter values may differ, what you see is a default string representation of values

 

drop function if exists geo_reverse(numeric,numeric);

create extension if not exists plpython3u;
CREATE FUNCTION geo_reverse (lon numeric, lat numeric)
  RETURNS text
AS $$
import json
from geopy.geocoders import Nominatim
geolocator = Nominatim()
location = geolocator.reverse("{0},{1}".format(lat,lon))
return json.dumps(location.raw)
$$ LANGUAGE plpython3u;



REVOKE ALL on function geo_reverse(numeric,numeric) from PUBLIC;

grant execute on function
  geo_reverse(numeric,numeric)  
  to author;

select geo_reverse(73.8844305,18.5630778);

---NEWS Sites
drop table if exists public.news_content;
drop table if exists public.news_sites;
create table if not exists public.news_sites (id bigserial primary key,name text,url text,typeof text);
create table if not exists public.news_content (author text ,title text,typeof text,news text,news_sites_id BIGSERIAL references news_sites(id),intrst_type text,intrst_area text);
grant select on public.news_content,public.news_sites to author;

---TWITTER data
drop table if exists public.twitter;
create table if not exists public.twitter(tweets json);
drop table if exists public.twitter_content;
create table if not exists public.twitter_content(id bigserial,email text,created_at timestamptz, author text,tweet text,retweet_count int,favorite_count int,content_type text default 'timeline');




  
ALTER TABLE public.twitter_content ENABLE ROW LEVEL SECURITY;
grant select on table public.twitter_content to author;
grant insert on table public.twitter_content to author;




drop policy if exists twitter_timeline_for_view on public.twitter_content;
create policy twitter_timeline_for_view on public.twitter_content FOR SELECT 
  using (email = basic_auth.current_email() );
  
 