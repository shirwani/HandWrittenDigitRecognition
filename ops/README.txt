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
    # mkdir -p /root/HandWrittenDigitRecognition/datasets
    # mkdir -p /root/HandWrittenDigitRecognition/ops
    # mkdir -p /root/HandWrittenDigitRecognition/models
    # scp ./HandWrittenDigitRecognition/training.py          -> /root/HandWrittenDigitRecognition/.
    # scp ./HandWrittenDigitRecognition/testing.py           -> /root/HandWrittenDigitRecognition/.
    # scp ./HandWrittenDigitRecognition/utils.py             -> /root/HandWrittenDigitRecognition/.
    # scp ./HandWrittenDigitRecognition/requirements.txt     -> /root/HandWrittenDigitRecognition/.
    # scp ./HandWrittenDigitRecognition/datasets/mnist.npz   -> /root/HandWrittenDigitRecognition/datasets/.
    # scp ./HandWrittenDigitRecognition/datasets/train_X.npy -> /root/HandWrittenDigitRecognition/datasets/.
    # scp ./HandWrittenDigitRecognition/datasets/train_y.npy -> /root/HandWrittenDigitRecognition/datasets/.
    # scp ./HandWrittenDigitRecognition/datasets/cv_X.npy    -> /root/HandWrittenDigitRecognition/datasets/.
    # scp ./HandWrittenDigitRecognition/datasets/cv_y.npy    -> /root/HandWrittenDigitRecognition/datasets/.
    # scp ./HandWrittenDigitRecognition/config.json          -> /root/HandWrittenDigitRecognition/.
    # scp ./HandWrittenDigitRecognition/ops/deploy-model     -> /root/HandWrittenDigitRecognition/ops/.


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
    # scp ./models/* -> /var/www/flask-apps/HandWrittenDigitRecognition/models/.


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
    # mkdir -p /var/www/flask-apps/HandWrittenDigitRecognition/models
    # mkdir -p /var/www/flask-apps/HandWrittenDigitRecognition/templates
    # mkdir -p /var/www/flask-apps/HandWrittenDigitRecognition/static/js
    # mkdir -p /var/www/flask-apps/HandWrittenDigitRecognition/static/images
    # scp ./application.py                -> /var/www/flask-apps/HandWrittenDigitRecognition/.
    # scp ./utils.py                      -> /var/www/flask-apps/HandWrittenDigitRecognition/.
    # scp ./static/js/script.js           -> /var/www/flask-apps/HandWrittenDigitRecognition/static/js/.
    # scp ./templates/getUserInput.html   -> /var/www/flask-apps/HandWrittenDigitRecognition/templates/.
    # scp ./templates/showResult.html     -> /var/www/flask-apps/HandWrittenDigitRecognition/templates/.
    # scp ./requirements.txt              -> /var/www/flask-apps/HandWrittenDigitRecognition/.
    # scp ./config.json                   -> /var/www/flask-apps/HandWrittenDigitRecognition/.

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

