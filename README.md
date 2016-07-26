    sudo apt-get install python-pip python-opencv python-virtualenv
    mkdir ~/venv
    cd ~/venv
    virtualenv --system-site-packages cammie
    source cammie/bin/activate
    cd ~/projects/cammie
    pip install -r requirements.txt

