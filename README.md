# A webapp for the CA of Advance programming
https://github.com/bkcelebi/DBS-project

https://taskmate-ca.herokuapp.com/


**TaskMate is a web app that helps you to manage your tasks easily.**


In the app there are 8 parts as follows:
- env
- static
- templates
- app.py
- procfile
- readme.md
- requirements.txt
- test.db

- Env:
The app was built in a virtual environment to make sure all the dependencies are packed with the app itself and also transfered all together when needed. 

- Static:
The static file was not used in this particular project. 

- Templates:
Templates are html pages that are rendered to show dynamic content based on user action. There are 8 html templates as follows:
  - ads.html      # This page is used to render all users' tasks in a table format
  - base.html     # This page is the skeleton of all the pages and other pages inherit some parts from this page
  - index.html    # This page is the reception page
  - login.html    # Log in page
  - profile.html  # This page is where users can only see their own tasks and where users can create new tasks
  - search.html   # This page is where the users' search result is rendered
  - signup.html   # Sign up page
  - update.html   # This page is where users can update existing tasks

-app.py:
This is the file where the Flask app, database and bcrypt are initiated and also where models and views are. 

-procfile:
Procfile is required by Heroku as the app is hosted on that platform. Procfile specifies the commands that are executed by the app on startup.

-readme.md:
This contains the remote repository link, the heroku link, where the app is hosted, and the documentation of the app.

-requirements.txt:
This txt file contains the required packages/libraries that are used in the app.

-test.db:
This is sqlalchemy, the database used in the app.
