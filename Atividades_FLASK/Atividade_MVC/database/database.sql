CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    email TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS books (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    titulo TEXT NOT NULL,
    user_id INTEGER NOT NULL,
    FOREIGN KEY(user_id) REFERENCES users(id)
);

CREATE TABLE IF NOT EXISTS loans (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    data_emprestimo DATETIME NOT NULL DEFAULT (datetime('now', 'localtime')),
    data_devolucao DATETIME NOT NULL DEFAULT (datetime('now', 'localtime', '+14 days')),
    book_id INTEGER NOT NULL,
    user_id INTEGER NOT NULL,
    FOREIGN KEY(book_id) REFERENCES books(id),
    FOREIGN KEY(user_id) REFERENCES users(id)
);