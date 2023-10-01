# {App Name } Robinhood Hackathon App
{App name } is a mobile app that enables citizens to easily report local issues like potholes, broken lights, and graffiti directly to their city using their smartphone camera and GPS location tagging. 
By engaging residents in identifying and reporting problems in their community, {App name} aims to strengthen accountability, collaboration between citizens and government, and overall quality of life. 
The app makes participating fun with features like achievement badges and neighborhood leaderboards while allowing users to track the status of issues they submit. 
With {App name}, it only takes a few taps on your phone to help improve your local area.

## Table of Contents
- [Installation & Setup](#installation--setup)
- [Usage](#usage)
- [Features](#features)
- [Screenshots/Demo](#screenshotsdemo)
- [Technologies Used](#technologies-used)
- [Contact](#contact)

## Installation & Setup

This project is built using Flask, a web development framework for Python. To get this project up and running locally on your machine, follow these steps:

### 1. Prerequisites:

Ensure you have the following installed:
- **Python** (3.6 or newer is recommended)
- **pip** (Python package installer)

### 2. Clone the repository:

```bash
git clone https://github.com/chijioke01/robinhood-hackathon.git
cd robinhood-hackathon
```

### 3.  Set up a virtual environment (optional but recommended)

Windows
```bash
python -m venv myenv
.\myenv\Scripts\activate
```

MacOS and Linux 

```bash
python3 -m venv myenv
source myenv/bin/activate

```

### 4. Install the required packages:
pip install Flask SQLAlchemy Werkzeug


### 5. Initialize the Database:
python
>>> from run import db
>>> db.create_all()
>>> exit()

### 6. Run the Application:
python run.py

## Usage
After setting up, navigate to `http://localhost:5000` on your web browser. Register a new account or login and start reporting issues.

## Features
- User registration and authentication.
- Ability to report community-based issues.
- View all reported issues on a map.
- Leaderboard to rank neighborhoods based on the number of reported issues.

## System Diagrmas 
*To Be Added*

## Screenshots/Demo
*To Be Added*

## Technologies Used
- Flask
- SQLite
- Bootstrap
- JavaScript
- HTM & CSS

## Contact
If you have any questions, concerns, or feedback, please contact:

- Chijioke: [chijioke-01]
- Yash:[yash-dubs] 
- Lee:[leemabhena]
- Xiaoyi: [Xiaoyi-Lin]
- John : [JohnExantus]

