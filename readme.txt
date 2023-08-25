This project utilizes the following:

pip
flask
Flask-SQLalchemy
sqlalchemy
marshmallow
psycopg2
sqlalchemy-utils
flask-marshmallow
marshmallow-sqlalchemy
MarkupSafe
flask-bcrypt
PyGit


See here for sqlalchemy-utils docs:
https://sqlalchemy-utils.readthedocs.io/en/latest/data_types.html#module-sqlalchemy_utils.types.json



To run:
git clone
python3 -m pipenv install
python3 -m pipenv shell
use postman in repo
(github_username when creating a user has to be a valid github user, the password is for cyclone)
(the github_token in add auth needs to be an personal access token (fine-graned tokens recommended, soon will be a requirement) made by the account with the username given when creating a user)
run through CRUD operations (work flow is add user -> add auth -> back to users -> back to auth -> Full CRUD on Repositories -> -Commits -> Sessions)

Pulling and commiting to github with this application is not yet implimented