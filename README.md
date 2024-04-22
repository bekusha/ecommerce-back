## Ecommerce Backend API
Describe your Django project here. A brief description explaining what the project does, its purpose, and any other relevant information.

## Description 
The Bekas Store Backend API powers the dynamic e-commerce platform that allows users to operate as consumers or vendors. This API handles all data transactions for user registration, product management, shopping cart operations, and payment processing. It employs JWT authentication to secure all endpoints and provide a safe environment for transactions.

## Getting Started
These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

Prerequisites
What things you need to install the software and how to install them:

bash
Copy code
pip install django
pip install djangorestframework
# Any other dependencies
Installing
A step-by-step series of examples that tell you how to get a development environment running:

bash
Copy code
# Clone the repository
git clone https://github.com/bekusha/ecommerce-back.git
cd ecommerce-back

# Set up a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows use `env\Scripts\activate`

# Install required packages
pip install -r requirements.txt

# Migrate the database
python manage.py migrate

# Run the development server
python manage.py runserver
Now navigate to http://127.0.0.1:8000 in your browser to see the project home page.