# PetMed

## Project Description

PetMed is a pet health and social media application designed to help pet owners manage their pets' health while connecting with other pet owners and professionals. Users will be able to create profiles for their pets, share experiences, ask health-related questions, track symptoms and medications, and find useful pet health information.

PetMed will have five main user roles:

- Pet Owner
- Veterinarian
- Pet Health Expert
- Community Moderator
- Administrator

The goal of PetMed is to create a helpful community where pet owners can learn more about their pets' health and communicate with others. The system will also separate regular community advice from professional guidance provided by veterinarians and pet health experts.

---

## Team Members

- Miles Sharpton
- Makai Lyn-Ah-Ping
- David Bahidika
- 
- 

## Scrum Master

- Dorien Parris

---

## Selected Technologies

### Programming Language
- C++

C++ will be used as the main programming language for the project. It was selected because it provides good performance and supports object-oriented programming, which will help organize different parts of the PetMed application.

### Frontend
- React
- JavaScript
- HTML
- CSS

React will be used to develop the user interface for PetMed. It will allow the team to create a responsive interface that can be used to display pet profiles, health information, community posts, and other features in future sprint cycles.

### Database
- MySQL

MySQL will be used to store and manage the application's data. In later sprint cycles, it may store information such as users, pet profiles, symptoms, medications, posts, comments, and other PetMed information.

### Coding IDE
- Visual Studio Code (VS Code)

Visual Studio Code will be the main coding IDE used by the team. Team members will use VS Code to write and manage the C++, React, JavaScript, HTML, and CSS files used throughout the project.

### Version Control
- Git
- GitHub

Git will be used to track changes made to the project. GitHub will contain the team's official shared repository and will allow each team member to contribute to the project.

### Testing
- GoogleTest
- Jest

GoogleTest can be used to test C++ code, while Jest can be used to test the React portion of the application. Automated testing is not required during Sprint Cycle 0.

---

## Repository Structure

    PetMed/
    |
    |-- frontend/
    |   `-- README.md
    |
    |-- src/
    |   `-- README.md
    |
    |-- include/
    |   `-- README.md
    |
    |-- docs/
    |   `-- README.md
    |
    |-- tests/
    |   `-- README.md
    |
    `-- README.md

### Folder Descriptions

- `frontend/` - Will contain the React frontend.
- `src/` - Will contain C++ source files.
- `include/` - Will contain C++ header files.
- `docs/` - Will contain project documentation.
- `tests/` - Will contain testing files in future sprint cycles.
- `README.md` - Contains general project information and setup instructions.

No PetMed-specific functionality will be implemented during Sprint Cycle 0.

---

## Development Setup

Each team member should have the following installed:

- Visual Studio Code
- C++ compiler
- Node.js and npm
- Git
- MySQL
- GitHub account

Testing tools such as GoogleTest and Jest may be configured when automated testing begins.

---

## GitHub Setup Instructions

### 1. Accept Repository Access

Each team member must accept the invitation to the team's GitHub repository.

### 2. Clone the Repository

Open the terminal in VS Code and run:

    git clone [GITHUB REPOSITORY URL]

### 3. Enter the Project Folder

    cd PetMed

### 4. Pull the Current Version

Before making changes, run:

    git pull origin main

### 5. Make a Sprint Cycle 0 Contribution

Each team member must make at least one small nonfunctional contribution.

Examples include:

- Updating the README
- Adding team member information
- Adding setup instructions
- Creating a documentation file
- Creating a project folder
- Correcting documentation

No PetMed functionality should be added during Sprint Cycle 0.

### 6. Commit Your Changes

    git add .
    git commit -m "Add Sprint Cycle 0 contribution"

### 7. Push Your Changes

    git push origin main

Each team member must make their contribution using their own GitHub account.

### 8. Pull the Final Version

After all team members have made their contributions:

    git pull origin main

Verify that everyone's changes are included.

---

## Running the Development Environment

Sprint Cycle 0 is focused on setting up the development environment. The final PetMed application has not been implemented yet.

### C++

Team members can verify their C++ environment using a basic C++ program.

Example compilation command:

    g++ main.cpp -o petmed

### React

When the React project is created in a future sprint, team members will navigate to the frontend folder:

    cd frontend

Install the required packages:

    npm install

Start the development environment:

    npm start

### MySQL

Team members should verify that MySQL is installed and can be accessed from their development environment.

PetMed-specific database tables will not be created during Sprint Cycle 0.

---

## GitHub Workflow

Each team member is responsible for:

1. Accepting access to the GitHub repository.
2. Cloning the repository to their own computer.
3. Pulling the latest version of the repository.
4. Making one small nonfunctional contribution.
5. Committing the contribution using their own GitHub account.
6. Pushing the contribution to GitHub.
7. Pulling the repository again after all contributions are complete.
8. Verifying that all team changes are available.

---

## Sprint Cycle 0 Goals

During Sprint Cycle 0, the team will:

- Review the complete PetMed functional requirements.
- Understand the five system roles and major use cases.
- Identify unclear requirements or questions.
- Select the project's development technologies.
- Set up the shared GitHub repository.
- Add each team member as a collaborator.
- Create the initial repository structure.
- Verify that each team member can clone and pull the repository.
- Verify that each team member can commit and push changes.
- Prepare the initial project documentation.

---

## Sprint Cycle 0 Restrictions

During Sprint Cycle 0, the team will not:

- Implement PetMed-specific use cases.
- Implement authentication or authorization.
- Create PetMed-specific database tables.
- Develop the final PetMed user interface.
- Implement project-specific functionality.
- Use ZIP files or file sharing as the normal method of combining project work.

All official project work will be stored in the team's GitHub repository.

---

## Sprint Cycle 0 Verification

Each team member must provide:

- Evidence of successfully cloning or pulling the repository.
- At least one commit or push from their own GitHub account.
- A screenshot showing a successful pull of the current repository.
- Verification that they can access the current project files.

---

## Current Project Status

**Sprint Cycle:** Sprint Cycle 0 - Team Setup and Project Preparation

The team is currently preparing the development environment, GitHub repository, and project documentation. PetMed functionality, database design, and the final user interface will be developed during later sprint cycles.
