
user_doc = dbh.users.find_one({"facebook.username":"foofacebook"})


# update modifiers such as $set also support the dot notation
dbh.users.update({"facebook.username":"foofacebook"},
    {"$set":{"facebook.username":"bar"}}, safe=True)


# Atomically remove an email address from a user document race-free using the
# $pull update modifier
user_doc = {
    "username":"foouser",
    "emails":[
        {
         "email":"foouser1@example.com",
         "primary":True
        },
        {
         "email":"foouser2@example2.com",
         "primary":False
        },
        {
         "email":"foouser3@example3.com",
         "primary":False
        }
    ]
}
# Insert the user document
dbh.users.insert(user_doc, safe=True)
# Use $pull to atomically remove the "foouser2@example2.com" email sub-document
dbh.users.update({"username":"foouser"},
    {"$pull":{"emails":{"email":"foouser2@example2.com"}}}, safe=True)


# Use $push to atomically append a new email sub-document to the user document
new_email = {"email":"fooemail4@exmaple4.com", "primary":False}
dbh.users.update({"username":"foouser"},
    {"$push":{"emails":new_email}}, safe=True)





# Demonstrate usage of the positional operator ($) to modify
# matched sub-documents in-place.
user_doc = {
    "username":"foouser",
    "emails":[
        {
         "email":"foouser1@example.com",
         "primary":True
        },
        {
         "email":"foouser2@example2.com",
         "primary":False
        },
        {
         "email":"foouser3@example3.com",
         "primary":False
        }
    ]
}
# Insert the user document
dbh.users.insert(user_doc, safe=True)
# Now make the "foouser2@example2.com" email address primrary
dbh.users.update({"emails.email":"foouser2@example2.com"},
    {"$set":{"emails.$.primary":True}}, safe=True)
# Now make the "foouser1@example.com" email address not primary
dbh.users.update({"emails.email":"foouser1@example.com"},
    {"$set":{"emails.$.primary":False}}, safe=True)






user_doc = {
    "username":"foouser",
    "emails":[
        {
         "email":"foouser1@example.com",
         "primary":True
        },
        {
         "email":"foouser2@example2.com",
         "primary":False
        },
        {
         "email":"foouser3@example3.com",
         "primary":False
        }
    ]
}

dbh.users.insert(user_doc)
# If we place an index on property "emails.email",
# e.g. dbh.users.create_index("emails.email")
# this find_one query can use a btree index
user = dbh.users.find_one({"emails.email":"foouser2@example2.com"})




# Create index on username property
dbh.users.create_index("username")



# Create a compound index on first_name and last_name properties
# with ascending index direction
dbh.users.create_index([("first_name", pymongo.ASCENDING), ("last_name", pymongo.ASCENDING)])



# Create a compound index called "name_idx" on first_name and last_name properties
# with ascending index direction
dbh.users.create_index([
    ("first_name", pymongo.ASCENDING),
    ("last_name", pymongo.ASCENDING)
    ],
    name="name_idx")


# Create index in the background
# Database remains usable
dbh.users.create_index("username", background=True)


# Create index with unique constraint on username property
dbh.users.create_index("username", unique=True)


# Create index with unique constraint on username property
# instructing MongoDB to drop all duplicates after the first document it finds.
dbh.users.create_index("username", unique=True, drop_dups=True)
# Could equally be written:
# dbh.users.create_index("username", unique=True, dropDups=True)


# Create a compound index on first_name and last_name properties
# with ascending index direction
dbh.users.create_index([("first_name", pymongo.ASCENDING), ("last_name", pymongo.ASCENDING)])
# Delete this index
dbh.users.drop_index([("first_name", pymongo.ASCENDING), ("last_name", pymongo.ASCENDING)])


# Create index on username property called "username_idx"
dbh.users.create_index("username", name="username_idx")
# Delete index called "username_idx"
dbh.users.drop_index("username_idx")


# Create geospatial index on "user_location" property.
dbh.users.create_index([("user_location", pymongo.GEO2D), ("username", pymongo.ASCENDING)])



# Find the 10 users nearest to the point 40, 40 with max distance 5 degrees
nearest_users = dbh.users.find(
    {"user_location":
        {"$near" : [40, 40],
         "$maxDistance":5}}).limit(10)
# Print the users
for user in nearest_users:
    # assume user_location property is array x,y
    print "User %s is at location %s,%s" %(user["username"], user["user_location"][0],
        user["user_location"[1])



box = [[50.73083, -83.99756], [50.741404,  -83.988135]]
users_in_boundary = dbh.users.find({"user_location":{"$within": {"$box":box}}})



users_in_circle = dbh.users.find({"user_location":{"$within":{"$center":[40, 40, 5]}}}).limit(10)


# Find the 10 users nearest to the point 40, 40 with max distance 5 degrees
# Uses the spherical model provided by MongoDB 1.8.x and up

earth_radius_km = 6371.0
max_distance_km = 5.0
max_distance_radians = max_distance_km / earth_radius_km
nearest_users = dbh.users.find(
    {"user_location":
        {"$nearSphere" : [40, 40],
         "$maxDistance":max_distance_radians}}).limit(10)
# Print the users
for user in nearest_users:
    # assume user_location property is array x,y
    print "User %s is at location %s,%s" %(user["username"], user["user_location"][0],
        user["user_location"[1])



total_score = 0
for username in ("jill", "sam", "cathy"):
    user_doc = dbh.users.find_one({"username":username})
    total_score += user_doc.get("score", 0)



# Email each supplier of this product.
# Default value is the empty list so no special casing
# is needed if the suppliers property is not present.
for supplier in product_doc.get("suppliers", []):
    email_supplier(supplier)


# Using upsert=True
def edit_or_add_session(description, session_id):
    dbh.sessions.update({"session_id":session_id},
        {"$set":{"session_description":description}}, safe=True, upsert=True)



# User X adds $20 to his/her account, so we atomically increment
# account_balance and return the resulting document
ret = dbh.users.find_and_modify({"username":username},
    {"$inc":{"account_balance":20}}, safe=True, new=True)
new_account_balance = ret["account_balance"]



