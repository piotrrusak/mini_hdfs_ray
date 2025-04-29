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
│   ├── local_demo.py                   # Demonstration of local system usage
│   ├── remote_auto_healer_init.py      # Initialization of auto healer
│   ├── remote_demo.py                  # Demonstration of remote system usage
│   ├── remote_manager_init.py          # Initialization of manager
│   ├── remote_space_init.py            # Initialization of space
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

## ▶️ Run Local Demo

```bash
    python examples/local_demo.py
```

This runs a sample scenario including:
- Uploading an artifact
- Simulating node failure
- Healing lost replicas
- Retrieving the full data

---

## ▶️ Run Remote Demo

To run the remote demo, follow the steps below in three separate terminals:

### 🖥️ Terminal 1 – Launch DataManager

```
    ray start --head --port=6379 --resources='{"manager": 1}'
    python examples/remote_manager_init.py
```

When you launch the DataManager (head node), you will see a log like:

```
    Next steps
      To add another node to this Ray cluster, run
        ray start --address='<HEAD_NODE_IP>:6379'
```

Use this IP address as <HEAD_NODE_IP> in Terminal 2.

### 🖥️ Terminal 2 – Launch DataSpaces

```
    ray start --address=<HEAD_NODE_IP>:6379 --resources='{"space": 10}'
    python examples/remote_space_init.py
```

### 🖥️ Terminal 3 – Launch AutoHealer

```
    python examples/remote_auto_healer_init.py
```

### 🖥️ Terminal 4 – Run the Demo

```
    python examples/remote_demo.py
```

You should see logs about storing and retrieving artifacts from the distributed storage system.

This runs a sample scenario including:
- Uploading an artifact
- Retrieving the full data

The Ray Dashboard is available at:
📍 http://127.0.0.1:8265

⚠️ All remote components (manager and spaces) will automatically terminate after 90 seconds. You can adjust this in the demo scripts.

### 🛑 Stop the Ray Cluster

After running the remote demo, you may want to stop all Ray processes to free system resources.


Run the following command in any terminal:

```
    ray stop
```

This cleanly stops the Ray runtime.

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
