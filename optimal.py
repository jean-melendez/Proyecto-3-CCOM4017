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
memSpaces = [] #almacena el numero del espacio en memoria de la lista de acceso 
space = 0 #variable que almacena los espacios de memoria a la cual accede la pagina

def splitter(something): #con esta funcion se cogen las paginas de acceso 
	#y se cambian a un formato apto para los algoritmos de reemplazamiento
	global space

	page_splitter = something.split(':')
	space = page_splitter[1]			
	if (DEBUG): print("split page: ", page_splitter[0], space)	
	
	return space


def memory_checker(whatever): #esta funcion recopila la lista entera de accesos a memoria para poder verificar
	#cual se repetira mas tarde en el futuro
	
	for i in range(len(pages)):
		memSpaces.append(splitter(pages[i]))
		
	if (DEBUG): print("memSpaces: ", memSpaces)


def optimalReplacement(algo): #funcion de remplazamiento
	
	valReplacement = 0 #almacena el valor a remplazar
	maximum = 0 #almacena la suma mayor de la proxima variable para poder comparar esta
	k = 0 #el espacio en memoria repetido que se encuentre lo mas tarde en la lista tendra el valor mas grande de esta variable
	index_to_replace = 0 #almacena el indice del espacio en memoria mayor que se repite
	if (len(physicalMem) >= pm_size):
		
		if (DEBUG): print("page_dictionary: ", page_dictionary)
		if (DEBUG): print("memSpaces: ", memSpaces)

		for i in range(len(page_dictionary)):
			if (page_dictionary[i] in memSpaces): #si la direccion en memoria se repite, corre esta parte del codigo
				if (DEBUG): print(page_dictionary[i], "is in memSpaces")
				k = 0
				for z in range(len(memSpaces)):
					if (memSpaces[z] == page_dictionary[i]): #si las dirreciones son la misma, se compara si es el ultimo en repetirse
						if (DEBUG): print("k: ", k, "z: ", z)
						if (k > maximum):
							maximum = k
							index_to_replace = i
							valReplacement = memSpaces[z]						
					else:
						k += z
				
			if (page_dictionary[i] not in memSpaces): #si hay alguno que no se repita, entonces simplemente se reemplaza ese y ya
				if (DEBUG): print(page_dictionary[i], "not in memSpaces")
				page_dictionary[i] = space
				physicalMem[i] = algo
				if (DEBUG): print("new page_dictionary: ", page_dictionary)
				if (DEBUG): print("physicalMem: ", physicalMem)
				if (DEBUG): print("memSpaces: ", memSpaces)
				return space

		#aqui occurre el reemplazamiento fuera del for loop en el caso que todos se encuentren en el futuro
		if (DEBUG): print(index_to_replace, memSpaces[index_to_replace], valReplacement)
		page_dictionary[index_to_replace] = space
		physicalMem[index_to_replace] = algo
		if (DEBUG): print("new page_dictionary: ", page_dictionary)
		if (DEBUG): print("physicalMem: ", physicalMem)
		if (DEBUG): print("memSpaces: ", memSpaces)
		return space

	#solo corre esta parte del codigo si la lista aun no ha sido llenada ya que no hay que reemplazar nada a este punto
	if (len(page_dictionary) < pm_size): 
		page_dictionary.append(space)
		if (DEBUG): print("page_dictionary append: ", page_dictionary)
	if (len(physicalMem) < pm_size): 
		physicalMem.append(algo)
		if (DEBUG): print("physicalMem memory append: ", physicalMem)

	return space	

def pageFinder(x):#funcion donde se reciben un arreglo de strings simulando paginas de acceso y se verifica si estan o no en memoria fisica
	faultCount = 0

	memory_checker(pages)

	for i in range(len(pages)):
		splitter(pages[i]) #llamada a la funcion que divide los strings de acceso del file abierto 
		memSpaces.pop(0) #como ya se comparo este, el mismo puede ser descartado para ahorrase la busqueda
		#si el espacio en memoria esta en este arreglo, significa que la pagina tambien esta en memoria fisica
		if (space in page_dictionary):
			if (DEBUG): print("page hit")

	#de lo contrario, esto significa un page fault y se corre el algoritmo de optimal replacementent	
		else:
			if (DEBUG): print("page fault")
			faultCount += 1			
			optimalReplacement(space)
	if (DEBUG): print("Number of page faults:")
	print(faultCount)
	

pageFinder(pages)
fd.close()