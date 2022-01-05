import dropbox
import os
import cv2
import datetime
import json

class Acsess_dropbox():
    def __init__(self):
        # get tolen to acsess dropbox
        config = json.load(open("dropbox_config.json", "r"))
        TOKEN = config["TOKEN"]

        # acsess to dropbox
        self.dbx = dropbox.Dropbox(TOKEN)
        self.dbx.users_get_current_account()

    def upload(self, file_path):
        """ upload file to dropbox """
        with open(file_path, "rb") as f:
            self.dbx.files_upload(f.read(), "/sango_image/" + os.path.basename(file_path))
    
    def download(self, file_path, save_path):
        """ download file in dropbox """
        #self.dropbox_path + 
        self.dbx.files_download_to_file(save_path, "/" + file_path)

class Camera():
    def __init__(self, camera_num):
        self.cap = cv2.VideoCapture(camera_num)
        if not self.cap.isOpened():
            print("カメラを認識できません")
            exit()
    
    def take_image(self, file_name):
        """ take a image and save as "file name" """
        ret, frame = self.cap.read()
        cv2.imwrite(file_name, frame)

def load_config(dbx, file_name):
    """ download config file in dropbox """
    dbx.download(save_path = os.getcwd() + "/" + file_name, file_path = "config/" + file_name)
    # load configure (shooting interval and image encoding in)
    return json.load(open(file_name, "r"))

if __name__ == "__main__":

    # set dropbox conf
    dbx = Acsess_dropbox()

    # set camera conf
    config = load_config(dbx, file_name="config.json")

    # configure the camera 0
    cap = Camera(0)

    # set save directory(save in local)
    dir_path = "sango/remote_ovseration"
    os.makedirs(dir_path, exist_ok=True)
    base_path = os.path.join(dir_path)

    print("これから{}秒ごとに撮影を行います".format(config["shooting interval"]))
    print("撮影された画像は https://www.dropbox.com/--各自のdropboxの保存先リンク-- で確認できます")
    print('終了させたい場合は "ctul" キーを押しながら "c" を入力してください')

    # set start time
    
    image_previous_time = datetime.datetime.now()
    config_previous_time = datetime.datetime.now()

    while True:
        # if push q key, program is stopped
        if cv2.waitKey(3) & 0xFF == ord('q'):
            break

        image_now_time = datetime.datetime.now()
        config_now_time = datetime.datetime.now()
        # take a image every "shooting interval" secounds
        
        if ((image_now_time - image_previous_time).seconds // int(config["shooting interval"])) >= 1:
            file_name = '{}/{}.{}'.format(base_path, datetime.datetime.now().strftime('%Y%m%d%H%M%S%f'), config["image encoding"])
            try:
                cap.take_image(file_name)
                dbx.upload(file_name)
            except:
                # dropboxへの再接続
                print("再接続します")
                dbx = Acsess_dropbox()
                print("再接続できました")

            image_previous_time = image_now_time
        
        # update camera conf(every 3 minutes)
        if ((config_now_time - config_previous_time).seconds // 180) >= 1:
            try:
                config = load_config(dbx, file_name="config.json")
            except:
                # dropboxへの再接続
                print("再接続します")
                dbx = Acsess_dropbox()
                print("再接続できました")
            config_previous_time = config_now_time
