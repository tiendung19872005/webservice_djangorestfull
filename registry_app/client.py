'''
Created on Jul 16, 2014

@author: tiendung
'''
   
# import pycurl
# import pprint
# import json
# from io import BytesIO
# ############################## get
# c = pycurl.Curl()
# data = BytesIO()
# urlheroku = 'http://rocky-everglades-6801.herokuapp.com/global_ssh/chat/'
# # url = 'http://127.0.0.1:8000/global_ssh/ssh/'
#   
# c.setopt(c.URL, urlheroku)
# c.setopt(c.WRITEFUNCTION, data.write)
# c.perform()
#   
# dictionary = json.loads(data.getvalue())
# # value = dictionary["pool"],dictionary["nat_type"],dictionary["ipaddr"],dictionary["port_ex"]
# # print(value)
# print(dictionary)


# ok
############################# post
import pycurl
# urlpost = 'http://127.0.0.1:8000/global_ssh/'
  
urlherokuppost = 'http://rocky-everglades-6801.herokuapp.com/global_ssh/'
headers = {"Accept: application/json","Content-type: application/json"}
valuepost = {"pool": "ssh", "nat_type": "FullCore", "ipaddr": "192.168.1.11", "port_ex": 12345} 
   
post_data = {'pool': 'chat', 'nat_type': 'FullCore', 'ipaddr': '192.168.1.11', 'port_ex': 12345}
try:
#     # python 3
    from urllib.parse import urlencode
except ImportError:
#     # python 2
    from urllib import urlencode
postfiles = urlencode(post_data)
cc = pycurl.Curl()
cc.setopt(cc.URL,urlherokuppost)
cc.setopt(cc.POSTFIELDS, postfiles)
cc.perform()
cc.close()

#ok
#############################################

