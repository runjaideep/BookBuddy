# BookBuddy

## **Overview**
Book Buddy is a personal application I designed to organize and analyze my reading journey. The project provides a user-friendly platform to track books, manage genres, analyze reading trends, and seek recommendations.

---

## **Features**
- **Book Management**: Add, update, delete, and retrieve books.
- **Author & Genre Management**: Organize books by authors and genres.
- **API Integration**: RESTful APIs for backend operations.
- **Recommendation using Googlebooks API
- **Interactive UI**: User-friendly interface for smooth navigation.

---

## **Tech Stack**
- **Backend**: Python, FastAPI
- **Frontend**: Streamlit
- **Database**: MySQL
- **Tools & Libraries**:
  - FastAPI: API framework
  - Streamlit: Frontend framework
  - Pandas & Matplotlib: Data analytics and visualization

---

## **Project Structure**
```
BookBuddy/
|-- backend/
|   |-- server.py           # FastAPI app entry point
|   |-- db_helper.py      # Helper functions for database operations
|   |-- server.log           # Server log to capture events as set in the logger
|   |-- logger.py           # Logger definitions
|-- frontend/
|   |-- app.py                # Streamlit frontend application
|   |-- components/           # UI components
|-- tests/
|   |-- test_apis.py          # API unit tests
|   |-- test_ui.py            # Frontend tests
|-- requirements.txt          # Python dependencies
|-- README.md                 # Project documentation
```

---

## **Setup Instructions**
### **1. Prerequisites**
Ensure the following tools are installed:
- Python 3.9+
- MySQL Server
- pip (Python package manager)

### **2. Clone the Repository**
```bash
git clone <repository_url>
cd BookBuddy
```

### **3. Set Up the Database**
- Import the database schema:
  ```bash
  mysql -u <username> -p < database/schema.sql
  ```
- Configure database credentials in `backend/database/db_helper.py`.

### **4. Install Dependencies**
```bash
pip install -r requirements.txt
```

### **5. Run the Backend**
```bash
cd backend/app
uvicorn main:app --reload
```
Access the FastAPI docs at: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

### **6. Run the Frontend**
```bash
cd frontend
streamlit run app.py
```

---

## **Key Functionalities**
- **Insert Book**: Add a new book with title, author, and genre.
- **View Library**: Retrieve a list of books, filterable by genre or author.
- **Analytics Dashboard**: Get insights into the most-read genres or authors.
- **Search Recommendations**: Locate books similar to your taste based on book title or author.

---

## **License**
This project is licensed under the MIT License. See `LICENSE` for details.

---

## **Contact**
For questions or support, reach out to:
- **Email**: <jaideep.sharma@outlook.com>

