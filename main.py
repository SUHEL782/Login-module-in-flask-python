import secrets
from main import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)
app.secret_key = 'your_secret_key'
# Change this to secret key

# In memory user database
users = {
    'user1': {
        'username': 'user1',
        'password': 'password1'
    },
    'user2': {
        'username': 'user2',
        'password': 'password2'
    },
}

# In memory password reset tokens
reset_tokens = {}


def is_valid_user(username, password):
  user = users.get(username)
  return user and user['password'] == password


def generate_reset_token(username):
  token = secrets.token_urlsafe(16)
  reset_tokens[username] = token
  return token


@app.route('/')
def home():
  return render_template('login.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
  if request.method == 'POST':
    username = request.form['username']
    password = request.form['password']

    if is_valid_user(username, password):
      flash('Login successful', 'success')
      return redirect(url_for('home'))
    else:
      flash('Invalid username or password', 'error')

  return render_template('login.html')


@app.route('/reset_password/<username>', methods=['GET', 'POST'])
def reset_password(username):
  if request.method == 'POST':

    # In a real application, you would send an email with a reset link containing the username and reset token
    # For simplicity, we'll generate a reset token and store it in memory
    reset_token = generate_reset_token(username)
    flash(
        f'Reset link sent to {username} email address. (Token: {reset_token})',
        'success')

  return render_template('reset_password.html', username=username)


if __name__ == '__main__':
  app.run(host='0.0.0.0', port=8080, debug=True)
