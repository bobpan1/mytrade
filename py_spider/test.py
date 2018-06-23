#coding:utf-8
import urllib, base64
from aip import AipOcr

#APP_ID = '7087275';
#API_KEY = 'PXg3EbbgGAqXLICYAB4zKW8N';
#SECRET_KEY = 'P6XZ5Tg2NtONSZOG53UNm5agFC3LirYe';    		
				
				
#APP_ID = '11260487';
#API_KEY = 'Aw8GaNW6Rit9rdW6evSkYp8Q';
#SECRET_KEY = 'qNtDfqUpK9c2NzHZibWDmCh9sC2FjRMb';  
				
APP_ID = '11260487'
API_KEY = 'Aw8GaNW6Rit9rdW6evSkYp8Q'
SECRET_KEY = 'qNtDfqUpK9c2NzHZibWDmCh9sC2FjRMb'

client = AipOcr(APP_ID, API_KEY, SECRET_KEY)

def get_file_content(filePath):
    with open(filePath, 'rb') as fp:
        return fp.read()

options = {}
options["recognize_granularity"] = "big"
options["probability"] = "true"
options["accuracy"] = "normal"
options["detect_direction"] = "true"

image = get_file_content('/tmp/invoice.jpeg')

result = client.receipt(image, options)

print(result)