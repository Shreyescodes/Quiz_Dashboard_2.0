# Quiz Dashboard

A dynamic quiz dashboard application built using Python and Django. This application allows administrators to manage quizzes and users to request access, attempt quizzes, and view their scores.

## Features

- **User Authentication**: Login and signup functionality for users.
- **Quiz Access Management**: Users can request access to quizzes, and admins can approve or deny these requests.
- **CSV Upload**: Admins can upload quiz questions via CSV files.
- **Quiz Navigation**: Users can navigate between questions with a highlighted current question.
- **Score Calculation**: Automatic calculation of scores based on correct answers.
- **Incorrect Questions Review**: Display of incorrectly answered questions with correct answers.
- **Responsive UI**: User-friendly interface with a scrollable question navigation bar.
- **Dynamic Quiz Types**: Support for various quiz categories (e.g., Python, Java, JavaScript).

## Tech Stack

- **Backend**: Django
- **Frontend**: HTML, CSS
- **Data Handling**: CSV Parsing
- **Database**: SQLite (default Django database)

## Installation

### Prerequisites

- Python 3.x
- Django 5.x

### Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/Shreyescodes/quiz-dashboard.git
   cd quiz-dashboard
   ```

2. Create and activate a virtual environment:
   
   Windows:
   ```bash
   python -m venv env
   .\env\Scripts\activate
   ```
   
   MacOS/Linux:
   ```bash
   python3 -m venv env
   source env/bin/activate
   ```

3. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Apply migrations:
   ```bash
   python manage.py migrate
   ```

5. Run the development server:
   ```bash
   python manage.py runserver
   ```

6. Open your browser and navigate to `http://127.0.0.1:8000`.

## Usage

1. **Sign Up/Login**: Create an account or log in to an existing one.
2. **Request Quiz Access**: Browse available quizzes and request access.
3. **Admin Approval**: Administrators can approve or deny access requests.
4. **Upload Quiz (Admin)**: Admins can upload new quizzes via CSV files.
5. **Attempt Quiz**: Once approved, navigate through the questions to complete the quiz.
6. **View Results**: After completion, view your score and review incorrect answers.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
