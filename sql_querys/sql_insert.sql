create function insert_into_secure_matrix_object() returns trigger as
$on_object_create$
declare
	object_id int := (select id from objects order by id desc limit 1);
	users_ar int[] := (select array_agg(id) from users);
	x int;
	user_role text;
	creator_id int;
begin
	raise info '%', users_ar;
	creator_id  := (select owner_id from objects where id=object_id);
	if users_ar is not NULL then
		foreach x in array users_ar
		loop
			if x = creator_id then 
				insert into secure_matrix
					values(object_id, x, '1111');
			else
				user_role = (select role from users where id=x);
				if user_role='admin' then 
					insert into secure_matrix
						values(object_id, x, '1110');
				else
					insert into secure_matrix
						values(object_id, x, '1000');
				end if;
			end if;
		end loop;
		return NEW;
	else
		return NEW;
	end if;
end;
$on_object_create$ language plpgsql;

create function insert_into_secure_matrix_user() returns trigger as
$on_user_create$
declare
	user_id int := (select id from users order by id desc limit 1);
	object_ar int[] := (select array_agg(id) from objects);
	x int;
begin
	if object_ar is not NULL then 
		foreach x in array object_ar
		loop
			insert into secure_matrix
				values(x, user_id, '1000');
		end loop;
		return NEW;
	else
		return NEW;
	end if;
end;
$on_user_create$ language plpgsql;

create trigger on_object_create
	after insert on objects
	execute function insert_into_secure_matrix_object();

create trigger on_user_create
	after insert on users
	execute function insert_into_secure_matrix_user();
	
insert into users
	values(default, 'admin', 'admin');

insert into objects
	values(default, 2, 'test_3', 'test_uri')