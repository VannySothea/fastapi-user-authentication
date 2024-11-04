# FastAPI User Authentication
<p><em>Python and FastAPI for User Authentication module focuses on security and standard.</em></p>

An open-source user authentication module for applications built with Python and FastAPI, designed to handle user registration, email verification, authentication, reset password, device detection, rate limiting, account lockout, IP blacklisting, and refresh token rotation.

## Features
- **User Registration**: Allows new users to create an account and verify with 6-digit code via email verification.
- **User Authentication**: Enables users to log in securely using their credentials.
- **Password Reset**: Facilitates password recovery and verify with 6-digit code via email verification.
- **Device Limitation**: Allows users to log in on up to 5 devices per account, removing the oldest device upon exceeding the limit.
- **Rate Limiting**: Restricts repeated requests within a defined period to prevent abuse.
- **Account Lockout**: Temporarily locks user accounts after multiple failed login attempts.
- **IP Blacklisting**: Blocks requests from specific IPs to enhance security.
- **Refresh Token Rotation**: Provides secure, rotating access and refresh tokens for session management.

## Table of Contents
1. [Installation](#installation)
   - [Redis Setup](#redis-setup)
2. [Configuration](#configuration)
3. [Usage](#usage)
   - [Postman Collection](#postman-collection)
   - [Check Rate Limit and Account Lockout](#check-rate-limit-and-account-lockout)
4. [Project Structure](#project-structure)
5. [Testing](#testing)  <!-- Placeholder section -->
6. [Contributing](#contributing)
7. [License](#license)

## Installation
1. **Clone the Repository**:
   ```bash
   git clone https://github.com/VannySothea/fastapi-user-authentication.git
   cd fastapi-user-authentication
   ```
2. **Install Dependencies**: Make sure you have Python installed, then install required packages:
   ```bash
   pip install -r requirements.txt
   ```
3. **Setup Database**: Configure a database (e.g., PostgreSQL) for user authentication data storage. Update your .env file with the database URI.
  
### Redis Setup
This authentication module requires Redis for rate limiting, account lockout, and IP blacklisting features. Redis acts as a fast, in-memory database to manage these features efficiently.

#### Installation Instructions
To install Redis, follow the instructions for your operating system:

- **macOS**:
  ```bash
  brew install redis
  ```
  Then start Redis:
  ```bash
  brew services start redis
  ```

- **Linux** (Ubuntu/Debian):
  ```bash
  sudo apt update
  sudo apt install redis-server
  ```
  To start the Redis service:
  ```bash
  sudo systemctl start redis
  sudo systemctl enable redis
  ```

- **Windows**:
  1. Download the latest [Redis release for Windows](https://github.com/microsoftarchive/redis/releases).
  2. Extract the downloaded file, then open the extracted folder in Command Prompt.
  3. Run Redis with the following command:
     ```bash
     redis-server.exe
     ```
     Or
     ```bash
     ./redis-server.exe
     ```

## Configuration
You can configure database, email, rate limits, lockout settings, token secret, and other settings via environment variables or by modifying the `.env` file format.

**Sample `.env` File**:
```ini
APP_NAME=APP_NAME
COMPANY_NAME=COMPANY_NAME

FRONTEND_HOST=http://localhost:3000 #local host for frontend

JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=3
REFRESH_TOKEN_EXPIRE_MINUTES=25920 #18 days = 25920 minutes
```

**Sample `.env.mail` File**:
```ini
MAIL_USERNAME=REPLACE_THIS_WITH_YOUR_EMAIL_ADDRESS_@GMAIL.COM
MAIL_PASSWORD=REPLACE_THIS_WITH_YOUR_EMAIL_PASSWORD
MAIL_PORT=EMAIL_PORT
MAIL_SERVER=YOUR_EMAIL_SERVER
MAIL_STARTTLS=True
MAIL_SSL_TLS=False
MAIL_DEBUG=True
MAIL_FROM=REPLACE_THIS_WITH_YOUR_EMAIL_ADDRESS_@GMAIL.COM
MAIL_FROM_NAME=APP_NAME
USE_CREDENTIALS=True
```

**Sample `.env.settings` File**:
```ini
DATABASE_HOSTNAME=localhost
DATABASE_PORT=5432
DATABASE_USERNAME=postgres
DATABASE_PASSWORD=YOUR_DATABASE_PASSWORD
DATABASE_NAME=YOUR_DATABASE_NAME

# JWT Secret Key
JWT_SECRET=355fa9f6f9c491417c53b701b26dd97df5825d4abd02957ce3bb1b9658593d9a

# App Secret Key
SECRET_KEY=9a35f82513e1cdf2748afbd4681ff2eda8fc29a46df52cc8c4cdd561c0632400
```

**Sample `.env.ratelimiting` File**:
By using the value below, rate limit will apply after the operation reach
- Device: 4 requests in 30 seconds will cooldown for 5 minutes
- IP Address: 10 requests in 30 seconds will cooldown for 10 minutes
```ini
OPERATION_PERIOD=30
OPERATION_DEVICE_RATE_LIMIT=4
OPERATION_DEVICE_COOLDOWN=300
OPERATION_IP_RATE_LIMIT=10
OPERATION_IP_COOLDOWN=600
```

**Sample `.env.lockout` File**:
By using the value below, lockout will apply after the operation reach
- Device: 5 failed in 3 minutes will lockout for 30 minutes
- IP Address: 15 failed in 3 minutes will lockout for 3 hours
```ini
OPERATION_COOLDOWN_PERIOD=180
OPERATION_DEVICE_FAIL_LIMIT=5 
OPERATION_DEVICE_LOCKOUT_PERIOD=1800
OPERATION_IP_FAIL_LIMIT=15
OPERATION_IP_LOCKOUT_PERIOD=10800
```

## Usage
This module can be tested and used via Postman. Below is example of how to interact with the user authentication API using Postman.

### Register a User
**Endpoint**: `POST /user`

- **URL**: `http://localhost:8000/user`
- **Headers**:
  - Content-Type: application/json
  - device-id: `your_device_id_here`
- **Body** (JSON):
  ```json
  {
    "user_name": "User Name",
    "email": "email@domain.com"
    "password": "password",
  }
  ```
  
### Postman Collection

To make it easier, you can use the provided Postman collection that includes all the requests for this user authentication module.

#### Importing the Postman Collection
1. Download the Postman collection file from the link below:
   - [Download User Authentication Postman Collection](https://github.com/VannySothea/fastapi-user-authentication/blob/main/user_authentication_VannySothea.postman_collection)

2. Open Postman and click on "Import" in the top left corner.

3. Choose the downloaded collection file and click "Open."

4. The collection will appear in your Postman app, ready to use.

### Check Rate Limit and Account Lockout
For routes that implement rate limiting and lockout, you can make requests to that endpoint multiple times to test the functionality.

1. **Successful Login**: Make repeated requests with valid credentials to trigger rate limiting.
2. **Failed Login Attempts**: Make repeated requests with invalid credentials to trigger lockout and rate limiting.

## Project Structure
Here’s an overview of the project directory structure:

```plaintext
fastapi-user-authentication/
├── .github/              # GitHub templates and settings
├── alembic/              # Database migrations
├── app/                  # Main application code
│   ├── config/           # Configuration files (database, email, security)
│   ├── jobs/             # Background tasks and schedulers
│   ├── models/           # Database models
│   ├── responses/        # API response schemas
│   ├── routes/           # API route handlers
│   ├── schemas/          # Pydantic schemas for validation
│   ├── services/         # Service logic (e.g., email, security)
│   ├── templates/        # Email templates
│   ├── utils/            # Utility functions
│   └── main.py           # Entry point for starting the FastAPI application
├── env/                  # Environment variables
├── .gitignore            # Files and directories to be ignored by Git
├── LICENSE               # Project license
├── README.md             # Project documentation
├── alembic.ini           # Alembic configuration
├── requirements.txt      # Python dependencies
└── user_authentication_VannySothea.postman_collection  # Postman API collection
```

## Testing

Testing is planned for future updates. Contributions are welcome to help us implement a comprehensive testing suite for this project!

If you're interested in contributing, here are some ways you can help:

- **Write Unit Tests**: Help us create unit tests for existing features.
- **Integration Tests**: Consider writing integration tests to ensure components work together seamlessly.
- **Test Documentation**: Assist in documenting the testing process and how to run tests.

Feel free to open an issue or submit a pull request to discuss your contributions!
## Contributing
Contributions are welcome! If you’d like to contribute, please follow these guidelines:

1. **Fork the Repository**: Make a copy of this repo on your own GitHub account.
2. **Create a New Branch**: For each feature or bug fix, create a new branch:
   ```bash
   git checkout -b feature/new-feature
   ```
3. **Write Clear, Detailed Commits**: Aim for concise, meaningful commit messages.
4. **Create a Pull Request**: Once your code is ready, open a pull request (PR) from your branch to the `main` branch.

**Code of Conduct**:
Please review the `CODE_OF_CONDUCT.md` file for community guidelines and best practices when contributing.

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
