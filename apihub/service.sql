drop table if exists service_asset cascade;
drop table if exists service cascade;
drop table if exists booking_details cascade;
drop table if exists booking cascade;
drop table if exists service_payment_info cascade;
drop table if exists customer_payment_info cascade;
drop table if exists customer_payments cascade;


create table if not exists  service(
	id bigserial  primary key ,
	company_name text,
	service_name text,
	app_name text,	
	type text check (type in ('cleaning','gardening','pet','medical','consultation','personal')),
	service_email text references basic_auth.users(email)
	
);

create table if not exists service_asset(
	id  bigserial primary key,
	name text,
	type text,	
	is_booked bool,	
	current_lat numeric,
	current_lon numeric,
	service_id bigserial references service(id)
);


create table if not exists service_payment_info(
	id  bigserial primary key,
	payment_provider text,
	pub_key text,	
	service_id bigserial references service(id)
	
);

create table if not exists customer_payment_info(
	id  bigserial primary key,
	customer_payment_email text,
	customer_app_email text references basic_auth.users(email),
	token text,
	customer_id text,
	service_payment_info_id integer references service_payment_info(id)
);

create table if not exists booking(
	id  bigserial primary key,	
	created_at timestamptz default now(),
	booked_by text references basic_auth.users(email)
	
);

create table if not exists booking_details(		
	updated_at timestamptz default now(),
	booking_time timestamptz default now() CHECK (booking_time >= now()),
	status text check (status in ('initiated','inprogress','cancelled','rescheduled','rejected','completed')) default 'draft',
	booking_id bigserial references booking(id),
	booked_by text references basic_auth.users(email),
	service_id bigserial references service(id),
	booked_lat numeric,
	booked_lon numeric,
	error_log text
	
);

create table if not exists customer_payments(
	id  bigserial primary key,	
	amount numeric,
	currency varchar(3),
	payment_status text check( payment_status in ('initiated','successful','failed','cancelled','refunded')) default 'initiated',
	booking_id bigserial references booking(id),
	payment_time timestamptz default now(),
	error_log text
);

grant usage, select on sequence booking_id_seq, service_id_seq,customer_payments_id_seq to apiuser;
grant select on table service,service_asset,booking,booking_details,customer_payments,service_payment_info,customer_payment_info to apiuser;
grant insert on table booking,booking_details,customer_payments,service_payment_info,customer_payment_info to apiuser;
grant update on table booking,booking_details,customer_payments,service_payment_info,customer_payment_info to apiuser;

ALTER TABLE booking ENABLE ROW LEVEL SECURITY;
drop policy if exists apiuser_eigenedit on booking;
create policy apiuser_eigenedit on booking
  using (booked_by = basic_auth.current_email())
  with check (
    booked_by = basic_auth.current_email()
);

drop policy if exists apiuser_for_view on booking;
create policy apiuser_for_view on booking FOR SELECT 
  using (booked_by = basic_auth.current_email() );

  
 ALTER TABLE booking_details ENABLE ROW LEVEL SECURITY;
drop policy if exists apiuser_eigenedit on booking_details;
create policy apiuser_eigenedit on booking_details
  using (booked_by = basic_auth.current_email())
  with check (
    booked_by = basic_auth.current_email()
);

drop policy if exists apiuser_for_view on booking_details;
create policy apiuser_for_view on booking_details FOR SELECT 
  using (booked_by = basic_auth.current_email() );

------------------------------------------------------
--	insert statements 
	
insert into service(company_name,service_name,app_name,type,service_email) values('Car Wash Company','carwash_service','carwash_app', 'cleaning','ranjanprj@gmail.com');
insert into service_asset(name,type,is_booked,current_lat,current_lon,service_id) values('wasing van 1','locomotive','false',18.5630956,73.8844194,1) ;
insert into service_asset(name,type,is_booked,current_lat,current_lon,service_id) values('wasing van 1','locomotive','false',18.6630956,73.9844194,1) ;


insert into service_payment_info(payment_provider,pub_key,service_id) values('stripe','sk_test_dYakoNYe6QfUf2ptPuMbCA2E',1);
insert into booking(created_at,booked_by) values(now(),'ranjanprj@gmail.com');
--
--updated_at timestamptz default now(),
--	status text check (status in ('initiated','created','accepted','inprogress','cancelled','rescheduled','rejected','post_booking_cancelled')),
--	booking_id bigserial references booking(id),
--	booked_by text references basic_auth.users(email),
--	service_asset_id bigserial references service_asset(id),
--	booked_lat numeric,
--	booked_lon numeric
--	
	
insert into booking_details(booking_time,updated_at,status,booking_id,booked_by,service_id,booked_lat,booked_lon) values(now(),now(),'rescheduled',1,'ranjanprj@gmail.com',1,34.234,65.45);

--
--create or replace view service_booking_view as
--select sa.id as said,b.*,ST_Distance(
--  ST_Point(sa.current_lat, sa.current_lon)::geography,
--  ST_Point(b.booked_lat,b.booked_lon)::geography
--)/1000 as dist_in_km
--from booking_details as b inner join service_asset as sa
--on sa.id = b.service_id ;

drop view if exists service_booking_view;
create or replace view service_booking_view as
select s.*,sa.id as said,sa.current_lat,sa.current_lon,b.*,
ST_Distance(
  ST_Point(sa.current_lat, sa.current_lon)::geography,
  ST_Point(b.booked_lat,b.booked_lon)::geography
)/1000 as dist_in_km
from booking_details as b 
inner join service_asset as sa   on b.service_id = sa.service_id
inner join service s on s.id = sa.service_id;

grant select on table service_booking_view to apiuser;


