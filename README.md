# Ticket Tracker

----

## Purpose

This project serves as a demonstration of the author's handling of backend functionalities along with the ability to bring an application to a live, online environment. 

## Description

The Ticket Tracker app is a Django-based web application meant to manage work orders (tickets). This app has been designed for software companies to process tickets that include bug fixes, modifications, and feature additions.

----

## Features

### Submitting Tickets
- Supervisors can submit tickets directly through the app.
- Each ticket should clearly describe the issue, the urgency level, and any relevant details about the software in question.
- The tickets also include a field for uploading files.

### Assigning Tickets
- Once a ticket is submitted, it can be assigned to specific employees.
- Assignments can be based on expertise, availability, or workload.

### Managing Tickets
- Employees can view their assigned tickets, update their status (e.g., in progress, completed), and add notes or queries as needed.

### Tracking Progress
- The app provides real-time updates on ticket status, allowing both supervisors and employees to monitor progress efficiently.

----

## Installation

To run this app, the following are required: Python (v3.9+).

----

## Demo Version

You can visit the demo version at [munks.pythonanywhere.com](http://munks.pythonanywhere.com)

- **Data Reset**: If you want to revert back to the original demo information, click on "Reset Data" link in the sidebar. This will remove any tickets, messages, and other modifications you have made. Furthermore, this app has a scheduled task to reset on a daily basis.

## How to run locally

After cloning the app to your computer, navigate to the project directory in the terminal. Initiate the virtual environment, install the requirements, migrate and run the project. 

1. Virtual environment command: 
`env\Scripts\activate`

2. Install the project requirements: 
`pip install -r requirements.txt`

3. Migrate and run the project:
`python manage.py migrate`
`python manage.py runserver`

----

## Contact

Hunter Weselosky - huntermweselosky@gmail.com

