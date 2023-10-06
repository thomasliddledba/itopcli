# itopcli

ITopcli is a python program to query (read-only) the popular ITIL tool [Combodo iTop ITSM Software](https:/www.combodo.com/).
Currently this focuses on the Configuration Management aspect of the software.  I'll continue to work on other areas.

```console
    Usage: itopcli [OPTIONS] COMMAND [ARGS]...

    Options:
    --help  Show this message and exit.

    Commands:
    configure  Configure itopcli options.
    query      Query classes (core/get) in iTop
```

## Support

ITop Version 3.x +

>Note - I have tested this in ITop 2.x versions also with no issues.

| OS | Success |
| --- | --- |
| Ubuntu 22.04 + Python3.5+ | Yes |
| Ubuntu 20.04 + Python3.5+ | Yes |
| Ubuntu 18.04 + Python3.5+ | Yes |
| Ubuntu 16.04 + Python3.5+ | Yes |
| Windows + Python3.5+ | Yes |

## Installation

```console
sudo apt install python3-pip -y
git clone https://github.com/thomasliddledba/itopcli.git
cd itopcli/
pip3 install -r requirements.txt
chmod +x ./itopcli
```

### Configure

### Create config file

```console
./itopcli configure \
--location=".itopcli" \
--url="http://localhost:8000" \
--apisuffix="/webservices/rest.php" \
--apiversion="1.3" \
--organization="Demo" \
--timeout=10 \
--username="admin" \
--password="MyAdminPassword1!"
```

## Usage

### Query Command

This client produces JSON for every query (even errors). You can format the JSON to your specs using the popular (jq) command. You can specify the `--outputfields` to list specific fields you would like to have displayed. The default is `*` or all fields.

The class, attribute, and criteria are based on iTop's object schema. The object schema is found in the software under `Administration>Data Model`. I tried to mimic the [iTop Data Model](https://www.itophub.io/wiki/page?id=latest%3Adatamodel%3Astart) in this tool closely.

If specified in the same command, the --key option precedes the --criteria option.

#### Get All Records

```console
./itopcli query --class='Server' --attribute='name' --criteria='*' --outputfields='*'
```

```console
{
  "objects": {
    "Server::1": {
      "code": 0,
      "message": "",
      "class": "Server",
      "key": "1",
      "fields": {
        "name": "Server1",
        "description": "",
...
    },
    "Server::2": {
      "code": 0,
      "message": "",
      "class": "Server",
      "key": "2",
      "fields": {
        "name": "Server2",
        "description": ""
        ...
      },
      ...
  },
{
  "code": 0,
  "message": "Found: 4"
}
```

#### Query Specific Records

```console

./itopcli query --class='Server' --attribute='name' --criteria='Server1' --outputfields='*'
```

```console
{
  "objects": {
    "Server::1": {
      "code": 0,
      "message": "",
      "class": "Server",
      "key": "1",
      "fields": {
        "name": "Server1",
        ...
      }
  },
{
  "code": 0,
  "message": "Found: 1"
}
```

#### Query Specific Records with target data fields

```console
./itopcli query --class='Server' --attribute='name' --criteria='Server1' --outputfields='name, status'
 ```

 ```console
{
  "objects": {
    "Server::1": {
      "code": 0,
      "message": "",
      "class": "Server",
      "key": "1",
      "fields": {
        "name": "Server1",
        "status": "production"
      }
    }
  },
  "code": 0,
  "message": "Found: 1"
}
```

## How to Contribute

I'd love for anyone to contribute.  Please read the [CONTRIBUTING.md](CONTRIBUTING.md) document for more information.
