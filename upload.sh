rm -r /Users/2017-A/Dropbox/web_dev/modelcraft/data
mkdir /Users/2017-A/Dropbox/web_dev/modelcraft/data
rsync -r -v /Users/2017-A/Dropbox/web_dev/modelcraft root@167.99.7.144:/Users/2017-A/Dropbox/web_dev
ssh root@167.99.7.144 'killall screen'
ssh root@167.99.7.144 'screen -dm python /Users/2017-A/Dropbox/web_dev/modelcraft/server_main.py'
