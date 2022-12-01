## Installation

#### Install Python latest release.

Follow the instructions [here](https://wiki.python.org/moin/BeginnersGuide/Download) how to download and install python for you OS

For windows make sure you have included python installation in enviroment path
 
#### Clone the repository

`git clone https://github.com/ShadeGr/saphetor.git`

#### Install dependencies

Enter project directory

`cd saphetor/`

install required packages from requirements.txt

```
PS E:\saphetor> ls

    Directory: E:\saphetor

Mode                 LastWriteTime         Length Name
----                 -------------         ------ ----
d----          29/11/2022  1:11 πμ                saphetor
d----           1/12/2022  3:19 πμ                vcfapi
-a---          30/11/2022 10:47 μμ            728 .gitignore
-a---          30/11/2022  9:34 μμ            379 .project
-a---          30/11/2022  9:34 μμ            323 .pydevproject
-a---          29/11/2022  1:11 πμ              0 db.sqlite3
-a---          30/11/2022  9:13 μμ             88 instructions.txt
-a---          29/11/2022 12:59 πμ            686 manage.py
-a---           1/12/2022 11:36 πμ            649 README.md
-a---          30/11/2022  9:32 μμ             76 requirements.txt
```

`pip install -r requirements.txt`

## Configuring file
To import a vcf file as database, edit `VCF_FILE` variable in saphetor/settings.py file. Prefer absolute path. If relative path is used, the root directory is saphetor/vcfapi

## Running the server

In project directory there should be a python file manage.py

`python manage.py runserver`


## Running tests

`python manage.py test vcfapi.tests.VCFApiTestcase`

Note: Running tests needs a vcf file that will 

