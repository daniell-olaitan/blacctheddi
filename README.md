# BLACCTHEDDI

This is a FastAPI backend application built to manage video content, event updates, and administrator accounts for a client-facing media application. It provides RESTful APIs for secure authentication, video uploads, event updates, and more.

---

## ✨ Features

- 🔐 **Admin Authentication**: Secure login system with hashed passwords.
- 📹 **Video Uploads**: Upload and serve videos.
- 📰 **Live Updates**: Post and retrieve updates.
- 🎟️ **Event Management**: Create and fetch event details via dedicated endpoints.
- ❤️ **Likes System**: Enable users to like content.
- 💬 **Comment System**: Enable users comment on updates and videos.

---

## 🚀 How to Host Locally

### 1. **Clone the Repository**
```bash
git clone https://github.com/daniell-olaitan/blacctheddi.git
cd blacctheddi
````

### 2. **Create a Virtual Environment**

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. **Install Dependencies**

```bash
pip install -r requirements.txt
```

### 4. **Configure Environment Variables**

Create a `.env` file in the root directory and copy the content of `.env.example`:

```bash
cp .env.example .env
```

> Update the `.env` file with your actual values.

### 5. **Run the Server**

```bash
fastapi dev main.py
```

Server will start at: [http://127.0.0.1:8000](http://127.0.0.1:8000)

---

## 📂 Folder Structure

```
app/
├── core/              # Utility functions
├── crud/              # Business logic for DB operations
├── routers/           # FastAPI routers (auth, video, event, etc.)
├── schemas/           # Pydantic models
├── storage/
│   ├── database.py    # DB connection and session
│   └── models.py      # SQLModel ORM models
├── config.py          # Configs
├── main.py            # FastAPI entry point
uploads/
├── videos/
├── images/
```

---

## 📫 Contact

**Daniel Olaitan** | Software Developer<br>
[daniell.olaitan@gmail.com](mailto:daniell.olaitan@gmail.com)<br>
[Github](https://github.com/daniell-olaitan)


