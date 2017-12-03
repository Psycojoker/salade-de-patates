# this is for dev only normally

import requests
from pymongo import MongoClient

client = MongoClient()
token = open("wekan_webhook_token", "r").read().strip()

for project in ["yunohost", "yunohost-admin", "moulinette", "ssowat"]:
    milestones = requests.get("https://api.github.com/repos/yunohost/%s/milestones?state=all" % project, headers={"Authorization": "bearer %s" % token}).json()

    used_numbers = {x["number"] for x in milestones}

    for i in client.wekan.bridge_for_milestones.find({"github_project": project}):
        if i["github_id"] not in used_numbers:
            print 'client.wekan.remove({"github_id": %s, "github_project": %s})' % (i["github_id"], project)
            client.wekan.remove({"github_id": i["github_id"], "github_project": project})
