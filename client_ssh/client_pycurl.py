'''
Created on Jul 18, 2014

@author: tiendung
'''

import pycurl
# urlpost = 'http://127.0.0.1:8000/global_ssh/'
  
def userSshPost(urlherokuppost,post_data):
#     urlherokuppost = 'http://rocky-everglades-6801.herokuapp.com/global_ssh/'
    headers = {"Accept: application/json","Content-type: application/json"}
#     valuepost = {"pool": "ssh", "nat_type": "FullCore", "ipaddr": "192.168.1.11", "port_ex": 12345} 
       
#     post_data = {'pool': 'chat', 'nat_type': 'FullCore', 'ipaddr': '192.168.1.11', 'port_ex': 12345}
    try:
    #     # python 3
        from urllib.parse import urlencode
    except ImportError:
    #     # python 2
        from urllib import urlencode
    postfiles = urlencode(post_data)
    c = pycurl.Curl()
    c.setopt(c.URL,urlherokuppost)
    c.setopt(c.POSTFIELDS, postfiles)
    c.perform()
    c.close()
    '''
    bat loi ngay tai day, neu post thanh cong thi thoi,
     neu khong thanh cong thi return ve mot cai loi nao do (  t
     rong view tren server, thi status tra ve 400
     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
      
    return
    '''
    return

def userSshDelete(urlherokudelete):
    c = pycurl.Curl()
#     urlherokudelete = 'http://rocky-everglades-6801.herokuapp.com/global_ssh/chat/'
    c.setopt(pycurl.URL, urlherokudelete)
    c.setopt(pycurl.CUSTOMREQUEST,"DELETE")
    c.perform()
    '''
    bat loi o day, neu delete duoc hay khong
    '''
    return

# 
# def main(urlherokuppost,post_data):
#     userSshPost(urlherokuppost, post_data)
# 
# #ok
# #############################################
# 
# if __name__ == '__main__':
#     main()