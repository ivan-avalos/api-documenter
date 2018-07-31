cd htmldom-2.0
sudo python3 setup.py install
cd ..
chmod +x apidoc.py
echo Creating symbolic link of $(pwd)/apidoc.py
sudo ln -s $(pwd)/apidoc.py /usr/local/bin/apidoc
