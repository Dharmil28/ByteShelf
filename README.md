# ByteShelf — Gen Z Library & DAA Search Arena

A dark, neon-accented library management mini-project built with Python, Flask, SQLite, HTML, CSS, and Chart.js.

## Features
- 100+ technology, programming, electronics, design, and career titles are seeded automatically on first run.
- Search by title, author, topic/category, or shelf ID.
- Add new books and copies; there is no 100-book limit.
- Borrow and return workflow with borrower name, checkout time, active-loan list, and SQLite persistence.
- Availability updates automatically when a copy is borrowed or returned.
- DAA Arena compares Linear Search, Binary Search, and Hash Search with comparison counts and a chart.
- JSON endpoint at `/api/books`.

## Run on Windows
Open Command Prompt in the folder containing `app.py` and `requirements.txt`, then run:

```cmd
py -m venv .venv
.venv\Scripts\activate
python -m pip install -r requirements.txt
python app.py
```

Open http://127.0.0.1:5000 in your browser. Keep the terminal open while using the app.

## Database
`library.db` is created automatically next to `app.py`. Keep this file to preserve your local books and loan records. If updating an existing ByteShelf project, replace `app.py`, `templates/index.html`, and `static/style.css`, but keep your existing `library.db` file.

## DAA note
The arena uses exact-match comparisons for a fair comparison. Binary search requires sorted input; hash lookup is average O(1), excluding index construction. Timing values are illustrative and can vary on small datasets.
