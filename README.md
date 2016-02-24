# Project 3

*By [CJ](https://github.com/vssrcj)*

This project utilizes web frameworks, an ORM and authentication to make a South African Sport Players Web Application.

## How to get the files

Clone a copy of this repository on your local machine

```
git clone git://github.com/vssrcj/udacity-fullstack-project3.git
```

### Install Vagrant

Vagrant is needed for this application to work.

First install Virtualbox (or another supported provider) for virtualisation.
A guide is found [here](https://www.udacity.com/wiki/ud197/install-vagrant) to install both virtualbox and vagrant.

### Launch Vagrant

Navigate to the cloned repository.
Run:
```
vagrant up
vagrant ssh
```

Once Vagrant is booted up, and logged into, navigate to the sports directory with:
```
cd /vagrant/sports
```

Description
-----------

* **database_setup.py** is must be run first with python in order for the database to work
* **data.py** can be run to insert sample data into the web application

### Running the application

```
python project.py
```
Navigate to **http://localhost:5000/sports** with your favourite web browser

### Application functionality

* You will be displayed a list of sports in South Africa at the top
* Each tab displays the most popular players of that sport, and any person may view it
* You must log into the application by clicking on the right top-hand corner.  This will authenticate you using Google's services.
* Only after you are authenticated may you create a new player by clicking on the tab
* You can only edit or delete the players you have created
* You can navigate to /json for a JavaScript endpoint, or /atom for an Atom one

How the program is made
-----------------------
* [Foundation](http://foundation.zurb.com/) is used for the styling and layout
* [Google](https://developers.google.com/identity/) is used for authentication
* [Flask](http://flask.pocoo.org/) is used as the Python framework
* [SQLAlchemy](http://www.sqlalchemy.org/) is used as the ORM to connect Flask and a SQLite database
