cd ~
mkdir impactlab
cd impactlab
git clone https://github.com/yesdelft/SPOT.git
git clone https://github.com/boston-dynamics/spot-sdk.git
sudo add-apt-repository ppa:deadsnakes/ppa
sudo apt update
sudo apt install software-properties-common
sudo apt install python3.7
sudo update-alternatives --config python
sudo update-alternatives --install /usr/bin/python python /usr/bin/python3.7 1
python -m pip install -r spot-sdk/python/examples/estop/requirements.txt
python -m pip install -r spot-sdk/python/examples/wasd/requirements.txt
python -m pip install -r spot-sdk/python/examples/spot_tensorflow_detector/requirements.txt
python -m pip install -r spot-sdk/python/examples/spot_detect_and_follow/requirements.txt
python -m pip install -r spot-sdk/python/examples/get_image/requirements.txt
cd SPOT
git checkout python
python -m pip install -r ui/requirements.txt
python -m pip install -r blindpath/requirements.txt
python -m pip install -r human_count/requirements.txt
cd ~/impactlab
