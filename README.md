[![Code Climate](https://codeclimate.com/github/Neutrollized/artifactory-REST-cli.png)](https://codeclimate.com/github/Neutrollized/artifactory-REST-cli)

# artifactory-REST-cli
CLI written in Python to supplement what the [jfrog-cli](https://jfrog.com/getcli/) can't do at the moment (mainly repo creation, groups, etc.)


## Requirements

You will need Python 2.7 and the following [PyPI](https://pypi.org) packages:
* [jq](https://pypi.org/project/jq/)
* [requests](https://pypi.org/project/requests/)


### Example

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


## Notes

There's very little error checking/input validation as I developed this mainly for use at work which uses [Rundeck](https://www.rundeck.com/) to call this script and values passed to it will be selected from dropdowns so very little can go wrong.  I will work on this to add more functionality and robustness as a standalone cli script.

### PRs welcome!
