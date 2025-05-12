[![Tests](https://github.com/Mat-O-Lab/ckanext-multiuploader/actions/workflows/test.yml/badge.svg)](https://github.com/Mat-O-Lab/ckanext-multiuploader/actions/workflows/test.yml)


# ckanext-multiuploader

This CKAN extension helps users to upload multiple resources at once with drag&drop. 


## Requirements

Compatibility with core CKAN versions:

| CKAN version    | Compatible?   |
| --------------- | ------------- |
| 2.9 and arlier  | not tested    |
| 2.10             | yes    |
| 2.11            | yes    |

* "yes"
* "not tested" - I can't think of a reason why it wouldn't work
* "not yet" - there is an intention to get it working
* "no"


## Installation

To install the extension:

1. Activate your CKAN virtual environment, for example:
```bash
. /usr/lib/ckan/default/bin/activate
```
2. Use pip to install package
```bash
pip install ckanext-multiuploader
```
3. Add `multiuploader` to the `ckan.plugins` setting in your CKAN
   config file (by default the config file is located at
   `/etc/ckan/default/ckan.ini`).

4. Restart CKAN. For example, if you've deployed CKAN with Apache on Ubuntu:
```bash
sudo service apache2 reload
```

## Usage and Config

**Note**: you have to set the max resource size in ckan configuration (`/etc/ckan/default/ckan.ini`)
```bash
ckan.max_resource_size
```

## Developer installation

To install ckanext-multiuploader for development, activate your CKAN virtualenv and
do:
```bash
git clone https://github.com/Mat-O-Lab/ckanext-multiuploader.git
cd ckanext-multiuploader
python setup.py develop
pip install -r dev-requirements.txt
```

## Tests

To run the tests, do:
```bash
pytest --ckan-ini=test.ini
```

# Acknowledgments
The authors would like to thank the developers of the original project https://github.com/TIBHannover/ckanext-multiuploader.