#!/bin/bash

echo "Deleting ANY old migrations"
rm -f "./firewall_rules/migrations/0*.py" 


echo "Clean/Recreate MySQL database"
echo "drop database firewall_mason_db;" > tempsql.sql
echo "create database firewall_mason_db;" >> tempsql.sql
sudo mysql < tempsql.sql
#rm -f tempsql.sql


echo "Create Django Migrations"
python2 ./manage.py makemigrations firewall_rules
python2 ./manage.py migrate firewall_rules
python2 ./manage.py migrate authtoken
python2 ./manage.py migrate
