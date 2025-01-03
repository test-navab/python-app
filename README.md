# run flask app in ec2 with systemd service

git clone https://gitlab.com/group-for-devops/python.git demo-project

<NOTE: 
  In git repo I am not storing ".env" file it has data base credentials so make sure befor you start application the file ".env" with data should exist in root folder of project

cd demo-project

sudo apt update

sudo apt install python3-pip -y


# install dependencies

pip install wheel

pip install gunicorn

pip install flask 

# Install  application dependencies

pip install pymysql

pip install python-dotenv

# you can run application using below command 

python3 app.py

# NOTE: the above python app fails because mysql should run and configure user and password for mysql server

# install mysql on ec2 i am using docker here for run mysql

docker run --name mysql -e MYSQL_ROOT_PASSWORD=root -e MYSQL_DATABASE=usersdata -e MYSQL_USER=navab -e MYSQL_PASSWORD=admin123 -d mysql

# NOTE: actually we run mysql on another ec2 if we have data base team if not use rds service in AWS for data base


# now my mysql running fine now wee run our python application

# for my python application i need to pass these environment variables
vim .env 

DB_HOST=localhost
DB_USER=navab
DB_PASS=admin123
DB_NAME=usersdata

# run python application in two ways general 

python3 app.py 

# above command is for just test purpose only. for production run case use gunicorn

# Run Gunicorn WSGI server to serve the Flask Application When you “run” flask, you are actually running Werkzeug’s development WSGI server, which forward requests from a web server. Since Werkzeug is only for development, we have to use Gunicorn, which is a production-ready WSGI server, to serve our application

gunicorn -b 0.0.0.0:8000 app:app & 

# access in browser "ec2IP:8000"

=====================================================================================================================

# above is enough for running but if you want to run your application as system service use below thing 


# Use systemd to manage Gunicorn Systemd is a boot manager for Linux. We are using it to restart gunicorn if the EC2 restarts or reboots for some reason. We create a .service file in the /etc/systemd/system folder, and specify what would happen to gunicorn when the system reboots. We will be adding 3 parts to systemd Unit file — Unit, Service, Install

sudo vim /etc/systemd/system/demo.service

[Unit]

Description=Gunicorn instance to serve myproject

After=network.target

[Service]

User=ubuntu

Group=www-data

WorkingDirectory=/home/ubuntu/demo-project

Environment="PATH=/home/ubuntu/demo-projectd"

ExecStart=/home/ubuntu/demo-project/gunicorn --bind 0.0.0.0:5000 app:app

[Install]

WantedBy=multi-user.target

# Then start the service:

sudo systemctl start demo

sudo systemctl enable demo

sudo systemctl status demo

=================================================================================================================================



# we can run this application using docker

# build docker image

docker build -t python-users-data:v1

docker run -d --name python python-users-data:v1

# the above command will not work because we need to pass environmnet variables

docker run -d --name python --network=my-net -p 8000:5000 -e DB_HOST=mysql -e DB_PORT=3306 -e DB_USER=navab -e DB_PASS=admin123 -e DB_NAME=usersdata python_users_data:v5

# but it will exit because there is no mysql container so first deploy mysql container

docker run --name mysql --network=my-net -e MYSQL_ROOT_PASSWORD=root -e MYSQL_DATABASE=usersdata -e MYSQL_USER=navab -e MYSQL_PASSWORD=admin123 -d mysql

# NOTE:
   # we need deploy both containers in custom netwrok only then only communicate with dns ispossible



kubectl create secret docker-registry github-docker-secret \
  --docker-server=ghcr.io \
  --docker-username= \
  --docker-password=