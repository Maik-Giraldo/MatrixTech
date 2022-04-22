import dropbox
from PIL import Image
from io import BytesIO
import string, random
import base64
import os


class UploadDropbox:
    def __init__(self):
        self.oauth2_refresh_token = 'zC2eiWgNVpUAAAAAAAAAAfXgfpGQTQksaNLpbYIPFrhvIDxKXOWOBj8tI2aY2BPu'
        self.app_key = '5u8ktcuugtxwss5'
        self.app_secret = 'ys24g3nbq80zs4c'

    def __fixB64(self, img):
        try:
            if "data:image/jpeg;base64," in img:
                imgFix = img.replace("data:image/jpeg;base64,", "")
                return imgFix
            elif "data:image/png;base64," in img:
                imgFix = img.replace("data:image/png;base64,", "")
                return imgFix
            else:
                return None
        except Exception as e:
            print("FIXIMGB64:")
            return None


    def __createImg(self, img):
        try:
            route = 'assets/img/'
            rnd = ''.join(random.choice(
                f"{string.ascii_uppercase}")for i in range(20))
            nameImg = rnd + ".jpg"
            im = Image.open(BytesIO(base64.b64decode(img)))
            im.save("{}".format(route + nameImg), "jpeg", quality=100)
            return nameImg
        except Exception as e:
            print(e)
            return None


    def __saveFileCloudDpBx(self, nameImg):
        try:
            con = dropbox.Dropbox(app_key = self.app_key, app_secret = self.app_secret, oauth2_refresh_token = self.oauth2_refresh_token)
            result = ""
            with open('assets/img/' + nameImg, "rb") as f:
                result = con.files_upload(f.read(), '/ComApp/Qrcode/' + nameImg)

            os.remove('assets/img/' + nameImg)

            link = con.sharing_create_shared_link(
                path='/ComApp/Qrcode/' + nameImg, short_url=False
            )

            ImageFinal = link.url.replace("?dl=0", "?dl=1")

            return ImageFinal

        except Exception as e:
            print(e)
            return None


    def saveImage(self, imgB64):
        try:
            img = self.__fixB64(imgB64)

            if img:
                nameImg = self.__createImg(img)
                if nameImg:
                    url = self.__saveFileCloudDpBx(nameImg)
                    if url:
                        return url
            return None

        except Exception as e:
            print(e)
            return None