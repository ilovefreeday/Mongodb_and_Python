# dbh.usrs is a typo, we mean dbh.users!  Unlike an RDBMS, MongoDB won't
# protect you from this class of mistake.
dbh.usrs.insert(user_doc)

# safe=True ensures that your write
# will succeed or an exception will be thrown
dbh.users.insert(user_doc, safe=True)

# w=2 means the write will not succeed until it has
# been written to at least 2 servers in a replica set.
dbh.users.insert(user_doc, w=2)

# Assuming we already have a database handle in scope named dbh
# find a single document with the username "janedoe".
user_doc = dbh.users.find_one({"username" : "janedoe"})
if not user_doc:
    print "no document found for username janedoe"

# Assuming we already have a database handle in scope named dbh
# find all documents with the firstname "jane".
# Then iterate through them and print out the email address.
users = dbh.users.find({"firstname":"jane"})
for user in users:
    print user.get("email")

# Only retrieve the "email" field from each matching document.
users = dbh.users.find({"firstname":"jane"}, {"email":1})
for user in users:
    print user.get("email")

# Find out how many documents are in users collection, efficiently
userscount = dbh.users.find().count()
print "There are %d documents in users collection" % userscount

# Return all user with firstname "jane" sorted
# in descending order by birthdate (ie youngest first)
users = dbh.users.find(
    {"firstname":"jane"}).sort(("dateofbirth", pymongo.DESCENDING))
for user in users:
    print user.get("email")

# Return all user with firstname "jane" sorted
# in descending order by birthdate (ie youngest first)
users = dbh.users.find({"firstname":"jane"},
    sort=[("dateofbirth", pymongo.DESCENDING)])
for user in users:
    print user.get("email")

# Return at most 10 users sorted by score in descending order
# This may be used as a "top 10 users highscore table"
users = dbh.users.find().sort(("score", pymongo.DESCENDING)).limit(10)
for user in users:
    print user.get("username"), user.get("score", 0)

# Return at most 20 users sorted by name,
# skipping the first 20 results in the set
users = dbh.users.find().sort(
    ("surname", pymongo.ASCENDING)).limit(20).skip(20)

# Traverse the entire users collection, employing Snapshot Mode
# to eliminate potential duplicate results.
for user in dbh.users.find(snapshot=True):
    print user.get("username"), user.get("score", 0)

# run the update query, using the $set update modifier.
# we do not need to know the current contents of the document
# with this approach, and so avoid an initial query and
# potential race condition.
dbh.users.update({"username":"janedoe"},
    {"$set":{"email":"janedoe74@example2.com"}}, safe=True)

# update the email address and the score at the same time
# using $set in a single write.
dbh.users.update({"username":"janedoe"},
    {"$set":{"email":"janedoe74@example2.com", "score":1}}, safe=True)

# once we supply the "multi=True" parameter, all matched documents
# will be updated
dbh.users.update({"score":0},{"$set":{"flagged":True}}, multi=True, safe=True)

# Delete all documents in user collection with score 1
dbh.users.remove({"score":1}, safe=True)

# Delete all documents in user collection
dbh.users.remove(None, safe=True)