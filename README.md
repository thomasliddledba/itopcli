# 🚀 itopcli — Python CLI for iTop ITSM / CMDB

> A lightweight, powerful command-line interface for interacting with **Combodo iTop** via Web Services.

itopcli is a powerful, lightweight Python command-line tool for interacting with the Combodo iTop ITSM platform via Web Services.
Designed for DevOps engineers and IT administrators, it enables seamless CMDB automation—supporting query, create, update, and delete operations, along with safe dry-run previews.
Perfect for scripting, integrations, and infrastructure management workflows.

---

## ⭐ Star this project on GitHub

If you find this useful, please ⭐ star the repository and share it!

👉 Watch the repo to stay updated with new features and improvements.

---

## 📌 Overview

**itopcli** is a Python-based CLI tool designed to interact with the iTop REST API.  
It focuses primarily on **CMDB (Configuration Management Database)** operations, allowing you to:

- 🔍 Query objects
- ✏️ Update records
- ➕ Create new objects
- ❌ Delete objects
- 🧪 Preview API payloads with `--dry-run`

Perfect for:
- DevOps engineers
- ITSM automation
- CMDB management
- Scripting and integrations

---

## ✅ Features

- Simple CLI interface (built with `click`)
- Full CRUD support (Create, Read, Update, Delete)
- JSON output for automation (pipe to `jq`)
- `--dry-run` mode for safe testing
- Flexible input (`--set` or JSON)
- Supports iTop 2.x and 3.x+

---

## 🖥️ Supported Platforms

| OS | Supported |
|----|----------|
| Ubuntu 16.04+ | ✅ |
| Ubuntu 18.04+ | ✅ |
| Ubuntu 20.04+ | ✅ |
| Ubuntu 22.04+ | ✅ |
| Windows | ✅ |

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
./itopcli configure   --location=".itopcli"   --url="http://localhost:8000"   --apisuffix="/webservices/rest.php"   --apiversion="1.3"   --organization="1"   --timeout=10   --username="admin"   --password="MyAdminPassword1!"
```

---

## 🚀 Usage Guide

### 🔍 Query

```bash
./itopcli query --class Server --attribute name --criteria '*'
```

### ✏️ Update

```bash
./itopcli update --class Server --key 1 --set cpu=8
```

### ➕ Create

```bash
./itopcli create --class Server --set name=test --set org_id=1
```

### ❌ Delete

```bash
./itopcli delete --class Server --key 1
```

---

## 🧪 Dry Run

```bash
./itopcli create --class Server --set name=test --set org_id=1 --dry-run
```

---

## 🔮 Roadmap

- Lookup helpers
- apply_stimulus support
- Relationship management

---

## 🤝 Contributing

Pull requests welcome!
