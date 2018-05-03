# Database

## Table schema

![schema](https://github.com/Rsl1122/Forum-Aurum/blob/master/documentation/drawio/img/Schema-v3.1.png?raw=true)

## Create Table statements (PostGreSQL)

### Role table
```
CREATE TABLE role (
 	id SERIAL NOT NULL, 
 	name VARCHAR(100), 
 	PRIMARY KEY (id)
);
```
### Account table
```
CREATE TABLE account (
 	id SERIAL NOT NULL, 
 	name VARCHAR(100), 
 	created TIMESTAMP WITHOUT TIME ZONE, 
 	password VARCHAR(150), 
 	PRIMARY KEY (id)
);
```
### Account-Role table
```
CREATE TABLE user_role (
 	id SERIAL NOT NULL, 
 	account_id INTEGER, 
 	role_id INTEGER, 
 	PRIMARY KEY (id), 
 	FOREIGN KEY(account_id) REFERENCES account (id), 
 	FOREIGN KEY(role_id) REFERENCES role (id)
);
```
### Area table
```
CREATE TABLE area (
 	id SERIAL NOT NULL, 
 	name VARCHAR(100), 
 	description VARCHAR(5000), 
 	created TIMESTAMP WITHOUT TIME ZONE, 
 	role_id INTEGER NOT NULL, 
 	PRIMARY KEY (id), 
 	FOREIGN KEY(role_id) REFERENCES role (id)
);
```
### Topic table
```
CREATE TABLE topic (
 	id SERIAL NOT NULL, 
 	name VARCHAR(100), 
 	created TIMESTAMP WITHOUT TIME ZONE, 
 	account_id INTEGER NOT NULL, 
 	area_id INTEGER NOT NULL, 
 	PRIMARY KEY (id), 
 	FOREIGN KEY(account_id) REFERENCES account (id), 
 	FOREIGN KEY(area_id) REFERENCES area (id)
);
```
### Message table
```
CREATE TABLE message (
 	id SERIAL NOT NULL, 
 	content VARCHAR(1000), 
 	created TIMESTAMP WITHOUT TIME ZONE, 
 	account_id INTEGER NOT NULL, 
 	topic_id INTEGER NOT NULL, 
 	PRIMARY KEY (id), 
 	FOREIGN KEY(account_id) REFERENCES account (id), 
 	FOREIGN KEY(topic_id) REFERENCES topic (id)
);
```
