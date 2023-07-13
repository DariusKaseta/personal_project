# CSS App

This is a Django-based web application that allows users to send emails to multiple recipients using a user-friendly interface. The app provides a simple and convenient way to compose and send emails with custom subjects and contents to a selected list of recipients.

# Features

User authentication: Users can log in, and log out to access the email sending functionality.
Compose email: Users can compose emails by entering a subject, content, and selecting recipients from a list.
Multiple recipients: Users can select multiple recipients from the provided list or search for specific recipients using the search functionality.
Error handling: The app provides appropriate error handling for scenarios such as no recipient selection or errors encountered during email sending.
Success message: Users receive a success message upon successful email sending.
Responsive design: The app is designed to be responsive and compatible with different screen sizes.

# Installation

1. Clone the repository: git clone https://github.com/DariusKaseta/personal_project

2. Create and activate a virtual environment (optional but recommended): python3 -m venv venv
source venv/bin/activate

3. Install the dependencies: pip install -r requirements.txt

4. Set up the environment variables depending on your host: (e.a.

EMAIL_BACKEND =

EMAIL_HOST = 

EMAIL_PORT = 

EMAIL_USE_TLS = 

EMAIL_USE_SSL = 

EMAIL_HOST_USER = 

EMAIL_HOST_PASSWORD = )

6. Apply database migrations: python manage.py migrate

7. Start the development server: python manage.py runserver

8. Open your web browser and visit http://localhost:8000

# Dependencies

The app has the following dependencies:

Django: web framework for building the application
Django REST Framework: for creating the API endpoints (if applicable)
Bootstrap: front-end framework for responsive design
Other dependencies listed in the requirements.txt file

# Contribution

Contributions to the CSS App are welcome! If you find any bugs or have suggestions for improvements, please open an issue or submit a pull request.

# License

The CSS App is open-source and available under the MIT License.

Feel free to customize the README.md according to your specific app requirements and add any additional sections or information you deem necessary.
