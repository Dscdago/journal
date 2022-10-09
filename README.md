# Online Journal
#### Video Demo: [Online Journal](https://youtu.be/SqH8njp6lVU)
### Description:
I decided to create an online journal. Much like a notebook journal where you write what happened throughout the day, the online journal let's you do the same and keep it stored online. 

To begin, you need to sign up for an account with an username and password. There you can see your entried already submitted and write a new one. Only one entry is allowed per day, so you can't write multiple entries.

I decided to use bootstrap to design the website and flask to manage the backend of the journal entries. The entries are saved in a database where there are two table; one for users and one for all the entries. 

*`journal.db`*: The data base for the users takes the user's id, used to know who's logged in with flask's session function, the user's username, and a hash made from werkzeug's security library. The entry table takes into account the user's entry, date, and user_id.

*`app.py`*: the flask application ensures there is one username in the database, so there aren't any duplicates. It then connects to the sqlite database for the project. Inside the application, the index route ensures the user is logged in. If they are not, then they are sent to the login route where the user can log in using the form or create an account using the register route. If they are logged in, then the route renders `index.html` with their journal entries loaded into them. The index function also allows the user to delete entries from the table if the delete form is called.

The application also has a route to write an entry. A page is loaded where the user can write the entry for the day. The application then takes the entry and other variables such as date and user id to add into the table. The application also checks for entries on the same day, so if there is an entry already submitted for the day, then the function in to add an entry is disabled and instead shows an error saying that an entry already exists for today.

The application also has a logout route that logs the user out and and redirects them to the index route, which then redirects them to the login route.

*`helpers.py`*: I used the `helpers.py` file from CS50 Finance to facilitate login and checking that a user is logged in.

*`index.html`*: This shows the main page, once logged in, to the user. This page shows a table of the entries submitted. The table shows the entry number for the user, date it was written, and two buttons. The first button is to view the entry through a modal component where they can read the entry, the second button deletes the entry from the table. This page uses a JacaScript file to make the modal work.

*`index.js`*: The JavaScript file connects the `view` button in `index.html`. The content of the modal window is filled with the data from the entries table. The script fills in the data into the modal component.

*`entry.html`*: This shows the page where an user can input their entry for the day. It shows the current date and a `<textarea>` where they can write their entry. At the end there is a submit button to submit the entry. If there is an entry for the day already, then the `<textarea>` is substituted with a red message saying that an entry already exists for the day. In which case, they'll have to wait until the next day to submit an entry.

*`register.html`*: This is the register page. The user is welcomed by a form where they can submit a username, password, and confirmation of the password.

*`style.css`*: It makes some style changes to the site to make it more comfortable for the user to read and submit their entries. 