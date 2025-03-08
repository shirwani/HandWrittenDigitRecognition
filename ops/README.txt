###################################################################
# PREREQ ON ALL SYSTEMS
#   Install python 3.12 if it's not already installed on the server
#   Make sure python3 is aliased to python 3.12
###################################################################

#####################################################
# SETTING UP THE LOCAL DEV MACHINE TO RUN THE SCRIPTS
#####################################################
    cd HandWrittenDigitRecognition
    mkdir -p ./models
    which python3 # -> shoud point to python 3.12 on the system
    python3 -m venv venv
    alias python="venv/bin/python3.12"
    alias pip="venv/bin/pip3.12"
    source venv/bin/activate
    pip install --upgrade pip
    pip install -r requirements.txt

######################################################
# COPYING TRAINING FILES FROM LOCAL -> TRAINING SERVER
######################################################
    ssh root@[ TRAINING SERVER ] 'mkdir -p /root/HandWrittenDigitRecognition/datasets'
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

    ###############################
    # APPLICATION ENVIRONMENT SETUP
    ###############################
    cd ~/HandWrittenDigitRecognition
    apt update
    apt install python3.12-venv
    which python3 # -> shoud point to python 3.12 on the system
    python3 -m venv venv
    alias python="venv/bin/python3.12"
    alias pip="venv/bin/pip3.12"
    source venv/bin/activate
    pip install --upgrade pip
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

    ###############################
    # APPLICATION ENVIRONMENT SETUP
    ###############################
    cd /var/www/flask-apps/HandWrittenDigitRecognition
    apt update
    apt install python3.12-venv
    which python3 # -> shoud point to python 3.12 on the system
    python3 -m venv venv
    alias python="venv/bin/python3.12"
    alias pip="venv/bin/pip3.12"
    source venv/bin/activate
    pip install --upgrade pip
    pip install -r requirements.txt
    pip install gunicorn

    ##########################
    # APPLICATION SERVER SETUP
    ##########################
    # Update /etc/nginx/sites-available/sites on the application server
    sudo ln -s /etc/nginx/sites-available/sites /etc/nginx/sites-enabled
    sudo service nginx restart

#######################################################
# RUNNING TRAINING & APPLICATION LOCALLY ON DEV MACHINE
#######################################################
    python training.py --dev
    python application.py --dev

    ########################################
    # TO COPY MODEL FROM THE TRAINING SERVER
    ########################################
    scp root@[ TRAINING SERVER ]:/root/HandWrittenDigitRecognition/models/*.keras ./models/.

#########################################
# RUNNING TRAINING ON THE TRAINING SERVER
#########################################
    pkill -f HandWrittenDigitRecognition
    nohup python training.py > /dev/null 2>&1 &

    ############################################################################
    # DEPLOYING THE TRAINED MODEL FROM THE TRAINING SERVER -> APPLICATION SERVER
    ############################################################################
    cd ~/HandWrittenDigitRecognition
    scp ./models/* root@[ APPLICATION SERVER ]:/var/www/flask-apps/HandWrittenDigitRecognition/models/.

###################################################
# RUNNING THE APPLICATION ON THE APPLICATION SERVER
###################################################
    cd /var/www/flask-apps/HandWrittenDigitRecognition
    pkill -f HandWrittenDigitRecognition

    #################################
    # To use model from ./config.json
    #################################
    nohup gunicorn -b 127.0.0.1:5002 application:app > /dev/null 2>&1 &

    ##########################################
    # To use model specified from command line
    ##########################################
    # MODEL="m_20250307023936.keras" nohup gunicorn -b 127.0.0.1:5002 application:app > /dev/null 2>&1 &

