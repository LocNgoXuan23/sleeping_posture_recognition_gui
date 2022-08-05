import torch
from torch.utils.data import Dataset, DataLoader
import cv2
import random
from torchvision import  transforms
from utils import readJson

class IR_Dataset(Dataset):
    def __init__(self, cfgs, mode = 'train'):
        self.cfgs = cfgs
        self.mode = mode
        self.data_path = cfgs['data'][mode+'_path']
        self.data = readJson(self.data_path)

    def __getitem__(self, item):
        image_path = self.data[item]
        
        img, label = process(image_path, self.cfgs)
        return img, label

    def __len__(self):
        return len(self.data)

def get_label(path):
    lookup = {str(k): k for k in range(1,24)}
    try:
        return lookup[path.split('/')[-2]] - 1
    except:
        return None

def transform(image):
	return transforms.Compose(
		[transforms.ToTensor(),
		transforms.Normalize((0.5), (0.5,)),
		transforms.RandomRotation(10),
		transforms.RandomAutocontrast(p=0.2),]
	)(image)

def process(image_path, cfgs):
    label = get_label(image_path)
    img = cv2.imread(image_path)#, cv2.IMREAD_GRAYSCALE)
    # thres = random.choice(list(range(0,15)))
    thres = 10
    img[img < thres] = 0# cfgs['data']['pix_thres']] = 0 
    # img = cv2.equalizeHist(img)
    img = cv2.resize(img, (224, 224)) #cfgs['data']['image_size'])
    img = transform(img)
    label = torch.LongTensor([int(label)])
    return img, label

def processSingleImage(img):
    # img = cv2.imread(image_path)
    thres = 10
    img[img < thres] = 0
    img = cv2.resize(img, (224, 224)) #cfgs['data']['image_size'])
    img = transform(img)
    return img


def getTestLoader(cfgs, dataset_type):
	test_dataset = dataset_type(cfgs,'test')

	test_loader = DataLoader(
			dataset = test_dataset,
			batch_size = 1,
			num_workers = cfgs['data']['num_workers']
	)
	print("DONE LOADING TEST DATA !")
	return test_loader


if __name__ == '__main__':
	img = cv2.imread('imgs/flip_Frame142_10.png')
	img = process(img)

	print(img.shape)

