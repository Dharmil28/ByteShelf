from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
import sqlite3
import time
from pathlib import Path
from datetime import datetime

app = Flask(__name__)
app.secret_key = "byteshelf-local-demo-change-me"
BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "library.db"

# A starter catalogue plus a larger technology collection (100+ titles total).
SAMPLE_BOOKS = [
    ("Grokking Algorithms", "Aditya Bhargava", "Algorithms", 4),
    ("Introduction to Algorithms", "Thomas H. Cormen et al.", "Algorithms", 3),
    ("The Pragmatic Programmer", "David Thomas and Andrew Hunt", "Software Engineering", 5),
    ("Clean Code", "Robert C. Martin", "Software Engineering", 2),
    ("Designing Data-Intensive Applications", "Martin Kleppmann", "System Design", 4),
    ("Python Crash Course", "Eric Matthes", "Python", 6),
    ("Automate the Boring Stuff with Python", "Al Sweigart", "Python", 3),
    ("Cracking the Coding Interview", "Gayle Laakmann McDowell", "Interview Prep", 2),
    ("Computer Networking: A Top-Down Approach", "James Kurose and Keith Ross", "Networking", 4),
    ("Operating Systems: Three Easy Pieces", "Remzi H. Arpaci-Dusseau and Andrea C. Arpaci-Dusseau", "Operating Systems", 2),
    ("Database System Concepts", "Abraham Silberschatz et al.", "Database", 3),
    ("Artificial Intelligence: A Modern Approach", "Stuart Russell and Peter Norvig", "AI & Machine Learning", 2),
    ("The Art of Electronics", "Paul Horowitz and Winfield Hill", "Electronics", 4),
    ("Making Embedded Systems", "Elecia White", "Embedded Systems", 3),
    ("Think Like a Programmer", "V. Anton Spraul", "Programming", 5),
]

EXTRA_BOOKS = [
("Algorithms Unlocked", "Thomas H. Cormen", "Algorithms"),
("The Algorithm Design Manual", "Steven S. Skiena", "Algorithms"),
("Algorithms", "Robert Sedgewick and Kevin Wayne", "Algorithms"),
("A Common-Sense Guide to Data Structures and Algorithms", "Jay Wengrow", "Algorithms"),
("Data Structures and Algorithms in Python", "Michael T. Goodrich et al.", "Algorithms"),
("Data Structures and Algorithm Analysis in C++", "Mark Allen Weiss", "Algorithms"),
("Data Structures and Algorithms in Java", "Robert Lafore", "Algorithms"),
("The Little Book of Semaphores", "Allen B. Downey", "Operating Systems"),
("Computer Systems: A Programmer's Perspective", "Randal E. Bryant and David R. O'Hallaron", "Computer Systems"),
("Code: The Hidden Language of Computer Hardware and Software", "Charles Petzold", "Computer Systems"),
("The Elements of Computing Systems", "Noam Nisan and Shimon Schocken", "Computer Systems"),
("But How Do It Know?", "J. Clark Scott", "Computer Systems"),
("Structure and Interpretation of Computer Programs", "Harold Abelson and Gerald Jay Sussman", "Programming"),
("The C Programming Language", "Brian W. Kernighan and Dennis M. Ritchie", "Programming"),
("Effective C", "Robert C. Seacord", "Programming"),
("C Programming: A Modern Approach", "K. N. King", "Programming"),
("Head First Java", "Kathy Sierra and Bert Bates", "Programming"),
("Effective Java", "Joshua Bloch", "Programming"),
("Head First Design Patterns", "Eric Freeman et al.", "Software Engineering"),
("Refactoring", "Martin Fowler", "Software Engineering"),
("Working Effectively with Legacy Code", "Michael Feathers", "Software Engineering"),
("Code Complete", "Steve McConnell", "Software Engineering"),
("Peopleware", "Tom DeMarco and Timothy Lister", "Software Engineering"),
("The Mythical Man-Month", "Frederick P. Brooks Jr.", "Software Engineering"),
("Domain-Driven Design", "Eric Evans", "Software Engineering"),
("Patterns of Enterprise Application Architecture", "Martin Fowler", "Software Engineering"),
("Continuous Delivery", "Jez Humble and David Farley", "DevOps"),
("The Phoenix Project", "Gene Kim et al.", "DevOps"),
("Site Reliability Engineering", "Betsy Beyer et al.", "DevOps"),
("The DevOps Handbook", "Gene Kim et al.", "DevOps"),
("Learning SQL", "Alan Beaulieu", "Database"),
("SQL Cookbook", "Anthony Molinaro and Robert de Graaf", "Database"),
("Database Internals", "Alex Petrov", "Database"),
("Seven Databases in Seven Weeks", "Eric Redmond and Jim R. Wilson", "Database"),
("SQL Performance Explained", "Markus Winand", "Database"),
("Fundamentals of Database Systems", "Ramez Elmasri and Shamkant B. Navathe", "Database"),
("Learning Python", "Mark Lutz", "Python"),
("Fluent Python", "Luciano Ramalho", "Python"),
("Effective Python", "Brett Slatkin", "Python"),
("Python for Data Analysis", "Wes McKinney", "Data Science"),
("Hands-On Machine Learning with Scikit-Learn, Keras, and TensorFlow", "Aurélien Géron", "AI & Machine Learning"),
("Deep Learning", "Ian Goodfellow et al.", "AI & Machine Learning"),
("The Hundred-Page Machine Learning Book", "Andriy Burkov", "AI & Machine Learning"),
("Pattern Recognition and Machine Learning", "Christopher M. Bishop", "AI & Machine Learning"),
("Machine Learning Yearning", "Andrew Ng", "AI & Machine Learning"),
("Artificial Intelligence: A Guide to Intelligent Systems", "Michael Negnevitsky", "AI & Machine Learning"),
("Hands-On Computer Vision with TensorFlow 2", "Benjamin Planche and Eliot Andres", "AI & Machine Learning"),
("Practical Statistics for Data Scientists", "Peter Bruce et al.", "Data Science"),
("R for Data Science", "Hadley Wickham and Garrett Grolemund", "Data Science"),
("Storytelling with Data", "Cole Nussbaumer Knaflic", "Data Science"),
("Data Science from Scratch", "Joel Grus", "Data Science"),
("The Data Warehouse Toolkit", "Ralph Kimball and Margy Ross", "Data Science"),
("Computer Networking: A Top-Down Approach", "James Kurose and Keith Ross", "Networking"),
("TCP/IP Illustrated, Volume 1", "W. Richard Stevens", "Networking"),
("Computer Networks", "Andrew S. Tanenbaum and David J. Wetherall", "Networking"),
("Network Warrior", "Gary A. Donahue", "Networking"),
("Practical Packet Analysis", "Chris Sanders", "Networking"),
("Operating System Concepts", "Abraham Silberschatz et al.", "Operating Systems"),
("Modern Operating Systems", "Andrew S. Tanenbaum and Herbert Bos", "Operating Systems"),
("Linux Kernel Development", "Robert Love", "Operating Systems"),
("Linux Basics for Hackers", "OccupyTheWeb", "Cybersecurity"),
("Computer Security: Principles and Practice", "William Stallings and Lawrie Brown", "Cybersecurity"),
("The Web Application Hacker's Handbook", "Dafydd Stuttard and Marcus Pinto", "Cybersecurity"),
("Threat Modeling", "Adam Shostack", "Cybersecurity"),
("Security Engineering", "Ross Anderson", "Cybersecurity"),
("The Art of Invisibility", "Kevin Mitnick", "Cybersecurity"),
("Cryptography and Network Security", "William Stallings", "Cybersecurity"),
("The Web Developer Bootcamp", "Colt Steele", "Web Development"),
("Eloquent JavaScript", "Marijn Haverbeke", "Web Development"),
("You Don't Know JS Yet", "Kyle Simpson", "Web Development"),
("JavaScript: The Good Parts", "Douglas Crockford", "Web Development"),
("Learning React", "Alex Banks and Eve Porcello", "Web Development"),
("Fullstack Vue", "Hassan Djirdeh et al.", "Web Development"),
("CSS Secrets", "Lea Verou", "Web Development"),
("HTML and CSS: Design and Build Websites", "Jon Duckett", "Web Development"),
("Don't Make Me Think", "Steve Krug", "UI/UX Design"),
("The Design of Everyday Things", "Don Norman", "UI/UX Design"),
("Refactoring UI", "Adam Wathan and Steve Schoger", "UI/UX Design"),
("About Face", "Alan Cooper et al.", "UI/UX Design"),
("Designing Interfaces", "Jenifer Tidwell et al.", "UI/UX Design"),
("The Lean Startup", "Eric Ries", "Product & Startups"),
("Zero to One", "Peter Thiel and Blake Masters", "Product & Startups"),
("Inspired", "Marty Cagan", "Product & Startups"),
("Sprint", "Jake Knapp et al.", "Product & Startups"),
("Hooked", "Nir Eyal", "Product & Startups"),
("The Startup Owner's Manual", "Steve Blank and Bob Dorf", "Product & Startups"),
("The Innovator's Dilemma", "Clayton M. Christensen", "Product & Startups"),
("The Art of Electronics", "Paul Horowitz and Winfield Hill", "Electronics"),
("Practical Electronics for Inventors", "Paul Scherz and Simon Monk", "Electronics"),
("Make: Electronics", "Charles Platt", "Electronics"),
("The Circuit Designer's Companion", "Peter Wilson", "Electronics"),
("Microelectronic Circuits", "Adel S. Sedra and Kenneth C. Smith", "Electronics"),
("Electronic Devices and Circuit Theory", "Robert L. Boylestad and Louis Nashelsky", "Electronics"),
("Digital Design", "M. Morris Mano and Michael D. Ciletti", "Digital Systems"),
("Digital Design and Computer Architecture", "David Money Harris and Sarah L. Harris", "Digital Systems"),
("Computer Organization and Design", "David A. Patterson and John L. Hennessy", "Computer Systems"),
("The Definitive Guide to ARM Cortex-M3 and Cortex-M4 Processors", "Joseph Yiu", "Embedded Systems"),
("Making Embedded Systems", "Elecia White", "Embedded Systems"),
("Embedded Systems: Introduction to Arm Cortex-M Microcontrollers", "Jonathan W. Valvano", "Embedded Systems"),
("Programming Embedded Systems", "Michael Barr and Anthony Massa", "Embedded Systems"),
("Embedded C Coding Standard", "Michael Barr", "Embedded Systems"),
("Designing Embedded Hardware", "John Catsoulis", "Embedded Systems"),
("Mastering STM32", "Carmine Noviello", "Embedded Systems"),
("The Art of Software Testing", "Glenford J. Myers et al.", "Software Testing"),
("Agile Testing", "Lisa Crispin and Janet Gregory", "Software Testing"),
("Test-Driven Development: By Example", "Kent Beck", "Software Testing"),
("The Unicorn Project", "Gene Kim", "DevOps"),
("Accelerate", "Nicole Forsgren et al.", "DevOps"),
("Kubernetes Up and Running", "Kelsey Hightower et al.", "Cloud Computing"),
("Cloud Native Patterns", "Cornelia Davis", "Cloud Computing"),
("Designing Distributed Systems", "Brendan Burns", "System Design"),
("Building Microservices", "Sam Newman", "System Design"),
("Fundamentals of Software Architecture", "Mark Richards and Neal Ford", "System Design"),
("System Design Interview", "Alex Xu", "System Design"),
("System Design Interview – An Insider's Guide", "Alex Xu", "System Design"),
("The Staff Engineer's Path", "Tanya Reilly", "Career & Interview Prep"),
("The Manager's Path", "Camille Fournier", "Career & Interview Prep"),
("Decode and Conquer", "Lewis C. Lin", "Career & Interview Prep"),
("Elements of Programming Interviews in Python", "Adnan Aziz et al.", "Interview Prep"),
("Programming Interviews Exposed", "John Mongan et al.", "Interview Prep"),
("The Complete Software Developer's Career Guide", "John Sonmez", "Career & Interview Prep"),
]


def connect_db():
    con = sqlite3.connect(DB_PATH)
    con.row_factory = sqlite3.Row
    con.execute("PRAGMA foreign_keys = ON")
    return con


def init_db():
    with connect_db() as con:
        con.execute("""CREATE TABLE IF NOT EXISTS books (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            author TEXT NOT NULL,
            category TEXT NOT NULL,
            copies INTEGER NOT NULL DEFAULT 1 CHECK(copies >= 0)
        )""")
        con.execute("CREATE TABLE IF NOT EXISTS app_meta (key TEXT PRIMARY KEY, value TEXT NOT NULL)")
        con.execute("""CREATE TABLE IF NOT EXISTS loans (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            book_id INTEGER NOT NULL,
            borrower_name TEXT NOT NULL,
            borrowed_at TEXT NOT NULL,
            returned_at TEXT,
            FOREIGN KEY(book_id) REFERENCES books(id) ON DELETE CASCADE
        )""")
        # Seed initial titles into an empty database.
        count = con.execute("SELECT COUNT(*) FROM books").fetchone()[0]
        if count == 0:
            con.executemany("INSERT INTO books (title, author, category, copies) VALUES (?, ?, ?, ?)", SAMPLE_BOOKS)
        # Add the 100+ title catalogue once, while keeping user-added records intact.
        seeded = con.execute("SELECT value FROM app_meta WHERE key='byteshelf_catalog_v2'").fetchone()
        if not seeded:
            for i, (title, author, category) in enumerate(EXTRA_BOOKS):
                exists = con.execute("SELECT 1 FROM books WHERE title=? AND author=?", (title, author)).fetchone()
                if not exists:
                    con.execute("INSERT INTO books (title, author, category, copies) VALUES (?, ?, ?, ?)",
                                (title, author, category, 1 + (i % 5)))
            con.execute("INSERT OR REPLACE INTO app_meta(key,value) VALUES('byteshelf_catalog_v2','done')")

# DAA search demonstrations. Comparisons are displayed alongside timing because tiny timings vary by machine.
def linear_search(records, key, field):
    comparisons = 0
    target = key.casefold()
    for book in records:
        comparisons += 1
        if target == str(book[field]).casefold():
            return book, comparisons
    return None, comparisons


def binary_search(records, key, field):
    ordered = sorted(records, key=lambda b: str(b[field]).casefold())
    target = key.casefold()
    low, high, comparisons = 0, len(ordered) - 1, 0
    while low <= high:
        mid = (low + high) // 2
        value = str(ordered[mid][field]).casefold()
        comparisons += 1
        if value == target:
            return ordered[mid], comparisons
        if value < target:
            low = mid + 1
        else:
            high = mid - 1
    return None, comparisons


def hash_search(records, key, field):
    index = {str(book[field]).casefold(): book for book in records}
    return index.get(key.casefold()), 1


def benchmark(records, key, field):
    results = []
    for label, algorithm in [("Linear Search", linear_search), ("Binary Search", binary_search), ("Hash Search", hash_search)]:
        start = time.perf_counter_ns()
        found, comparisons = algorithm(records, key, field)
        elapsed_ms = (time.perf_counter_ns() - start) / 1_000_000
        results.append({"name": label, "found": found is not None,
                        "comparisons": comparisons, "time_ms": round(elapsed_ms, 6)})
    return results


def get_books_with_availability(con):
    rows = con.execute("""SELECT b.*,
        (SELECT COUNT(*) FROM loans l WHERE l.book_id=b.id AND l.returned_at IS NULL) AS borrowed_count
        FROM books b ORDER BY b.title COLLATE NOCASE""").fetchall()
    books = []
    for row in rows:
        book = dict(row)
        book['available_copies'] = max(0, book['copies'] - book['borrowed_count'])
        books.append(book)
    return books


@app.route("/")
def index():
    query = request.args.get("q", "").strip()
    field = request.args.get("field", "title")
    if field not in {"title", "author", "category", "id"}:
        field = "title"
    with connect_db() as con:
        all_books = get_books_with_availability(con)
        categories = [r[0] for r in con.execute("SELECT DISTINCT category FROM books ORDER BY category COLLATE NOCASE").fetchall()]
        active_loans = con.execute("""SELECT l.id, l.book_id, l.borrower_name, l.borrowed_at, b.title, b.author
            FROM loans l JOIN books b ON b.id=l.book_id WHERE l.returned_at IS NULL ORDER BY l.borrowed_at DESC""").fetchall()
        total = len(all_books)
        available = sum(1 for b in all_books if b['available_copies'] > 0)
        active_loan_count = len(active_loans)
    if query:
        if field == "id":
            books = [b for b in all_books if str(b["id"]) == query]
        else:
            books = [b for b in all_books if query.casefold() in str(b[field]).casefold()]
        stats = benchmark(all_books, query, field)
    else:
        books = all_books
        stats = None
    return render_template("index.html", books=books, query=query, field=field, categories=categories,
                           total=total, available=available, stats=stats, result_count=len(books),
                           active_loans=active_loans, active_loan_count=active_loan_count)


@app.route("/add", methods=["POST"])
def add_book():
    title = request.form.get("title", "").strip()
    author = request.form.get("author", "").strip()
    category = request.form.get("category", "").strip()
    try:
        copies = int(request.form.get("copies", "1"))
        if copies < 0:
            raise ValueError
    except ValueError:
        flash("Copies must be a whole number greater than or equal to zero.", "error")
        return redirect(url_for("index") + "#manage")
    if not title or not author or not category:
        flash("Please complete all book fields.", "error")
        return redirect(url_for("index") + "#manage")
    with connect_db() as con:
        con.execute("INSERT INTO books (title, author, category, copies) VALUES (?, ?, ?, ?)", (title, author, category, copies))
    flash(f'“{title}” added to ByteShelf.', "success")
    return redirect(url_for("index") + "#manage")


@app.route("/borrow", methods=["POST"])
def borrow_book():
    borrower = request.form.get("borrower_name", "").strip()
    try:
        book_id = int(request.form.get("book_id", "0"))
    except ValueError:
        book_id = 0
    if not borrower:
        flash("Enter the borrower's name before checking out a book.", "error")
        return redirect(url_for("index") + "#collection")
    with connect_db() as con:
        book = con.execute("SELECT * FROM books WHERE id=?", (book_id,)).fetchone()
        if not book:
            flash("That book could not be found.", "error")
        else:
            active = con.execute("SELECT COUNT(*) FROM loans WHERE book_id=? AND returned_at IS NULL", (book_id,)).fetchone()[0]
            if active >= book['copies']:
                flash("Sorry, all copies of this title are currently borrowed.", "error")
            else:
                con.execute("INSERT INTO loans (book_id, borrower_name, borrowed_at) VALUES (?, ?, ?)",
                            (book_id, borrower, datetime.now().strftime("%Y-%m-%d %H:%M")))
                flash(f'Enjoy “{book["title"]}”, {borrower}! Borrow recorded.', "success")
    return redirect(url_for("index") + "#loans")


@app.route("/return/<int:loan_id>", methods=["POST"])
def return_book(loan_id):
    with connect_db() as con:
        loan = con.execute("SELECT * FROM loans WHERE id=? AND returned_at IS NULL", (loan_id,)).fetchone()
        if not loan:
            flash("This loan was already returned or could not be found.", "error")
        else:
            con.execute("UPDATE loans SET returned_at=? WHERE id=?", (datetime.now().strftime("%Y-%m-%d %H:%M"), loan_id))
            flash("Book returned. One more title is back on the shelf!", "success")
    return redirect(url_for("index") + "#loans")


@app.route("/delete/<int:book_id>", methods=["POST"])
def delete_book(book_id):
    with connect_db() as con:
        active = con.execute("SELECT COUNT(*) FROM loans WHERE book_id=? AND returned_at IS NULL", (book_id,)).fetchone()[0]
        if active:
            flash("Return the active loan before removing this book.", "error")
        else:
            con.execute("DELETE FROM books WHERE id=?", (book_id,))
            flash("Book removed from the shelf.", "success")
    return redirect(url_for("index") + "#collection")


@app.route("/api/books")
def api_books():
    with connect_db() as con:
        return jsonify(get_books_with_availability(con))


@app.route("/seed", methods=["POST"])
def seed_books():
    added = 0
    with connect_db() as con:
        for i, (title, author, category) in enumerate(EXTRA_BOOKS):
            exists = con.execute("SELECT 1 FROM books WHERE title=? AND author=?", (title, author)).fetchone()
            if not exists:
                con.execute("INSERT INTO books (title, author, category, copies) VALUES (?, ?, ?, ?)",
                            (title, author, category, 1 + (i % 5)))
                added += 1
    flash(f"Catalog boost complete: added {added} new titles. ByteShelf has room for unlimited books.", "success")
    return redirect(url_for("index") + "#collection")


init_db()

if __name__ == "__main__":
    app.run(debug=True)
