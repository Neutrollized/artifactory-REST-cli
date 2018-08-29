[![Code Climate](https://codeclimate.com/github/Neutrollized/artifactory-REST-cli.png)](https://codeclimate.com/github/Neutrollized/artifactory-REST-cli)

# artifactory-REST-cli
CLI written in Python to supplement what the [jfrog-cli](https://jfrog.com/getcli/) can't do at the moment (mainly repo creation, groups, etc.)


## Requirements

You will need Python 2.7 and the following [PyPI](https://pypi.org) packages:
* [jq](https://pypi.org/project/jq/)
* [requests](https://pypi.org/project/requests/)


## Usage/--help
```
usage: artifactory-REST-cli.py [-h] (--get | --add | --delete) [--cred CRED]
                               [-s S] [-u U] [-p P] [--user USER]
                               [--usergroup USERGROUP] [--group GROUP]
                               [--grouprealm GROUPREALM] [--repo REPO]
                               [--repoclass REPOCLASS]
                               [--repopackage REPOPACKAGE] [--perm PERM]
                               [--groupperm GROUPPERM] [--public]

optional arguments:
  -h, --help            show this help message and exit
  --get
  --add
  --delete

login:
  --cred CRED           credentials file for Artifactory login containing
                        servername, username and password
  -s S                  Artifactory server name
  -u U                  Artifactory login username
  -p P                  Artifactory login password

user:
  --user USER
  --usergroup USERGROUP

group:
  --group GROUP
  --grouprealm GROUPREALM
                        internal | crowd | ldap

repository:
  --repo REPO
  --repoclass REPOCLASS
                        local | remote | virtual
  --repopackage REPOPACKAGE
                        generic | maven | npm , etc.

permission:
  --perm PERM
  --groupperm GROUPPERM
                        m=manage, d=delete, w=deploy, n=annotate, r=read
  --public              enable public/anonymous user read
```


## Example

Command
```
./artifactory-REST-cli.py --add --repo myrepo --repopackage npm --group mygroup --perm mypermissions --groupperm rd
```

Output
```
CREATE REPOSITORY...
CREATE GROUP...
CREATE PERMISSIONS...
{
  "name" : "mypermissions",
  "includesPattern" : "**",
  "excludesPattern" : "",
  "repositories" : [ "myrepo" ],
  "principals" : {
    "groups" : {
      "mygroup" : [ "r", "d" ]
    }
  }
}
```

### Docker Container Usage Example
```
docker run -it --rm -v /tmp/mycredentialsfile:/mnt/artifactory_info neutrollized/artifactory-rest-cli:0.1.1 --cred /mnt/artifactory_info --get --user glen 
```


## Notes

There's very little error checking/input validation as I developed this mainly for use at work which uses [Rundeck](https://www.rundeck.com/) to call this script and values passed to it will be selected from dropdowns so very little can go wrong.  I will work on this to add more functionality and robustness as a standalone cli script.

### PRs welcome!
