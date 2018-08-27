#!/usr/bin/env python

#requires pypi jq and requests
import json
import re
import requests
from jq import jq
from requests.auth import HTTPBasicAuth


# ----- Variables

package_layout = {
    'generic': 'simple-default',
    'bower': 'bower-default',
    'docker': 'simple-default',
    'gradle': 'gradle-default',
    'maven': 'maven-2-default',
    'npm': 'npm-default',
    'nuget': 'nuget-default',
    'pypi': 'simple-default',
    'rpm': 'simple-default',
    'ruby': 'simple-default',
    'vagrant': 'simple-default'}

permissions = {
    'manage': 'm',
    'delete': 'd',
    'deploy': 'w',
    'annotate': 'n',
    'read': 'r'}


# ----- Get password/API key ----- #

def readcreds():
    pw_file = '/tmp/.artifactory_info'
    f = open(pw_file, "r")
    contents = f.readlines()

    return contents


# ----- Repo REST API functions ----- #

# https://www.jfrog.com/confluence/display/RTF/Artifactory+REST+API#ArtifactoryRESTAPI-RepositoryConfiguration
def getrepo(repo_name):
    url = artifactory_url + 'repositories/' + repo_name

    return requests.get(
        url,
        auth=HTTPBasicAuth(user, password),
        verify=False)


# https://www.jfrog.com/confluence/display/RTF/Artifactory+REST+API#ArtifactoryRESTAPI-CreateRepository
def createrepo(repo_name, package_type):
    url = artifactory_url + 'repositories/' + repo_name
    data = {
        "rclass": "local",
        "packageType": package_type,
        "repoLayoutRef": package_layout[package_type]
    }
    headers = {'Content-Type': 'application/json'}

    return requests.put(
        url,
        auth=HTTPBasicAuth(user, password),
        data=json.dumps(data),
        headers=headers,
        verify=False)


# https://www.jfrog.com/confluence/display/RTF/Artifactory+REST+API#ArtifactoryRESTAPI-DeleteRepository
def deleterepo(repo_name):
    url = artifactory_url + 'repositories/' + repo_name

    return requests.delete(
        url,
        auth=HTTPBasicAuth(user, password),
        verify=False)


# ----- Groups REST API functions ----- #

# https://www.jfrog.com/confluence/display/RTF/Artifactory+REST+API#ArtifactoryRESTAPI-GetGroupDetails
def getgroup(group_name):
    url = artifactory_url + 'security/groups/' + group_name

    return requests.get(
        url,
        auth=HTTPBasicAuth(user, password),
        verify=False)


# https://www.jfrog.com/confluence/display/RTF/Artifactory+REST+API#ArtifactoryRESTAPI-CreateorReplaceGroup
# realm_type: internal | ldap
def creategroup(group_name, realm_type):
    url = artifactory_url + 'security/groups/' + group_name
    data = {
        "autoJoin": "false",
        "realm": realm_type,
        "adminPrivileges": "false"
    }
    headers = {'Content-Type': 'application/json'}

    return requests.put(
        url,
        auth=HTTPBasicAuth(user, password),
        data=json.dumps(data),
        headers=headers,
        verify=False)


# https://www.jfrog.com/confluence/display/RTF/Artifactory+REST+API#ArtifactoryRESTAPI-DeleteGroup
def deletegroup(group_name):
    url = artifactory_url + 'security/groups/' + group_name

    return requests.delete(
        url,
        auth=HTTPBasicAuth(user, password),
        verify=False)


# ----- Permissions REST API functions ----- #

def getperm(perm_name):
    url = artifactory_url + 'security/permissions/' + perm_name

    return requests.get(
        url,
        auth=HTTPBasicAuth(user, password),
        verify=False)


def createperm(perm_name, repo_names, group_name, group_perms, public_read):
    '''
    repo_names (List): list of repos that the permissions is to be applied
    group_perms (List): list of perms for the group
    public_read (Boolean): if True, anonymous users have read access
    '''
    if public_read == True:
        anonymous_perms = ['r']
    else:
        anonymous_perms = ['']

    url = artifactory_url + 'security/permissions/' + perm_name
    data = {
        "repositories": repo_names,
        "principals": {
            "users": {
                "anonymous": anonymous_perms
            },
            "groups": {
                group_name: group_perms
            }
        }
    }
    headers = {'Content-Type': 'application/json'}

    return requests.put(
        url,
        auth=HTTPBasicAuth(user, password),
        data=json.dumps(data),
        headers=headers,
        verify=False)


def deleteperm(perm_name):
    url = artifactory_url + 'security/permissions/' + perm_name

    return requests.delete(
        url,
        auth=HTTPBasicAuth(user, password),
        verify=False)


def addtoperm(perm_name, repo_names, group_name, group_perms, public_read):
    '''
    perm_name (String): permission name to updated/add to
    repo_names (List): list of repos that the permissions is to be applied
    group_name (String): group name to add to permission
    group_perms (List): list of perms for the group
    public_read (Boolean): if True, anonymous users have read access
    '''
    if public_read == True:
        anonymous_perms = ['r']
    else:
        anonymous_perms = ['']

    p = getperm(perm_name)

    # users, groups, repos and config are dictionaries
    repos = jq(".repositories").transform(json.loads(p.text))
    new_repos = repos + repo_names
    config = jq(".").transform(json.loads(p.text))
    config['repositories'] = new_repos
    # each user/group and perms are its own key:value pair
    config['principals']['users']['anonymous'] = anonymous_perms
    config['principals']['groups'][group_name] = group_perms

    url = artifactory_url + 'security/permissions/' + perm_name
    headers = {'Content-Type': 'application/json'}

    return requests.put(
        url,
        auth=HTTPBasicAuth(user, password),
        data=json.dumps(config),
        headers=headers,
        verify=False)



# ----- MAIN ----- #

connection_info = readcreds()
hostname = connection_info[0].strip('\n\r')
artifactory_url = 'https://' + hostname + '/artifactory/api/'
user = connection_info[1].strip('\n\r')
password = connection_info[2].strip('\n\r')


createrepo('glen-generic1-local', 'generic')
#a = getrepo('glen-generic1-local')
#print(a.text)
creategroup('glen-group1', 'internal')
#b = getgroup('glen-group1')
#print(b.text)
createperm('glen-perm1', ['glen-generic1-local'], 'glen-group1', ['r','d'], True)
c = getperm('glen-perm1')
print(c.text)
createrepo('glen-maven1-local', 'maven')
d = getrepo('glen-maven1-local')
#print(d.text)
addtoperm('glen-perm1', ['glen-maven1-local'], 'glen-group1', ['r','d', 'n'], False)
e = getperm('glen-perm1')
print(e.text)
#print(e.status_code)
#if e.status_code == 200:
#    newgroups = jq(".principals.groups").transform(json.loads(e.text))
#    print(newgroups)
#    newlist = jq(".repositories").transform(json.loads(e.text))
#    print(newlist)
#    existing_config = jq(".").transform(json.loads(e.text))
#    print('COMBINED LIST')
#    blah = newlist + ['glen-maven1-local']
#    print(blah)
#    print('EXISTING_CONFIG')
#    print(type(existing_config))
#    print(existing_config)
#    print('DICT REPLACE')
#    for key in existing_config.keys():
#      print(key) 
#    print('HERE')
#    print(existing_config['principals']['groups'])
#    existing_config['repositories'] = blah
#    print(blah)
#    print(existing_config)
# elif e.status_code == 404 # Not found
#     print('perm not found!')

del_a = deleterepo('glen-generic1-local')
print(del_a.text)
del_b = deletegroup('glen-group1')
print(del_b.text)
del_c = deleteperm('glen-perm1')
print(del_c.text)
del_d = deleterepo('glen-maven1-local')
print(del_d.text)

test_group = 'somename'
test_group_perms = ['r','d']
