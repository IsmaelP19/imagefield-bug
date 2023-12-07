# imagefield-bug
Minimal example to reproduce the bug described on https://github.com/jowilf/starlette-admin/issues/422

## How to reproduce
1. Clone this repo: `git clone https://github.com/IsmaelP19/imagefield-bug`.
2. Get to the project: `cd imagefield-bug`.
3. Now, you can open it with the code editor of your preference. In my case, I use vscode: `code .`
4. The first thing you need to do once completed the previous steps is to start Docker Desktop, and after that, run the following command on the root of the project: `docker compose up`.
5. Now you can access to the database manager (adminer) by going to [http://localhost:8080](http://localhost:8080).
6. The credentials are the following:
   - Database engine: PostgreSQL
   - User: user
   - Password: password
   - Database name: exampledb

### ⚠️ It is important to notice that I used Poetry as a virtual environment. You can use any other you prefer.

7. `poetry install` will install all dependencies inside the pyproject.tml
8. To start the backend, just run the following command: `python app/main.py`
9. You will need a user to access the starlette-admin page. For that, go to [docs](http://localhost:8009/docs) and create a new user with the POST user endpoint.


# 🆕📣UPDATE
For some reason I still don't know, the bug is not here. However, the following bug has appeared (and is not present on my other project where I have this imagefield bug).

If you go to the Facilities tab, you will be able to create a new instance of a facility. However, the user relationship is not poblated on the select. That is not the main problem. The main issue here is that after you create the facility instance, if you try to view its details or edit them it does not go to the correct [url](http://localhost:8009/admin/facilities/edit/1), but it goes to an undefined one, as it wasn't getting the primary key specified.
