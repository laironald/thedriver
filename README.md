thedriver
=========
email:  thedriverjones@gmail.com
t*d*j*[3]!

installation
------------

```
sudo apt-get install -y apache2
sudo apt-get install -y git
sudo apt-get install -y python-pip
sudo apt-get install -y python-mysqldb
sudo apt-get install -y sqlite3
sudo apt-get install -y libapache2-mod-wsgi

git clone https://github.com/laironald/thedriver.git

pip install -r requirements.txt
gem install sass
gem install haml
```

gotchas
-----------


https://code.google.com/apis/console

  * need to enable both drive API and drive SKD
  * [Ignoring Files in GIT](https://help.github.com/articles/ignoring-files)
  * need to avoid the error caused by a timed out connection to MySQL

http://mofanim.wordpress.com/2013/01/02/sqlalchemy-mysql-has-gone-away/
http://docs.sqlalchemy.org/en/rel_0_8/dialects/mysql.html#connection-timeouts
