from flask import render_template, Blueprint, url_for, request, flash, redirect
from models.loan import Loan
from models.book import Book
from models.user import User

bp = Blueprint('loans', __name__, url_prefix='/loans')

@bp.route('/')
def index():
    return render_template('loans/index.html', loans = Loan.all())

@bp.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        user_id = request.form['user']
        book_id = request.form['book']

        loan = Loan(book_id, user_id)
        loan.save()
        return redirect(url_for('loans.index'))
    
    return render_template('loans/register.html', users=User.all(), books=Book.all())
