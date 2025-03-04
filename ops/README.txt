#######################
# TRAINING SERVER SETUP
#######################
mkdir -p ~/HandWrittenDigitRecognition
cd ~/HandWrittenDigitRecognition
sudo apt update
apt install python3.12-venv
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

######################################################
# COPYING TRAINING FILES FROM LOCAL -> TRAINING SERVER
######################################################
# Uploading the relevant files on the training server
./ops/copy-files-to-training-server

#########################################
# RUNNING TRAINING ON THE TRAINING SERVER
#########################################
source venv/bin/activate
python training.py

################################################################################
# DEPLOYING THE TRAINED MODEL FROM THE TRAINING SERVER TO THE APPLICATION SERVER
################################################################################

# Run this on the training server
cd ~/HandWrittenDigitRecognition
./ops/copy-models-to-app-server


##########################
# APPLICATION SERVER SETUP
##########################
# Update /etc/nginx/sites-available/sites on the application server
sudo ln -s /etc/nginx/sites-available/sites /etc/nginx/sites-enabled
sudo service nginx restart

###############################
# APPLICATION ENVIRONMENT SETUP
###############################
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install gunicorn
pip install -r requirements.txt

#####################################################
# DEPLOYING THE APPLICATION ON THE APPLICATION SERVER
#####################################################
# Upload the relevant files on the application server - run this locally
./ops/copy-files-to-app-server

###################################################
# RUNNING THE APPLICATION ON THE APPLICATION SERVER
###################################################
cd /var/www/flask-apps/HandWrittenDigitRecognition
python3 -m venv venv
source venv/bin/activate
pkill -f HandWrittenDigitRecognition
# python application.py
nohup gunicorn -b 127.0.0.1:5002 application:app > /dev/null 2>&1 &


