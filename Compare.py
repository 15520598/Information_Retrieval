import os
import sys

def getListTaiLieuTraVe(Path):
	listTaiLieuTraVe = {}
	for fileName in os.listdir(Path):		
		filePath = os.path.join(os.getcwd(), Path, fileName)
		idQuery = os.path.basename(filePath)[:-4]
		listDocument = []
		with open(filePath) as f:
			listDocument = []
			for string in f:
				listDocument.append(int(string))
		listTaiLieuTraVe[idQuery] = listDocument
	return listTaiLieuTraVe

def getListTaiLieuLienQuan(Path):
	listTaiLieuLienQuan = {}
	for fileName in os.listdir(Path):		
		filePath = os.path.join(os.getcwd(), Path, fileName)
		idQuery = os.path.basename(filePath)[:-4]
		listDocument = []
		with open(filePath) as f:
			listDocument = []
			for string in f:
				string = string.split()[1]
				listDocument.append(int(string))
		listTaiLieuLienQuan[idQuery] = listDocument
	return listTaiLieuLienQuan

def Compare(listTaiLieuTraVe, listTaiLieuLienQuan):
	dictTrungKhop = {}
	dictDoPhu = {}
	dictDoChinhXac = {}
	avgDoPhu = 0
	avgDoChinhXac = 0
	for key in listTaiLieuLienQuan.keys():
		temp = [value for value in listTaiLieuTraVe[key] if value in listTaiLieuLienQuan[key]]
		DoPhu = len(temp)/len(listTaiLieuLienQuan[key])		# Độ phủ
		DoChinhXac = len(temp)/len(listTaiLieuTraVe[key])	# Độ chính xác
		dictTrungKhop[key] = temp
		dictDoPhu[key] = DoPhu
		avgDoPhu += DoPhu
		dictDoChinhXac[key] = DoChinhXac
		avgDoChinhXac += DoChinhXac
	avgDoPhu = avgDoPhu/len(listTaiLieuTraVe.keys())
	avgDoChinhXac = avgDoChinhXac/len(listTaiLieuTraVe.keys())
	return dictTrungKhop, dictDoPhu, avgDoPhu, dictDoChinhXac, avgDoChinhXac

def main(src1, src2):
	TaiLieuTraVe = getListTaiLieuTraVe(src1)
	TaiLieuLienQuan = getListTaiLieuLienQuan(src2)
	TrungKhop, ListDoPhu, DoPhuTB, listDoChinhXac, DoChinhXacTB = Compare(TaiLieuTraVe, TaiLieuLienQuan)

	print('---------- Do Phu -------------------------')
	for key, value in ListDoPhu.items():
		print(key + '\t' + str(value))
	print(DoPhuTB)
	print()
	print('---------- Do Chinh Xac -------------------')
	for key, value in listDoChinhXac.items():
		print(key + '\t' + str(value))
	print(DoChinhXacTB)

if __name__ == '__main__':
	src1 = sys.argv[1]
	src2 = sys.argv[2]
	main(src1, src2)