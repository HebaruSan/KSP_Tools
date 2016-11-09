#!/usr/bin/env python3

import gi, random, math, sys
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk

class DeltaVWindow(Gtk.Window):
	"""
	Interactive GUI window for delta v calculations.
	"""

	def __init__(self):
		"""
		Set up the components of the UI.
		"""

		Gtk.Window.__init__(self)
		self.set_title('Delta V')
		self.set_border_width(5)
		self.set_resizable(False)
		self.set_icon_name(Gtk.STOCK_GO_UP)

		grid = Gtk.Table()
		grid.set_row_spacings(5)
		grid.set_col_spacings(2)
		self.add(grid)

		row_num = 0
		self.mass_entry = self.mk_entry_row(grid, row_num, 'Initial mass:', 'kg', self.mass_changed)

		row_num = row_num+1
		grid.attach(Gtk.HSeparator(), 0, 4, row_num, row_num+1)

		row_num = row_num+1
		self.liquidfuel_entry = self.mk_entry_row(grid, row_num, 'LiquidFuel:', 'L', self.mass_changed)

		row_num = row_num+1
		self.use_oxidizer_checkbutton = Gtk.CheckButton(label='Use oxidizer')
		self.use_oxidizer_checkbutton.set_alignment(0.0, 0.0)
		grid.attach(self.use_oxidizer_checkbutton, 1, 2, row_num, row_num+1, xoptions=Gtk.AttachOptions.FILL, yoptions=0)
		self.use_oxidizer_checkbutton.set_alignment(0.0, 0.0)
		self.use_oxidizer_checkbutton.connect('toggled', self.mass_changed)

		row_num = row_num+1
		grid.attach(Gtk.HSeparator(), 0, 4, row_num, row_num+1)

		row_num = row_num+1
		self.oxidizer_entry = self.mk_entry_row(grid, row_num, 'Oxidizer:', 'L', self.mass_changed)

		row_num = row_num+1
		grid.attach(Gtk.HSeparator(), 0, 4, row_num, row_num+1)

		row_num = row_num+2
		self.isp_entry = self.mk_entry_row(grid, row_num, '', 's', self.mass_changed)
		row_num = row_num-1
		self.mk_quickbuttons(grid, row_num, 'ISP:', self.isp_entry, [240, 250, 275, 315, 350, 800, 4200])
		row_num = row_num+1

		row_num = row_num+1
		grid.attach(Gtk.HSeparator(), 0, 4, row_num, row_num+1)

		row_num = row_num+1
		self.output_label = self.mk_lbl_row(grid, row_num, 'Delta V:', 'm/s')

		self.mass_entry.set_value(24500)
		self.liquidfuel_entry.set_value(4*360)
		self.use_oxidizer_checkbutton.set_active(True)
		self.oxidizer_entry.set_value(4*440)
		self.isp_entry.set_value(350)

		self.connect('destroy', lambda widget: Gtk.main_quit())
		self.connect('key-press-event', self.on_key_press_event)

		style_provider = Gtk.CssProvider()
		style_provider.load_from_data(bytes(self.stylesheet().encode()))
		Gtk.StyleContext.add_provider_for_screen(
			Gdk.Screen.get_default(),
			style_provider,
			Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)

		self.show_all()

	def stylesheet(self) -> str:
		"""
		CSS to tweak the appearance of the components.
		"""

		return """
			GtkHBox > GtkButton {
				padding-left: 2px;
				padding-right: 2px;
				border-radius: 0;
			}
		"""

	def on_key_press_event(self, widget, event):
		"""
		Hotkeys:
			ctrl-W	quit
			ctrl-Q	quit
			Escape	quit
		"""

		if event.state & Gdk.ModifierType.CONTROL_MASK \
			and (event.keyval == Gdk.KEY_w or event.keyval == Gdk.KEY_q):
				Gtk.main_quit()
		if event.keyval == Gdk.KEY_Escape:
			Gtk.main_quit()

	def mk_quickbuttons(self, grid, row_num, left_lbl, entry, options: list):
		"""
		Create a horizontal box containing buttons with common values as one-click presets.
		"""

		lbl1 = Gtk.Label(left_lbl)
		lbl1.set_alignment(0.0, 0.0)
		grid.attach(lbl1,  0, 1, row_num, row_num+1, xoptions=Gtk.AttachOptions.FILL, yoptions=0)

		box = Gtk.HBox(spacing=0)
		grid.attach(box, 1, 4, row_num, row_num+1)
		for opt in options:
			btn = Gtk.Button(opt)
			btn.connect('clicked', self.on_quickbutton_click, opt, entry)
			box.add(btn)

	def on_quickbutton_click(self, button, option, entry):
		"""
		Event handler for when you click a button to set a field to a preset.
		"""

		entry.set_value(option)

	def mk_entry_row(self, grid, row_num, left_lbl, right_lbl, changed_handler):
		"""
		Add a row to 'grid' at y-position row_num:
			left_lbl	| Spin button control	| right_lbl
		Calls 'changed_handler' when the spin button's value changes.
		Returns a reference to the spin button.
		"""

		lbl1 = Gtk.Label(left_lbl)
		lbl2 = Gtk.Label(right_lbl)
		entry = Gtk.SpinButton()
		entry.set_increments(5, 100)
		entry.set_digits(0)
		entry.set_range(1, 999999999) # One billion kg seems like a reasonable upper limit
		entry.set_numeric(True)

		lbl1.set_alignment(0.0, 0.0)
		lbl2.set_alignment(0.0, 0.0)

		grid.attach(lbl1,  0, 1, row_num, row_num+1, xoptions=Gtk.AttachOptions.FILL, yoptions=0)
		grid.attach(entry, 1, 2, row_num, row_num+1, xoptions=Gtk.AttachOptions.FILL, yoptions=0)
		grid.attach(lbl2,  2, 3, row_num, row_num+1, xoptions=Gtk.AttachOptions.FILL, yoptions=0)

		entry.connect('changed', changed_handler)
		return entry

	def mk_lbl_row(self, grid, row_num, left_lbl, right_lbl):
		"""
		Add a row to 'grid' at y-position row_num:
			left_lbl	| special label for output purposes	| right_lbl
		Returns a reference to the middle label.
		"""

		lbl1 = Gtk.Label(left_lbl)
		lbl2 = Gtk.Label()
		lbl3 = Gtk.Label(right_lbl)

		lbl1.set_alignment(0.0, 0.0)
		lbl2.set_alignment(0.0, 0.0)
		lbl3.set_alignment(0.0, 0.0)

		grid.attach(lbl1, 0, 1, row_num, row_num+1, xoptions=Gtk.AttachOptions.FILL, yoptions=0)
		grid.attach(lbl2, 1, 2, row_num, row_num+1, xoptions=Gtk.AttachOptions.FILL, yoptions=0)
		grid.attach(lbl3, 2, 3, row_num, row_num+1, xoptions=Gtk.AttachOptions.FILL, yoptions=0)

		return lbl2

	def mass_changed(self, editable):
		"""
		Event handler to handle changes to the editable controls.
		Updates the output field with the current delta v value.
		"""

		self.update_dv()

	def update_dv(self):
		"""
		Update the output field with the current delta v value.
		"""

		try:
			self.output_label.set_markup("<b>{0:.1f}</b>".format(self.delta_v(
				self.mass_entry.get_value(),
				self.liquidfuel_entry.get_value(),
				self.use_oxidizer_checkbutton.get_active(),
				self.oxidizer_entry.get_value(),
				self.isp_entry.get_value())))
		except Exception as e:
			self.output_label.set_markup("<b>{0}</b>".format(e))

	def delta_v(self, mass: float, liquidfuel: float, use_oxidizer: bool, oxidizer: float, isp: float) -> float:
		"""
		Given initial mass, fuel levels, and specific impulse,
		return the delta v in m/s.
		Raises exceptions if the inputs are contradictory.
		"""

		def G0()                      -> float: return 9.80665
		def fuel_kg_per_liter()       -> float: return 5.0
		def liquidfuel_per_oxidizer() -> float: return 360.0 / 440.0

		dry_mass = mass
		if use_oxidizer:
			if liquidfuel < oxidizer * liquidfuel_per_oxidizer():
				oxidizer = liquidfuel / liquidfuel_per_oxidizer()
			else:
				liquidfuel = oxidizer * liquidfuel_per_oxidizer()
			dry_mass = mass - fuel_kg_per_liter() * (liquidfuel + oxidizer)
		else:
			dry_mass = mass - fuel_kg_per_liter() * liquidfuel

		if dry_mass <= 0:
			raise Exception('Fuel is heavier than the ship!')
		return G0() * isp * math.log(mass / dry_mass)

	def main(self):
		"""
		Run the window.
		"""

		Gtk.main()

DeltaVWindow().main()
