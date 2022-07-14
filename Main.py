from tkinter import *
from tkinter import filedialog as fd
from tkinter import messagebox as mb
import zipfile
from PIL import Image, ImageTk
import os
import sys
import json
import hjson

from PyQt6.QtWidgets import QApplication, QLabel, QPushButton, QWidget

window_close = True

window = None
MaiL = None

WS = 0
TempMod = None




def reMod():
	global window
	window.destroy()
	MainL()

def MainL():
	global Mod1, window, window_close
	window = Tk()
	window.title("Mindustry Mod Construct (Test)")
	window.geometry("800x700")
	window.minsize(800, 700)
	window["bg"] = "white"

	app = QApplication(sys.argv)

	windowNew = QWidget()
	windowNew.setBaseSize(800, 700)
	windowNew.setMinimumSize(800, 700)
	windowNew.setWindowTitle("Mindustry Mod Construct (Test)")
	windowNew.setBackgroundRole = "white"
	windowNew.show()



	def on_closing():
		window.destroy()
		window_close = False
		

	window.protocol("WM_DELETE_WINDOW", on_closing)

	sucsFold = False

	while sucsFold == False:
		Mod1 = fd.askdirectory(title = "Выберете папку с модом")

		Mod = os.listdir(Mod1)

		for i in Mod:
			if i == "mod.json" or i == "mod.hjson":
				sucsFold = True
				break
		if sucsFold == False and len(Mod) == 1:
			Mod1 = Mod1 + "/" + Mod[0]
			Mod = os.listdir(Mod1)
			for i in Mod:
				if i == "mod.json" or i == "mod.hjson":
					sucsFold = True
					break

		if sucsFold == False:
			mb.showerror("Мод не обнаружен!\nПопробуйте еще раз!")



	#QLabel(windowNew, text="Выбрать другой мод").setGeometry(0, 0, 100, 200)
	ChoseModButton = QPushButton(text="Выбрать другой мод").move(100,70)

	#ChoseModButton.clicked.connect(reMod)

	Label(window).place(anchor = CENTER, relx = 0.675, rely = 0.975, relwidth = 0.65, relheight = 0.05)

	Button(window, text = "Выбрать другой мод", font = ("Arial", 12, "normal"), command = reMod).place(anchor = "e", relx = 1, rely = 0.975)

	FileW = {}

	def openFile(pathF, typeF, typeM):
		if pathF != None:
			Filer = open(pathF, "r")
			if typeF == "json":
				Filer = json.load(Filer)
			elif typeF == "hjson":
				Filer = hjson.load(Filer)
			FileW = {}
			if typeM == "Mod":
				FileW.add("name", [Label(window, text = "Название:"), Entry(window)])



	if os.path.exists(Mod1 + "/mod.json"):
		Button(window, text = "mod.json", font = ("Arial", 12, "normal"), command = lambda: SelLC(Type = "mod.json")).place(anchor = "w", relx = 0.35, rely = 0.975)
	elif os.path.exists(Mod1 + "/mod.hjson"):
		Button(window, text = "mod.hjson", font = ("Arial", 12, "normal"), command = lambda: SelLC(Type = "mod.hjson")).place(anchor = "w", relx = 0.35, rely = 0.975)

	SaveObj = Button(window, text = "Save", font = ("Arial", 12, "normal"), command = lambda: ModSave(TempMod, "mod")).place(anchor = CENTER, relx = 0.65 , rely = 0.975)

	Mod = os.listdir(Mod1)

	# def Lister():
	# 	global Mod1

	# 	ListItem.delete(0, END)
	# 	ListBlock.delete(0, END)
	# 	ListItemImg.delete(0, END)
	# 	ListBlockImg.delete(0, END)

	# 	if os.path.exists(Mod1 + "/content"):
	# 		if os.path.exists(Mod1 + "/content/items"):
	# 			for i in os.listdir(Mod1 + "/content/items"):
	# 				ListItem.insert(0, i)
	# 		if os.path.exists(Mod1 + "/content/blocks"):
	# 			for i in os.listdir(Mod1 + "/content/blocks"):
	# 				ListBlock.insert(0, i)
	# 	if os.path.exists(Mod1 + "/sprites"):
	# 		if os.path.exists(Mod1 + "/sprites/items"):
	# 			for i in os.listdir(Mod1 + "/sprites/items"):
	# 				ListItemImg.insert(0, i)
	# 		if os.path.exists(Mod1 + "/sprites/blocks"):
	# 			for i in os.listdir(Mod1 + "/sprites/blocks"):
	# 				ListBlockImg.insert(0, i)

	CreateW = None

	def CreateFile(name, path):
		global CreateW
		if path == "Item":
			f = open(Mod1 + "/content/items/" + name + ".json", "w+")
			f.close
			Lister()
			CreateW.destroy()
		if path == "Block":
			f = open(Mod1 + "/content/blocks/" + name + ".json", "w+")
			f.close
			Lister()
			CreateW.destroy()


	def Create(mat):
		global CreateW
		CreateW = Toplevel()
		CreateW.title("Создать " + mat + " (Test)")
		CreateW.geometry("200x100")
		CreateW["bg"] = "#ffffff"

		Label(CreateW, text = "Создать новый " + mat + "\nНе надо писать расширение файла!", bg = "#ffffff").place(anchor = CENTER, relx = 0.5, rely = 0.25, relwidth = 1)

		Ent = Entry(CreateW, font = ("Arial", 12, "normal"), bg = "#dedede")
		Ent.place(anchor = CENTER, rely = 0.5, relwidth = 1, relx = 0.5)

		Button(CreateW, text = "Создать", command = lambda: CreateFile(Ent.get(), mat)).place(anchor = CENTER, relx = 0.5, rely = 0.75)




	Button(window, text = "Создать", font = ("Arial", 11, "normal"), command = lambda: Create("Item")).place(anchor = CENTER, relx = 0.125, rely = 0.07)
	Button(window, text = "Создать", font = ("Arial", 11, "normal"), command = lambda: Create("Block")).place(anchor = CENTER, relx = 0.125, rely = 0.57)




	if os.path.exists(Mod1 + "/icon.png"):
		Logo = Image.open(Mod1 + "/icon.png")
	else:
		Logo = Image.open("noneMod.png")

	Label(window, background="gray").place(relx = 0, rely = 0, relwidth = 1, relheight = 0.1)

	Logo = Logo.resize((48, 48))
	Logo = ImageTk.PhotoImage(Logo)

	ModImg = Label(window, image = Logo)
	ModImg.place(anchor = CENTER, relx = 0.4, rely = 0.05)

	ModImg1 = Label(window, image = Logo)
	ModImg1.place(anchor = CENTER, relx = 0.95, rely = 0.05)

	if os.path.exists(Mod1 + "/mod.json"):
		ModJson = json.load(open(Mod1 + "/mod.json", "r"))
	elif os.path.exists(Mod1 + "/mod.hjson"):
		ModJson = hjson.load(open(Mod1 + "/mod.hjson", "r"))
	else:
		reMod()





	if "displayName" in ModJson:
		ModLab = Label(window, text = ModJson["displayName"], font = ("Arial", 14, "normal"), bg = "#ffffff")
		ModLab.place(anchor = CENTER, relx = 0.675, rely = 0.025)
	else:
		ModLab = Label(window, text = ModJson["name"], font = ("Arial", 15, "normal"), bg = "#ffffff")
		ModLab.place(anchor = CENTER, relx = 0.675, rely = 0.025)

	

	ModVer = Label(window, text = "v" + str(ModJson["version"]), font = ("Arial", 8, "normal"), bg = "#ffffff")
	ModVer.place(anchor = CENTER, relx = 0.675, rely = 0.085)

	def AutS():
		mb.showinfo("Автори", ModJson["author"])


	if len(ModJson["author"]) > 80:
		ModAut = Button(window, text = "Автори", font = ("Arial", 8, "normal"), command = AutS)
	else:
		ModAut = Label(window, text = ModJson["author"], font = ("Arial", 10, "normal"), bg = "#ffffff")
	ModAut.place(anchor = CENTER, relx = 0.675, rely = 0.06)

	
	
	

	def ModSave(mod, Ttype = None):
		if Ttype == None:
			if mod["type"] == "material":
				pass
		else:
			if Ttype == "mod":
				ModSaveTemp = {}
				for i in ["name", "displayName", "author", "description", "version", "minGameVersion"]:
					try:
						ModSaveTemp.update({i: EObj[i][1].get()})
					except Exception:
						ModSaveTemp.update({i: EObj[i][1].get("1.0",END)})
				print(ModSaveTemp)



	# canvas = Canvas(window)
	# canvas.place(relx=0, rely=0.1, relheight=0.9, relwidth=0.35)

	# def on_configure(event):
	# 	canvas.configure(scrollregion=canvas.bbox('all'))

	# frame = Frame(canvas)
	# # resize the canvas scrollregion each time the size of the frame changes
	# frame.bind('<Configure>', on_configure)
	# # display frame inside the canvas
	# canvas.create_window(0, 0, window=frame)

	# scrolly = Scrollbar(window, command=canvas.yview)
	# scrolly.place(relx=0.35, rely=0.1, relheight=0.9, anchor='ne')
	# canvas.configure(yscrollcommand=scrolly.set)

	ContentL = []
	ContentL1 = []
	for root, dirs, files in os.walk(Mod1 + "/content"):
		for file in files:
			if file.endswith(".json") or file.endswith(".hjson"):
				ContentL.append(str(os.path.join(root, file)))
				ContentL1.append(file)

	SpriteL = []

	for root, dirs, files in os.walk(Mod1 + "/sprites"):
		for file in files:
			if file.endswith(".png"):
				SpriteL.append(str(os.path.join(root, file)))
	

	def testAdd(text):
		if text[-5:] == ".json":
			return "json"
		if text[-6:] == ".hjson":
			return "hjson"
	def toPng(text):
		if text[-5:] == ".json":
			text1 = text[:-5]
			text1 += ".png"
		if text[-6:] == ".hjson":
			text1 = text[:-6]
			text1 += ".png"
		return text1

	def ImagOPT(img):
		for t in range(0, len(SpriteL)):
			if SpriteL[t][-1*(len(img)):] == img:
				return SpriteL[t]
				break
		return "noneMod.png"
	


	def openFiler(pathF):
		opsa = open(pathF, "r")
		try:
			if testAdd(pathF) == "json":
				# opsa = json.load(opsa)
				with open(pathF, 'r', encoding='utf-8') as f:
					data = json.load(f)
			
				opsa = json.loads(json.dumps(data, sort_keys=False, indent=4))
			if testAdd(pathF) == "hjson":
				with open(pathF, 'r', encoding='utf-8') as f:
					data = hjson.load(f)
			
				opsa = hjson.loads(hjson.dumps(data, sort_keys=False, indent=4))
		except Exception:
			opsa = {"name": "Ошибка"}
		return opsa

	ListC = Listbox(window)
	ListC.place(rely = 0.1, relwidth = 0.35, relheight = 0.85)

	for i in range(0, len(ContentL)):
		ListC.insert(i, str(openFiler(ContentL[i])["name"]))



	NameObj = Label(window, text = "None", font = ("Arial", 11, "normal"))
	NameObj.place(anchor = CENTER, relx = 0.675, rely = 0.125, relwidth = 0.65, relheight = 0.05)

	

	ImageObj = Image.open("noneMod.png")

	ImageObj = ImageObj.resize((30, 30))
	ImageObj = ImageTk.PhotoImage(ImageObj)

	ImgObj = Label(window, image = ImageObj)
	ImgObj.place(anchor = "w", relx = 0.35, rely = 0.125)

	ImgObj1 = Label(window, image = ImageObj)
	ImgObj1.place(anchor = "e", relx = 1, rely = 0.125)

	EObj = {"img": Label(window, image = None, width = 64, height = 64), "name": [Label(window, text = "Name"), Entry(window)], "displayName": [Label(window, text = "DName"), Entry(window)], "author": [Label(window, text = "Author"), Entry(window)], "description": [Label(window, text = "Desc\nript\nion"), Text(window)], "version": [Label(window, text = "Version"), Entry(window)], "minGameVersion": [Label(window, text = "minVer"), Entry(window)]}


	def EObjOP(par, text = ["", 0], label = [None, None, None, None], entry = [None, None, None, None]):
		EObj[par][0].place_forget()
		EObj[par][1].place_forget()
		EObj[par][1].delete(text[1], END)

		EObj[par][0].place(relx = label[0], rely = label[1], relwidth = label[2], relheight = label[3])
		EObj[par][1].place(relx = entry[0], rely = entry[1], relwidth = entry[2], relheight = entry[3])
		EObj[par][1].insert(text[1], text[0])


	def EntryObj(Mods, Type = None):
		try:
			if Type != None:
				EObj["img"].place_forget()
				EObj["name"][0].place_forget()
				EObj["name"][1].place_forget()
				EObj["displayName"][0].place_forget()
				EObj["displayName"][1].place_forget()
				EObj["author"][0].place_forget()
				EObj["author"][1].place_forget()
				EObj["description"][0].place_forget()
				EObj["description"][1].place_forget()
				EObj["version"][0].place_forget()
				EObj["version"][1].place_forget()
				EObj["minGameVersion"][0].place_forget()
				EObj["minGameVersion"][1].place_forget()
				if Type[:3] == "mod":
					if os.path.exists(Mod1 + "/icon.png"):
						ImageObj = Image.open(Mod1 + "/icon.png")
					else:
						ImageObj = Image.open("noneMod.png")
					if ImageObj.width > 32:
						ImageObj = ImageObj.resize((64, 64))
					ImageObj = ImageTk.PhotoImage(ImageObj)


					EObj["img"].place_forget()
					EObj["img"].configure(image = ImageObj)
					EObj["img"].image = ImageObj
					EObj["img"].place(relx = 0.36, rely = 0.16, width = 64, height = 64)

					EObjOP("name", [Mods["name"], 0], [0.45, 0.16, None, 0.025], [0.5, 0.16, 0.495, 0.025])
					EObjOP("displayName", [Mods["displayName"], 0], [0.45, 0.19, None, 0.025], [0.5, 0.19, 0.495, 0.025])
					EObjOP("author", [Mods["author"], 0], [0.45, 0.22, None, 0.025], [0.5, 0.22, 0.495, 0.025])

					EObjOP("description", [Mods["description"], 1.0], [0.36, 0.26, None, 0.08], [0.41, 0.26, 0.585, 0.08])

					EObjOP("version", [Mods["version"], 0], [0.36, 0.35, None, 0.025], [0.41, 0.35, 0.585, 0.025])
					EObjOP("minGameVersion", [Mods["minGameVersion"], 0], [0.36, 0.38, None, 0.025], [0.41, 0.38, 0.585, 0.025])


				else:
					if Type == "material" or Type == "resource":
						if os.path.exists(ImagOPT(toPng(ContentL1[ListC.curselection()[0]]))):
							ImageObj = Image.open(ImagOPT(toPng(ContentL1[ListC.curselection()[0]])))
						else:
							ImageObj = Image.open("noneMod.png")
						if ImageObj.width > 32:
							ImageObj = ImageObj.resize((64, 64))
						ImageObj = ImageTk.PhotoImage(ImageObj)

						EObj["img"].place_forget()
						EObj["img"].configure(image = ImageObj)
						EObj["img"].image = ImageObj
						EObj["img"].place(relx = 0.36, rely = 0.16, width = 64, height = 64)

						EObjOP("name", [Mods["name"], 0], [0.45, 0.16, None, 0.025], [0.5, 0.16, 0.495, 0.025])
						EObjOP("description", [Mods["description"], 1.0], [0.45, 0.19, None, 0.065], [0.5, 0.19, 0.495, 0.065])
					if Type == "Wall":
						if os.path.exists(ImagOPT(toPng(ContentL1[ListC.curselection()[0]]))):
							ImageObj = Image.open(ImagOPT(toPng(ContentL1[ListC.curselection()[0]])))
						else:
							ImageObj = Image.open("noneMod.png")
						if ImageObj.width > 32:
							ImageObj = ImageObj.resize((64, 64))
						ImageObj = ImageTk.PhotoImage(ImageObj)

						EObj["img"].place_forget()
						EObj["img"].configure(image = ImageObj)
						EObj["img"].image = ImageObj
						EObj["img"].place(relx = 0.36, rely = 0.16, width = 64, height = 64)

						EObjOP("name", [Mods["name"], 0], [0.45, 0.16, None, 0.025], [0.5, 0.16, 0.495, 0.025])
						EObjOP("description", [Mods["description"], 1.0], [0.45, 0.19, None, 0.065], [0.5, 0.19, 0.495, 0.065])


				
			else:
				pass			
		except Exception:
			pass
			

	WS = 0
	TempMod = None

	def SelLC(event = None, Type = None):
		global WS, TempMod
		try:
			if WS == 0:
				if ListC.curselection() != ():
					WS = 0
					
					if Type != None:
						if Type[:3] == "mod":
							TempModI = openFiler(Mod1 + "/" + Type)
							print(TempModI)
							TempMod = Mod1 + "/" + Type
							NameObj.configure(text = TempModI["name"] + "\ntype - " + "mod")

							EntryObj(TempModI, Type)
							ImageObj = Image.open(Mod1 + "/icon.png")
					else:

						TempModI = openFiler(ContentL[ListC.curselection()[0]])
						TempMod = ContentL[ListC.curselection()[0]]
						NameObj.configure(text = TempModI["name"] + "\ntype - " + TempModI["type"])
						EntryObj(TempModI, TempModI["type"])
						if os.path.exists(ImagOPT(toPng(ContentL1[ListC.curselection()[0]]))):
							ImageObj = Image.open(ImagOPT(toPng(ContentL1[ListC.curselection()[0]])))
						else:
							ImageObj = Image.open("noneMod.png")

					ImageObj = ImageObj.resize((30, 30))
					ImageObj = ImageTk.PhotoImage(ImageObj)

					ImgObj.configure(image = ImageObj)
					ImgObj.image = ImageObj
					ImgObj1.configure(image = ImageObj)
					ImgObj1.image = ImageObj



				else:
					WS = 1
			else:
				SaveW = Toplevel()
				SaveW.title("Екстреное Сохронение (Test)")
				SaveW.geometry("200x100")
				SaveW["bg"] = "#ffffff"

				Label(SaveW, text = "Сохранить?").pack()
				TempFSW = Frame(SaveW)
				Button(TempFSW, text = "Да").pack(side = LEFT)
				Button(TempFSW, text = "Нет").pack(side = LEFT)
				Button(TempFSW, text = "Назад").pack(side = LEFT)
				TempFSW.pack()
		except Exception:
			pass



	ListC.bind("<<ListboxSelect>>", SelLC)












	# for i in range(0, len(ContentL)):
	# 	ListContent.append([Frame(frame)])
	# 	Temp = ImagOPT(toPng(ContentL1[i]))
	# 	Temp = Image.open(Temp)
	# 	Temp = Temp.resize((18, 18))
	# 	Temp = ImageTk.PhotoImage(Temp)

	# 	ListContent[i].append(Label(ListContent[i][0], image = Temp, width = 18, height = 18))
	# 	ListContent[i][1].image = Temp
	# 	ListContent[i][1].pack(side=LEFT)
	# 	ListContent[i].append(Label(ListContent[i][0], text = str(openFiler(ContentL[i])["name"])).pack(side=LEFT))
	# 	ListContent[i].append(Button(ListContent[i][0], text = "Открыть", command = lambda: openObj(ContentL[i])).pack(side=LEFT))
	# 	ListContent[i].append(Button(ListContent[i][0], text = "Удалить").pack(side=LEFT))
	# 	testAdd(ContentL)


	# 	ListContent[i][0].pack()






	Mod = os.listdir(Mod1)

	window.withdraw()
	window.deiconify()


	while window_close:
		Mod = os.listdir(Mod1)
		try:
			window.update()

		except Exception:
			break
if window_close:
	MainL()

quit()