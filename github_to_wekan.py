# encoding: utf-8

import json
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

query = open("./query.graphql", "r").read()
token = open("graphql_token", "r").read().strip()

client = MongoClient()

pull_requests = requests.post("https://api.github.com/graphql", headers={"Authorization": "bearer %s" % token}, json={"query": query}).json()

# pull_requests = json.load(open("./data.json", "r"))

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

    sort = 1 + max([x.get("sort", 0) for x in client.wekan.lists.find({"boardId": board["_id"]})])

    print "'No roadmap' didn't exist, create it"
    return client.wekan.lists.insert({
        "title" : "No roadmap",
        "boardId" : board["_id"],
        "archived" : False,
        "createdAt" : datetime.now(),
        "sort" : sort
    })


def get_list_for_milestone(client, board, milestone):
    bridge_milestone = get_none(client.wekan.bridge_for_milestones, {
        "github_id": milestone["number"],
        "github_project": "yunohost"
    })

    if bridge_milestone:
        print "Found bridge_milestone, return list"
        return get_by_id(client.wekan.lists, bridge_milestone["wekan_id"])["_id"]

    # let's try to find an existing colum with the milestone name
    list_ = get_none(client.wekan.lists, {"title": milestone["title"]})

    # create it
    if not list_:
        sort = 1 + max([x.get("sort", 0) for x in client.wekan.lists.find({"boardId": board["_id"]})])

        print "create new list '%s'" % milestone["title"]
        list_ = client.wekan.lists.insert({
            "title" : milestone["title"],
            "boardId" : board["_id"],
            "archived" : False,
            "createdAt" : datetime.now(),
            "sort" : sort
        })
    else:
        list_ = list_["_id"]
        print "List exists for milestone '%s', return it"

    print "Create bridge for milestone %s -> %s" % (milestone["number"], list_)
    bridge_milestone = client.wekan.bridge_for_milestones.insert({
        "github_id": milestone["number"],
        "github_project": "yunohost",
        "wekan_id": list_
    })

    return list_


def get_user(client, author):
    bridge_user = get_none(client.wekan.bridge_for_users, {"username": author["login"]})

    if bridge_user:
        print "Found bridge user, return matching user (%s)" % bridge_user["wekan_id"]
        return get_by_id(client.wekan.users, bridge_user["wekan_id"])

    user = get_none(client.wekan.users, {"username": author["login"]})

    if user is None:
        # TODO I need to grab the real user to fill the data, I only have the actor edge here
        user = client.wekan.users.insert({
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


# TODO create the bord if it doesn't exist
board = get(client.wekan.boards, {"slug": "yunohost"})


for pr in pull_requests["data"]["repository"]["pullRequests"]["edges"]:
    pr = pr["node"]
    print "Working on '%s' (%s)" % (pr["title"], pr["url"])

    bridge_pr = get_none(client.wekan.bridge_for_prs, {
        "github_id": pr["number"],
        "github_project": "yunohost"
    })

    # we haven't imported this PR yet
    if not bridge_pr:
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

        cards_in_column = list(client.wekan.cards.find({"boardId": board["_id"], "listId": list_}))
        sort = 1 + (max([x.get("sort", 0) for x in cards_in_column]) if cards_in_column else 0)

        card = client.wekan.cards.insert({
            "title" : "[%s] %s" % ("yunohost", pr["title"]),
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
            "github_project": "yunohost",
            "wekan_id": card,
        })
        print "create card bridge %s -> %s" % (pr["number"], card)

    else:
        print "Card already exist, update"
        card = get_by_id(client.wekan.cards, bridge_pr["wekan_id"])

        title = "[%s] %s" % ("yunohost", pr["title"])
        if card["title"] != title:
            print "change title from '%s' to '%s'" % (card["title"], title)
            card["title"] = title

        client.wekan.cards.update({"_id": card["_id"]}, {"$set": card})

    print "----"


# TODO
# * auto archive columns
# * auto archive cards
# * prefix project name on title or color ?
# * import labels
# * import description
# * import comments
