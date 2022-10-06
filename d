[33mcommit 931dddc4ac63c1ef9d601ba50f9529c5d2a72e4a[m[33m ([m[1;36mHEAD -> [m[1;32mhome[m[33m)[m
Author: Dscdago <daguito_saenz@hotmail.com>
Date:   Wed Oct 5 21:30:36 2022 -0600

    Continued to add modal functionality

[1mdiff --git a/app.py b/app.py[m
[1mindex ace5172..c497bac 100644[m
[1m--- a/app.py[m
[1m+++ b/app.py[m
[36m@@ -1,7 +1,7 @@[m
 # Flask application[m
 import os[m
 from cs50 import SQL[m
[31m-from flask import Flask, render_template, request, session, redirect, flash[m
[32m+[m[32mfrom flask import Flask, render_template, request, session, redirect[m
 from flask_session import Session[m
 from tempfile import mkdtemp[m
 from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError[m
[36m@@ -40,7 +40,6 @@[m [mdef after_request(response):[m
 def index():[m
     # Get entry data from database. Fill in select menus[m
     entries = db.execute("SELECT * FROM entries WHERE customer_id == ?", session["user_id"])[m
[31m-    [m
     return render_template("index.html", entries=entries)[m
 [m
 # Login route[m
[1mdiff --git a/flask_session/a96aa4e62beec8d56482478c8d9ef820 b/flask_session/a96aa4e62beec8d56482478c8d9ef820[m
[1mindex f9e0cc4..69e9eb2 100644[m
Binary files a/flask_session/a96aa4e62beec8d56482478c8d9ef820 and b/flask_session/a96aa4e62beec8d56482478c8d9ef820 differ
[1mdiff --git a/templates/index.html b/templates/index.html[m
[1mindex 4afc312..a98752b 100644[m
[1m--- a/templates/index.html[m
[1m+++ b/templates/index.html[m
[36m@@ -25,7 +25,7 @@[m
                     <tr>[m
                         <td>{{ entry["journal_id"] }}</td>[m
                         <td>{{ entry["date"] }}</td>[m
[31m-                        <td><button type="button" class="btn btn-info" data-bs-toggle="modal" data-bs-target="#journalEntry" data-bs-journal='{{ entry | tojson }}'>View</button></td>[m
[32m+[m[32m                        <td><button type="button" class="btn btn-info" data-bs-toggle="modal" data-bs-target="#journalEntry" data-myentry='{{ entry | tojson }}'>View</button></td>[m
                     </tr>[m
                 {% endfor %}[m
             </tbody>[m
[36m@@ -40,7 +40,7 @@[m
                     <button type="button" class="btn-close" data-bs-dismiss="modal"></button>[m
                 </div>[m
                 <div class="modal-body">[m
[31m-                    [m
[32m+[m[32m                    <p id="entryParagraph"></p>[m
                 </div>[m
                 <div class="modal-footer">[m
                     <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>[m
[36m@@ -56,13 +56,13 @@[m
         const button = event.relatedTarget[m
 [m
         // Extract info from data-bs-journal[m
[31m-        const entryNumber = button.getAttribute('data-bs-journal')[m
[32m+[m[32m        const entryJSON = event.target.dataset.myentry[m
         [m
         // Update modal's content[m
         const motalTitle = journalModal.querySelector('.modal-title')[m
         const modalBody = journalModal.querySelector('.modal-body')[m
 [m
[31m-        modalTitle.textContent = 'Journal Entry # ${entryNumber}'[m
[31m-        modalBodyInput.textContent = 'Hello'[m
[32m+[m[32m        modalTitle.textContent = 'Journal Entry # ${entryJSON.journal_id}'[m
[32m+[m[32m        modalBodyInput.innerHTML = entryJSON["entry"][m
     })[m
 </script>[m
\ No newline at end of file[m
