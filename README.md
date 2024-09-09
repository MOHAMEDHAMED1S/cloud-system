

# Cloud System Project

Welcome to the File Sharing Project using Flask! This project allows you to upload and share files securely with others.

## Table of Contents

- [Description](#description)
- [Features](#features)
- [Installation](#installation)
- [Running the Project](#running-the-project)
- [Configuration](#configuration)
- [Files and Folders](#files-and-folders)
- [Version Control](#version-control)
- [Contributing](#contributing)
- [License](#license)

## Description

This project provides an application built using Flask, enabling users to manage files through a web interface. Features include file uploads, organization into folders, sharing files with others, and setting access permissions to be either public or private.

## Features

- **Login and Registration:** Allows users to create accounts and log in to access their files.
- **File Uploads:** Upload multiple files simultaneously.
- **File Management:** Ability to delete files, move them between folders, and create new folders.
- **File Sharing:** Set files as public for others to access, or keep them private.
- **User-Friendly Interface:** Simple interface for managing files and folders.

## Installation

To install and run the project locally, follow these steps:

1. **Clone the Repository:**

    ```bash
    git clone https://github.com/MOHAMEDHAMED1S/cloud-system.git
    ```

2. **Navigate to the Project Directory:**

    ```bash
    cd cloud-system
    ```

3. **Create and Activate a Virtual Environment:**

    On **Unix-like Systems** (Linux/macOS):
    ```bash
    python -m venv venv
    source venv/bin/activate
    ```

    On **Windows**:
    ```bash
    python -m venv venv
    venv\Scripts\activate
    ```

4. **Install Dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

5. **Create the Database:**

    Run the Flask command to create the database:
    ```bash
    flask create_db
    ```

## Running the Project

To start the application, use the following command:

```bash
python app.py
```

Open your web browser and go to [http://localhost:4000](http://localhost:4000) to view the application.

## Configuration

You can modify project settings through the `app.py` file. Important settings include:

- **Secret Keys:** `app.secret_key` - Use a secret key to ensure session security.
- **Database Path:** `app.config['SQLALCHEMY_DATABASE_URI']` - Specify the path to your database here.
- **Upload Folder Path:** `app.config['UPLOAD_FOLDER']` - Specify the folder where files will be stored.

Ensure these settings are configured to fit your working environment.

## Files and Folders

Here’s a breakdown of the project’s file and folder structure:

- **`app.py`**: Contains Flask application definitions and all routes and main functions.
- **`extensions.py`**: Contains initialization for extensions such as SQLAlchemy and Flask-Login.
- **`manage.py`**: Tool for managing migrations and updating the database.
- **`migrations/`**: Contains migration files for Flask-Migrate. Includes `alembic.ini`, `env.py`, and migration files in the `versions` folder.
- **`models.py`**: Contains database model definitions representing database tables.
- **`requirements.txt`**: Lists the packages required to run the project.
- **`static/`**: Contains static CSS and JavaScript files. Includes `styles.css` in the example.
- **`templates/`**: Contains HTML template files. Includes `index.html`, `login.html`, and `register.html`.
- **`uploads/`**: Contains files uploaded by users.
- **`venv/`**: Contains the project’s virtual environment. Do not add this folder to the repository, and it’s typically added to `.gitignore`.

## Version Control

This project uses Git for version control. To review the change history, you can use:

```bash
git log
```

## Contributing

We welcome your contributions! If you’d like to add new features or fix bugs, please follow these steps:

1. **Create a New Branch:**

    ```bash
    git checkout -b feature-branch
    ```

2. **Make Your Changes.**

3. **Commit Your Changes to GitHub:**

    ```bash
    git add .
    git commit -m "Description of the changes"
    git push origin feature-branch
    ```

4. **Open a Pull Request on GitHub.**

The pull request will be reviewed and merged by maintainers.

## License

This project is licensed under the [MIT License](LICENSE). You can find the license details in the `LICENSE` file included with the project.

---

If you have any questions or need assistance, feel free to open an issue in the GitHub repository.

---
