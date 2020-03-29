# itopcli

Python program to query (read-only) the popular ITSM/CMDB software [Combodo iTop ITSM Software](https:/www.combodo.com/).

```console
    Usage: itopcli [OPTIONS] COMMAND [ARGS]...

    Options:
    --help  Show this message and exit.

    Commands:
    configure  Configure itopcli options.
    query      Query classes (core/get) in iTop
```

## Tests

| OS | Success |
| --- | --- |
| Ubuntu 18.04 + Python3| Yes |
| Ubuntu 18.04 + Python2 | Yes |
| Ubuntu 16.04 + Python3 | Yes |
| Ubuntu 16.04 + Python2 | Yes |
| Windows + Python2 | Yes |
| Windows + Python3 | Yes |

## Prerequisites

### Pip (non-v3)

```console
git clone https://github.com/thomasliddledba/itopcli.git
cd itopcli/
pip install -r requirements.txt
chmod +x ./itopcli
```

### Pip3

```console
sudo apt install python3-pip -y
git clone https://github.com/thomasliddledba/itopcli.git
cd itopcli/
pip3 install -r requirements.txt
chmod +x ./itopcli
```

## Installation

## Usage

### Configure Help

```console
./itopcli configure --help
 $ ./itopcli configure --help
Usage: itopcli configure [OPTIONS]

  Configure itopcli options.  This command takes arguments. Use the 'itopcli
  --help' command to get a list of arguments.

  Notes:

  The user configured to use this client tool must be part of the Profile
  called 'REST Services User' within iTop.

Options:
  --location TEXT         Location of iTopcli configuration file to configure
  --url TEXT              Root Domain name of iTop Server  [required]
  --apisuffix TEXT        Web Context location of rest.php
  --apiversion [1.2|1.3]  Supported iTop REST Version
  --organization TEXT     Default iTop Organization
  --timeout INTEGER       HTTP Timeout  [required]
  --username TEXT         User Name for REST User
  --password TEXT         Password for REST User
  --help                  Show this message and exit.

```

### Configure Command

```console
./itopcli configure \
--location=".itopcli" \
--url="lucy.local" \
--apisuffix="/webservices/rest.php" \
--apiversion="1.3" \
--organization="My Company/Department" \
--timeout=10 \
--username="admin" \
--password="passwordForAdminUser"
```

### Query Help

```console
./itopcli query --help
Usage: itopcli query [OPTIONS]

  Description:

  Query classes (core/get) in iTop

  Notes:

  The --key option takes precedence over --criteria option

Options:
  --class TEXT         iTop Server Class  [required]
  --attribute TEXT     Attribute code for iTop Class  [required]
  --criteria TEXT      Search criteria for iTop Class Attribute  [required]
  --outputfields TEXT  Fields to be displayed in JSON (Comma-separated)
  --help               Show this message and exit.
```

### Query Command

This client produces json for every query (even errors).  You can use the popular (jq) command
to format the json to your specs.  You can specify the `--outputfields` to list specific
fields you would like to have displayed.  The default is `*` or all fields.

The class, attribute, and criteria are based on iTop's object schema.  You can find
the object schema in the software under `Admin Tools>Data Model`.  I tried to closely mimic the
[iTop Data Model](https://www.itophub.io/wiki/page?id=latest%3Adatamodel%3Astart) in this tool.

The `--key` option takes precedence over `--criteria` option if specified in the same command.

```console

./itopcli query --class='WebServer' --attribute='name' --criteria='lucy' --outputfields='*'
{
  "objects": {
    "WebServer::2": {
      "code": 0,
      "message": "",
      "class": "WebServer",
      "key": "2",
      "fields": {
        "name": "lucy",
        "description": "",
        "org_id": "1",
        "organization_name": "My Company/Department",
        "business_criticity": "low",
        "move2production": ""
        ...
      }
    }
  },
  "code": 0,
  "message": "Found: 1"
}

```

```console

./itopcli query --class='WebServer' --attribute='name' --criteria='*' --outputfields='*'
{
  "objects": {
    "WebServer::2": {
      "code": 0,
      "message": "",
      "class": "WebServer",
      "key": "2",
      "fields": {
        "name": "lucy",
        "description": "",
        "org_id": "1",
        "organization_name": "My Company/Department",
        "business_criticity": "low",
        "move2production": ""
        ...
      }
    }
  },
  "code": 0,
  "message": "Found: 1"
}

```

### Things to Note

1. I originally wrote this for Python3 but I understood, even in my own setup that users still
use Python2 (despite its support).  Feel free to change the program (she-bash Line 1), if needed.
2. I don't have a pipeline setup yet (it's on my TODO).
3. I use `pylint3` WITHOUT configuration file.  If you contirubte please lint with `pylint3` with no config file.

## How to Contribute

I'd love for anyone to contribute.  Please read the [CONTRIBUTING.md](CONTRIBUTING.md) document for more information.

## Thanks

Not applicable at this time
