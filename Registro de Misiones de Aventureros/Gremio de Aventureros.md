Sistema de Gestión para Gremio de Aventureros

Modelo Lógico

Tabla: heroes

	- id (INTEGER, PRIMARY KEY)
    - nombre (TEXT)
	- clase (TEXT)
	- nivel_experiencia (INTEGER)

Tabla: misiones

	- id (INTEGER, PRIMARY KEY)
	- descripcion (TEXT)
	- nivel_dificultad (INTEGER)
	- localizacion (TEXT)
	- recompensa_oro (INTEGER)

Tabla: monstruos

	- id (INTEGER, PRIMARY KEY)
	- nombre (TEXT)
	- tipo (TEXT)
	- nivel_amenaza (INTEGER)

Tabla: misiones_heroes

	- mision_id (INTEGER, FOREIGN KEY REFERENCES misiones(id))
	- heroe_id (INTEGER, FOREIGN KEY REFERENCES heroes(id))
	- PRIMARY KEY (mision_id, heroe_id)

Tabla: misiones_monstruos

	- mision_id (INTEGER, FOREIGN KEY REFERENCES misiones(id))
	- monstruo_id (INTEGER, FOREIGN KEY REFERENCES monstruos(id))
	- PRIMARY KEY (mision_id, monstruo_id)

Modelo Entidad-Relación (ER)

	+------------------+         +---------------------+         +------------------+
	|      HEROES      |         |   MISIONES_HEROES   |         |     MISIONES     |
	+------------------+         +---------------------+         +------------------+
	| PK  id           |<-------O| PK,FK1  mision_id   |O------->| PK  id           |
	|     nombre       |         | PK,FK2  heroe_id    |         |     descripcion  |
	|     clase        |         +---------------------+         |     nivel_difi.. |
	|     nivel_exp..  |                                         |     localizacion |
	+------------------+                                         |     recompensa.. |
                                                             +------------------+
                                                                      ^
                                                                      |
                             +---------------------+                  |
                             | MISIONES_MONSTRUOS  |                  |
                             +---------------------+                  |
                             | PK,FK1  mision_id   |O-----------------+
                             | PK,FK2  monstruo_id |O-----+
                             +---------------------+      |
                                                          v
                                                     +------------------+
                                                     |    MONSTRUOS     |
                                                     +------------------+
                                                     | PK  id           |
                                                     |     nombre       |
                                                     |     tipo         |
                                                     |     nivel_amena..|
                                                     +------------------+
