from database import get_connection

class Loan:
    def __init__(self, book_id, user_id):
        self.book_id = book_id
        self.user_id = user_id

    def save(self):
        conn = get_connection()
        conn.execute("INSERT INTO loans(book_id, user_id) values(?,?)", (self.book_id, self.user_id))
        conn.commit()
        conn.close()
        return True

    @classmethod
    def all(cls):
        conn = get_connection()
        loan = conn.execute('''
            SELECT loans.*, users.nome AS user_name, books.titulo AS book_title 
            FROM loans
            JOIN users ON loans.user_id = users.id
            JOIN books ON loans.book_id = books.id
        ''').fetchall()
        return loan