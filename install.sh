#!/bin/bash

# Instalación de cfabots

home_dir=$(pwd)
install_dir=/opt/sispi  # testbed


ln -s -T ${home_dir}/publicar.py ${install_dir}/publicar.py
ln -s -T ${home_dir}/TelBot.py ${install_dir}/TelBot.py
ln -s -T ${home_dir}/TwittBot.py ${install_dir}/TwittBot.py
ln -s -T ${home_dir}/CFABot.py ${install_dir}/CFABot.py
ln -s -T ${home_dir}/FaceBot.py ${install_dir}/FaceBot.py
ln -s -T ${home_dir}/scripts/imgconvert.py ${install_dir}/scripts/imgconvert.py

