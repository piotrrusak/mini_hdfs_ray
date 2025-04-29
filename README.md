# mini_hdfs_ray

A minimalist distributed storage system inspired by HDFS (Hadoop Distributed File System), built in Python using the Ray framework.

---

## 🚀 Overview

This project demonstrates the core principles of distributed file systems:
- Splitting data into chunks
- Distributing and replicating chunks across storage nodes
- Monitoring node health and healing data
- Centralized coordination (NameNode)

**Core components:**
- `DataManager`: The central node managing metadata and chunk distribution (like HDFS NameNode)
- `DataSpace`: Worker nodes that store chunks (like HDFS DataNode)
- `AutoHealer`: Background actor that restores lost replicas in case of node failure

---

## 📁 Project Structure

```
mini_hdfs_ray/
├── examples/
│   ├── demo.py        # Demonstration of system usage
├── src/
│   ├── artifact.py        # Handles metadata of stored artifacts
│   ├── auto_healer.py     # Actor that monitors and restores lost data
│   ├── data_manager.py    # Main coordination logic for storing and retrieving
│   ├── data_space.py      # Simulated storage nodes
│   └── logger.py          # Central logging setup
├── tests/
│   └── test_basic.py      # PyTest tests for key system operations
├── requirements.txt       # Required Python packages
├── README.md              # Project documentation
└── .gitignore             # Files to ignore in version control
```

---

## 🛠️ Installation

```bash
git clone https://github.com/your-username/mini_hdfs_ray.git
cd mini_hdfs_ray
pip install -r requirements.txt
```

---

## ▶️ Run Demo

```bash
python examples/demo.py
```

This runs a sample scenario including:
- Uploading an artifact
- Simulating node failure
- Healing lost replicas
- Retrieving the full data

---

## ✅ Run Tests

```bash
pytest
```

---

## 📚 Technologies Used

- Python 3.10
- [Ray](https://docs.ray.io/) — Actor-based distributed computing framework
- NumPy — Chunking and data manipulation
- PyTest — Testing framework
- Logging — Configurable system logs

---

## 💼 License

This project is licensed under the MIT License.

---

## 👨‍💻 Author

Feel free to use, adapt or extend it for your own learning or portfolio!
