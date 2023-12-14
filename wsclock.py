import sys

DEBUG = 0

class wsPage: #esta clase es utilizada para poder insertar y comparar dentro del working set
	def __init__(self, space, pageTime, referenceBit):
		self.space = space
		self.pageTime = pageTime
		self.referenceBit = referenceBit


file_to_open = str(sys.argv[3])
tau = int(sys.argv[2]) #determina si una pagina esta dentro del working set o no
memory_size = int(sys.argv[1])

fd = open(file_to_open, "r")
pages = fd.read().split() #esto forma un arreglo de strings para cada acceso en memoria de notacion "R:1"
if (DEBUG): print(pages)
if (DEBUG): print(len(pages))

page_dictionary = [] #record de los accesos a memoria
physicalMem = [] #un artefacto de debugging, para ver los espacios en memoria como aparecen en el archivo de entrada
space = 0 #variable que almacena los espacios de memoria a la cual accede la pagina

working_set = [] #en esta estructura de datos es donde se hace la computacion de si un elemento esta en el ws y cual debe ser removido
ct = 0 #current time
hand = 0 #manecilla del reloj


def splitter(something): #con esta funcion se cogen las paginas de acceso 
	#y se cambian a un formato apto para los algoritmos de reemplazamiento
	global space
	page_splitter = something.split(':') #divide en dos partes los accesos a memoria, la parte que no importa y la direccion en memoria
	space = page_splitter[1]	
	if (DEBUG): print("**********")		
	if (DEBUG): print("split page: ", page_splitter[0], space)
	return space


def moveHand(): #mueve la mano del reloj
	global hand
	hand  = (hand + 1) % len(working_set)
	if (DEBUG): print("hand: ", hand)
	return hand


def wsclock(algo):
	global hand

	referenced = 1 #si la pagina esta sucia/referenciada recientemente en memoria
	oldest = 0 #cual pagina es la mas vieja
	oldest_time = 0 #el tola mayor
	tola = 0 #time of last access, (current time - page time)
	
	ages = [0]*(len(working_set)) #arreglo comparando los tola

	wsPag = wsPage(space, ct, referenced) #clase para incertar paginas dentro del working set
	if (DEBUG): print("wsPag: ", int(wsPag.space), int(wsPag.pageTime), int(wsPag.referenceBit))

	if (DEBUG):
		for i in range(len(working_set)):
			print(int(working_set[i].space), int(working_set[i].pageTime), int(working_set[i].referenceBit), "age :", ct - working_set[i].pageTime)

	for j in range(len(working_set)):
		if (DEBUG): print("here!")
		if (working_set[hand].referenceBit == 0): #si el rf esta en 0 desde antes de el page fault actual, verficiar su tola 
			if (DEBUG): print("there!")
			tola = ct - working_set[hand].pageTime
			ages[hand] = tola
			moveHand()

		else: 
			working_set[hand].referenceBit = 0 #de lo contrario simplemente se pone su rf en 0
			ages[hand] = 0
			moveHand()

	if (DEBUG):
		for i in range(len(working_set)):
			print(int(working_set[i].space), int(working_set[i].pageTime), int(working_set[i].referenceBit), "age :", ct - working_set[i].pageTime)
		print("ages: ", ages)

	if len(working_set) == memory_size: 
		for bad_bunny in range(len(ages)): #necesitaba una variable llamada diferente que i o j
			if ages[bad_bunny] > oldest_time: #si el tola de esta pagina, los indices estan sincronizados, es el mayor, entonces es
				#candidata a ser remplazada
				oldest_time = ages[bad_bunny]
				oldest = bad_bunny
		if (DEBUG): 
			print("the oldest page: ", oldest)
			print(working_set[oldest].space, int(working_set[oldest].pageTime), int(working_set[oldest].referenceBit))
			print(page_dictionary[oldest])
		#aqui es donde se reemplaza la pagina y se mueve el reloj
		working_set[oldest].space = wsPag.space
		working_set[oldest].pageTime = ct
		working_set[oldest].referenceBit = 1
		page_dictionary[oldest] = space
		hand = oldest
		
	#en el caso de que la memoria aun no este llena simplemente llenarla
	if (len(working_set) < memory_size):
		working_set.append(wsPag)
		moveHand()
		if (DEBUG): 
			print(working_set)

	if (len(page_dictionary) < memory_size):
		page_dictionary.append(space)
		if (DEBUG): print(page_dictionary)



def pageFinder(x):#funcion donde se reciben un arreglo de strings simulando paginas de acceso y se verifica si estan o no en memoria fisica
	global ct	
	faultCount = 0

	for i in range(len(pages)):
		splitter(pages[i]) #llamada a la funcion que divide los strings de acceso del file abierto 
		ct += 1
		#si el espacio en memoria esta en este arreglo, significa que la pagina tambien esta en memoria fisica
		if (space in page_dictionary):
			if (DEBUG): print("page hit")
			for j in range(len(working_set)):
				if (space == working_set[j].space): 
				#al contrario a fifo y optimal, hay que hacerles ajustes a la pagina en memoria
					working_set[j].referenceBit = 1 #poner como que esta recientemente accesada
					working_set[j].pageTime = ct #actualizar su tola
					if (DEBUG): print(page_dictionary)
					if (DEBUG): 
						print("hit wsPag: ", int(working_set[j].space), int(working_set[j].pageTime), int(working_set[j].referenceBit))
			if (DEBUG):
				for i in range(len(working_set)):
					print(int(working_set[i].space), int(working_set[i].pageTime), int(working_set[i].referenceBit), "age :", ct - working_set[i].pageTime)
				
		#si no esta, significa un page fault y se corre el algoritmo de wsclock 
		else:
			if (DEBUG): print("page fault")
			faultCount += 1	
			wsclock(space)
			moveHand() #mueve la manecilla del reloj al siguiente despues del indice modificado

	if (DEBUG): print("final page_dictionary: ", page_dictionary)	

	if (DEBUG): print("Number of page faults:")
	print(faultCount)


pageFinder(pages)
fd.close()