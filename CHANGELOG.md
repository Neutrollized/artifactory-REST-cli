# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](http://keepachangelog.com/en/1.0.0/)
and this project adheres to [Semantic Versioning](http://semver.org/spec/v2.0.0.html).

## [0.1.2] - 2018-??-??
### Added
- `requirements.txt` file

## [0.1.1] - 2018-08-28
### Added
- Login info can be passed as commandline argumentments (with `-s servername -u username -p password`)
- Credentials file for logging in can also be specified from commandline (with `--cred /path/to/file`)
- Functionality added for `--get`, `--add` and `--delete` actions
- Disabled `InsecureRequestWarning` warnings when SSL verification is disabled (`verify_ssl = False`)
### Fixed
- Some typos and incorrect variable references (the risks of cutting/pasting)


## [0.1.0] - 2018-08-27
### Added
- Initial release (beta?  no error validation of inputs as it was mean for use with Rundeck for now...)  Will be made more robust as a standalone later one
