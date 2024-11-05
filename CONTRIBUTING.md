# Contributing to fastapi-user-authentication

Thank you for your interest in contributing! We welcome contributions to improve our project, including bug fixes, new features, documentation updates, and more.

## Table of Contents

- [Getting Started](#getting-started)
- [Development Workflow](#development-workflow)
- [Guidelines](#guidelines)
- [Documents](#documents)
- [Contact](#contact)

## Getting Started

Checkout [Project Issues](https://github.com/VannySothea/fastapi-user-authentication/issues) for details to-do information.

1. **Fork the Repository**: Start by forking the repository to your GitHub account.
2. **Clone Your Fork**:
   ```bash
   git clone https://github.com/VannySothea/fastapi-user-authentication.git
   cd fastapi-user-authentication
   ```
3. **Install Dependencies**: 
   Ensure you have Python 3.12+ installed. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. **Set Up Environment**: Configure the necessary environment variables:
   - Copy the `.env.example` file to `.env` and update values as needed.

## Development Workflow

1. **Create a Branch**: Use a descriptive branch name for your feature or fix.
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make Changes**: Implement your changes following the project's coding standards.

3. **Run Tests**: (Once tests are available) Run tests to ensure your changes don't break existing functionality.
   ```bash
   # Example command to run tests
   pytest
   ```

4. **Commit Changes**: Write clear, descriptive commit messages.
   ```bash
   git add .
   git commit -m "Add description of changes"
   ```

5. **Push to Your Fork**:
   ```bash
   git push origin feature/your-feature-name
   ```

6. **Create a Pull Request (PR)**: Go to the repository on GitHub and create a PR from your branch.

## Guidelines

### Code Style

- Follow **PEP 8** guidelines.
- Use descriptive variable names and comments where necessary.
- Ensure consistent formatting, especially in Python files.

### Documentation

- Update the documentation for any new features, modules, or functions you add.
- Include code comments and docstrings for complex logic.

### Commit Messages

- Use descriptive messages to explain the "why" behind each change.
- Use the format: `[Type]: Description` (e.g., `feat: add role-based access control`).

### Pull Request Checklist

- Ensure your PR description explains what changes are made and why.
- Reference any relevant issues by including the issue number.
- Address any feedback from code reviewers.

## Documents

### License

`VannySothea/fastapi-user-authentication` is open source and free to use based on `MIT License` and can be used for commercial purposes for free, but please clearly display the copyright information about VannySothea/fastapi-user-authentication in the display interface.

- This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

### Security

Please see [SECURITY.md](SECURITY.md) for details on reporting security vulnerabilities.

### Code of Conduct:

Please review the [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md) file for community guidelines and best practices when contributing.

### Release Notes

See [RELEASE_NOTES.md](RELEASE_NOTES.md) for a detailed changelog of the project's versions.

### Thanks
Thanks to the following developers for their contributions to fastapi-user-authentication:

<a href="https://github.com/VannySothea/fastapi-user-authentication/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=VannySothea/fastapi-user-authentication"  alt="Project Contributor"/>
</a>

## Contact

If you have any questions or need further guidance, feel free to reach out by creating an issue in the repository or contacting the maintainers or project owner `v.sothea.personal@gmail.com`.
