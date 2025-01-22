## Ecommerce Backend API
Describe your Django project here. A brief description explaining what the project does, its purpose, and any other relevant information.

## Description 
**AI Chatbot Integration:** Provides personalized engine oil recommendations based on user car details using the OpenAI API.
- **Real-time Communication:** Utilizes WebSockets via Django Channels for live updates and interactions.
- **E-commerce Functionality:** Includes shopping cart, order management, and car mileage tracking for oil change predictions.
- **Admin Panel:** Django’s built-in admin panel for managing products, orders, and users.

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

# Install Daphne for WebSocket support
pip install daphne

# Run the ASGI server for WebSocket connections
daphne -b 127.0.0.1 -p 8001 ecommerce-back.asgi:application


# Migrate the database
python manage.py migrate

# Run the development server
python manage.py runserver
Now navigate to http://127.0.0.1:8000 in your browser to see the project home page.
