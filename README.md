# Activewizards_test_task

## For start Tornado application python version must be >= 3.5

## Create venv
python3.6 -m venv venv_name
cd venv_name

## Install MongoDB:
	sudo apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv 	0C49F3730359A14518585931BC711F9BA15703C6
Create a sudo nano /etc/apt/sources.list.d/mongodb-org-3.4.list
echo "deb http://repo.mongodb.org/apt/debian jessie/mongodb-org/3.4 main" | sudo tee /etc/apt/sources.list.d/mongodb-org-3.4.list
sudo apt-get update
sudo apt-get install -y mongodb-org

## pip install -r  requirements.txt

sudo service mongod start (sudo service mongod stop, sudo service mongod restart)
mongoimport --db testdb --collection world --file world_bank.json

#### Start Flask dvelopment server
export FLASK_APP=hello.py
python -m flask run

#### Start Tornado dev server
virtualenv must be activate
python -m tornado_asunc_serv.py
