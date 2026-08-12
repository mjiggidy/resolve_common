import enum

class TrackTypes(enum.StrEnum):
	"""Track types in a timeline"""
	
	VIDEO       = "video"
	AUDIO       = "audio"
	SUBTITLE    = "subtitle"