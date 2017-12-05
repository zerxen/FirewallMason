echo "Deleting ANY old migrations"
del "..\backend\firewall_rules\migrations\0*.py" 


echo "Clean/Recreate MySQL database"
echo drop database firewall_mason_db; > .\tempsql.sql
echo create database firewall_mason_db; >> .\tempsql.sql
"C:\Program Files\MySQL\MySQL Server 5.7\bin\mysql.exe" -u root -phegy2CxgD3pyQWJjUjIX < .\tempsql.sql


echo "Create Django Migrations"
python ..\backend\manage.py makemigrations firewall_rules
python ..\backend\manage.py migrate firewall_rules
python ..\backend\manage.py migrate authtoken
python ..\backend\manage.py migrate