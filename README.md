# 🚀 itopcli — Python CLI for iTop ITSM / CMDB

<p align="left">
  <a href="https://github.com/thomasliddledba/itopcli/blob/main/LICENSE">
    <img src="https://img.shields.io/badge/License-MIT-yellow.svg" />
  </a>
  <img src="https://img.shields.io/github/v/release/thomasliddledba/itopcli" />
  <img src="https://img.shields.io/badge/iTop-2.x%20%7C%203.x-orange.svg" />
  <img src="https://img.shields.io/badge/Maintained-Yes-brightgreen.svg" />
</p>

> A lightweight, powerful command-line interface for interacting with **Combodo iTop** via Web Services.

---

## ⭐ Star & Watch This Project

If you find this useful:

* ⭐ **Star the repo** to support development
* 👀 **Watch the repo** for updates and new features

---

## 📌 Overview

**itopcli** is a Python-based CLI tool for interacting with the iTop REST API, designed for:

* DevOps engineers
* IT administrators
* CMDB automation workflows
* Infrastructure management scripting

It provides a simple way to perform **CRUD operations** on iTop objects directly from the command line.

---

## 🎯 Key Use Cases

* Automating CMDB updates from scripts or pipelines
* Bulk querying infrastructure data
* Updating server attributes programmatically
* Integrating iTop with external systems
* Safe testing of API payloads with `--dry-run`

---

## ✅ Features

* 🔍 Query iTop objects (`core/get`)
* ✏️ Update objects (`core/update`)
* ➕ Create objects (`core/create`)
* ❌ Delete objects (`core/delete`)
* 🧪 Dry-run mode (preview API payloads)
* 📦 JSON output (perfect for `jq`, pipelines, automation)
* ⚡ Lightweight and fast

---

## 🖥️ Supported Platforms

| OS            | Supported |
| ------------- | --------- |
| Ubuntu 16.04+ | ✅         |
| Ubuntu 18.04+ | ✅         |
| Ubuntu 20.04+ | ✅         |
| Ubuntu 22.04+ | ✅         |
| Windows       | ✅         |

Supports:

* iTop 2.x
* iTop 3.x+

---

## 📦 Installation

```bash
sudo apt install python3-pip -y
git clone https://github.com/thomasliddledba/itopcli.git
cd itopcli
pip3 install -r requirements.txt
chmod +x ./itopcli
```

---

## ⚙️ Configuration

```bash
./itopcli configure \
  --location=".itopcli" \
  --url="http://localhost:8000" \
  --apisuffix="/webservices/rest.php" \
  --apiversion="1.3" \
  --organization="1" \
  --timeout=10 \
  --username="admin" \
  --password="MyAdminPassword1!"
```

---

# 🚀 Usage Guide

---

## 🔍 Query Command (core/get)

The query command is the **most powerful feature** of itopcli.

It mirrors iTop’s internal query language:

```
SELECT Class WHERE attribute = value
```

---

### 🔹 Get All Records

```bash
./itopcli query \
  --class Server \
  --attribute name \
  --criteria '*'
```

---

### 🔹 Query Specific Object

```bash
./itopcli query \
  --class Server \
  --attribute name \
  --criteria "Server01"
```

---

### 🔹 Query by Key (Recommended for automation)

```bash
./itopcli query \
  --class Server \
  --key 1
```

---

### 🔹 Limit Output Fields

```bash
./itopcli query \
  --class Server \
  --attribute name \
  --criteria '*' \
  --outputfields name,status,org_id
```

---

### 🔹 Query + jq (DevOps workflow)

```bash
./itopcli query --class Server --attribute name --criteria '*' \
  | jq '.objects[].fields.name'
```

---

### 🔹 Example Output

```json
{
  "objects": {
    "Server::1": {
      "fields": {
        "name": "Server01",
        "status": "production"
      }
    }
  }
}
```

---

## ✏️ Update Command (core/update)

Update specific fields on an object:

```bash
./itopcli update \
  --class Server \
  --key 1 \
  --set cpu=8 \
  --set ram=32 \
  --comment "Updated via CLI"
```

---

### 🔹 Update Using JSON

```bash
./itopcli update \
  --class Server \
  --key 1 \
  --fields-json '{"cpu":8,"ram":32}'
```

---

## ➕ Create Command (core/create)

Create a new object in iTop:

```bash
./itopcli create \
  --class Server \
  --set name=test-server-01 \
  --set cpu=8 \
  --set ram=32 \
  --set org_id=1
```

⚠️ **Important:**
Many iTop classes require specific fields (e.g. `org_id`).
Refer to your iTop data model for required attributes.

---

## ❌ Delete Command (core/delete)

```bash
./itopcli delete \
  --class Server \
  --key 1 \
  --comment "Removed via CLI"
```

---

## 🧪 Dry Run Mode

Preview API payloads safely before execution:

```bash
./itopcli update \
  --class Server \
  --key 1 \
  --set cpu=16 \
  --dry-run
```

---

## ⚙️ DevOps Tips & Best Practices

### ✔ Always use dry-run first

Prevent mistakes in production environments.

---

### ✔ Use jq for automation

```bash
./itopcli query ... | jq
```

---

### ✔ Prefer key-based operations

```bash
--key 1
```

More reliable than attribute matching.

---

### ✔ Understand required fields

Some classes require:

* `org_id`
* `location_id`
* etc.

---

### ✔ Use JSON for complex updates

```bash
--fields-json '{"tags":["web","prod"]}'
```

---

## 🔧 How Query Works (Important)

itopcli builds queries like:

```
SELECT Server WHERE name = 'Server01'
```

Understanding this helps you:

* debug queries
* build automation
* match iTop UI behavior

---

## 🔮 Roadmap

* 🔍 Lookup helpers (resolve names → IDs)
* 🔄 Workflow support (`apply_stimulus`)
* 🔗 Relationship management
* 📦 pip install packaging

---

## 🤝 Contributing

Contributions are welcome!

1. Fork the repo
2. Create a feature branch
3. Submit a PR

---

## 📄 License

MIT License

---

## 🙌 Acknowledgements

* Combodo iTop
* Python Click
* Open Source Community
