# a = int(input("input : "))
# for x in range(a,0,-1):
#     for y in range(0,x):
#         if y%2 == 0:
#             print("*",end=" ")
#         else:
#             print("#",end=" ")
#     print("\n")



    
# importing required libraries
import requests, json

# enter your api key here
api_key ='Your_api_key'

# Take source as input
source = input("enter your starting point =")

# Take destination as input
dest = input("enter your destination point =")

# url variable store url
url ='https://maps.googleapis.com/maps/api/distancematrix/json?'

# Get method of requests module
# return response objecttha
r = requests.get(url + 'origins = ' + source +
				'&destinations = ' + dest +
				'&key = ' + api_key)
					
# json method of response object
# return json format result
x = r.json()

# by default driving mode considered

# print the value of x
print(x)




