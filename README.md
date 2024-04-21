To run the app, navigate into databasesproj -> appFolder -> run.py 

To execute run.py, either press the Play Button in IDE *OR* do the following in terminal:

export FLASK_DEBUG=1

flask run


The web application is accessible on URL    http://127.0.0.1:5000/



Execute this query in your own database to add a Logging table:

CREATE TABLE Logs (
	query_run VARCHAR(255)
);

The logging page will refer to entries in this table.
