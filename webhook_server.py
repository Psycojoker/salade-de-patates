import hmac
import hashlib
import requests

from flask import Flask, request, abort
from pymongo import MongoClient

from common import get_by_id, get_none
from github_to_wekan import import_pr, get_list_for_milestone, get_board


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

@app.route("/wekan/<secret>", methods=['POST'])
def wekan(secret):
    print request
    print request.json

    # sekuritay
    local_secret = open("./wekan_webhook_secret", "r").read().strip()

    if local_secret != secret.strip():
        abort(403)

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


    # stolen and adapted from here
    # https://github.com/carlos-jenkins/python-github-webhooks/blob/d485b31c0291d06b5153198bc1de685d50731536/webhooks.py#L72-L93
    secret = open("./github_webhook_secret", "r").read().strip()

    # Only SHA1 is supported
    header_signature = request.headers.get('X-Hub-Signature')
    if header_signature is None:
        print "no header X-Hub-Signature"
        abort(403)

    sha_name, signature = header_signature.split('=')
    if sha_name != 'sha1':
        print "signing algo isn't sha1, it's '%s'" % sha_name
        abort(501)

    # HMAC requires the key to be bytes, but data is string
    mac = hmac.new(str(secret), msg=request.data, digestmod=hashlib.sha1)

    if not hmac.compare_digest(str(mac.hexdigest()), str(signature)):
        abort(403)

    hook_type = request.headers.get("X-Github-Event")

    print "Hook type:", hook_type

    if hook_type == "pull_request":
        token = open("graphql_token", "r").read().strip()
        query = open("./query-one.graphql", "r").read()

        project = request.json["repository"]["name"]
        number = request.json["pull_request"]["number"]

        pr = requests.post("https://api.github.com/graphql",
                           headers={"Authorization": "bearer %s" % token},
                           json={"query": query % (project, number)}).json()

        print "reimporting pr %s#%s" % (project, number)
        import_pr(client, project, pr["data"]["repository"]["pullRequest"])

    elif hook_type == "milestone":
        # XXX in theory, I only need to run the importation script on one
        # milestone here
        # XXX but I don't have that, don't I? I probably need to write some
        # code for that then
        # actions: created, closed, opened, edited, deleted

        project = request.json["repository"]["name"]

        if request.json["action"] == "created":
            # I need to import it here

            # this is badly name but will create list (column) on the fly
            get_list_for_milestone(client, get_board(client), project, request.json["milestone"])
        elif request.json["action"] == "closed":
            # if all milestone are closed, archive to column
            pass
        elif request.json["action"] == "opened":
            # set column state to unarchived
            pass
        elif request.json["action"] == "edited":
            # only care about title change
            # if title change:
            # * look if I'm the only milestone on that column
            # * if yes, change title
            # * if not:
            #   - are they any other column with new title?
            #     -> if so, merge into it
            #     -> else, create new list, move all my cards into it
            pass
        elif request.json["action"] == "deleted":
            # if all milestone are closed, archive to column
            pass
        else:
            print "unkown action for milestone webhook: '%s'" % request.json["action"]

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
