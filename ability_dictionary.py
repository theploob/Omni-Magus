import random
import math

random.seed()
ability_names = [
	"Blizzard",
	# "High Blizzard 2",
	"Blizzard 3",
	"Blizzard 4",
	# "Freeze",
	"Fire",
	# "High Fire 2",
	"Fire 3",
	"Fire 4",
	# "Flare",
	"Despair",
	"Paradox",
	# "Thunder 3",
	# "Thunder 4",
	"Transpose",
	"Scathe",
	"Manafont",
	# "Manaward",
	# "Aetherial Manipulation",
	# "Ley Lines",
	"Sharpcast",
	# "Between the Lines",
	"Triplecast",
	"Foul",
	"Xenoglossy",
	"Umbral Soul"
	# "Amplifier"
]

ability_list = {}
ability_f_list = {}


class Ability:
	def __init__(self, name):
		self.name = name
		self.func = ability_f_list[self.name]


def init_dictionary():
	ability_f_list['Blizzard'] = f_blizzard
	ability_f_list['Blizzard 3'] = f_blizzard_3
	ability_f_list['Blizzard 4'] = f_blizzard_4
	ability_f_list['Fire'] = f_fire
	ability_f_list['Fire 3'] = f_fire_3
	ability_f_list['Fire 4'] = f_fire_4
	ability_f_list['Despair'] = f_despair
	ability_f_list['Paradox'] = f_paradox

	ability_f_list['Scathe'] = f_scathe
	ability_f_list['Xenoglossy'] = f_scathe
	ability_f_list['Foul'] = f_foul

	ability_f_list['Transpose'] = f_transpose
	ability_f_list['Sharpcast'] = f_sharpcast
	ability_f_list['Umbral Soul'] = f_umbral_soul
	ability_f_list['Manafont'] = f_manafont
	ability_f_list['Triplecast'] = f_triplecast

	for ability_name in ability_names:
		ability_list[ability_name] = Ability(ability_name)


def mana_cost_ice(val, level):
	if level == 3:
		return 0
	return val * (1 - 0.25 * level)


# Ability functions
# A function will return an array of information about its casting
# [validity (bool), mana cost (int), potency (int)]
def f_blizzard(ms):
	ret = [False, 0, 0]

	mana_cost = 4
	potency = 180
	cooldown = 2.5
	cast_time = 2.5

	astral = ms.get_astral()
	astral_type = astral[0]
	astral_level = astral[1]

	if astral_type == 'Ice':
		mana_cost = mana_cost_ice(mana_cost, astral_level)
	elif astral_type == 'Fire':
		mana_cost = 0
		potency = round(potency * (1 - 0.1 * astral_level))

	if mana_cost > ms.get_mana() and not ms.get_infinite_mana():
		ret[0] = False
		return ret

	ms.add_astral('Ice')

	ret = [True, mana_cost, potency]
	return ret


def f_blizzard_3(ms):
	ret = [False, 0, 0]

	mana_cost = 8
	potency = 240
	cooldown = 2.5
	cast_time = 3.5

	astral = ms.get_astral()
	astral_type = astral[0]
	astral_level = astral[1]

	if astral_type == 'Ice':
		mana_cost = mana_cost_ice(mana_cost, astral_level)
	elif astral_type == 'Fire':
		mana_cost = 0
		potency = round(potency * (1 - 0.1 * astral_level))

	if mana_cost > ms.get_mana() and not ms.get_infinite_mana():
		ret[0] = False
		return ret

	ms.set_astral('Ice', 3)

	ret = [True, mana_cost, potency]
	return ret


def f_blizzard_4(ms):
	ret = [False, 0, 0]

	mana_cost = 8
	potency = 300
	cooldown = 2.5
	cast_time = 2.5

	astral = ms.get_astral()
	astral_type = astral[0]
	astral_level = astral[1]

	if astral_type == 'Ice':
		mana_cost = mana_cost_ice(mana_cost, astral_level)
	else:
		ret[0] = False
		return ret

	if mana_cost > ms.get_mana() and not ms.get_infinite_mana():
		ret[0] = False
		return ret

	ms.set_heart(3)

	ret = [True, mana_cost, potency]
	return ret


def f_fire(ms):
	ret = [False, 0, 0]

	mana_cost = 8
	potency = 180
	cooldown = 2.5
	cast_time = 2.5

	use_heart = False
	astral = ms.get_astral()
	astral_type = astral[0]
	astral_level = astral[1]

	if astral_type == 'Ice':
		mana_cost = 0
		potency *= (1 - 0.1 * astral_level)
	elif astral_type == 'Fire':
		if ms.has_heart():
			use_heart = True
		else:
			mana_cost *= 2
		potency = round(potency * (1.2 + 0.2 * astral_level))

	if mana_cost > ms.get_mana() and not ms.get_infinite_mana():
		ret[0] = False
		return ret

	ms.add_astral('Fire')
	if use_heart:
		ms.sub_umbral()

	if ms.get_sharpcast():
		ms.set_sharpcast(False)
		ms.set_firestarter(True)
	else:
		if random.randrange(100) < 40:
			ms.set_firestarter(True)

	ret = [True, mana_cost, potency]
	return ret


def f_fire_3(ms):
	ret = [False, 0, 0]

	mana_cost = 20
	potency = 240
	cooldown = 2.5
	cast_time = 3.5

	use_heart = False
	astral = ms.get_astral()
	astral_type = astral[0]
	astral_level = astral[1]

	if astral_type == 'Ice':
		mana_cost = 0
		potency *= (1 - 0.1 * astral_level)
	elif astral_type == 'Fire':
		if ms.has_heart():
			use_heart = True
		else:
			mana_cost *= 2
		potency = round(potency * (1.2 + 0.2 * astral_level))

	if ms.get_firestarter():
		ms.set_firestarter(False)
		use_heart = False
		mana_cost = 0

	if mana_cost > ms.get_mana() and not ms.get_infinite_mana():
		ret[0] = False
		return ret

	ms.set_astral('Fire', 3)
	if use_heart:
		ms.sub_umbral()

	ret = [True, mana_cost, potency]
	return ret


def f_fire_4(ms):
	ret = [False, 0, 0]

	mana_cost = 8
	potency = 300
	cooldown = 2.5
	cast_time = 2.8

	use_heart = False
	astral = ms.get_astral()
	astral_type = astral[0]
	astral_level = astral[1]

	if astral_type == 'Fire':
		if ms.has_heart():
			use_heart = True
		else:
			mana_cost *= 2
		potency = round(potency * (1.2 + 0.2 * astral_level))
	else:
		ret[0] = False
		return ret

	if mana_cost > ms.get_mana() and not ms.get_infinite_mana():
		ret[0] = False
		return ret
	if use_heart:
		ms.sub_umbral()

	ret = [True, mana_cost, potency]
	return ret


def f_despair(ms):
	ret = [False, 0, 0]

	mana_cost = ms.get_mana()
	if mana_cost < 8:
		mana_cost = 8
	potency = 340
	cooldown = 2.5
	cast_time = 4

	use_heart = False
	astral = ms.get_astral()
	astral_type = astral[0]
	astral_level = astral[1]

	if astral_type == 'Fire':
		if ms.has_heart():
			use_heart = True
			mana_cost = math.trunc(mana_cost * 2 / 3)
		potency = round(potency * (1.2 + 0.2 * astral_level))
	else:
		ret[0] = False
		return ret

	if mana_cost > ms.get_mana() and not ms.get_infinite_mana():
		ret[0] = False
		return ret
	if use_heart:
		ms.sub_umbral()

	ms.set_astral('Fire', 3)

	ret = [True, mana_cost, potency]
	return ret


def f_paradox(ms):
	ret = [False, 0, 0]

	mana_cost = 16
	potency = 500
	cooldown = 2.5
	cast_time = 2.5

	if ms.get_paradox():
		ms.set_paradox(False)
		astral_type = ms.get_astral()[0]

		if astral_type == 'Fire':
			if mana_cost > ms.get_mana() and not ms.get_infinite_mana():
				ret[0] = False
				return ret
			ms.add_astral('Fire')
			if ms.get_sharpcast():
				ms.set_sharpcast(False)
				ms.set_firestarter(True)
			else:
				if random.randrange(100) < 40:
					ms.set_firestarter(True)

		elif astral_type == 'Ice':
			mana_cost = 0
			ms.add_astral('Ice')

		else:
			ret[0] = False
	else:
		ret[0] = False

	ms.set_paradox(False)

	ret[0] = True
	ret[1] = mana_cost
	ret[2] = potency

	return ret


def f_scathe(ms):
	ret = [False, 0, 0]

	mana_cost = 8
	potency = 100
	cooldown = 2.5
	cast_time = 0

	if mana_cost > ms.get_mana() and not ms.get_infinite_mana():
		ret[0] = False
		return ret

	if ms.get_sharpcast():
		ms.set_sharpcast(False)
		potency = 200
	else:
		if random.randrange(100) < 20:
			potency = 200

	ret = [True, mana_cost, potency]
	return ret


def f_xenoglossy(ms):
	ret = [False, 0, 0]

	cooldown = 2.5
	cast_time = 0

	if ms.has_polyglot():
		ms.sub_polyglot()
		ret = [True, 0, 660]
	else:
		return ret


def f_foul(ms):
	ret = [False, 0, 0]

	cooldown = 2.5
	cast_time = 3

	if ms.has_polyglot():
		ret = [True, 0, 560]
	else:
		return ret


def f_transpose(ms):
	ret = [False, 0, 0]

	cooldown = 5
	cast_time = 0

	astral_type = ms.get_astral()[0]
	if astral_type == 'Fire':
		ms.set_astral('Ice', 1)
	elif astral_type == 'Ice':
		ms.set_astral('Fire', 1)

	ret = [True, 0, 0]
	return ret


def f_sharpcast(ms):
	ret = [False, 0, 0]

	cooldown = 30
	cast_time = 0

	ms.set_sharpcast(True)

	ret = [True, 0, 0]
	return ret


def f_umbral_soul(ms):
	ret = [False, 0, 0]

	cooldown = 2.5
	cast_time = 0

	astral_type = ms.get_astral()[0]
	if astral_type == 'Ice':
		ms.add_astral('Ice')
		ms.add_umbral()
		ret[0] = True

	return ret


def f_manafont(ms):
	ret = [False, 0, 0]

	cooldown = 180
	cast_time = 0

	ms.mod_mana(30)
	ret[0] = True

	return ret


def f_triplecast(ms):
	ret = [False, 0, 0]

	cooldown = 60
	cast_time = 0

	ms.set_triplecast(3)
	ret[0] = True

	return ret
