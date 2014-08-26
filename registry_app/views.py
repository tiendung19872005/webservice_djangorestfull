from django.shortcuts import render
from registry_app.models import User_ssh
from registry_app.serializers import UserSshRegisSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

listrequest = []

@api_view(['GET','POST'])
def user_list(request, format=None):
	global listrequest
	listrequest.append(request)
	if request.method == 'GET':
		user = User_ssh.objects.all()
# 		user = User_ssh.objects.filter(pool = 'ssh')
		serializer = UserSshRegisSerializer(user, many=True)
		return Response(serializer.data)
	elif request.method == 'POST':
		serializer = UserSshRegisSerializer(data = request.DATA)
		print ('POST')
		if serializer.is_valid():
			serializer.save()
			return  Response(serializer.data, status=status.HTTP_201_CREATED)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
	print('list request --------------')
	for i in listrequest: print(str(i))
	

@api_view(['GET','PUT','DELETE'])
def user_detail(request,pool,format=None):
	global listrequest
	listrequest.append(request)
	print('list request --------------')
	for i in listrequest: print(str(i))
	try:
		user = User_ssh.objects.filter(pool = pool)
	except User_ssh.DoesNotExist:
		return Response(status=status.HTTP_404_NOT_FOUND)
	if request.method == 'GET':
		serializer = UserSshRegisSerializer(user)
		return Response(serializer.data)
	elif request.method == 'PUT':
		serializer = UserSshRegisSerializer(user, date=request.DATA)
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
	elif request.method=='DELETE':
	
		user.delete()
		return Response(status=status.HTTP_204_NO_CONTENT)


'''
post
 
curl -H "Accept: application/json" -H "Content-type: application/json" -X POST http://127.0.0.1:8000/global_ssh/ -d '{"pool":"ssh","nat_type":"FullCore","ipaddr":"192.168.1.10","port_ex":12345}'
{"pool": "ssh", "nat_type": "FullCore", "ipaddr": "192.168.1.10", "port_ex": 12345}


get 

curl http://127.0.0.1:8000/global_ssh/ssh/

delete
	curl -i -H "Accept: application/json" -X DELETE http://192.168.0.165/persons/person/1  
	
	http://blogs.plexibus.com/2009/01/15/rest-esting-with-curl/
	http://www.angryobjects.com/2011/10/15/http-with-python-pycurl-by-example/
	
	http://blog.kevinastone.com/getting-started-with-django-rest-framework-and-angularjs.html
	http://stackoverflow.com/questions/22799648/convert-curl-example-to-pycurl
	http://isbullsh.it/2012/06/Rest-api-in-python/ 
'''

