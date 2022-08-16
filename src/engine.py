from utils import readJson, addData, getClassName, writeJson
import cv2
import time
from efficientnet_pytorch import EfficientNet
import torch
from getPredict import predict

def effi():
	model = EfficientNet.from_pretrained('efficientnet-b0', num_classes=23)
	return model

device = 'cuda' if torch.cuda.is_available() else 'cpu'
model = effi().to(device)
model.load_state_dict(torch.load('../weights/model.pth'))
model.eval()

def showCamera(path):
	# for i in range(20):
	# 	img = cv2.imread('imgs/flip_Frame1918_11.png')
	# 	print(predict(img, device, model))

	cap = cv2.VideoCapture(path)
	while True:
		success, img = cap.read()
		c = predict(img, device, model)
		c_name = getClassName(c)
		print(c_name)
		img = cv2.resize(img, (800, 600))
		img = cv2.putText(img, c_name, (50, 50), cv2.FONT_HERSHEY_SIMPLEX,
				1, (255, 255, 255), 2, cv2.LINE_AA)
		cv2.imshow('video', img)

		time.sleep(1)

		if cv2.waitKey(1) & 0xFF == ord('q'):
			break

	cap.release()
	cv2.destroyAllWindows()

def changePassword(email, oldPassword, newPassword, confirmPassword):
	print(email, oldPassword, newPassword, confirmPassword)
	if email == '' or oldPassword == '' or newPassword == '' or confirmPassword == '':
		print("Vui long nhap day du thong tin")
		return -1
	
	userData = readJson()
	key = email

	# check email exist
	if key not in userData:
		print("Ko ton tai email !!")
		return -2
	
	if userData[key].split("/")[2] != oldPassword:
		print("Sai current password")
		return -3
	
	if newPassword != confirmPassword:
		print("Sai Confirm Password!!")
		return -4
	
	userData[key] = f'{userData[key].split("/")[0]}/{userData[key].split("/")[1]}/{newPassword}'
	writeJson(userData)
	print("Change password Successfully !!")
	return 1



def addPatientData(name, cameraID):
	print(name, cameraID)
	if name == '' or cameraID == '':
		print("Vui long nhap thong tin")
		return -1

	patientData = readJson('patientData.json')

	if name in patientData:
		print("Da co ten benh nhan nay trong du lieu")
		return -2
	
	patient = {name: cameraID}
	addData(patient, 'patientData.json')
	print("Add patient thanh cong !!")

	return 1

def loginUser(email, password):
	print(email, password)
	# check empty value 
	if email == '' or password == '':
		print("Vui long nhap day du thong tin")
		return -1, None

	userData = readJson()
	key = email

	# check email exist
	if key not in userData:
		print("Ko ton tai email !!")
		return -2, None
	
	if userData[key].split("/")[2] == password:
		print("Login thanh cong")
		return 1, [userData[key].split("/")[0], userData[key].split("/")[1], email]
	else:
		print("Sai Password !!")
		return -3, None

def registerUser(name, email, password):
	print(name, email, password)
	# check empty value
	if name == '' or email == '' or password == '':
		print("Vui long nhap day du thong tin")
		return -2

	userData = readJson('userData.json')
	key = email

	# Check Exist Email
	if key in userData:
		print("Da ton tai")
		return -1

	# check Role
	role = None
	if len(userData) == 0:
		role = 'doctor'
	else:
		role = 'nurse'
	
	# Add
	value = f'{role}/{name}/{password}'
	user = {key: value}
	addData(user, 'userData.json')
	print("Dang Ky thanh cong!!")

	if role == 'nurse':
		addData({name: ''}, 'nurseData.json')

	return 1

if __name__ == '__main__':
	showCamera("video.mp4")
	print(123)
	for i in range(100):
		print(i)