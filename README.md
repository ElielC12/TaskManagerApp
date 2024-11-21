# Task Manager App
Overview
The Task Manager App is a productivity application designed to help students organize and manage their school assignments efficiently. It features intuitive task categorization, color-coded priorities, and scheduling capabilities, empowering users to stay on top of deadlines and optimize their productivity.

## Features
### Core Features
Add, Edit, and Delete Tasks: Easily manage tasks with fields like name, category, priority, and due date/time.
Color-Coded Priorities: Highlight tasks based on urgency (e.g., High: Red, Medium: Yellow, Low: Green).
Task Categorization: Group tasks under categories such as "Assignments," "Exams," and "Homework."
Sorting and Filtering: Sort tasks by due date, priority, or category; filter tasks based on selected criteria.
Persistent Data Storage: Automatically save tasks to a JSON file, ensuring data is retained between sessions.
Intuitive UI: A simple, visually intuitive interface for seamless navigation and task management.
## Stretch Goals
Recurring Tasks: Support for tasks that repeat daily, weekly, or at custom intervals.
Search Feature: Quickly locate tasks using keywords or categories.
Calendar Integration: Sync tasks and deadlines with calendar services (e.g., Google Calendar).
<br/>
## Tools & Technologies
### Languages & Frameworks
Python: Backend logic.
PySide6: Graphical User Interface (GUI) development.
### Additional Libraries
datetime module for managing task deadlines.
JSON for persistent storage.
### Development Tools
IDE: Visual Studio Code for development and debugging.
Assets: Free resources for icons and color palettes.

## App Architecture
### Front-End
Built with PySide6 for creating a responsive and user-friendly interface.
### Back-End
Task Class: Represents individual tasks with attributes like name, category, priority, and due date.
TaskManager Class: Manages tasks using methods like add_task, remove_task, and update_task.
### Persistent Storage
Uses a JSON file for storing and retrieving tasks, ensuring data persistence across sessions.
## User Interface
### Main Screens
Task Overview Screen: Displays all tasks with sorting and filtering options.
Task Editor Screen: Allows users to add or edit task details.
Settings/Help Screen: Offers app customization and usage instructions.


## Project Roadmap
### Minimum Viable Product (MVP)
To be completed by the second lab period:

1. Basic interface for adding, editing, and deleting tasks.
2. Task prioritization with visual color coding.
3. Task categorization and sorting functionality.
4. Persistent storage via a JSON file.
### Future Improvements
* Recurring tasks implementation.
* Enhanced search capabilities.
* Integration with calendar APIs for syncing deadlines.
  
## Installation Instructions
1. **Clone the Repository:**
'''git clone https://github.com/<your-username>/task-manager-app.git'''
cd task-manager-app'
2. **Set Up the Environment:** Ensure Python is installed on your system. Install PySide6:
'''pip install PySide6'''
3. **Run the Application:** Execute the main Python file to launch the app:
'''python main.py'''

## Contribution Guidelines
We welcome contributions to enhance the app!
Please follow these steps:

1. Fork the repository and create a new branch.
2. Commit changes with clear descriptions.
3. Submit a pull request for review.

For major feature suggestions, open an issue first to discuss the idea.
<br/>
## Authors
**Eliel Cortes**
**Logan Gardner**
<br/>
## License
This project is licensed under the MIT License.
<br/>
## Acknowledgments
Special thanks to our mentors and peers for feedback and guidance.
