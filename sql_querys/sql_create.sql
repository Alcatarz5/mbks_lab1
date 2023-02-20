create table users(
	id integer primary key generated always as identity,
	name text not null,
	role text not null
);

create table objects(
	id integer primary key generated always as identity,
	owner_id integer references users (id) on delete cascade,
	name text not null,
	uri text not null
);

create table secure_matrix(
	object_id integer references objects (id) on delete cascade,
	user_id integer references users (id) on delete cascade,
	rights text not null,
	
	primary key (object_id, user_id)
);