echo "Initiating Move"
cp * /home/server/installs/anusaaraka_controller/data/3/
ls /home/server/installs/anusaaraka_controller/data/3/4.json
#ls ~
if [ $? -eq 0 ]; then
    echo "Done"
else
    echo "Something broke"
fi
