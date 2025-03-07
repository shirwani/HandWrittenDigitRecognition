######################################################
# COPYING TRAINING FILES FROM LOCAL -> TRAINING SERVER
######################################################
    ssh root@[ TRAINING SERVER ] 'mkdir -p /root/HandWrittenDigitRecognition/datasets'
    ssh root@[ TRAINING SERVER ] 'mkdir -p /root/HandWrittenDigitRecognition/ops'
    ssh root@[ TRAINING SERVER ] 'mkdir -p /root/HandWrittenDigitRecognition/models'
    scp ./training.py          root@[ TRAINING SERVER ]:/root/HandWrittenDigitRecognition/.
    scp ./testing.py           root@[ TRAINING SERVER ]:/root/HandWrittenDigitRecognition/.
    scp ./utils.py             root@[ TRAINING SERVER ]:/root/HandWrittenDigitRecognition/.
    scp ./requirements.txt     root@[ TRAINING SERVER ]:/root/HandWrittenDigitRecognition/.
    scp ./datasets/train_X.npy root@[ TRAINING SERVER ]:/root/HandWrittenDigitRecognition/datasets/.
    scp ./datasets/train_y.npy root@[ TRAINING SERVER ]:/root/HandWrittenDigitRecognition/datasets/.
    scp ./datasets/cv_X.npy    root@[ TRAINING SERVER ]:/root/HandWrittenDigitRecognition/datasets/.
    scp ./datasets/cv_y.npy    root@[ TRAINING SERVER ]:/root/HandWrittenDigitRecognition/datasets/.
    scp ./config.json          root@[ TRAINING SERVER ]:/root/HandWrittenDigitRecognition/.

#########################################
# RUNNING TRAINING ON THE TRAINING SERVER
#########################################
    # Prereq: Install python 3.12 if it's not already installed on the server
    cd ~/HandWrittenDigitRecognition
    python3 -m venv venv
    alias python="./venv/bin/python3.12"
    alias pip="./venv/bin/pip3.12"
    source venv/bin/activate
    pip install --upgrade pip
    pip install -r requirements.txt
    python training.py

############################################################################
# DEPLOYING THE TRAINED MODEL FROM THE TRAINING SERVER -> APPLICATION SERVER
############################################################################
    cd ~/HandWrittenDigitRecognition
    scp ./models/* root@[ APPLICATION SERVER ]:/var/www/flask-apps/HandWrittenDigitRecognition/models/.

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
    ssh root@[ APPLICATION SERVER ] 'mkdir -p /var/www/flask-apps/HandWrittenDigitRecognition/models'
    ssh root@[ APPLICATION SERVER ] 'mkdir -p /var/www/flask-apps/HandWrittenDigitRecognition/templates'
    ssh root@[ APPLICATION SERVER ] 'mkdir -p /var/www/flask-apps/HandWrittenDigitRecognition/static/js'
    ssh root@[ APPLICATION SERVER ] 'mkdir -p /var/www/flask-apps/HandWrittenDigitRecognition/static/images'
    scp ./application.py                root@[ APPLICATION SERVER ]:/var/www/flask-apps/HandWrittenDigitRecognition/.
    scp ./utils.py                      root@[ APPLICATION SERVER ]:/var/www/flask-apps/HandWrittenDigitRecognition/.
    scp ./static/js/script.js           root@[ APPLICATION SERVER ]:/var/www/flask-apps/HandWrittenDigitRecognition/static/js/.
    scp ./templates/getUserInput.html   root@[ APPLICATION SERVER ]:/var/www/flask-apps/HandWrittenDigitRecognition/templates/.
    scp ./templates/showResult.html     root@[ APPLICATION SERVER ]:/var/www/flask-apps/HandWrittenDigitRecognition/templates/.
    scp ./requirements.txt              root@[ APPLICATION SERVER ]:/var/www/flask-apps/HandWrittenDigitRecognition/.
    scp ./config.json                   root@[ APPLICATION SERVER ]:/var/www/flask-apps/HandWrittenDigitRecognition/.

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
    MODEL="m_20250307023936.keras" nohup gunicorn -b 127.0.0.1:5002 application:app > /dev/null 2>&1 &

###############################################################
# DOWNLOADING MODEL FROM TRAINING SERVER LOCALLY TO DEV MACHINE
# RUNNING APP LOCALLY USING MODEL GENERATED ON TRAINING SERVER
###############################################################
    cd ~/HandWrittenDigitRecognition
    mkdir -p ./models
    mkdir -p ./static/images
    scp root@[ TRAINING SERVER ]:/root/HandWrittenDigitRecognition/models/m_20250307023936.keras ./models/.
    python3 -m venv venv
    source venv/bin/activate
    python application.py
