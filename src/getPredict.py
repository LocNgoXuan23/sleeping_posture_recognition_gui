import torch
from efficientnet_pytorch import EfficientNet
import cv2
from dataset import process, getTestLoader, IR_Dataset, processSingleImage
import numpy as np
# from engine import effi
from utils import getConfig
from sklearn.metrics import accuracy_score
from tqdm import tqdm

def predict(img, device, model):
	img = processSingleImage(img)
	imgs = torch.reshape(img, (1, img.shape[0], img.shape[1], img.shape[2]))
	imgs = imgs.to(device)
	out = model(imgs)
	# print(out)
	_, predicts = out.max(dim=1)
	return predicts[0].item()


if __name__ == '__main__':
	device = 'cuda' if torch.cuda.is_available() else 'cpu'
	cfgs = getConfig()
	model = effi().to(device)
	model.load_state_dict(torch.load('../weights/model.pth'))

	test_loader = getTestLoader(cfgs, IR_Dataset)

	model.eval()

	val_acc_epoch = []
	# with torch.no_grad():
	# 	for imgs, labels in tqdm(test_loader):
	# 		imgs = imgs.to(device)
	# 		# print(imgs)
	# 		out = model(imgs)
	# 		print(out)
	# 		# print(out)
	# 		_, predicts = out.max(dim=1)
	# 		# print(predicts)
	# 		# print(predicts.shape)
	# 		# print(labels.shape)
	# 		val_acc_epoch.append(accuracy_score(predicts.cpu().numpy(), labels.cpu().numpy()))
	# 		# break

	# print(sum(val_acc_epoch) / len(val_acc_epoch))

	for i in range(20):
		img = cv2.imread('imgs/flip_Frame1918_11.png')
		print(predict(img, device, model))
		

