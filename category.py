'''
Proporciona la classe "Category".
'''
class Category():
	'''
	Aquesta classe controla els atributs de la taula "category" de la base de dades.

	Atributs:
	---------
	id : int
		El identificador a la taula "category" de la base de dades.
	fee : float
		Quantitat a pagar corresponent a dita categoria.
	name : string
		Forma amb la que es nombra dita categoria.
	description : string
		Informació curta sobre les edats a les quals correspon la categoria.
	'''

	
	def __init__(self, id: int, fee: float, name: str, description: str, members_list: list = None):
		'''
		Inicialitza una nova instància de la classe Category.

		Paràmetres:
		-----------
		id : int
			El identificador a la taula "category" de la base de dades.
		fee : float
			Quantitat a pagar corresponent a dita categoria.
		name : string
			Forma amb la que es nombra dita categoria.
		description : string
			Informació curta sobre les edats a les quals correspon la categoria.
		'''
		self.id = id
		self.fee = fee
		self.name = name
		self.description = description
		self.members_list = members_list