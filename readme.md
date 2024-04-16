# Railway Management System

Railway Management System is a Flask-based API for managing train bookings similar to IRCTC.

## Setup Instructions

Follow these steps to set up the project:

1. **Clone the Repository:**

   ```bash
   git clone <repository_url>
   cd irctc

    ```

2. **Install Dependencies:**

```bash
python -m env 
(activate environment)
pip install -r requirements.txt

```

3.  **Database Configuration:**
Create a MySQL database named railway_management.Update the database configuration in config.py if necessary.

4.  **Database Migration:**

```bash
flask db upgrade
```

**Run the Application:**

```bash

python run.py

```
API Endpoints
/register (POST): Register a new user.
/login (POST): Log in to an existing user account.
/trains (POST): Add a new train (accessible only to admins).
/availability (GET): Get seat availability between two stations.
/book (POST): Book a seat on a particular train.
/booking/<booking_id> (GET): Get booking details by booking ID.

```


Authentication
The API uses JSON Web Tokens (JWT) for authentication.
Admin endpoints require an authorization token for authentication.
User-specific endpoints require an authorization token obtained after login.
