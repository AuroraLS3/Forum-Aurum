# User Stories

### As a site visitor

- I can see what is the most active area
- I can see what is the hot topic of the week
- I can see how many topics have been posted
- I can see how many messages have been posted

### As a Guest

- I can view a possible introduction area that a moderator has created
- I can start new threads in areas I can view
- I can edit messages I have posted (Including thread starting messages)
- I can remove threads I have started
- I can post messages in areas I can view
- I can remove messages I have posted
- I can use Markdown formatting in messages

### As a Member

- I can do everything a Guest can
- I can view more areas
- I can start new threads in areas I can view
- I can post messages in threads I can view

### As a Moderator

- I can do everything a Member can
- I can remove threads and messages of other users
- I can promote Guests to Member role
- I can create new areas and select role that can see them
- I can remove Guest and Member users
- I am protected from role changes by Moderators
- I am protected from user removal by Moderators (Unless Moderator role is revoked)

### As an Admin

- I can do everything a Moderator can
- I can change roles of any account
- I can remove any account
- I am protected from role changes by Moderators
- I am protected from user removal (Unless Admin role is revoked)

## SQL Related to stories

Statements are PostgreSQL.

#### Most active area
```
SELECT area.name, COUNT(*) as c FROM message 
JOIN topic on message.topic_id = topic.id 
JOIN area on topic.area_id = area.id 
GROUP BY area.id ORDER BY c DESC LIMIT 1
```
#### Hot topic of the week  
```
SELECT topic.name, COUNT(*) as c FROM message 
JOIN topic on message.topic_id = topic.id 
WHERE message.created > now() - INTERVAL '1 WEEK' 
GROUP BY topic.id ORDER BY c DESC LIMIT 1
```
#### Posted topics
```
SELECT COUNT(*) as c FROM topic LIMIT 1
```
#### Posted messages
```
SELECT COUNT(*) as c FROM message LIMIT 1
```

#### View area
```
SELECT * FROM area WHERE name=?
```

#### Start new topics
```
INSERT INTO topic (name, created, account_id, area_id) VALUES (?, ?, ?, ?);
INSERT INTO message (content, created, account_id, topic_id) VALUES (?, ?, ?, ?);
```

#### Edit posted messages
```
UPDATE message SET content=? WHERE topic_id=? AND created=?;
```

#### Remove threads
```
DELETE FROM message WHERE topic_id=?;
DELETE FROM topic WHERE id=?;
```

#### Remove messages
```
DELETE FROM message WHERE id=?;
```

#### Change account role
```
DELETE FROM user_role WHERE account_id=?;
INSERT INTO user_role (account_id, role_id) VALUES (?, ?) # run as batch
```

#### Remove account (and content created by the account)
```
DELETE FROM user_role WHERE account_id=?;
DELETE FROM message JOIN topic ON topic.id=message.topic_id WHERE topic.account_id=?;
DELETE FROM topic WHERE account_id=?;
DELETE FROM account WHERE id=?;
```
