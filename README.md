# SujhavMitra – Flask Backend

This is the backend server for SujhavMitra built using Flask.  
It provides APIs for user signup, preference selection, recommendations, and search using local datasets.

---

## 🚀 How to Run (Windows)

### 1. Open Command Prompt and go to this folder

```bash
cd path\to\SujhavMitra\backend
```

---

### 2. Create a virtual environment

```bash
python -m venv venv
```

---

### 3. Activate the virtual environment (Windows)

```bash
venv\Scripts\activate
```

---

### 4. Install the required dependencies

```bash
pip install -r requirements.txt
```

---

### 5. Run the Flask app

```bash
python app.py

or

flask run
```

The server will start at:  
📡 `http://127.0.0.1:5000/`

---

### 🧼 To stop the server

Press `Ctrl + C` in the terminal.

---

### 🔚 To deactivate the virtual environment

```bash
deactivate
```

---

> ⚠️ Make sure `books.csv` and `movies.csv` are inside the `data/` folder before running.
