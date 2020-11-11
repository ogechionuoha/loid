from __future__ import print_function
import csv, multiprocessing, cv2, os
import numpy as np
import urllib.request

class AppURLopener(urllib.request.FancyURLopener):
    version = "Mozilla/5.0"

opener = AppURLopener()
def url_to_image(url):
    resp = opener.open(url)
    image = np.asarray(bytearray(resp.read()), dtype="uint8")
    image = cv2.imdecode(image, cv2.IMREAD_UNCHANGED)
    return image


def download_image(im_url,location):
    im_url = im_url.strip('/')
    try:
        save_dir = os.path.join('./images/train/',location)
        if not os.path.exists(save_dir):
            os.makedirs(save_dir)

        save_path = os.path.join(save_dir,im_url.split('/')[-1])
        line = ",".join([im_url.strip(), location])
        if not os.path.isfile(save_path):
            img = url_to_image(im_url)
            cv2.imwrite(save_path,img)
            with open("./log/good.txt", "a") as good:
                good.write(line)
                good.write("\n")
        else:
            with open("./log/duplicate.txt", "a") as duplicate:
                duplicate.write(line)
                duplicate.write("\n")
            
    except:
        with open("./log/bad.txt", "a") as bad:
            bad.write(line)
            bad.write("\n")

def main():
    notuk_f = open('./data/url_csvs_500k/not_uk/not_uk.csv','r')
    notuk_reader = csv.reader(notuk_f)

    notukpool = multiprocessing.Pool(processes=2*multiprocessing.cpu_count())
    notukresults = [notukpool.apply_async(download_image, [info[0], 'not_uk'] ) for info in notuk_reader]
    notukpool.close()
    notukpool.join()

    uk_f = open('./data/url_csvs_500k/uk/uk.csv','r')
    uk_reader = csv.reader(uk_f)

    ukpool = multiprocessing.Pool(processes=2*multiprocessing.cpu_count())
    ukresults = [ukpool.apply_async(download_image, [info[0], 'uk'] ) for info in uk_reader]
    ukpool.close()
    ukpool.join()

    

if __name__ == '__main__':
    main()