ServiceLink API
Project Description

This project is a real-time service platform API built with FastAPI and JWT for authentication. It is designed to connect clients with workers for various on-demand services. The system features secure user management, real-time notifications via WebSockets, and a structured order and payment processing workflow.
Key Features

    Role-Based Access: The API supports three distinct user roles: client, worker, and admin, each with specific permissions.

    Secure Authentication: Users are authenticated using JSON Web Tokens (JWTs), ensuring that protected endpoints are accessible only to authorized users.

    Real-Time Notifications: Integrated WebSockets provide instant updates to users. Clients are notified about their order status, and workers receive notifications for new orders in their specialty.

    Order Management: A dedicated order management system handles the creation, processing, and tracking of service requests. A 10% service fee is automatically applied to all orders.

    Fake Payment Gateway: A mock payment API endpoint simulates the processing of card payments.

    Detailed Order History: Users can view their personalized order history based on their role:

        Clients see only their own orders.

        Workers see orders matching their assigned specialty.

        Admins have access to all orders and users in the system.

How to Run the Project

Follow these steps to set up and run the API locally.
1. Clone the Repository

git clone https://github.com/Diyorbek-MY/ServiceLink-API.git
cd ServiceLink-API

2. Create a Virtual Environment and Install Dependencies

It is highly recommended to use a virtual environment to manage project dependencies.

# Create a virtual environment
python -m venv venv

# Activate the virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install the required packages
pip install -r requirements.txt

Note: If you don't have a requirements.txt file, you can create one by running: pip freeze > requirements.txt after installing all your project's dependencies (e.g., fastapi, uvicorn, passlib, python-jose, etc.).
3. Run the Server

Start the API server using Uvicorn. The --reload flag will automatically restart the server on code changes.

uvicorn main:app --reload

The server will be running at http://127.0.0.1:8000.
4. Explore the API

You can access the interactive API documentation (Swagger UI) at the following URL:

http://127.0.0.1:8000/docs

From there, you can register users, log in, get a token, and test all the available endpoints.
API Endpoints

The API includes the following endpoints:

Path
	

Method
	

Description
	

Access Required

/register
	

POST
	

Register a new user (client, worker, admin)
	

Public

/token
	

POST
	

Log in and receive a JWT access token
	

Public

/users/me
	

GET
	

Get current user details
	

Authenticated

/users
	

GET
	

Get a list of all users
	

Admin

/orders
	

POST
	

Create a new order
	

Client

/orders/me
	

GET
	

Get current user's order history
	

Client / Worker

/orders
	

GET
	

Get a list of all orders
	

Admin

/payments/process
	

POST
	

Process a payment for an order
	

Authenticated
