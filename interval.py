import subprocess
import os
import json

from acsess_dropbox import Acsess_dropbox

def load_config(dbx, file_name):
    """ download config file in dropbox """
    dbx.download(save_path = os.getcwd() + "/" + file_name, file_path = "config/" + file_name)
    # load configure (shooting interval and image encoding in)
    return json.load(open(file_name, "r"))

if __name__ == "__main__":

    config = load_config(Acsess_dropbox(), file_name="config.json")
    interval = int(config["shooting interval"])

    #del_cmd = "sudo -E sed -e '$d' /tmp/crontab.8yZpMT/crontab"
    crontab_cmd = "'{} * * * * sudo -E python3 ~/sango/image_capture.py' ".format("*/" + str(interval))
    set_cmd = "sudo -E echo " + crontab_cmd + ">> /var/spool/cron/crontab"
    del_cmd = "sudo -E sed -i -e '$d' /var/spool/cron/crontab"

    subprocess.call(del_cmd, shell=True)
    subprocess.call(set_cmd, shell=True)
    

    
