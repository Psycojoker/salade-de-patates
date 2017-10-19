# encoding: utf-8

import string
import random
import requests
from datetime import datetime

from pymongo import MongoClient

# boards template
# { "_id" : "9w6PGYCWbbN7RcZc3", "title" : "Welcome Board", "permission" : "private", "slug" : "welcome-board", "archived" : false, "createdAt" : ISODate("2017-10-14T09:40:02.086Z"), "stars" : 0, "labels" : [ { "color" : "green", "_id" : "Y9Pt9F", "name" : "" }, { "color" : "yellow", "_id" : "cMrA9W", "name" : "" }, { "color" : "orange", "_id" : "bmK3vt", "name" : "" }, { "color" : "red", "_id" : "HTNK4F", "name" : "" }, { "color" : "purple", "_id" : "Kfw6hX", "name" : "" }, { "color" : "blue", "_id" : "aYofHr", "name" : "" } ], "members" : [ { "userId" : "WsrKTCja75gJ2dPJj", "isAdmin" : true, "isActive" : true, "isCommentOnly" : false } ], "color" : "belize" }

# issue template
# { "_id" : "ed4BDN4aYqDqQMDXB", "title" : "test", "members" : [ ], "labelIds" : [ ], "listId" : "JexoQp3Ey5yxcMo66", "boardId" : "2QJHWiPWsfBYRa692", "sort" : 2.5, "archived" : false, "createdAt" : ISODate("2017-10-14T09:45:02.179Z"), "dateLastActivity" : ISODate("2017-10-14T09:47:24.728Z"), "userId" : "WsrKTCja75gJ2dPJj" }

# lists template
# > db.lists.find()
# { "_id" : "5mzZsnWpHsX9Gzgqz", "title" : "Basics", "boardId" : "9w6PGYCWbbN7RcZc3", "archived" : false, "createdAt" : ISODate("2017-10-14T09:40:02.120Z") }
# { "_id" : "wAp7qkgSD2hW2s8E4", "title" : "Advanced", "boardId" : "9w6PGYCWbbN7RcZc3", "archived" : false, "createdAt" : ISODate("2017-10-14T09:40:02.151Z") }
# { "_id" : "JexoQp3Ey5yxcMo66", "title" : "qsd", "boardId" : "2QJHWiPWsfBYRa692", "sort" : 1, "archived" : false, "createdAt" : ISODate("2017-10-14T09:40:27.036Z") }
# { "_id" : "WRbSb5bB3RQcwacnr", "title" : "deuxième colonne", "boardId" : "2QJHWiPWsfBYRa692", "sort" : 2, "archived" : false, "createdAt" : ISODate("2017-10-14T09:44:54.324Z"), "updatedAt" : ISODate("2017-10-15T21:18:13.165Z") }

# user template
# { "_id" : "WsrKTCja75gJ2dPJj", "createdAt" : ISODate("2017-10-14T09:40:02.074Z"), "services" : { "password" : { "bcrypt" : "$2a$10$d03ReriSSsiNMMn4mX0cJ.vXTQV9PKojnvcawLGZ49XwYD9CcfUA6" }, "email" : { "verificationTokens" : [ { "token" : "nnBk7vtCcpt-D6MGCHwmcaSjMHaJsqsbA9cLfZ3UKuC", "address" : "cortex@worlddomination.be", "when" : ISODate("2017-10-14T09:40:02.115Z") } ] }, "resume" : { "loginTokens" : [ { "when" : ISODate("2017-10-14T09:40:02.236Z"), "hashedToken" : "zX5kd3geZ68uPUU3ss4OaV17c0dmReD0ahRWNbOOXys=" } ] } }, "username" : "psycojoker", "emails" : [ { "address" : "cortex@worlddomination.be", "verified" : false } ], "isAdmin" : true, "profile" : {  } }


# one PR
# {
#     "data": {
#         "repository": {
#             "pullRequests": {
#                 "edges": [
#                     {
#                         "node": {
#                             "assignees": {
#                                 "edges": []
#                             },
#                             "author": {
#                                 "avatarUrl": "https://avatars2.githubusercontent.com/u/690304?v=4",
#                                 "login": "abeudin",
#                                 "resourcePath": "/abeudin",
#                                 "url": "https://github.com/abeudin"
#                             },
#                             "bodyText": "",
#                             "closed": true,
#                             "comments": {
#                                 "edges": [
#                                     {
#                                         "node": {
#                                             "author": {
#                                                 "avatarUrl": "https://avatars0.githubusercontent.com/u/1279740?v=4",
#                                                 "login": "Kloadut",
#                                                 "resourcePath": "/Kloadut",
#                                                 "url": "https://github.com/Kloadut"
#                                             },
#                                             "bodyText": "obsolete :)",
#                                             "createdAt": "2014-05-24T10:32:31Z",
#                                             "id": "MDEyOklzc3VlQ29tbWVudDQ0MDgzNTE1",
#                                             "updatedAt": "2014-05-24T10:32:31Z"
#                                         }
#                                     }
#                                 ]
#                             },
#                             "createdAt": "2014-05-17T16:57:46Z",
#                             "headRef": null,
#                             "headRefName": "master",
#                             "headRepository": null,
#                             "labels": {
#                                 "edges": []
#                             },
#                             "mergeable": "CONFLICTING",
#                             "merged": false,
#                             "milestone": null,
#                             "number": 2,
#                             "state": "CLOSED",
#                             "title": "add check upnp",
#                             "updatedAt": "2014-06-15T20:26:45Z",
#                             "url": "https://github.com/YunoHost/yunohost/pull/2"
#                         }
#                     },

# bridge_pr_template = {
#     "github_id": "",
#     "github_project": "",
#     "wekan_id": "",
# }

def generate_id():
    # this is for a really weird bug
    # when using mongodb directly is generate a ObjectID()
    # but wekan seems to be generating a string instead
    # and some part of the code expect the id to be a string and not a objectID
    # so I need to generate string ids myself :|
    return "".join([random.SystemRandom().choice(list(set(string.hexdigits.lower()))) for x in range(17)])

def get(collection, query):
    return list(collection.find(query))[0]


def get_none(collection, query):
    result = list(collection.find(query))
    return result[0] if result else None


def get_by_id(collection, id):
    return get(collection, {"_id": id})


def get_default_list(client, board):
    # XXX also insert in bridge?
    default_list = get_none(client.wekan.lists, {"title": "No roadmap", "boardId": board["_id"]})

    if default_list:
        print "'No roadmap' list already exists, return it"
        return default_list["_id"]

    all_lists = client.wekan.lists.find({"boardId": board["_id"]})
    if list(all_lists):
        sort = 1 + max([x.get("sort", 0) for x in all_lists])
    else:
        sort = 0

    print "'No roadmap' didn't exist, create it"
    return client.wekan.lists.insert({
        "_id" : generate_id(),
        "title" : "No roadmap",
        "boardId" : board["_id"],
        "archived" : False,
        "createdAt" : datetime.now(),
        "sort" : sort
    })


def get_list_for_milestone(client, board, milestone):
    def update_list(list_, milestone):
        if list_["title"] != milestone["title"]:
            print "Updating milestone 'title from '%s' to '%s'" % (list_["title"], milestone["title"])
            list_["title"] = milestone["title"]
            client.wekan.lists.update({"_id": list_["_id"]}, {"$set": list_})

        archived = milestone["state"] == "CLOSED"
        if list_["archived"] != archived:
            if archived:
                print "Archiving milestone '%s'" % (list_['title'])
            else:
                print "Briging milestone '%s' back from archives" % (list_['title'])
            list_["archived"] = archived
            client.wekan.lists.update({"_id": list_["_id"]}, {"$set": list_})

    bridge_milestone = get_none(client.wekan.bridge_for_milestones, {
        "github_id": milestone["number"],
        "github_project": project
    })

    if bridge_milestone:
        print "Found bridge_milestone, return list"
        list_ = get_by_id(client.wekan.lists, bridge_milestone["wekan_id"])
        update_list(list_, milestone)
        return list_["_id"]

    # let's try to find an existing colum with the milestone name
    list_ = get_none(client.wekan.lists, {"title": milestone["title"]})

    # create it
    if not list_:
        sort = 1 + max([x.get("sort", 0) for x in client.wekan.lists.find({"boardId": board["_id"]})])

        print "create new list '%s'" % milestone["title"]
        list_ = client.wekan.lists.insert({
            "_id" : generate_id(),
            "title" : milestone["title"],
            "boardId" : board["_id"],
            "archived" : milestone["state"] == "CLOSED",
            "createdAt" : datetime.now(),
            "sort" : sort
        })
    else:
        update_list(list_, milestone)
        list_ = list_["_id"]
        print "List exists for milestone '%s', return it"

    print "Create bridge for milestone %s -> %s" % (milestone["number"], list_)
    bridge_milestone = client.wekan.bridge_for_milestones.insert({
        "github_id": milestone["number"],
        "github_project": project,
        "wekan_id": list_
    })

    return list_


def get_user(client, author):
    bridge_user = get_none(client.wekan.bridge_for_users, {"username": author["login"]})

    if bridge_user:
        print "Found bridge user, return matching user (%s)" % bridge_user["wekan_id"]
        return get_by_id(client.wekan.users, bridge_user["wekan_id"])["_id"]

    user = get_none(client.wekan.users, {"username": author["login"]})

    if user is None:
        # TODO I need to grab the real user to fill the data, I only have the actor edge here
        user = client.wekan.users.insert({
            "_id" : generate_id(),
            "createdAt" : datetime.now(),
            "services" : { "password" : {}, "email" : {}, "resume" : {}},
            "username" : author["login"],
            "emails" : [],
            "isAdmin" : False,
            "profile" : {
                # "fullname" : "Testeu",
                # TODO copy file
                # "avatarUrl" : "/cfs/files/avatars/vvwa5nMFBRCbMc6p6/2-punaise-des-bois-pentatomes.jpg"
            }
        })
    else:
        user = user["_id"]

    bridge_user = client.wekan.bridge_for_users.insert({
        "github_id": author["login"],
        "wekan_id": user
    })

    return user


query = open("./query.graphql", "r").read()
token = open("graphql_token", "r").read().strip()

client = MongoClient()

# pull_requests = json.load(open("./data.json", "r"))

# TODO create the bord if it doesn't exist
board = get(client.wekan.boards, {"slug": "yunohost"})

for project in ["yunohost", "yunohost-admin", "moulinette", "ssowat"]:
    pull_requests = requests.post("https://api.github.com/graphql", headers={"Authorization": "bearer %s" % token}, json={"query": query % (project, "")}).json()

    has_next_page = True
    while has_next_page:
        for pr in pull_requests["data"]["repository"]["pullRequests"]["edges"]:
            pr = pr["node"]
            print "Working on '%s' (%s)" % (pr["title"], pr["url"])

            bridge_pr = get_none(client.wekan.bridge_for_prs, {
                "github_id": pr["number"],
                "github_project": project
            })

            # get list for milestone
            milestone = pr["milestone"]
            if milestone is None:
                print "No milestone"
                list_ = get_default_list(client, board)
                print "selected default list (%s)" % (list_)
            else:
                print "Has milestone"
                list_ = get_list_for_milestone(client, board, milestone)
                print "selected list '%s' (%s)" % (milestone["title"], list_)

            # get user for ticket
            user = get_user(client, pr["author"])
            print "selected user '%s' (%s)" % (pr["author"]["login"], user)

            # we haven't imported this PR yet
            if not bridge_pr:
                cards_in_column = list(client.wekan.cards.find({"boardId": board["_id"], "listId": list_}))
                sort = 1 + (max([x.get("sort", 0) for x in cards_in_column]) if cards_in_column else -1)

                card = client.wekan.cards.insert({
                    "_id" : generate_id(),
                    "title" : "[%s] %s" % (project, pr["title"]),
                    "members" : [ ],
                    "labelIds" : [ ],
                    "listId" : list_,
                    "boardId" : board["_id"],
                    "sort" : sort,
                    "archived" : pr["closed"],
                    "createdAt" : datetime.now(), # XXX uses card value?
                    "dateLastActivity" : datetime.now(),
                    "userId" : user
                })
                print "create card '%s' (%s)" % (pr["title"], card)

                bridge_pr = client.wekan.bridge_for_prs.insert({
                    "github_id": pr["number"],
                    "github_project": project,
                    "wekan_id": card,
                })
                print "create card bridge %s -> %s" % (pr["number"], card)

            else:
                print "Card already exist, update"
                card = get_by_id(client.wekan.cards, bridge_pr["wekan_id"])

                title = "[%s] %s" % (project, pr["title"])
                if card["title"] != title:
                    print "change title from '%s' to '%s'" % (card["title"], title)
                    card["title"] = title

                if card["listId"] != list_:
                    before_list = get_by_id(client.wekan.lists, card["listId"])
                    after_list = get_by_id(client.wekan.lists, list_)
                    print "move card from '%s' -> '%s'" % (before_list["title"], after_list["title"])

                if card["archived"] != pr["closed"]:
                    if pr["closed"]:
                        print "archiving the card"
                    else:
                        print "card is re-opened"
                    card["archived"] = pr["closed"]

                if card["userId"] != user:
                    print "card has change of author for a weird reason, update it"
                    card["userId"] = user

                client.wekan.cards.update({"_id": card["_id"]}, {"$set": card})

            print "----"

        has_next_page = pull_requests["data"]["repository"]["pullRequests"]["pageInfo"]["hasNextPage"]
        if has_next_page:
            pagination = ', after: "%s"' % pull_requests["data"]["repository"]["pullRequests"]["pageInfo"]["endCursor"]
            print pull_requests["data"]["repository"]["pullRequests"]["pageInfo"]
            pull_requests = requests.post("https://api.github.com/graphql", headers={"Authorization": "bearer %s" % token}, json={"query": query % (project, pagination)}).json()



# TODO
# * import labels
# * import description
# * import comments
# * generate notifications stuff
