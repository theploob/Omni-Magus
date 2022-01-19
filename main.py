import sys
from tkinter import *
from tkinter import ttk
import ability_dictionary

mana_value = 10000

class AbilityButton:
	def __init__(self, name):
		self.name = name
		filename = "images/" + name + ".png"
		self.image_file = PhotoImage(file=filename)
		self.ability_function = ability_dictionary.get_ability_function(self.name)
		self.ability_button = None
		self.button_location = None




ability_list = []

ability_button_list = []

def main():
	global ability_list
	global ability_names

	def button_press(*args):
		global mana_value

		print("Button pressed")
		try:
			mana_value -= 1
			manabar_value.set(str(mana_value))

		except ValueError:
			pass

	root = Tk()
	root.title("The Omni Magus Calculator")

	for name in ability_dictionary.ability_names:
		ability_list.append(AbilityInfo(name))

	# Main frame
	frame_main = ttk.Frame(root, padding="3")
	frame_main.grid(column=0, row=0, sticky='n w e s')

	# Ability history frame
	frame_abilityhistory = ttk.Frame(frame_main, padding="3")
	frame_abilityhistory.grid(row=1, column=1, sticky='s e')
	frame_abilityhistory['borderwidth'] = 2
	frame_abilityhistory['relief'] = 'sunken'

	# Ability history widget
	# TODO

	# Ability buttons frame
	frame_abilitybuttons = ttk.Frame(frame_main, padding="3")
	frame_abilitybuttons.grid(row=3, column=0, sticky='s w')
	frame_abilitybuttons['borderwidth'] = 2
	frame_abilitybuttons['relief'] = 'sunken'

	# Individual buttons
	for ability_num, ability in enumerate(ability_list):
		ability_button_list.append(ttk.Button(frame_abilitybuttons, image=ability.image_file, command=button_press).grid(
			column=ability_num % 10, row=int(ability_num / 10), sticky='n w'))

	# Mana bar frame
	frame_manabar = ttk.Frame(frame_main, padding="3")
	frame_manabar.grid(row=2, column=0, sticky='s w e')
	frame_manabar['borderwidth'] = 2
	frame_manabar['relief'] = 'sunken'

	# Mana bar value
	manabar_value = StringVar()
	manabar_value.set("10000")
	label_manabar = ttk.Label(frame_manabar, textvariable=manabar_value).grid(column=0, row=0, sticky='w s e n')

	# Buffs and status frame
	frame_statuses = ttk.Frame(frame_main, padding="3")
	frame_statuses.grid(row=1, column=0, sticky='s w e')
	frame_statuses['borderwidth'] = 2
	frame_statuses['relief'] = 'sunken'

	# Buffs and status widget
	# TODO

	# Controls frame
	frame_controls = ttk.Frame(frame_main, padding="3")
	frame_controls.grid(row=0, sticky='n w e')
	frame_controls['borderwidth'] = 2
	frame_controls['relief'] = 'sunken'

	# Controls widgets
	# TODO
	ttk.Button(frame_controls, text="Reset", command=button_press)
	ttk.Button(frame_controls, text="Stop Timer", command=button_press)



	# Grid configure at the end of setup to draw the frames & their children
	for child in frame_abilitybuttons.winfo_children():
		child.grid_configure(padx=5, pady=5)
	for child in frame_abilityhistory.winfo_children():
		child.grid_configure(padx=5, pady=5)
	for child in frame_manabar.winfo_children():
		child.grid_configure(padx=5, pady=5)
	for child in frame_statuses.winfo_children():
		child.grid_configure(padx=5, pady=5)
	for child in frame_controls.winfo_children():
		child.grid_configure(padx=5, pady=5)
	for child in frame_main.winfo_children():
		child.grid_configure(padx=5, pady=5)




	root.columnconfigure(0, weight=1)
	root.rowconfigure(0, weight=1)


	root.mainloop()


if __name__ == "__main__":
	sys.exit(main())
