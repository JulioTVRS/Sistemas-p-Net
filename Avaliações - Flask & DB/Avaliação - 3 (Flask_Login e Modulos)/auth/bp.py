from flask import Blueprint, render_template, redirect, url_for, request
from flask_login import login_user, logout_user, LoginManager
from users.models import User


bp = Blueprint(
    name='auth', 
    import_name=__name__,
    url_prefix='/auth',
    template_folder='templates'
    )

login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.init_app(bp)

@login_manager.user_loader
def load_user(user_id):
    return User.find(id=user_id)


@bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        
        user = User.find(email=email)
        login_user(user)

        return redirect(url_for('users.index'))
    
    return render_template('auth/login.html')


@bp.route('/logout', methods=['POST'])
def logout():
    logout_user()
    return redirect(url_for('index'))
