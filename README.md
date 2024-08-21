
# Django Blog Project

This is a Django-based blog project that includes models for posts, categories, comments, likes, dislikes, and user follow relationships.

## Prerequisites

Before you begin, ensure you have met the following requirements:

- **Python 3.7+**: Make sure Python is installed on your machine. You can download it from the official [Python website](https://www.python.org/downloads/).
- **Django**: The project is built using Django, so make sure you have Django installed or available in your virtual environment.

## Installation

### 1. Clone the Repository

First, clone this repository to your local machine using:

```bash
git clone https://github.com/wspjoy2011/itea_education_project.git
cd your-repo-directory
```

### 2. Set Up a Virtual Environment

It is recommended to use a virtual environment to manage dependencies. You can set up a virtual environment using the following commands:

```bash
# Install virtualenv if you don't have it
pip install virtualenv

# Create a virtual environment
python3 -m venv venv

# Activate the virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

### 3. Install Dependencies

Once the virtual environment is activated, install the required packages using:

```bash
pip install -r requirements.txt
```

### 4. Apply Migrations

Before running the project, you need to apply the migrations to set up your database schema:

```bash
python manage.py makemigrations
python manage.py migrate
```

### 5. Create a Superuser

To access the Django admin interface, you'll need to create a superuser:

```bash
python manage.py createsuperuser
```

Follow the prompts to set up your superuser credentials.

### 6. Run the Development Server

Now you can run the development server using:

```bash
python manage.py runserver
```

### 7. Access the Admin Interface

To manage the blog content and user interactions, navigate to the Django admin interface:

- Open your web browser and go to `http://127.0.0.1:8000/admin/`
- Log in with the superuser credentials you created earlier.

## Models Overview

### 1. Category
- **Fields**: `name`, `slug`
- **Description**: Categories for blog posts.

### 2. Post
- **Fields**: `title`, `slug`, `author`, `body`, `publish`, `created`, `updated`, `image_url`, `status`, `category`
- **Description**: Represents a blog post.

### 3. PostLike and PostDisLike
- **Fields**: `post`, `user`, `created`
- **Description**: Models to track likes and dislikes on posts.

### 4. Comment
- **Fields**: `post`, `author`, `created`, `updated`, `active`
- **Description**: Represents comments on posts.

### 5. CommentLike and CommentDislike
- **Fields**: `comment`, `user`, `created`
- **Description**: Models to track likes and dislikes on comments.

### 6. Follow
- **Fields**: `follower`, `followed`, `created`
- **Description**: Tracks follower relationships between users.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
