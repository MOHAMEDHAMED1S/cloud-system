from flask import Flask, render_template, redirect, url_for, request, flash, send_from_directory
from extensions import db, login_manager
from models import User, File
from flask_login import login_user, login_required, logout_user, current_user
import os
import shutil
from werkzeug.utils import secure_filename
from flask_migrate import Migrate

def create_app():
    app = Flask(__name__)
    app.secret_key = 'supersecretkey'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///file_sharing.db'
    app.config['UPLOAD_FOLDER'] = 'uploads'
    app.config['MAX_CONTENT_LENGTH'] = 1024 * 1024 * 100 * 1024  # Set max file size (100GB)

    db.init_app(app)  # Initialize SQLAlchemy with the app
    login_manager.init_app(app)
    login_manager.login_view = 'login'

    migrate = Migrate(app, db)

    with app.app_context():
        db.create_all()

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    @app.route('/')
    @login_required
    def index():
        search_query = request.args.get('search', '')
        files_query = File.query.filter(File.filename.ilike(f'%{search_query}%'), 
                                        (File.user_id == current_user.id) | (File.is_public == True))
        files = files_query.all()
        folders = [f for f in os.listdir(app.config['UPLOAD_FOLDER']) if os.path.isdir(os.path.join(app.config['UPLOAD_FOLDER'], f))]
        return render_template('index.html', files=files, folders=folders, search_query=search_query)

    @app.route('/upload', methods=['POST'])
    @login_required
    def upload_file():
        if 'files' not in request.files:
            flash('No files part')
            return redirect(request.url)
        
        files = request.files.getlist('files')
        
        if not files:
            flash('No selected files')
            return redirect(request.url)

        for file in files:
            if file.filename == '':
                flash('One or more files have no selected file')
                continue
            
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)

            base, extension = os.path.splitext(filename)
            counter = 1
            new_filename = filename
            while os.path.exists(os.path.join(app.config['UPLOAD_FOLDER'], new_filename)):
                new_filename = f"{base}_{counter}{extension}"
                counter += 1
            
            new_file_path = os.path.join(app.config['UPLOAD_FOLDER'], new_filename)
            file.save(new_file_path)

            is_public = request.form.get('is_public') == 'on'  # Check if public is selected
            new_file = File(filename=new_filename, user_id=current_user.id, is_public=is_public)
            db.session.add(new_file)
        
        db.session.commit()
        flash('Files successfully uploaded')
        return redirect(url_for('index'))

    @app.route('/files/<filename>')
    @login_required
    def download_file(filename):
        file = File.query.filter_by(filename=filename).first()
        if file and (file.is_public or file.user_id == current_user.id):
            return send_from_directory(app.config['UPLOAD_FOLDER'], filename)
        else:
            flash('File not found or you do not have permission to access it')
            return redirect(url_for('index'))

    @app.route('/delete/<filename>')
    @login_required
    def delete_file(filename):
        file_to_delete = File.query.filter_by(filename=filename, user_id=current_user.id).first()
        if file_to_delete:
            os.remove(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            db.session.delete(file_to_delete)
            db.session.commit()
            flash('File successfully deleted')
        else:
            flash('File not found or you do not have permission to delete it')
        return redirect(url_for('index'))

    @app.route('/create-folder', methods=['POST'])
    @login_required
    def create_folder():
        folder_name = request.form['folder_name']
        folder_path = os.path.join(app.config['UPLOAD_FOLDER'], folder_name)
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
            flash('Folder successfully created')
        else:
            flash('Folder already exists')
        return redirect(url_for('index'))

    @app.route('/move-file', methods=['POST'])
    @login_required
    def move_file():
        filename = request.form['filename']
        new_folder = request.form['new_folder']
        old_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        new_path = os.path.join(app.config['UPLOAD_FOLDER'], new_folder, filename)
        if os.path.exists(old_path):
            shutil.move(old_path, new_path)
            file = File.query.filter_by(filename=filename, user_id=current_user.id).first()
            if file:
                db.session.delete(file)
                db.session.commit()
                new_file = File(filename=filename, user_id=current_user.id)
                db.session.add(new_file)
                db.session.commit()
            flash('File successfully moved')
        else:
            flash('File not found')
        return redirect(url_for('index'))

    @app.route('/login', methods=['GET', 'POST'])
    def login():
        if request.method == 'POST':
            username = request.form['username']
            password = request.form['password']
            user = User.query.filter_by(username=username).first()
            if user and user.check_password(password):
                login_user(user)
                return redirect(url_for('index'))
            flash('Invalid username or password')
        return render_template('login.html')

    @app.route('/register', methods=['GET', 'POST'])
    def register():
        if request.method == 'POST':
            username = request.form['username']
            password = request.form['password']
            if User.query.filter_by(username=username).first():
                flash('Username already exists')
            else:
                user = User(username=username)
                user.set_password(password)
                db.session.add(user)
                db.session.commit()
                return redirect(url_for('login'))
        return render_template('register.html')

    @app.route('/logout')
    @login_required
    def logout():
        logout_user()
        return redirect(url_for('login'))

    @app.route('/make-public/<filename>', methods=['POST'])
    @login_required
    def make_public(filename):
        file = File.query.filter_by(filename=filename, user_id=current_user.id).first()
        if file:
            file.is_public = True
            db.session.commit()
            flash('File is now public')
        else:
            flash('File not found or you do not have permission to change it')
        return redirect(url_for('index'))

    @app.route('/make-private/<filename>', methods=['POST'])
    @login_required
    def make_private(filename):
        file = File.query.filter_by(filename=filename, user_id=current_user.id).first()
        if file:
            file.is_public = False
            db.session.commit()
            flash('File is now private')
        else:
            flash('File not found or you do not have permission to change it')
        return redirect(url_for('index'))

    return app
app = create_app()

@app.cli.command('create_db')
def create_db():
    """Create the database tables."""
    with app.app_context():
        db.create_all()

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=4000, debug=True)
