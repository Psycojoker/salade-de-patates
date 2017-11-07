import requests

from flask import Flask, request
from pymongo import MongoClient

from common import get_by_id, get_none
from github_to_wekan import import_pr


client = MongoClient()

# Card creation
# 
# {
#   text: '{{wekan-username}} added "{{card-title}}" to "{{list-name}}"\nhttp://{{wekan-host}}/b/{{board-id}}/{{board-name}}/{{card-id}}',
#   cardId: '{{card-id}}',
#   listId: '{{list-id}}',
#   boardId: '{{board-id}}',
#   user: '{{wekan-username}}',
#   card: '{{card-title}}',
#   description: 'act-createCard'
# }
# Card archival
# 
# {
#   text: '{{wekan-username}} archived "{{card-title}}"\nhttp://{{wekan-host}}/b/{{board-id}}/{{board-name}}/{{card-id}}',
#   cardId: '{{card-id}}',
#   listId: '{{list-id}}',
#   boardId: '{{board-id}}',
#   user: '{{wekan-username}}',
#   card: '{{card-title}}',
#   description: 'act-archivedCard'
# }
# Comment creation
# 
# {
#   text: '{{wekan-username}} commented on "{{card-title}}": "{{comment-body}}"\nhttp://{{wekan-host}}/b/{{board-id}}/{{board-name}}/{{card-id}}',
#   cardId: '{{card-id}}',
#   boardId: '{{board-id}}',
#   comment: '{{comment-body}}',
#   user: '{{wekan-username}}',
#   card: '{{card-title}}',
#   description: 'act-addComment'
# }
# Card move
# 
# {
#   text: '{{wekan-username}} moved "{{card-title}}" from "{{old-list-name}}" to "{{new-list-name}}"\nhttp://{{wekan-host}}/b/{{board-id}}/{{board-name}}/{{card-id}}',
#   cardId: '{{card-id}}',
#   listId: '{{new-list-id}}',
#   oldListId: '{{old-list-id}}',
#   boardId: '{{board-id}}',
#   user: '{{wekan-username}}',
#   card: '{{card-title}}',
#   description: 'act-moveCard'
# }

app = Flask(__name__)
token = open("wekan_webhook_token", "r").read().strip()

@app.route("/wekan", methods=['POST'])
def wekan():
    print request
    print request.json

    # TODO check that request is json and correct or some stuff like that

    # card create -> we don't care about it

    # if card not linked to github, we don't care about it

    # card archival
    # * does that mean that we close the PR?
    # * do we have unarchival event?

    # comment creation
    # * not yet supported

    # card move -> interesting part
    # TODO: mark "[MILESTONE]" or something like that in columns titles
    # * if card move in another milestone than its one -> change of milestone
    # * if card is moved out of milestone keep its milestone

    # we don't have card modification like title or description?

    # do we have milestone modifications events?
    # apparently no :(

    client = MongoClient()

    if request.json["description"] == "act-moveCard":
        card_id = request.json["cardId"]
        card = get_by_id(client.wekan.cards, card_id)

        bridge = get_none(client.wekan.bridge_for_prs, {"wekan_id": card_id})

        print "bridge:", bridge
        print "card:", card

        if bridge is None:
            print "unhandled card", card_id
            return "unhandled card"

        project = bridge["github_project"]

        list_id = request.json["listId"]

        list_ = get_none(client.wekan.bridge_for_milestones, {"wekan_id": list_id, "github_project": project})

        # list itself can't be none
        # list can be: know (a milestone), unknow
        # card was in a milestone, wasn't [back to its milestone or in another milestone]

        github_pr = requests.get("https://api.github.com/repos/yunohost/%s/pulls/%s" % (project, bridge["github_id"])).json()

        github_milestone_id = github_pr["milestone"]["number"]

        if list_ is None:
            # TODO try to detect if there is a list that is a milestone with
            # the same name but that isn't in that project, if so, create the
            # milestone in the project where it's missing

            # rename to include milestone name in list?
            print "new list is not known as a milestone, skip"
            return "ok"

        # TODO default list for unmilestoning a card

        # check if target column milestone number != github_milestone_id
        # if so, change it
        # else return

        if list_["github_id"] != github_milestone_id:
            print "online github PR is different than the targeted list, change it"
            print requests.patch("https://api.github.com/repos/yunohost/%s/issues/%s" % (project, bridge["github_id"]), json={"milestone": list_["github_id"]}, headers={"Authorization": "bearer %s" % token})

            query = open("./query-one.graphql", "r").read()
            pr = requests.post("https://api.github.com/graphql",
                               headers={"Authorization": "bearer %s" % token},
                               json={"query": query % (project, bridge["github_id"])}).json()

            import_pr(client, project, pr["data"]["repository"]["pullRequest"])
        else:
            print "online github PR is the same than the targeted list, don't do anything"
            return "ok"

    return "ok"

@app.route("/github", methods=['POST'])
def github():
    # print request
    # print request.json

    # github_hook_secret = open("./secret_for_webhook", "r").read().strip()

    # > HMAC hex digest of the payload, using the hook's secret as the key (if
    # > configured)
    # if request.headers.get("X-Hub-Signature").strip() != github_hook_secret:
        # TODO real exception
        # raise 400

    hook_type = request.headers.get("X-Github-Event")

    if hook_type == "pull_request":
        token = open("graphql_token", "r").read().strip()
        query = open("./query-one.graphql", "r").read()

        project = request.json["repository"]["name"]
        number = request.json["pull_request"]["number"]

        pr = requests.post("https://api.github.com/graphql",
                           headers={"Authorization": "bearer %s" % token},
                           json={"query": query % (project, number)}).json()

        import_pr(client, project, pr["data"]["repository"]["pullRequest"])

    elif hook_type == "milestone":
        # XXX in theory, I only need to run the importation script on one
        # milestone here
        # XXX but I don't have that, don't I? I probably need to write some
        # code for that then
        pass

    elif hook_type == "label":
        # TODO
        pass

    # XXX really need to do that?
    elif hook_type == "user":
        # TODO
        pass

    else:
        print "unsupported hook type: %s" % hook_type

    return "ok"


if __name__ == '__main__':
    app.run(host="0.0.0.0")
