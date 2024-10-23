'''
Proporciona la classe "Falla".
'''
from tkinter import messagebox

from database import Database

from movement import Movement
from family import Family
from member import Member
from category import Category
from lottery import Lottery


class Falla():
	'''
	Aquesta classe pot controlar llistats de les classes "Member", "Movement"
	"Family" i "Category" i operar amb elles.

	Atributs:
	---------
	members_list : list
		Llistat d'objectes de la classe "Member".
	movements_list : list
		Llistat d'objectes de la classe "Movement".
	categories_list: list
		Llistat d'objectes de la classe "Category".
	families_list : list
		Llistat d'objectes de la classe "Family".
	lotteries_list : list
		Llistat d'objectes de la classe "Lottery".

	Mètodes:
	--------
	get_members(*args)
	get_movements(id_member, falla_year)
	get_categories()
	get_falla_year()
	assign_fee(transaction_date, amount, falla_year, id_member, description)
	assign_lottery(transaction_date, amount, falla_year, id_member, description)
	assign_raffle(transaction_date, amount, falla_year, id_member, description)
	assign_massive_raffle()
	calculate_assigned_fee(id_member, falla_year): float
	calculate_payed_fee(id_member, falla_year): float
	calculate_assigned_lottery(id_member, falla_year): float
	calculate_payed_lottery(id_member, falla_year): float
	calculate_assigned_raffle(id_member, falla_year): float
	calculate_payed_raffle(id_member, falla_year): float
	pay_fee(transaction_date, amount, falla_year, description,
		receipt_number, id_member)
	pay_lottery(transaction_date, amount, falla_year, description,
		receipt_number, id_member)
	pay_raffle(transaction_date, amount, falla_year, description,
		receipt_number, id_member)
	'''
	

	def __init__(self):
		'''
		Inicialitza una nova instància de la classe Falla.
		'''
		self.members_list = []
		self.movements_list = []
		self.categories_list = []
		self.families_list = []
		self.lotteries_list = []
		self.falla_year = 0


	def get_members(self, *args):
		'''
		Recupera i guarda en self.members_list el llistat de membres
		demanat a través de *args.

		Paràmetres:
		-----------
		args : list
			Llistat d'un màxim de 2 arguments:
			El filtre de cerca i la cadena necessària per a la cerca.
		'''
		db = Database('sp')
		if args[0] == "surname":
			result = db.select_members_by_surname(args[1])
		elif args[0] == "adult":
			result = db.select_adult_members()
		elif args[0] == "underage":
			result = db.select_underage_members()
		elif args[0] == "is_registered":
			result = db.select_registered_members(args[1])
		elif args[0] == "category":
			result = db.select_members_by_category(args[1])
		db.close_connection()
		for values in result:
			family = Family(values[12], values[13], values[14])
			category = Category(values[15], values[16], values[17], values[18])
			member = Member(
				values[0],
				values[1],
				values[2],
				values[3],
				values[4],
				values[5],
				values[6],
				values[7],
				values[8],
				values[11],
				family,
				category
			)
			self.members_list.append(member)


	def get_movements(self, id_member, falla_year):
		'''
		Recupera i guarda en self.movements_list el llistat de moviments
		per al faller i exercici demanats.

		Paràmetres:
		-----------
		id_member : int
			Identificació del faller del que volem treure els moviments.
		falla_year: int
			Any de l'exercici faller.
		'''
		db = Database('sp')
		result = db.select_movements_by_member(id_member, falla_year)
		db.close_connection()
		for values in result:
			movement = Movement(
				values[0],
				values[1],
				values[2],
				values[3],
				values[4],
				values[5],
				values[7],
				values[8]
			)
			self.movements_list.append(movement)


	def get_categories(self):
		'''
		Recupera i guarda en self.categories_list el llistat de categories.
		'''
		db = Database('sp')
		result = db.select_categories()
		db.close_connection()
		for values in result:
			category = Category(values[0], values[1], values[2], values[3])
			self.categories_list.append(category)

	
	def get_families(self):
		'''
		Recupera i guarda en self.families_list el llistat de families.
		'''
		db = Database('sp')
		result = db.select_families()
		db.close_connection()
		for values in result:
			family = Family(values[0], values[1], values[2])
			self.families_list.append(family)


	def get_lotteries(self, lottery_name, falla_year):
		db = Database('sp')
		result = db.select_lotteries_by_lottery_name(lottery_name, falla_year)
		db.close_connection()
		for values in result:
			member = Member(
				values[15],
				values[16],
				values[17],
				values[18],
				values[19],
				values[20],
				values[21],
				values[22],
				values[23],
				values[26]
			)
			lottery = Lottery(
				values[0],
				values[1],
				values[2],
				values[3],
				values[4],
				values[6],
				values[7],
				values[8],
				values[9],
				values[10],
				values[11],
				values[12],
				values[13],
				values[14],
				member
			)
			self.lotteries_list.append(lottery)


	def get_current_falla_year(self):
		'''
		Recupera i guarda en self.falla_year l'any de l'exercici actual.
		'''
		db = Database('sp')
		self.falla_year = db.select_current_falla_year()
		db.close_connection()


	def assign_fee(
		self, transaction_date, amount, falla_year, id_member, description
	):
		'''
		Crida a la classe Movement per a crear una assignació de quota.

		Paràmetres:
		-----------
		transaction_date : date
			Data que volem fixar per al moviment.
		amount : float
			Quantitat de diners corresponents a la quota.
		falla_year : int
			Any de l'exercici faller.
		id_member : int
			Identificació del faller a qui li assignem la quota.
		description : string
			Breu descripció del concepte del moviment.
		'''
		Movement.set_movement(
			transaction_date,
			amount,
			1,
			1,
			falla_year,
			description,
			0,
			id_member
		)


	def assign_lottery(
		self, transaction_date, amount, falla_year, id_member, description
	):
		'''
		Crida a la classe Movement per a crear una assignació de loteria.

		Paràmetres:
		-----------
		transaction_date : date
			Data que volem fixar per al moviment.
		amount : float
			Quantitat de diners corresponents a la loteria.
		falla_year : int
			Any de l'exercici faller.
		id_member : int
			Identificació del faller a qui li assignem la loteria.
		description : string
			Breu descripció del concepte del moviment.
		'''
		Movement.set_movement(
			transaction_date,
			amount,
			1,
			2,
			falla_year,
			description,
			0,
			id_member
		)


	def assign_raffle(
		self, transaction_date, amount, falla_year, id_member, description
	):
		'''
		Crida a la classe Movement per a crear una assignació de rifa.

		Paràmetres:
		-----------
		transaction_date : date
			Data que volem fixar per al moviment.
		amount : float
			Quantitat de diners corresponents a la rifa.
		falla_year : int
			Any de l'exercici faller.
		id_member : int
			Identificació del faller a qui li assignem la rifa.
		description : string
			Breu descripció del concepte del moviment.
		'''
		Movement.set_movement(
			transaction_date,
			amount,
			1,
			3,
			falla_year,
			description,
			0,
			id_member
		)


	def assign_massive_raffle(self):
		'''
		Crea un moviment per cadascún dels fallers amb obligació de pagar rifa i
		el guarda a la base de dades.
		'''
		answer=messagebox.askquestion(
			"Assignar rifa",
			"Estàs segur que vols assignar la rifa als fallers corresponents?"
		)
		if answer == "yes":
			self.get_members("adult")
			try:
				for member in self.members_list:
					self.assign_raffle(None, 15, None, member.id, "rifa")
			except TypeError:
				messagebox.showerror(
					"Assignar rifa",
					"La rifa no s'ha pogut assignar correctament"
				)
			else:
				messagebox.showinfo(
					"Assignar rifa",
					"La rifa s'ha assignat correctament"
				)


	def calculate_assigned_fee(self, id_member, falla_year):
		'''
		Calcula i retorna la quota total assignada a un faller
		a partir del seu identificador i l'any de l'exercici faller.

		Paràmetres:
		-----------
		falla_year : int
			Any de l'exercici faller.
		id_member : int
			Identificació del faller.

		Retorna:
		--------
		fee : float
			Total de quota assignada al faller.
		'''
		db = Database('sp')
		result = db.select_fee_by_member(id_member)
		fee = result[0]
		result = db.select_discount_by_member(id_member)
		discount = result[0]*fee/100
		fee = fee - discount
		result = db.select_fee_assignment_movements_by_member(
			id_member, falla_year
		)
		db.close_connection()
		for value in result:
			fee = fee + value[0]
		return fee


	def calculate_payed_fee(self, id_member, falla_year):
		'''
		Calcula i retorna la quota total pagada per un faller
		a partir del seu identificador i l'any de l'exercici faller.

		Paràmetres:
		-----------
		falla_year : int
			Any de l'exercici faller.
		id_member : int
			Identificació del faller.

		Retorna:
		--------
		fee : float
			Total de quota pagada pel faller.
		'''
		db = Database('sp')
		result = db.select_fee_payment_movements_by_member(
			id_member, falla_year
		)
		db.close_connection()
		fee = 0
		for value in result:
			fee = fee + value[0]
		return fee


	def calculate_assigned_lottery(self, id_member, falla_year):
		'''
		Calcula i retorna la loteria total assignada a un faller
		a partir del seu identificador i l'any de l'exercici faller.

		Paràmetres:
		-----------
		falla_year : int
			Any de l'exercici faller.
		id_member : int
			Identificació del faller.

		Retorna:
		--------
		fee : float
			Total de loteria assignada al faller.
		'''
		db = Database('sp')
		result = db.select_lottery_assignment_movements_by_member(
			id_member, falla_year
		)
		db.close_connection()
		lottery = 0
		for value in result:
			lottery = lottery + value[0]
		return lottery


	def calculate_payed_lottery(self, id_member, falla_year):
		'''
		Calcula i retorna la loteria total pagada per un faller
		a partir del seu identificador i l'any de l'exercici faller.

		Paràmetres:
		-----------
		falla_year : int
			Any de l'exercici faller.
		id_member : int
			Identificació del faller.

		Retorna:
		--------
		fee : float
			Total de loteria pagada pel faller.
		'''
		db = Database('sp')
		result = db.select_lottery_payment_movements_by_member(
			id_member, falla_year
		)
		db.close_connection()
		lottery = 0
		for value in result:
			lottery = lottery + value[0]
		return lottery


	def calculate_assigned_raffle(self, id_member, falla_year):
		'''
		Calcula i retorna la rifa total assignada a un faller
		a partir del seu identificador i l'any de l'exercici faller.

		Paràmetres:
		-----------
		falla_year : int
			Any de l'exercici faller.
		id_member : int
			Identificació del faller.

		Retorna:
		--------
		fee : float
			Total de rifa assignada al faller.
		'''
		db = Database('sp')
		result = db.select_raffle_assignment_movements_by_member(
			id_member, falla_year
		)
		db.close_connection()
		raffle = 0
		for value in result:
			raffle = raffle + value[0]
		return raffle


	def calculate_payed_raffle(self, id_member, falla_year):
		'''
		Calcula i retorna la rifa total pagada per un faller
		a partir del seu identificador i l'any de l'exercici faller.

		Paràmetres:
		-----------
		falla_year : int
			Any de l'exercici faller.
		id_member : int
			Identificació del faller.

		Retorna:
		--------
		fee : float
			Total de rifa pagada pel faller.
		'''
		db = Database('sp')
		result = db.select_raffle_payment_movements_by_member(
			id_member, falla_year
		)
		db.close_connection()
		raffle = 0
		for value in result:
			raffle = raffle + value[0]
		return raffle
	

	def get_daily_payments(self, date, description):
		'''
		Recupera i guarda en self.movements_list el llistat de moviments
		de pagament del dia indicat.

		Paràmetres:
		-----------
		date : string
			Data de la que volem els moviments.
		'''
		db = Database('sp')
		result = db.select_payment_movements_by_date(date, description)
		db.close_connection()
		for values in result:
			member = Member(
				values[9],
				values[10],
				values[11],
				values[12],
				values[13],
				values[14],
				values[15],
				values[16],
				values[17],
				values[18]
			)
			movement = Movement(
				values[0],
				values[1],
				values[2],
				values[3],
				values[4],
				values[5],
				values[7],
				values[8],
				member
			)
			self.movements_list.append(movement)


	def pay_fee(
		self,
		transaction_date,
		amount,
		falla_year,
		description,
		receipt_number,
		id_member
	):
		'''
		Crea el moviment de pagar quota.

		Paràmetres:
		-----------
		transaction_date : date
			Data del moviment.
		amount : float
			Quantitat de diners.
		falla_year : int
			Exercici al que pertany el moviment.
		description : string
			Descripció del moviment.
		receipt_number : int
			Número de rebut.
		id_member : int
			Identificador del faller que fa el pagament.
		'''
		Movement.set_movement(
			transaction_date,
			amount,
			2,
			1,
			falla_year,
			description,
			receipt_number,
			id_member
		)


	def pay_lottery(
		self,
		transaction_date,
		amount,
		falla_year,
		description,
		receipt_number,
		id_member
	):
		'''
		Crea el moviment de pagar loteria.

		Paràmetres:
		-----------
		transaction_date : date
			Data del moviment.
		amount : float
			Quantitat de diners.
		falla_year : int
			Exercici al que pertany el moviment.
		description : string
			Descripció del moviment.
		receipt_number : int
			Número de rebut.
		id_member : int
			Identificador del faller que fa el pagament.
		'''
		Movement.set_movement(
			transaction_date,
			amount,
			2,
			2,
			falla_year,
			description,
			receipt_number,
			id_member
		)


	def pay_raffle(
		self,
		transaction_date,
		amount,
		falla_year,
		description,
		receipt_number,
		id_member
	):
		'''
		Crea el moviment de pagar rifa.

		Paràmetres:
		-----------
		transaction_date : date
			Data del moviment.
		amount : float
			Quantitat de diners.
		falla_year : int
			Exercici al que pertany el moviment.
		description : string
			Descripció del moviment.
		receipt_number : int
			Número de rebut.
		id_member : int
			Identificador del faller que fa el pagament.
		'''
		Movement.set_movement(
			transaction_date,
			amount,
			2,
			3,
			falla_year,
			description,
			receipt_number,
			id_member
		)


	def get_lotteries_list(self):
		db = Database('sp')
		lotteries_list = db.select_lotteries_list()
		return lotteries_list
	
	
	def new_falla_year(self):
		'''
		Crea un nou exercici seguint els següents passos:
		Guardem a la base de dades tots els membres actius amb les seues dades
		d'assignacions i pagaments.
		S'inserta el nou exercici a la taula "fallaYear".
		Es repasen les categories de tots els fallers no adults per vore si canvien de categoria.
		'''
		
		db = Database('sp')
		self.get_current_falla_year()
		self.get_members("is_registered", 1)
		for member in self.members_list:
			assigned_fee = 0
			payed_fee = 0
			assigned_lottery = 0
			payed_lottery = 0
			assigned_raffle = 0
			payed_raffle = 0
			assigned_fee = assigned_fee + self.calculate_assigned_fee(
				member.id, self.falla_year
			)
			payed_fee = payed_fee + self.calculate_payed_fee(
				member.id, self.falla_year
			)
			assigned_lottery = assigned_lottery + \
				self.calculate_assigned_lottery(
					member.id, self.falla_year
				)
			payed_lottery = payed_lottery + \
				self.calculate_payed_lottery(
					member.id, self.falla_year
				)
			assigned_raffle = assigned_raffle + \
				self.calculate_assigned_raffle(
					member.id, self.falla_year
				)
			payed_raffle = payed_raffle + self.calculate_payed_raffle(
				member.id, self.falla_year
			)
			db.insert_summary(member.id, assigned_fee, assigned_lottery, assigned_raffle, payed_fee, payed_lottery, payed_raffle)
		messagebox.showinfo("Exercici nou", "Resum de l'any anterior guardat correctament")
		
		db.update_falla_year_end(self.falla_year)
		db.insert_falla_year()
		messagebox.showinfo("Exercici nou", "Nou any assignat correctament")

		self.get_members("underage")
		for member in self.members_list:
			member.modify_member(
				member.id,
				member.name,
				member.surname,
				member.birthdate,
				member.gender,
				member.dni,
				member.address,
				member.phone_number,
				member.is_registered,
				member.email,
				member.family.id,
				member.category.id
			)
		messagebox.showinfo("Exercici nou", "Categories de fallers actualitzades")

		summary_list = db.select_summary_by_falla_year(self.falla_year)
		self.get_current_falla_year()
		for value in summary_list:
			Movement.set_movement(
				None,
				value[1],
				1,
				1,
				self.falla_year,
				"diferència any anterior",
				0,
				value[0]
			)
		messagebox.showinfo("Exercici nou", "Deutes i sobrants de l'exercici anterior actualitzats")

		# Afegim a cada faller l'historial de l'exercici nou.
		# Per fer la part de l'historial
		
		messagebox.showinfo("Exercici nou", "Historial faller actualitzat com a vocals. La resta de punts s'han d'assignar manualment")
		messagebox.showinfo("Exercici nou", "El canvi d'exercici s'ha realitzat correctament")
		
		db.close_connection()

	'''
	def nou_exercici(self):
		
		Crea un nou exercici seguint els següents passos:
		Es crea un arxiu binari amb la id de cada faller amb alta activa junt amb les dades
		d'assignacions i pagaments finals.
		Es modifica l'arxiu binari "exercici" amb l'any actual del sistema.
		Es repasen les categories de tots els fallers no adults per vore si canvien de categoria.
		Recuperem l'arxiu binari creat anteriorment de forma que assignem els deutes o sobrants
		al nou exercici per a cada faller que no haja acabat l'exercici anterior a 0.
		Finalment afegim l'estat de l'historial per a cada faller en el nou exercici depenent de
		si va acabar l'exercici anterior donat d'alta o no.
		
		
		# Creem una cópia en fitxer binari del resultat de l'exercici.
		bd=BaseDeDades("falla.db")
		arxiu=Arxiu("exercici")
		members_list=bd.llegir_fallers_per_alta(1)
		exercici_actual=arxiu.llegir_exercici_actual()
		llista=[]
		for faller in members_list:
			valors=[]
			quota_assignada=0
			quota_pagada=0
			loteria_assignada=0
			loteria_pagada=0
			rifa_assignada=0
			rifa_pagada=0
			valors.append(faller.id)
			quota_base=bd.llegir_quota_faller(faller.id)
			descompte=(faller.familia.descompte*quota_base/100)
			quota=quota_base-descompte
			llista_assignacions_pagaments=self.calcular_assignacions_pagaments(faller.id, exercici_actual)
			quota_assignada=llista_assignacions_pagaments[0]
			quota_pagada=llista_assignacions_pagaments[1]
			loteria_assignada=llista_assignacions_pagaments[2]
			loteria_pagada=llista_assignacions_pagaments[3]
			rifa_assignada=llista_assignacions_pagaments[4]
			rifa_pagada=llista_assignacions_pagaments[5]
			quota_final=quota+quota_assignada
			total_assignacions=quota_final+loteria_assignada+rifa_assignada
			total_pagaments=quota_pagada+loteria_pagada+rifa_pagada
			valors.append("{0:.2f}".format(quota_final))
			valors.append("{0:.2f}".format(loteria_assignada))
			valors.append("{0:.2f}".format(rifa_assignada))
			valors.append("{0:.2f}".format(total_assignacions))
			valors.append("{0:.2f}".format(quota_pagada))
			valors.append("{0:.2f}".format(loteria_pagada))
			valors.append("{0:.2f}".format(rifa_pagada))
			valors.append("{0:.2f}".format(total_pagaments))
			valors.append("{0:.2f}".format(total_assignacions-total_pagaments))
			llista.append(valors)
		nom_arxiu="resums"+"/"+"resum "+str(exercici_actual)
		arxiu=Arxiu(nom_arxiu)
		arxiu.crear_resum(llista)
		messagebox.showinfo("Exercici nou", "Resum de l'any anterior guardat correctament")

		# Modifiquem l'arxiu binari "exercici" amb l'any actual del sistema.
		llista=[]
		arxiu=Arxiu("exercici")
		utils=Utils()
		data_actual=utils.calcular_data_actual()
		dia_actual=int(data_actual[0])
		mes_actual=int(data_actual[1])
		any_actual=int(data_actual[2])
		if mes_actual>3:
			any_exercici=any_actual+1
		elif mes_actual<2:
			any_exercici=any_actual
		elif mes_actual==3 and dia_actual>19:
			any_exercici=any_actual+1
		elif mes_actual==3 and dia_actual<=19:
			any_exercici=any_actual
		llista.append(any_exercici)
		arxiu.modificar_exercici_actual(llista)
		messagebox.showinfo("Exercici nou", "Nou any assignat correctament")
		
		# Assignem la nova categoria a cada faller que haja canviat.
		exercici_actual=arxiu.llegir_exercici_actual()
		for faller in members_list:
			if faller.category.id>1:
				old_category_id=faller.category.id
				edat=faller.calcular_edat(faller.naixement, exercici_actual)
				category_id=faller.calculate_category(edat)
				if category_id!=old_category_id:
					category=bd.llegir_categoria(category.id)   #provar en la refactoritzacio a juntar les 2 linies
					faller.category=category                    #provar en la refactoritzacio a juntar les 2 linies
					bd.actualitzar_faller(faller)
		messagebox.showinfo("Exercici nou", "Categories de fallers actualitzades")

		# Recuperem l'arxiu binari de l'exercici anterior i assignem els valors distints de 0 a l'exercici actual.
		nom_arxiu="resums"+"/"+"resum "+str(exercici_actual-1)
		arxiu=Arxiu(nom_arxiu)
		llista=arxiu.llegir_resum()
		data=data_actual[0] + "-" + data_actual[1] + "-" + data_actual[2]
		for valor in llista:
				if valor[9]!="0.00":
				faller=bd.llegir_faller(valor[0])
				moviment=Movement(0, data, valor[9], 1, 1, exercici_actual, "any anterior", 0, faller)
				bd.crear_moviment(moviment)
		bd.tancar_conexio()
		messagebox.showinfo("Exercici nou", "Deutes i sobrants de l'exercici anterior actualitzats")

		# Afegim a cada faller l'historial de l'exercici nou.
		members_list=bd.llegir_fallers()
		for faller in members_list:
			nom_arxiu="historials"+"/"+str(faller.id)
			arxiu=Arxiu(nom_arxiu)
			historial=arxiu.llegir_historial()
			if faller.alta==1:
				historial[exercici_actual]=["vocal", "Sants Patrons"]
			else:
				historial[exercici_actual]=["baixa", ""]
			arxiu.modificar_historial(historial)
		messagebox.showinfo("Exercici nou", "Historial faller actualitzat com a vocals. La resta de punts s'han d'assignar manualment")
		messagebox.showinfo("Exercici nou", "El canvi d'exercici s'ha realitzat correctament")


	def borrar_historial(self):
		
		Borra tots els arxius d'historial de tots els fallers i els reinicia com si l'exercici
		actual fora el primer any de faller.
		
		valor=messagebox.askquestion("Borrar historial",
										"Estàs segur que vols reiniciar els historials de tots els fallers?")
		if valor=="yes":
			bd=BaseDeDades("falla.db")
			arxiu=Arxiu("exercici")
			exercici_actual=arxiu.llegir_exercici_actual()
			members_list=bd.llegir_fallers()
			for faller in members_list:
				exercici=faller.calcular_primer_exercici(faller.naixement)
				historial={}
				while exercici < exercici_actual:
					historial[exercici]=["baixa", ""]
					exercici=exercici+1
				if faller.alta==1:
					historial[exercici_actual]=["vocal", "Sants Patrons"]
				else:
					historial[exercici_actual]=["baixa", ""]
				nom_arxiu="historials"+"/"+str(faller.id)
				arxiu=Arxiu(nom_arxiu)
				arxiu.crear_historial(historial)
			bd.tancar_conexio()
			messagebox.showinfo("Borrar historial", "L'historial de tots els fallers s'ha reiniciat correctament")
			'''