import requests

from flask import Flask, request
from pymongo import MongoClient

from common import get_by_id, get_none


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

# github PR api request

# [
#   {
#     "id": 1,
#     "url": "https://api.github.com/repos/octocat/Hello-World/pulls/1347",
#     "html_url": "https://github.com/octocat/Hello-World/pull/1347",
#     "diff_url": "https://github.com/octocat/Hello-World/pull/1347.diff",
#     "patch_url": "https://github.com/octocat/Hello-World/pull/1347.patch",
#     "issue_url": "https://api.github.com/repos/octocat/Hello-World/issues/1347",
#     "commits_url": "https://api.github.com/repos/octocat/Hello-World/pulls/1347/commits",
#     "review_comments_url": "https://api.github.com/repos/octocat/Hello-World/pulls/1347/comments",
#     "review_comment_url": "https://api.github.com/repos/octocat/Hello-World/pulls/comments{/number}",
#     "comments_url": "https://api.github.com/repos/octocat/Hello-World/issues/1347/comments",
#     "statuses_url": "https://api.github.com/repos/octocat/Hello-World/statuses/6dcb09b5b57875f334f61aebed695e2e4193db5e",
#     "number": 1347,
#     "state": "open",
#     "title": "new-feature",
#     "body": "Please pull these awesome changes",
#     "assignee": {
#       "login": "octocat",
#       "id": 1,
#       "avatar_url": "https://github.com/images/error/octocat_happy.gif",
#       "gravatar_id": "",
#       "url": "https://api.github.com/users/octocat",
#       "html_url": "https://github.com/octocat",
#       "followers_url": "https://api.github.com/users/octocat/followers",
#       "following_url": "https://api.github.com/users/octocat/following{/other_user}",
#       "gists_url": "https://api.github.com/users/octocat/gists{/gist_id}",
#       "starred_url": "https://api.github.com/users/octocat/starred{/owner}{/repo}",
#       "subscriptions_url": "https://api.github.com/users/octocat/subscriptions",
#       "organizations_url": "https://api.github.com/users/octocat/orgs",
#       "repos_url": "https://api.github.com/users/octocat/repos",
#       "events_url": "https://api.github.com/users/octocat/events{/privacy}",
#       "received_events_url": "https://api.github.com/users/octocat/received_events",
#       "type": "User",
#       "site_admin": false
#     },
#     "milestone": {
#       "url": "https://api.github.com/repos/octocat/Hello-World/milestones/1",
#       "html_url": "https://github.com/octocat/Hello-World/milestones/v1.0",
#       "labels_url": "https://api.github.com/repos/octocat/Hello-World/milestones/1/labels",
#       "id": 1002604,
#       "number": 1,
#       "state": "open",
#       "title": "v1.0",
#       "description": "Tracking milestone for version 1.0",
#       "creator": {
#         "login": "octocat",
#         "id": 1,
#         "avatar_url": "https://github.com/images/error/octocat_happy.gif",
#         "gravatar_id": "",
#         "url": "https://api.github.com/users/octocat",
#         "html_url": "https://github.com/octocat",
#         "followers_url": "https://api.github.com/users/octocat/followers",
#         "following_url": "https://api.github.com/users/octocat/following{/other_user}",
#         "gists_url": "https://api.github.com/users/octocat/gists{/gist_id}",
#         "starred_url": "https://api.github.com/users/octocat/starred{/owner}{/repo}",
#         "subscriptions_url": "https://api.github.com/users/octocat/subscriptions",
#         "organizations_url": "https://api.github.com/users/octocat/orgs",
#         "repos_url": "https://api.github.com/users/octocat/repos",
#         "events_url": "https://api.github.com/users/octocat/events{/privacy}",
#         "received_events_url": "https://api.github.com/users/octocat/received_events",
#         "type": "User",
#         "site_admin": false
#       },
#       "open_issues": 4,
#       "closed_issues": 8,
#       "created_at": "2011-04-10T20:09:31Z",
#       "updated_at": "2014-03-03T18:58:10Z",
#       "closed_at": "2013-02-12T13:22:01Z",
#       "due_on": "2012-10-09T23:39:01Z"
#     },
#     "locked": false,
#     "created_at": "2011-01-26T19:01:12Z",
#     "updated_at": "2011-01-26T19:01:12Z",
#     "closed_at": "2011-01-26T19:01:12Z",
#     "merged_at": "2011-01-26T19:01:12Z",
#     "head": {
#       "label": "new-topic",
#       "ref": "new-topic",
#       "sha": "6dcb09b5b57875f334f61aebed695e2e4193db5e",
#       "user": {
#         "login": "octocat",
#         "id": 1,
#         "avatar_url": "https://github.com/images/error/octocat_happy.gif",
#         "gravatar_id": "",
#         "url": "https://api.github.com/users/octocat",
#         "html_url": "https://github.com/octocat",
#         "followers_url": "https://api.github.com/users/octocat/followers",
#         "following_url": "https://api.github.com/users/octocat/following{/other_user}",
#         "gists_url": "https://api.github.com/users/octocat/gists{/gist_id}",
#         "starred_url": "https://api.github.com/users/octocat/starred{/owner}{/repo}",
#         "subscriptions_url": "https://api.github.com/users/octocat/subscriptions",
#         "organizations_url": "https://api.github.com/users/octocat/orgs",
#         "repos_url": "https://api.github.com/users/octocat/repos",
#         "events_url": "https://api.github.com/users/octocat/events{/privacy}",
#         "received_events_url": "https://api.github.com/users/octocat/received_events",
#         "type": "User",
#         "site_admin": false
#       },
#       "repo": {
#         "id": 1296269,
#         "owner": {
#           "login": "octocat",
#           "id": 1,
#           "avatar_url": "https://github.com/images/error/octocat_happy.gif",
#           "gravatar_id": "",
#           "url": "https://api.github.com/users/octocat",
#           "html_url": "https://github.com/octocat",
#           "followers_url": "https://api.github.com/users/octocat/followers",
#           "following_url": "https://api.github.com/users/octocat/following{/other_user}",
#           "gists_url": "https://api.github.com/users/octocat/gists{/gist_id}",
#           "starred_url": "https://api.github.com/users/octocat/starred{/owner}{/repo}",
#           "subscriptions_url": "https://api.github.com/users/octocat/subscriptions",
#           "organizations_url": "https://api.github.com/users/octocat/orgs",
#           "repos_url": "https://api.github.com/users/octocat/repos",
#           "events_url": "https://api.github.com/users/octocat/events{/privacy}",
#           "received_events_url": "https://api.github.com/users/octocat/received_events",
#           "type": "User",
#           "site_admin": false
#         },
#         "name": "Hello-World",
#         "full_name": "octocat/Hello-World",
#         "description": "This your first repo!",
#         "private": false,
#         "fork": false,
#         "url": "https://api.github.com/repos/octocat/Hello-World",
#         "html_url": "https://github.com/octocat/Hello-World",
#         "archive_url": "http://api.github.com/repos/octocat/Hello-World/{archive_format}{/ref}",
#         "assignees_url": "http://api.github.com/repos/octocat/Hello-World/assignees{/user}",
#         "blobs_url": "http://api.github.com/repos/octocat/Hello-World/git/blobs{/sha}",
#         "branches_url": "http://api.github.com/repos/octocat/Hello-World/branches{/branch}",
#         "clone_url": "https://github.com/octocat/Hello-World.git",
#         "collaborators_url": "http://api.github.com/repos/octocat/Hello-World/collaborators{/collaborator}",
#         "comments_url": "http://api.github.com/repos/octocat/Hello-World/comments{/number}",
#         "commits_url": "http://api.github.com/repos/octocat/Hello-World/commits{/sha}",
#         "compare_url": "http://api.github.com/repos/octocat/Hello-World/compare/{base}...{head}",
#         "contents_url": "http://api.github.com/repos/octocat/Hello-World/contents/{+path}",
#         "contributors_url": "http://api.github.com/repos/octocat/Hello-World/contributors",
#         "deployments_url": "http://api.github.com/repos/octocat/Hello-World/deployments",
#         "downloads_url": "http://api.github.com/repos/octocat/Hello-World/downloads",
#         "events_url": "http://api.github.com/repos/octocat/Hello-World/events",
#         "forks_url": "http://api.github.com/repos/octocat/Hello-World/forks",
#         "git_commits_url": "http://api.github.com/repos/octocat/Hello-World/git/commits{/sha}",
#         "git_refs_url": "http://api.github.com/repos/octocat/Hello-World/git/refs{/sha}",
#         "git_tags_url": "http://api.github.com/repos/octocat/Hello-World/git/tags{/sha}",
#         "git_url": "git:github.com/octocat/Hello-World.git",
#         "hooks_url": "http://api.github.com/repos/octocat/Hello-World/hooks",
#         "issue_comment_url": "http://api.github.com/repos/octocat/Hello-World/issues/comments{/number}",
#         "issue_events_url": "http://api.github.com/repos/octocat/Hello-World/issues/events{/number}",
#         "issues_url": "http://api.github.com/repos/octocat/Hello-World/issues{/number}",
#         "keys_url": "http://api.github.com/repos/octocat/Hello-World/keys{/key_id}",
#         "labels_url": "http://api.github.com/repos/octocat/Hello-World/labels{/name}",
#         "languages_url": "http://api.github.com/repos/octocat/Hello-World/languages",
#         "merges_url": "http://api.github.com/repos/octocat/Hello-World/merges",
#         "milestones_url": "http://api.github.com/repos/octocat/Hello-World/milestones{/number}",
#         "mirror_url": "git:git.example.com/octocat/Hello-World",
#         "notifications_url": "http://api.github.com/repos/octocat/Hello-World/notifications{?since, all, participating}",
#         "pulls_url": "http://api.github.com/repos/octocat/Hello-World/pulls{/number}",
#         "releases_url": "http://api.github.com/repos/octocat/Hello-World/releases{/id}",
#         "ssh_url": "git@github.com:octocat/Hello-World.git",
#         "stargazers_url": "http://api.github.com/repos/octocat/Hello-World/stargazers",
#         "statuses_url": "http://api.github.com/repos/octocat/Hello-World/statuses/{sha}",
#         "subscribers_url": "http://api.github.com/repos/octocat/Hello-World/subscribers",
#         "subscription_url": "http://api.github.com/repos/octocat/Hello-World/subscription",
#         "svn_url": "https://svn.github.com/octocat/Hello-World",
#         "tags_url": "http://api.github.com/repos/octocat/Hello-World/tags",
#         "teams_url": "http://api.github.com/repos/octocat/Hello-World/teams",
#         "trees_url": "http://api.github.com/repos/octocat/Hello-World/git/trees{/sha}",
#         "homepage": "https://github.com",
#         "language": null,
#         "forks_count": 9,
#         "stargazers_count": 80,
#         "watchers_count": 80,
#         "size": 108,
#         "default_branch": "master",
#         "open_issues_count": 0,
#         "topics": [
#           "octocat",
#           "atom",
#           "electron",
#           "API"
#         ],
#         "has_issues": true,
#         "has_wiki": true,
#         "has_pages": false,
#         "has_downloads": true,
#         "archived": false,
#         "pushed_at": "2011-01-26T19:06:43Z",
#         "created_at": "2011-01-26T19:01:12Z",
#         "updated_at": "2011-01-26T19:14:43Z",
#         "permissions": {
#           "admin": false,
#           "push": false,
#           "pull": true
#         },
#         "allow_rebase_merge": true,
#         "allow_squash_merge": true,
#         "allow_merge_commit": true,
#         "subscribers_count": 42,
#         "network_count": 0
#       }
#     },
#     "base": {
#       "label": "master",
#       "ref": "master",
#       "sha": "6dcb09b5b57875f334f61aebed695e2e4193db5e",
#       "user": {
#         "login": "octocat",
#         "id": 1,
#         "avatar_url": "https://github.com/images/error/octocat_happy.gif",
#         "gravatar_id": "",
#         "url": "https://api.github.com/users/octocat",
#         "html_url": "https://github.com/octocat",
#         "followers_url": "https://api.github.com/users/octocat/followers",
#         "following_url": "https://api.github.com/users/octocat/following{/other_user}",
#         "gists_url": "https://api.github.com/users/octocat/gists{/gist_id}",
#         "starred_url": "https://api.github.com/users/octocat/starred{/owner}{/repo}",
#         "subscriptions_url": "https://api.github.com/users/octocat/subscriptions",
#         "organizations_url": "https://api.github.com/users/octocat/orgs",
#         "repos_url": "https://api.github.com/users/octocat/repos",
#         "events_url": "https://api.github.com/users/octocat/events{/privacy}",
#         "received_events_url": "https://api.github.com/users/octocat/received_events",
#         "type": "User",
#         "site_admin": false
#       },
#       "repo": {
#         "id": 1296269,
#         "owner": {
#           "login": "octocat",
#           "id": 1,
#           "avatar_url": "https://github.com/images/error/octocat_happy.gif",
#           "gravatar_id": "",
#           "url": "https://api.github.com/users/octocat",
#           "html_url": "https://github.com/octocat",
#           "followers_url": "https://api.github.com/users/octocat/followers",
#           "following_url": "https://api.github.com/users/octocat/following{/other_user}",
#           "gists_url": "https://api.github.com/users/octocat/gists{/gist_id}",
#           "starred_url": "https://api.github.com/users/octocat/starred{/owner}{/repo}",
#           "subscriptions_url": "https://api.github.com/users/octocat/subscriptions",
#           "organizations_url": "https://api.github.com/users/octocat/orgs",
#           "repos_url": "https://api.github.com/users/octocat/repos",
#           "events_url": "https://api.github.com/users/octocat/events{/privacy}",
#           "received_events_url": "https://api.github.com/users/octocat/received_events",
#           "type": "User",
#           "site_admin": false
#         },
#         "name": "Hello-World",
#         "full_name": "octocat/Hello-World",
#         "description": "This your first repo!",
#         "private": false,
#         "fork": false,
#         "url": "https://api.github.com/repos/octocat/Hello-World",
#         "html_url": "https://github.com/octocat/Hello-World",
#         "archive_url": "http://api.github.com/repos/octocat/Hello-World/{archive_format}{/ref}",
#         "assignees_url": "http://api.github.com/repos/octocat/Hello-World/assignees{/user}",
#         "blobs_url": "http://api.github.com/repos/octocat/Hello-World/git/blobs{/sha}",
#         "branches_url": "http://api.github.com/repos/octocat/Hello-World/branches{/branch}",
#         "clone_url": "https://github.com/octocat/Hello-World.git",
#         "collaborators_url": "http://api.github.com/repos/octocat/Hello-World/collaborators{/collaborator}",
#         "comments_url": "http://api.github.com/repos/octocat/Hello-World/comments{/number}",
#         "commits_url": "http://api.github.com/repos/octocat/Hello-World/commits{/sha}",
#         "compare_url": "http://api.github.com/repos/octocat/Hello-World/compare/{base}...{head}",
#         "contents_url": "http://api.github.com/repos/octocat/Hello-World/contents/{+path}",
#         "contributors_url": "http://api.github.com/repos/octocat/Hello-World/contributors",
#         "deployments_url": "http://api.github.com/repos/octocat/Hello-World/deployments",
#         "downloads_url": "http://api.github.com/repos/octocat/Hello-World/downloads",
#         "events_url": "http://api.github.com/repos/octocat/Hello-World/events",
#         "forks_url": "http://api.github.com/repos/octocat/Hello-World/forks",
#         "git_commits_url": "http://api.github.com/repos/octocat/Hello-World/git/commits{/sha}",
#         "git_refs_url": "http://api.github.com/repos/octocat/Hello-World/git/refs{/sha}",
#         "git_tags_url": "http://api.github.com/repos/octocat/Hello-World/git/tags{/sha}",
#         "git_url": "git:github.com/octocat/Hello-World.git",
#         "hooks_url": "http://api.github.com/repos/octocat/Hello-World/hooks",
#         "issue_comment_url": "http://api.github.com/repos/octocat/Hello-World/issues/comments{/number}",
#         "issue_events_url": "http://api.github.com/repos/octocat/Hello-World/issues/events{/number}",
#         "issues_url": "http://api.github.com/repos/octocat/Hello-World/issues{/number}",
#         "keys_url": "http://api.github.com/repos/octocat/Hello-World/keys{/key_id}",
#         "labels_url": "http://api.github.com/repos/octocat/Hello-World/labels{/name}",
#         "languages_url": "http://api.github.com/repos/octocat/Hello-World/languages",
#         "merges_url": "http://api.github.com/repos/octocat/Hello-World/merges",
#         "milestones_url": "http://api.github.com/repos/octocat/Hello-World/milestones{/number}",
#         "mirror_url": "git:git.example.com/octocat/Hello-World",
#         "notifications_url": "http://api.github.com/repos/octocat/Hello-World/notifications{?since, all, participating}",
#         "pulls_url": "http://api.github.com/repos/octocat/Hello-World/pulls{/number}",
#         "releases_url": "http://api.github.com/repos/octocat/Hello-World/releases{/id}",
#         "ssh_url": "git@github.com:octocat/Hello-World.git",
#         "stargazers_url": "http://api.github.com/repos/octocat/Hello-World/stargazers",
#         "statuses_url": "http://api.github.com/repos/octocat/Hello-World/statuses/{sha}",
#         "subscribers_url": "http://api.github.com/repos/octocat/Hello-World/subscribers",
#         "subscription_url": "http://api.github.com/repos/octocat/Hello-World/subscription",
#         "svn_url": "https://svn.github.com/octocat/Hello-World",
#         "tags_url": "http://api.github.com/repos/octocat/Hello-World/tags",
#         "teams_url": "http://api.github.com/repos/octocat/Hello-World/teams",
#         "trees_url": "http://api.github.com/repos/octocat/Hello-World/git/trees{/sha}",
#         "homepage": "https://github.com",
#         "language": null,
#         "forks_count": 9,
#         "stargazers_count": 80,
#         "watchers_count": 80,
#         "size": 108,
#         "default_branch": "master",
#         "open_issues_count": 0,
#         "topics": [
#           "octocat",
#           "atom",
#           "electron",
#           "API"
#         ],
#         "has_issues": true,
#         "has_wiki": true,
#         "has_pages": false,
#         "has_downloads": true,
#         "archived": false,
#         "pushed_at": "2011-01-26T19:06:43Z",
#         "created_at": "2011-01-26T19:01:12Z",
#         "updated_at": "2011-01-26T19:14:43Z",
#         "permissions": {
#           "admin": false,
#           "push": false,
#           "pull": true
#         },
#         "allow_rebase_merge": true,
#         "allow_squash_merge": true,
#         "allow_merge_commit": true,
#         "subscribers_count": 42,
#         "network_count": 0
#       }
#     },
#     "_links": {
#       "self": {
#         "href": "https://api.github.com/repos/octocat/Hello-World/pulls/1347"
#       },
#       "html": {
#         "href": "https://github.com/octocat/Hello-World/pull/1347"
#       },
#       "issue": {
#         "href": "https://api.github.com/repos/octocat/Hello-World/issues/1347"
#       },
#       "comments": {
#         "href": "https://api.github.com/repos/octocat/Hello-World/issues/1347/comments"
#       },
#       "review_comments": {
#         "href": "https://api.github.com/repos/octocat/Hello-World/pulls/1347/comments"
#       },
#       "review_comment": {
#         "href": "https://api.github.com/repos/octocat/Hello-World/pulls/comments{/number}"
#       },
#       "commits": {
#         "href": "https://api.github.com/repos/octocat/Hello-World/pulls/1347/commits"
#       },
#       "statuses": {
#         "href": "https://api.github.com/repos/octocat/Hello-World/statuses/6dcb09b5b57875f334f61aebed695e2e4193db5e"
#       }
#     },
#     "user": {
#       "login": "octocat",
#       "id": 1,
#       "avatar_url": "https://github.com/images/error/octocat_happy.gif",
#       "gravatar_id": "",
#       "url": "https://api.github.com/users/octocat",
#       "html_url": "https://github.com/octocat",
#       "followers_url": "https://api.github.com/users/octocat/followers",
#       "following_url": "https://api.github.com/users/octocat/following{/other_user}",
#       "gists_url": "https://api.github.com/users/octocat/gists{/gist_id}",
#       "starred_url": "https://api.github.com/users/octocat/starred{/owner}{/repo}",
#       "subscriptions_url": "https://api.github.com/users/octocat/subscriptions",
#       "organizations_url": "https://api.github.com/users/octocat/orgs",
#       "repos_url": "https://api.github.com/users/octocat/repos",
#       "events_url": "https://api.github.com/users/octocat/events{/privacy}",
#       "received_events_url": "https://api.github.com/users/octocat/received_events",
#       "type": "User",
#       "site_admin": false
#     }
#   }
# ]

app = Flask(__name__)
token = open("wekan_webhook_token", "r").read().strip()

@app.route("/wekan", methods=['POST'])
def hello():
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
        else:
            print "online github PR is the same than the targeted list, don't do anything"
            return "ok"

    return "ok"


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")
