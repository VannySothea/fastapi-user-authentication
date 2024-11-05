# Security Policy for fastapi-user-authentication

## Reporting a Vulnerability

We take security seriously and are committed to maintaining the security of our project. If you discover a security vulnerability, please report it as soon as possible.

### Steps to Report a Vulnerability

1. **Email**: Send an email to v.sothea.personal@gmail.com with the following information:
   - A description of the vulnerability.
   - Steps to reproduce the issue.
   - Any relevant logs or screenshots.

2. **Do Not Share Publicly**: Please do not disclose the vulnerability publicly until it has been addressed. This helps us protect our users and the integrity of the project.

3. **Response Time**: We will respond to your report as soon as possible and will keep you updated on the progress of the fix.

## Usage
### Sending Emails from the Shared Account
This application is configured to send emails from a dedicated account: `open.source.user.authentication@gmail.com`. This account is specifically created for application use and utilizes an app password for secure authentication.
#### Important Guidelines
- **Account Usage**: Emails sent from this account should only be related to application functionalities (e.g., account verification, password resets).
- **Rate Limits**: Be aware that this account has a limit on the number of emails sent per day. Please do not send excessive emails to avoid being flagged for spam.
- **Content Restrictions**: Ensure that the content of the emails adheres to community standards and does not include spam or unsolicited messages.
- **Consent**: Always obtain consent from recipients before sending emails, particularly for verification purposes.

#### Important Notice: Shared Email Account Security

As this application is open source, the email account used for sending communications is also publicly accessible to anyone who has access to the codebase. Please keep the following points in mind:

- **Account Transparency**: The email account (`open.source.user.authentication@gmail.com`) is intended solely for sending application-related emails, such as account verification and notifications. Since it is shared, any contributor or user of the codebase may see the email credentials.

- **Data Handling**: Be mindful of the data you handle and send through this shared account. Avoid including sensitive personal information in email communications to protect users' privacy.

- **Security Practices**: While we use an app password for secure access, it's crucial to maintain best practices around data security. Do not share or expose the email credentials in public forums or repositories.

- **Usage Guidelines**: Only use the shared email account for legitimate application purposes. This helps prevent misuse of the account and ensures that we maintain a positive reputation for the application.

## Secure Coding Practices
To help maintain the security of this project, we encourage contributors to follow these best practices:

- **Input Validation**: Always validate and sanitize user input to prevent injection attacks (e.g., SQL injection, XSS).
- **Authentication**: Use strong authentication mechanisms, such as hashed passwords and secure tokens.
- **Authorization**: Implement Role-Based Access Control (RBAC) to ensure users have appropriate permissions.
- **Use HTTPS**: Always use HTTPS to encrypt data in transit and protect against man-in-the-middle attacks.
- **Keep Dependencies Updated**: Regularly update dependencies and monitor for known vulnerabilities using tools like [Dependabot](https://dependabot.com/) or [Snyk](https://snyk.io/).

## Security Updates

We will provide security updates and patches as necessary. To stay informed about security-related updates, please watch the repository or check the [releases](https://github.com/VannySothea/fastapi-user-authentication/releases) page.

Thank you for helping us keep our project secure!
