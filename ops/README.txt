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
./ops/copy-files-to-training-server
    # ssh root@<TRAINING_SERVER> 'mkdir -p /root/HandWrittenDigitRecognition/datasets'
    # ssh root@<TRAINING_SERVER> 'mkdir -p /root/HandWrittenDigitRecognition/ops'
    # ssh root@<TRAINING_SERVER> 'mkdir -p /root/HandWrittenDigitRecognition/models'
    # scp ./training.py          root@<TRAINING_SERVER>:/root/HandWrittenDigitRecognition/.
    # scp ./testing.py           root@<TRAINING_SERVER>:/root/.
    # scp ./utils.py             root@<TRAINING_SERVER>:/root/.
    # scp ./requirements.txt     root@<TRAINING_SERVER>:/root/HandWrittenDigitRecognition/.
    # scp ./datasets/mnist.npz   root@<TRAINING_SERVER>:/root/HandWrittenDigitRecognition/datasets/.
    # scp ./datasets/train_X.npy root@<TRAINING_SERVER>:/root/HandWrittenDigitRecognition/datasets/.
    # scp ./datasets/train_y.npy root@<TRAINING_SERVER>:/root/HandWrittenDigitRecognition/datasets/.
    # scp ./datasets/cv_X.npy    root@<TRAINING_SERVER>:/root/HandWrittenDigitRecognition/datasets/.
    # scp ./datasets/cv_y.npy    root@<TRAINING_SERVER>:/root/HandWrittenDigitRecognition/datasets/.
    # scp ./config.json          root@<TRAINING_SERVER>:/root/HandWrittenDigitRecognition/.
    # scp ./ops/deploy-model     root@<TRAINING_SERVER>:/root/HandWrittenDigitRecognition/ops/.


#########################################
# RUNNING TRAINING ON THE TRAINING SERVER
#########################################
source venv/bin/activate
python training.py

############################################################################
# DEPLOYING THE TRAINED MODEL FROM THE TRAINING SERVER -> APPLICATION SERVER
############################################################################
cd ~/HandWrittenDigitRecognition
./ops/copy-models-to-app-server
    # scp ./models/* root@<APPLICATION_SERVER>:/var/www/flask-apps/HandWrittenDigitRecognition/models/.


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

################################################
# COPYING FILES FROM LOCAL -> APPLICATION SERVER
################################################
./ops/copy-files-to-app-server
    # ssh root@<APPLICATION_SERVER> 'mkdir -p /var/www/flask-apps/HandWrittenDigitRecognition/models'
    # ssh root@<APPLICATION_SERVER> 'mkdir -p /var/www/flask-apps/HandWrittenDigitRecognition/templates'
    # ssh root@<APPLICATION_SERVER> 'mkdir -p /var/www/flask-apps/HandWrittenDigitRecognition/static/js'
    # ssh root@<APPLICATION_SERVER> 'mkdir -p /var/www/flask-apps/HandWrittenDigitRecognition/static/images'
    # scp ./application.py                root@<APPLICATION_SERVER>:/var/www/flask-apps/HandWrittenDigitRecognition/.
    # scp ./utils.py                      root@<APPLICATION_SERVER>:/var/www/flask-apps/HandWrittenDigitRecognition/.
    # scp ./static/js/script.js           root@<APPLICATION_SERVER>:/var/www/flask-apps/HandWrittenDigitRecognition/static/js/.
    # scp ./templates/getUserInput.html   root@<APPLICATION_SERVER>:/var/www/flask-apps/HandWrittenDigitRecognition/templates/.
    # scp ./templates/showResult.html     root@<APPLICATION_SERVER>:/var/www/flask-apps/HandWrittenDigitRecognition/templates/.
    # scp ./requirements.txt              root@<APPLICATION_SERVER>:/var/www/flask-apps/HandWrittenDigitRecognition/.
    # scp ./config.json                   root@<APPLICATION_SERVER>:/var/www/flask-apps/HandWrittenDigitRecognition/.

###################################################
# RUNNING THE APPLICATION ON THE APPLICATION SERVER
###################################################
cd /var/www/flask-apps/HandWrittenDigitRecognition
python3 -m venv venv
source venv/bin/activate
pkill -f HandWrittenDigitRecognition
# python application.py

# Get model name from config.json
# nohup gunicorn -b 127.0.0.1:5002 application:app > /dev/null 2>&1 &

# Get model name from environment variable
MODEL="m_20250304205801.keras" nohup gunicorn -b 127.0.0.1:5002 application:app > /dev/null 2>&1 &

