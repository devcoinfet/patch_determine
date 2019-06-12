import requests
from zipfile import ZipFile
import uuid
import pyunpack
from pyunpack import Archive
import os
import subprocess
#https://twitter.com/hjy79425575
HEADER = b'7z\xBC\xAF\x27\x1C'
'''

hjy
‏ @hjy79425575

To my surprise, many people do not know how to find out which file is being updating in a patch. You just need to unzip the exe patch file and look into update.ver.
'''
#good shit thanks bro I wanted to know this u kick ass ;)
update = "http://download.windowsupdate.com/c/csa/csa/secu/2019/04/windowsxp-kb4500331-x86-custom-enu_d7206aca53552fececf72a3dee93eb2da0421188.exe"

def grab_update(update_download):
    try:
        print('Beginning file download with requests')

        download_nonce = uuid.uuid4().hex +  '.exe'
        r = requests.get(update_download)
        location = 'extracted_data/'+download_nonce
        location_binwalk_ready = 'extracted_data/_'+download_nonce+".extracted"
        with open(location, 'wb') as f:  
           f.write(r.content)

        # Retrieve HTTP meta-data
        print(r.status_code)  
        print(r.headers['content-type'])

        if "200" in str(r.status_code):
           return location,location_binwalk_ready
       
    except:
       pass


def uncab(filename_in,location_binwalk_ready):
    print(filename_in)
    results = subprocess.call(["binwalk", "-e","--directory","extracted_data", filename_in])
    
    extracted = location_binwalk_ready
    print(extracted)
    results = subprocess.call(["cabextract",extracted+"/A000.cab"])
    print(results)
    update_location = extracted +"/update/update.ver"
    print(update_location)
    with open(update_location) as f:
       lines = f.read().splitlines()
       for line in lines:
           data = line.split()
           for lines2 in data:
               if "termdd" in lines2:
                   termdd = lines2.split('=') 
                   print("File Modified: "+termdd[0])
    
    



def try_decompressing_archive(filename):
    print(filename)


location_binwalk_ready=""
download_nonce,location_binwalk_ready = grab_update(update)
if download_nonce:
   print("Update Grabbed: "+download_nonce+ " Performing Extraction")
   try:
      uncab(download_nonce,location_binwalk_ready)
   except:
       pass
