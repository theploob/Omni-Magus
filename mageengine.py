import ability_dictionary
import time

class MageEngine:
	def __init__(self):
		self.magestatus = MageStatus()
		self.print_detailed_cast = False
		self.print_statuses = False
		self.print_total_potency = False
		self.total_spell_potency = 0

		self.__action_queue = []
		self.time_passed = 0
		self.start_time = time.time()
		self.last_tick_time = 0

		ability_dictionary.init_dictionary()

	def add_spell_to_queue(self, name):
		self.__action_queue.append(name)

	def tick_update(self):
		cur_time = time.time()
		self.time_passed = cur_time - self.start_time
		self.last_tick_time = cur_time

	def cast_spell(self, name):
		spell_ret = ability_dictionary.ability_list[name].func(self.magestatus)
		spell_valid = spell_ret[0]
		if not spell_valid:
			print("Couldn't cast " + name)
			return
		spell_cost = spell_ret[1]
		spell_potency = spell_ret[2]
		if not self.magestatus.get_infinite_mana():
			self.magestatus.mod_mana(-1 * spell_cost)
		if spell_potency != 0:
			print("Cast {} with a potency of {} for {} mana, {} remaining".format(
				name, spell_potency, spell_cost, self.magestatus.get_mana()))
			if self.print_total_potency:
				self.total_spell_potency += spell_potency
				print("Total potency: {}".format(self.total_spell_potency))
		else:
			print("Cast {} for {} mana, {} remaining".format(name, spell_cost, self.magestatus.get_mana()))

		if self.print_statuses:
			self.magestatus.print_info()

		self.post_spell_effects()

	def post_spell_effects(self):
		# Mana Regen
		astral_mode = self.magestatus.get_astral()[0]
		astral_level = self.magestatus.get_astral()[1]
		if astral_mode == 'Ice':
			self.magestatus.mod_mana(17 + 15 * astral_level)
		elif astral_mode != 'Fire':
			self.magestatus.mod_mana(2)


class MageStatus:
	def __init__(self):
		self.level = 90
		self.__current_mana = 100
		self.__infinite_mana = False
		self.__astral_type = 'None'
		self.__astral_level = 0
		self.__umbral_heart = 0
		self.__triplecast = 0
		self.__polyglot = 0
		self.__sharpcast = False
		self.__firestarter = False
		self.__paradox = False

	def add_astral(self, element):
		if self.is_astral():
			if self.__astral_type == element.capitalize():
				if self.__astral_level < 3:
					self.__astral_level += 1
			else:
				self.__astral_level = 0
				self.__astral_type = 'None'
				self.__umbral_heart = 0
		else:
			self.set_astral(element, 1)

	# Flip astral type if possible. Does not change astral level
	def flip_astral(self):
		if self.__astral_type == 'Ice':
			if self.__astral_level == 3 and self.__umbral_heart == 3:
				self.__paradox = True
			self.__astral_type = 'Fire'

		elif self.__astral_type == 'Fire':
			if self.__astral_level == 3:
				self.__paradox = True
			self.__astral_type = 'Ice'

	def sub_umbral(self):
		if self.__umbral_heart > 0:
			self.__umbral_heart -= 1

	def add_umbral(self):
		if self.__umbral_heart < 3:
			self.__umbral_heart += 1

	def sub_triplecast(self):
		if self.__triplecast > 0:
			self.__triplecast -= 1

	def print_info(self):
		print("Mana: {}    Astral: {} {}    Umbral Hearts: {}    Triples: {}    Polyglots: {}    "
			"Sharpcast: {}    Firestarter: {}    Paradox: {}".format(
			self.__current_mana, self.__astral_type, self.__astral_level, self.__umbral_heart, self.__triplecast,
			self.__polyglot, self.__sharpcast, self.__firestarter, self.__paradox
		))


	# Getter / setter nonsense

	# Returns bool
	def get_infinite_mana(self):
		return self.__infinite_mana

	def set_infinite_mana(self, val=True):
		self.__infinite_mana = val

	# Returns int
	def get_mana(self):
		return self.__current_mana

	def set_mana(self, val):
		if val < 0:
			self.__current_mana = 0
		elif val > 100:
			self.__current_mana = 100
		else:
			self.__current_mana = val

	def mod_mana(self, val):
		mana = self.get_mana() + val
		self.set_mana(mana)

	def toggle_infinite_mana(self, val=None):
		if val is None:
			self.__infinite_mana = not self.__infinite_mana
		elif type(val) is bool:
			self.__infinite_mana = val

	# Returns bool
	def is_astral(self):
		return self.__astral_level > 0

	# Return [<str>, <int>]
	def get_astral(self):
		return [self.__astral_type, self.__astral_level]

	def set_astral(self, element='None', level=0):
		if (element == 'Fire' or element == 'Ice') and (1 <= level <= 3):
			if element == 'Fire':
				if self.__astral_level == 3 and self.__astral_type == 'Ice' and self.__umbral_heart == 3:
					self.__paradox = True
			elif element == 'Ice':
				if self.__astral_level == 3 and self.__astral_type == 'Fire':
					self.__paradox = True

			self.__astral_type = element
			self.__astral_level = level
		else:
			self.__astral_type = 'None'
			self.__astral_level = 0

	# Returns  bool
	def has_heart(self):
		return self.__umbral_heart > 0

	# Returns int
	def get_heart(self):
		return self.__umbral_heart

	def set_heart(self, val=0):
		if type(val) is int and 0 <= val <= 3:
			self.__umbral_heart = val
		else:
			self.__umbral_heart = 0

	# Returns  bool
	def has_triplecast(self):
		return self.__triplecast > 0

	# Returns int
	def get_triplecast(self):
		return self.__triplecast

	def set_triplecast(self, val=0):
		if type(val) is int and 0 <= val <= 3:
			self.__triplecast = val
		else:
			self.__triplecast = 0

	# Returns  bool
	def has_polyglot(self):
		return self.__polyglot > 0

	# Returns int
	def get_polyglot(self):
		return self.__polyglot

	def set_polyglot(self, val=0):
		if type(val) is int and 0 <= val <= 2:
			self.__polyglot = val
		else:
			self.__polyglot = 0

	def add_ployglot(self):
		if self.__polyglot < 2:
			self.__polyglot += 1

	def sub_polyglot(self, val=1):
		if 0 < val < 3:
			if self.__polyglot > 0:
				self.__polyglot -= val

	# Returns bool
	def get_sharpcast(self):
		return self.__sharpcast

	def set_sharpcast(self, val):
		self.__sharpcast = bool(val)

	# Returns bool
	def get_firestarter(self):
		return self.__firestarter

	def set_firestarter(self, val):
		self.__firestarter = bool(val)

	# Returns bool
	def get_paradox(self):
		return self.__paradox

	def set_paradox(self, val):
		self.__paradox = bool(val)
