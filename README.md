Proyecto por Jean Melendez para CCOM4017.

En este proyecto hay 3 programas de reemplazamiento de paginas en memoria. Primero es el fifo.py. Para correr este programa, escribir "python fifo.py <Number of physical memory pages> <access sequence file>" en command line. Como indica el nombre, este cuando encuentra un page fault simplemente saca la primera pagina en memoria fisica y inserta en la cola la pagina nueva.

Por segundo esta el optimal.py. Este es una simulacion de como este algoritmo seria implementado en un sistema operativo. Para lograr la simulacion, se hace una copia de la secuencia de entradas y esta es comparada con las entradas en memoria para asi encontrar cual se repite lo mas tarde posible y entonces eliminar esta de memoria. De no encontrarse alguna en el futuro entonces esa es reemplazada. Para correr este programa, escribir "python optimal.py <Number of physical memory pages> <access sequence file>" en el command line.

Por ultimo, esta el wsclock.py, este siendo el algoritmo de reemplazamiento que implementa una simulacion de un reloj logico para determinar cual pagina reemplazar. Ademas de usar el criterio de un tau para determinar que paginas estan dentro del working set, tambien utiliza un reference bit para saber si una pagina ha sido utlizada recientemente y por ende no considerar esta pagina como candidata a ser reemplazada. Tambien utiliza un "tola" o "time of last access" para determinar cual pagina fue accesada por ultimo hace el mayor tiempo posible para entonces escoger esta como candidata a reemplazo. Para correr este programa, escribir "python wsclock.py <Number of physical memory pages> <tau> <access sequence file>".

Al final de su ejecucion, los tres algoritmos despliegaran la cantidad de page faults que occurieron durante el transcurso de su ejecucion. 

Referencias:
1)Modern Operating Systems, 3/E by A. Tanenbaum: ISBN-10: 0136006639 or ISBN-13: 9780136006633 or 4/E ISBN-10: 013359162X ISBN-13: 978-0133591620 
2)Cualquier y toda persona que estuviece en la AECC durante mientras hacia el proyecto, incluyendo los miembros de esta que tambien cogen 4017. 
3)Dr. Jose Ortiz