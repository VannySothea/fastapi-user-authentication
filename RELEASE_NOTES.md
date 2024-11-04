# FastAPI User Authentication 1.0.0 Release Notes
This document includes the release notes for each version of the FastAPI User Authentication System.
## [1.0.0] Release date: November 05 2024

### Features
1. **User Registration**: Allows new users to create an account and verify with 6-digit code via email verification.
2. **User Authentication**: Enables users to log in securely using their credentials.
3. **Password Reset**: Facilitates password recovery and verify with 6-digit code via email verification.
4. **Device Limitation**: Allows users to log in on up to specific number of devices per account (e.g., 5 devices log in on 1 account), removing the oldest device upon exceeding the limit.
5. **Refresh Token Rotation**: Provides secure, rotating access and refresh tokens for session management.
6. **Role Base Acess Control (RBAC)**: Permissions and access levels within the application
7. **Rate Limiting**: Restricts repeated requests within a defined period to prevent abuse.
8. **Account Lockout**: Temporarily locks user accounts after multiple failed login attempts.
9. **IP Blacklisting**: Blocks requests from specific IPs to enhance security.
10. **Periodic Cleanup**: Schedule background jobs for tasks like cleanup. This keeps the database clean and prevents it from growing uncontrollably.
11. **Temporary Storage**: Store registration data in a temporary location (e.g., a separate database table) until the user verifies their email. Once verified, move the data to the main user table. This keeps the primary user table free from unverified accounts.
12. **Async SQLAlchemy**: for asynchronous database operations, allowing for improved performance and scalability in handling multiple concurrent requests.
