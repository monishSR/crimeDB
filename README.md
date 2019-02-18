# crimeDB


First we have to install sqlite3, the database our webapp uses.

```bash
    sudo apt-get install sqlite3
```

Then install python packages inside requirements.txt
```bash
    sudo pip3 install -r requirements.txt
```

To update our database, do migrate
```bash
    python3 manage.py migrate
```

To run the website, do runserver
```bash
    python3 manage.py runserver
```

And for logging in,
```
    username=monish
    password=test1234$
```
