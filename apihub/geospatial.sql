delete from user_loc;
insert into user_loc values('ranjanprj',ST_POINT(73.8893, 18.4593),now()),
('mayank',ST_POINT(73.8847 ,18.5641),now());


SELECT loc.username,
	   loc.lon,
	   loc.lat,
	   curr.lon,
	   curr.lat,        
	   ST_Distance(
  			ST_POINT(loc.lon,loc.lat)::geography, 
			--ST_POINT(72.8777, 19.0760 )::geography
			ST_POINT(curr.lon,curr.lat)::geography
) as distance_in_m
from user_loc as loc
join user_loc as curr
on loc.username <> curr.username
order by distance_in_m ;

grant select on table pg_authid, basic_auth.users, posts, comments, authors,twitter,user_loc_view to anon;
    SELECT first_name,last_name, salary FROM employees  
    WHERE salary >  
    (SELECT max(salary) FROM employees  
    WHERE first_name='Alexander');  

    
 create or replace view user_loc_view as
 select curr.username as current_user,other.username as other_user,curr.lon as clon,curr.lat as clat,other.lon as olon,other.lat as olat,
 	   ST_Distance(
  			ST_POINT(curr.lon,curr.lat)::geography, 
			--ST_POINT(72.8777, 19.0760 )::geography
			ST_POINT(other.lon,other.lat)::geography
) as distance_in_m

 from user_loc as curr
 inner join user_loc as other
 on curr.username <> other.username
order by distance_in_m;
    
SELECT ST_Distance(
  ST_Point(72.8777, 19.0760)::geography,
  ST_Point(73.8847, 18.5641)::geography
)/1000 as distance;
 


--- CONTACT table

create table if not exists  contacts(
	username text,
	contact_name text,
	contact_mob_no text 
); 

ALTER TABLE contacts ENABLE ROW LEVEL SECURITY;

drop policy if exists authors_eigenedit on contacts;
create policy authors_eigenedit on contacts
  using (true)
  with check (
    username = basic_auth.current_email()
  );


grant select, insert, update, delete
  on table posts, comments,contacts,user_loc to author;
  
