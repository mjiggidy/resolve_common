import enum, typing


class FlagColors(enum.StrEnum):
	"""Available color names for flags"""

	BLUE     = "Blue"
	CYAN     = "Cyan"
	GREEN    = "Green"
	YELLOW   = "Yellow"
	RED      = "Red"
	PINK     = "Pink"
	PURPLE   = "Purple"
	FUSCHIA  = "Fuchsia"
	CREAM    = "Cream"
	COCOA    = "Cocoa"
	SAND     = "Sand"
	LEMON    = "Lemon"
	MINT     = "Mint"
	SKY      = "Sky"
	LAVENDER = "Lavender"
	ROSE     = "Rose"

	@classmethod
	def from_resolve_string(cls, flag_string:str) -> list[typing.Self]:
		"""Parse from a resolve string list"""

		if not flag_string:
			return []

		flags = []

		for color_string in flag_string.split(","):
			flags.append(cls(color_string))

		return flags

	@classmethod
	def to_resolve_string(self, flags:list[typing.Self]) -> str:

		return ",".join(f.value for f in flags)