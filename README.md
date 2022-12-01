## Installation

#### Install Python latest release.

Follow the instructions [here](https://wiki.python.org/moin/BeginnersGuide/Download) how to download and install python for you OS

For windows make sure you have included python installation in enviroment path
 
#### Clone the repository

`git clone https://github.com/ShadeGr/saphetor.git`


#### Install dependencies

Enter project directory

`cd saphetor/`

the project directory should have a structure like below

```

│   .gitignore
│   db.sqlite3
│   manage.py
│   README.md
│   requirements.txt
│
├───saphetor
│       asgi.py
│       settings.py
│       urls.py
│       wsgi.py
│       __init__.py
│
└───vcfapi
    │   admin.py
    │   apps.py
    │   authentication.py
    │   models.py
    │   serializers.py
    │   tests.py
    │   urls.py
    │   usecases.py
    │   vcfreader.py
    │   views.py
    │   __init__.py
    │
    └───migrations
            __init__.py
```

install required packages from requirements.txt

`pip install -r requirements.txt`

## Configuring VCF file
To import a vcf file as database, edit `VCF_FILE` variable in saphetor/settings.py file and place the full path of the vcf file. 
Eg */home/user/path/to/file.vcf*

**Note** If relative path is used, the file should be placed under the root directory saphetor/vcfapi

## Starting the server

In project directory there should be a python file manage.py

`python manage.py runserver`

## Rest API

### Authorization

For POST, PUT, DELETE methods user must provide HTTP header ***Authorization: Basic test***

### Get record list.

User must provide valid parameters for:

**ofs:** incremental value representing the zero-based record in the file (ofs=0 means first record). 

**size:** the number of records the api returns starting from <ofs>

#### Headers
Headers should include Accept with a valid type
- application/json
- application/xml
- \*/\*

Eg

GET http://localhost:8000/vcfapi/records/?ofs=5&size=10

The above request fetches 10 vcf records starting from fifth record (5)

if no parameters are provided, default ofs = 0 and default size = 10

### Get exact record

GET http://localhost:8000/vcfapi/records/?id=rsXXX

#### Headers
Headers should include Accept with a valid type
- application/json
- application/xml
- \*/\*

where rsXXX is the requested id eg *rs62635284*

### Delete record

DELETE http://localhost:8000/vcfapi/records/?id=rsXXX

### Insert record

POST http://localhost:8000/vcfapi/records/

provide a valid json body like

{"CHROM": "chr1", "POS": 1000, "ALT": "A", "REF": "G",
"ID": "rs123"}

Headers:

Content-Type: application/json
Authorization: Basic test

### edit record

PUT http://localhost:8000/vcfapi/records/?id=rsXXX

provide a valid json body like

`{"CHROM": "chr1", "POS": 1000, "ALT": "A", "REF": "G",
"ID": "rs123"}`

request headers must include:

Content-Type: application/json
Authorization: Basic test

id in url must match the id in json body

## Running tests

`python manage.py test vcfapi.tests.VCFApiTestcase`

Note: Running tests needs a vcf file that will 

