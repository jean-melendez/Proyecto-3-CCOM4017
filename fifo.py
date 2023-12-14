import sys

DEBUG = 0

file_to_open = str(sys.argv[2])
pm_size = int(sys.argv[1])

fd = open(file_to_open, "r")
pages = fd.read().split() #esto forma un arreglo de strings para cada acceso en memoria de notacion "R:1"
if (DEBUG): print(pages)
if (DEBUG): print(len(pages))

page_dictionary = [] #record de los accesos a memoria
physicalMem = [] #un artefacto de debugging, para ver los espacios en memoria como aparecen en el archivo de entrada
space = 0 #variable que almacena los espacios de memoria a la cual accede la pagina


def splitter(something): #con esta funcion se cogen las paginas de acceso 
	#y se cambian a un formato apto para los algoritmos de reemplazamiento
	global space

	page_splitter = something.split(':') #divide en dos partes los accesos a memoria, la parte que no importa y la direccion en memoria
	
	space = page_splitter[1]			
	if (DEBUG): print("split page: ", page_splitter[0], space)
	
	return space


def fifoReplacement(algo): #funcion de remplazamiento
	#al ocurrir un page fault se le hace pop a la primera pagina en memoria fisica
	if (len(physicalMem) >= pm_size): 
		physicalMem.pop(0)
	if (len(page_dictionary) >= pm_size):	
		page_dictionary.pop(0)
	
	#luego se le hace append a memoria fisica con la nueva pagina
	page_dictionary.append(algo)
	if (DEBUG): print("page_dictionary: ", page_dictionary)
	physicalMem.append(algo)
	if (DEBUG): print("physicalMem memory: ", physicalMem)


def pageFinder(x):#funcion donde se reciben un arreglo de strings simulando paginas de acceso y se verifica si estan o no en memoria fisica	
		
	faultCount = 0

	for i in range(len(pages)):
		splitter(pages[i]) #llamada a la funcion que divide los strings de acceso del file abierto 
		#si el espacio en memoria esta en este arreglo, significa que la pagina tambien esta en memoria fisica
		if (space in page_dictionary): 
			if (DEBUG): print("page hit")
		#de lo contrario, esto significa un page fault y se corre el algoritmo de fifo replacementent
		else:
			if (DEBUG): print("page fault")
			faultCount += 1		
			
			if (len(page_dictionary) < pm_size):
				if (DEBUG): print("appending...")
				fifoReplacement(space) 
			else: 
				fifoReplacement(space)
	if (DEBUG): print("Number of page faults:")
	print(faultCount)


pageFinder(pages)
fd.close()