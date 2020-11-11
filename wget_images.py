from __future__ import print_function
import csv, multiprocessing, os
import numpy as np
import requests
import shutil

def download_image(im_url,location):
    im_url = im_url.strip('/')
    try:
        save_dir = os.path.join('./images/train/',location)

        save_path = os.path.join(save_dir,im_url.split('/')[-1])
        
        line = ",".join([im_url.strip('/').strip(), location])
        if not os.path.isfile(save_path):
            # Open a local file with wb ( write binary ) permission.
            with open(save_path, 'wb') as local_file:
                resp = requests.get(im_url, stream=True)
                resp.raw.decode_content = True
                # Copy the response stream raw data to local image file.
                shutil.copyfileobj(resp.raw, local_file)
                # Remove the image url response object.
                del resp
            with open("./log/good.txt", "a") as good:
                #print('good')
                good.write(line)
                good.write("\n")
        else:
            with open("./log/duplicate.txt", "a") as duplicate:
                #print('duplicate')
                duplicate.write(line)
                duplicate.write("\n")
            
    except Exception as e:
        #print('EXCEPTION!!!!!!!')
        #print(save_path)
        #print(im_url)
        #print(e)
        with open("./log/bad.txt", "a") as bad:
            bad.write(line)
            bad.write("\n")

def main():
    uk_f = open('./data/url_csvs_500k/uk/uk.csv','r')
    notuk_f = open('./data/url_csvs_500k/not_uk/not_uk.csv','r')
    
    uk_reader = csv.reader(uk_f)
    notuk_reader = csv.reader(notuk_f)

    ukpool = multiprocessing.Pool(processes=2*multiprocessing.cpu_count())
    ukresults = [ukpool.apply_async(download_image, [info[0], 'uk'] ) for info in uk_reader]
    ukpool.close()
    ukpool.join()

    notukpool = multiprocessing.Pool(processes=2*multiprocessing.cpu_count())
    notukresults = [notukpool.apply_async(download_image, [info[0], 'not_uk'] ) for info in notuk_reader]
    notukpool.close()
    notukpool.join()

if __name__ == '__main__':
    main()