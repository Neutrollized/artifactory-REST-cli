#!/usr/bin/env python

#
# Author: Glen Yu (glen.yu@gmail.com)
#
# example usage:
# ./artifactory-REST-cli.py --add \
#                           --repo mynpmrepo --repopackage npm \
#                           --group mygroup \
#                           --perm myperm --groupperm rd \
#                           --public
#
# will add a new (local) npm repository called 'mynpmrepo'
# create a new (internal) group called 'mygroup' 
# assign it the permission set 'myperm'
# 'myperm' dictates that 'mygroup' will have read(r) and delete(d) perms in the repo 'mynpmrepo'
# anonymous users will have read access to that repository
#


#requires PyPI jq and requests
import argparse
import json
import requests, urllib3
from jq import jq
from requests.auth import HTTPBasicAuth


# ----- Variables/Settings ----- #

verify_ssl = False
# disable the InsecureRequestWarning that warns about unverified HTTPS requests
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# https://www.jfrog.com/confluence/display/RTF/Repository+Layouts
repo_layout = {
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


# ----- Get password/API key ----- #

def readcreds(credential_file):
    pw_file = credential_file
    f = open(pw_file, "r")
    contents = f.readlines()

    return contents


# ----- Users REST API functions ----- #

# https://www.jfrog.com/confluence/display/RTF/Artifactory+REST+API#ArtifactoryRESTAPI-GetUserDetails
def getuser(user_name):
    url = artifactory_url + 'security/users/' + user_name

    return requests.get(
        url,
        auth=HTTPBasicAuth(artifactory_user, artifactory_password),
        verify=verify_ssl)


# https://www.jfrog.com/confluence/display/RTF/Artifactory+REST+API#ArtifactoryRESTAPI-UpdateUser
def addusergroup(user_name, group_name):
    u = getuser(user_name)
    groups = jq(".groups").transform(json.loads(u.text))

    group_name = [group_name]

    # is group_name is a subset of groups
    if set(group_name) <= set(groups):
        new_groups = groups
    else:
        new_groups = groups + group_name

    config = jq(".").transform(json.loads(u.text))
    config['groups'] = new_groups

    url = artifactory_url + 'security/users/' + user_name
    headers = {'Content-Type': 'application/json'}

    return requests.post(
        url,
        auth=HTTPBasicAuth(artifactory_user, artifactory_password),
        data=json.dumps(config),
        headers=headers,
        verify=verify_ssl)


# https://www.jfrog.com/confluence/display/RTF/Artifactory+REST+API#ArtifactoryRESTAPI-DeleteUser
def deleteuser(user_name):
    url = artifactory_url + 'security/users/' + user_name

    return requests.delete(
        url,
        auth=HTTPBasicAuth(artifactory_user, artifactory_password),
        verify=verify_ssl)


# ----- Groups REST API functions ----- #

# https://www.jfrog.com/confluence/display/RTF/Artifactory+REST+API#ArtifactoryRESTAPI-GetGroupDetails
def getgroup(group_name):
    url = artifactory_url + 'security/groups/' + group_name

    return requests.get(
        url,
        auth=HTTPBasicAuth(artifactory_user, artifactory_password),
        verify=verify_ssl)


# https://www.jfrog.com/confluence/display/RTF/Artifactory+REST+API#ArtifactoryRESTAPI-CreateorReplaceGroup
# realm_type: internal | ldap
def creategroup(group_name, group_realm):
    '''
    group_realm (String): local | crowd | ldap
    '''
    url = artifactory_url + 'security/groups/' + group_name
    data = {
        "autoJoin": "false",
        "realm": group_realm,
        "adminPrivileges": "false"
    }
    headers = {'Content-Type': 'application/json'}

    return requests.put(
        url,
        auth=HTTPBasicAuth(artifactory_user, artifactory_password),
        data=json.dumps(data),
        headers=headers,
        verify=verify_ssl)


# https://www.jfrog.com/confluence/display/RTF/Artifactory+REST+API#ArtifactoryRESTAPI-DeleteGroup
def deletegroup(group_name):
    url = artifactory_url + 'security/groups/' + group_name

    return requests.delete(
        url,
        auth=HTTPBasicAuth(artifactory_user, artifactory_password),
        verify=verify_ssl)


# ----- Repo REST API functions ----- #

# https://www.jfrog.com/confluence/display/RTF/Artifactory+REST+API#ArtifactoryRESTAPI-RepositoryConfiguration
def getrepo(repo_name):
    url = artifactory_url + 'repositories/' + repo_name

    return requests.get(
        url,
        auth=HTTPBasicAuth(artifactory_user, artifactory_password),
        verify=verify_ssl)


# https://www.jfrog.com/confluence/display/RTF/Artifactory+REST+API#ArtifactoryRESTAPI-CreateRepository
def createrepo(repo_name, repo_class, repo_package):
    '''
    repo_type (String): local | remote | virtual
    repo_package (String): see "repo_layout" dictionary in Variables section
    '''
    url = artifactory_url + 'repositories/' + repo_name
    data = {
        "rclass": repo_class,
        "packageType": repo_package,
        "repoLayoutRef": repo_layout[repo_package]
    }
    headers = {'Content-Type': 'application/json'}

    return requests.put(
        url,
        auth=HTTPBasicAuth(artifactory_user, artifactory_password),
        data=json.dumps(data),
        headers=headers,
        verify=verify_ssl)


# https://www.jfrog.com/confluence/display/RTF/Artifactory+REST+API#ArtifactoryRESTAPI-DeleteRepository
def deleterepo(repo_name):
    url = artifactory_url + 'repositories/' + repo_name

    return requests.delete(
        url,
        auth=HTTPBasicAuth(artifactory_user, artifactory_password),
        auth=HTTPBasicAuth(user, password),
        verify=verify_ssl)


# ----- Permissions REST API functions ----- #

# https://www.jfrog.com/confluence/display/RTF/Artifactory+REST+API#ArtifactoryRESTAPI-GetPermissionTargetDetails
def getperm(perm_name):
    url = artifactory_url + 'security/permissions/' + perm_name

    return requests.get(
        url,
        auth=HTTPBasicAuth(artifactory_user, artifactory_password),
        verify=verify_ssl)


# https://www.jfrog.com/confluence/display/RTF/Artifactory+REST+API#ArtifactoryRESTAPI-CreateorReplacePermissionTarget
def createperm(perm_name, repo_name, group_name, group_perms, public_read):
    '''
    repo_name (String): list of repos that the permissions is to be applied
    group_perms (List): list of perms for the group
    public_read (Boolean): if True, anonymous users have read access
    '''
    if public_read == True:
        anonymous_perms = ['r']
    else:
        anonymous_perms = ['']

    # make repo_name a list
    repo_name = [repo_name]

    url = artifactory_url + 'security/permissions/' + perm_name
    data = {
        "repositories": repo_name,
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
        auth=HTTPBasicAuth(artifactory_user, artifactory_password),
        data=json.dumps(data),
        headers=headers,
        verify=verify_ssl)


# https://www.jfrog.com/confluence/display/RTF/Artifactory+REST+API#ArtifactoryRESTAPI-DeletePermissionTarget
def deleteperm(perm_name):
    url = artifactory_url + 'security/permissions/' + perm_name

    return requests.delete(
        url,
        auth=HTTPBasicAuth(artifactory_user, artifactory_password),
        verify=verify_ssl)


# https://www.jfrog.com/confluence/display/RTF/Artifactory+REST+API#ArtifactoryRESTAPI-CreateorReplacePermissionTarget
# IMPORTANT: there is no ability to simply add a new repo or group, etc to an existing perm
#            you can only recreate.  Hence this will get the config of an existing permission
#            and modify it before having it recreated
def addtoperm(perm_name, repo_name, group_name, group_perms, public_read):
    '''
    perm_name (String): permission name to updated/add to
    repo_name (String): name of repo that the permissions is to be applied
    group_name (String): group name to add to permission
    group_perms (List): list of perms for the group
    public_read (Boolean): if True, anonymous users have read access
    '''
    if public_read == True:
        anonymous_perms = ['r']
    else:
        anonymous_perms = ['']

    repo_name = [repo_name]

    p = getperm(perm_name)
    # users, groups, repos and config are dictionaries
    repos = jq(".repositories").transform(json.loads(p.text))
    # is repo_name is a subset of repos
    if set(repo_name) <= set(repos):
        new_repos = repos
    else:
        new_repos = repos + repo_name

    config = jq(".").transform(json.loads(p.text))
    config['repositories'] = new_repos
    # each user/group and perms are its own key:value pair
    config['principals']['users'] = {'anonymous': anonymous_perms}
    config['principals']['groups'][group_name] = group_perms

    url = artifactory_url + 'security/permissions/' + perm_name
    headers = {'Content-Type': 'application/json'}

    return requests.put(
        url,
        auth=HTTPBasicAuth(artifactory_user, artifactory_password),
        data=json.dumps(config),
        headers=headers,
        verify=verify_ssl)



# ----- MAIN ----- #

if __name__ == '__main__':
    # parse command line arguments
    parser = argparse.ArgumentParser()
    action = parser.add_mutually_exclusive_group(required=True)
    action.add_argument('--get', action='store_true', default=False)
    action.add_argument('--add', action='store_true', default=False)
    action.add_argument('--delete', action='store_true', default=False)
    login = parser.add_argument_group('login')
    login.add_argument('--cred', default='/tmp/.artifactory_info', type=str,
                        help='credentials file for Artifactory login containing servername, username and password')
    login.add_argument('-s', type=str, help='Artifactory server name')
    login.add_argument('-u', type=str, help='Artifactory login username')
    login.add_argument('-p', type=str, help='Artifactory login password')
    user = parser.add_argument_group('user')
    user.add_argument('--user', type=str)
    user.add_argument('--usergroup', type=str)
    group = parser.add_argument_group('group')
    group.add_argument('--group', type=str)
    group.add_argument('--grouprealm', default='internal', type=str,
                        help='internal | crowd | ldap')
    repo = parser.add_argument_group('repository')
    repo.add_argument('--repo', type=str)
    repo.add_argument('--repoclass', default='local', type=str,
                        help='local | remote | virtual')
    repo.add_argument('--repopackage', default='generic', type=str,
                        help='generic | maven | npm , etc.')
    perm = parser.add_argument_group('permission')
    perm.add_argument('--perm', type=str)
    perm.add_argument('--groupperm', type=list,
                        help='m=manage, d=delete, w=deploy, n=annotate, r=read')
    perm.add_argument('--public', action='store_true', default=False,
                        help='enable public/anonymous user read')
    args = parser.parse_args()

    # get connection info
    if args.s != None and args.u != None and args.p != None: 
        artifactory_url = 'https://' + args.s + '/artifactory/api/'
        artifactory_user = args.u
        artifactory_password = args.p
    else:
        connection_info = readcreds(args.cred)
        hostname = connection_info[0].strip('\n\r')
        artifactory_url = 'https://' + hostname + '/artifactory/api/'
        artifactory_user = connection_info[1].strip('\n\r')
        artifactory_password = connection_info[2].strip('\n\r')


    # action selected was --get
    if args.get:
        if args.user != None:
            gu = getuser(args.user)
            print(gu.text)
        elif args.group != None:
            gg = getgroup(args.group)
            print(gg.text)
        elif args.repo != None:
            gr = getrepo(args.repo)
            print(gr.text)
        elif args.perm != None:
            gp = getperm(args.perm)
            print(gp.text)


    # action selected was --add
    if args.add and args.user != None and args.usergroup != None:
        gu = getuser(args.user)
        gg = getgroup(args.usergroup)
        if gu.status_code == 200 and gg.status_code == 200:    # user and group exists exists
            print('ADDING GROUP ' + args.usergroup + ' TO USER ' + args.user)
            addusergroup(args.user, args.usergroup)
            gu = getuser(args.user)
            print(gu.text)
        elif gu.status_code == 404 or gg.status_code == 404:
            print('USER and/or GROUP DOES NOT EXIST')
    elif args.add:
        gr = getrepo(args.repo)
        if gr.status_code == 400:    # create new repo 
            print('CREATE REPOSITORY ' + args.repo)
            cr = createrepo(args.repo, args.repoclass, args.repopackage)
            print(cr.text)
        
        gg = getgroup(args.group)
        if gg.status_code == 404:    # create new group
            print('CREATE GROUP ' + args.group)
            cg = creategroup(args.group, args.grouprealm)
            print(cg.text)

        gp = getperm(args.perm)
        if gp.status_code == 404:    # create new perm entry
            print('CREATE PERMISSIONS ' + args.perm)
            cp = createperm(args.perm, args.repo, args.group, args.groupperm, args.public)
            gp = getperm(args.perm)
            print(gp.text)
        elif gp.status_code == 200:    # perm already exists, modify existing
            print('UPDATE PERMISSIONS ' + args.perm)
            cp = addtoperm(args.perm, args.repo, args.group, args.groupperm, args.public)
            gp = getperm(args.perm)
            print(gp.text)


    # action selected was --delete
    if args.delete:
        if args.repo != None:
            print('DELETE REPOSITORY ' + args.repo)
            dr = deleterepo(args.repo)
            print(dr.text)
        elif args.group != None:
            print('DELETE GROUP ' + args.group)
            dg = deletegroup(args.group)
            print(dg.text)
        elif args.perm != None:
            print('DELETE PERMISSIONS ' + args.perm)
            dp = deleteperm(args.perm)
            print(dp.text)
