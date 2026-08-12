"""
session.py - Unified DaVinci Resolve API Environment Handler
Supports both internal Workflow Integration execution and external execution.
"""

import sys, logging

def _get_resolve_session():
	
	import __main__

	# Check for injected thingies
	existing_session = [
		getattr(__main__, "bmd",     None),
		getattr(__main__, "resolve", None),
		getattr(__main__, "fusion",  None),
	]

	if all(existing_session):

		logging.getLogger(__name__).debug("Found existing resolve session")
		return tuple(existing_session)

	# Check globals just in case
	globals_dict = globals()
	existing_globals = [
		globals_dict.get("bmd"),
		globals_dict.get("resolve"),
		globals_dict.get("fusion"),
	]

	if all(existing_globals):

		logging.getLogger(__name__).debug("Found existing globals")
		return tuple(existing_globals)

	# lol I dunno let"s import it then

	logging.getLogger(__name__).debug("Internal DaVinci Resolve environment not detected. Initializing external connection...")
	
	try:
		import DaVinciResolveScript as bmd
		logging.getLogger(__name__).debug("Imported module from PYTHONPATH")

	except ImportError:

		# NOTE: I don"t know if I really wanna go this far... like... read the Resolve installation documentation bro.  But anyway....
		
		if sys.platform.startswith("darwin"):
			expected_path = "/Library/Application Support/Blackmagic Design/DaVinci Resolve/Developer/Scripting/Modules/"

		elif sys.platform.startswith("win"): # or sys.platform.startswith("cygwin"):
			import os
			expected_path = os.getenv("PROGRAMDATA") + "\\Blackmagic Design\\DaVinci Resolve\\Support\\Developer\\Scripting\\Modules\\"

		elif sys.platform.startswith("linux"):
			expected_path = "/opt/resolve/Developer/Scripting/Modules/"
		else:
			expected_path = ""

		# Manually inject the path to sys.path to discover the module
		if expected_path and expected_path not in sys.path:
			sys.path.append(expected_path)
		
		try:
			import DaVinciResolveScript as bmd
			logging.getLogger(__name__).debug("Imported module from expected file path")

		except ImportError as ex:
			raise ImportError(f"Error: Unable to find or import module `DaVinciResolveScript`.  Was not found in {expected_path}.") from ex

	resolve = bmd.scriptapp("Resolve")
	fusion  = bmd.scriptapp("Fusion")

	return bmd, resolve, fusion


# Unpack the variables at the module level
bmd, resolve, fusion = _get_resolve_session()