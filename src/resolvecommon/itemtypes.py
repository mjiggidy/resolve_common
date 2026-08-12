import enum, typing

class ItemTypes(enum.StrEnum):
	
	TIMELINE    = "Timeline"
	VIDEO       = "Video"
	AUDIO       = "Audio"
	COMPOUND    = "Compound"
	MULTICAM    = "Multicam"
	VIDEO_AUDIO = "Video + Audio"
	FUSION      = "Fusion"

	@classmethod
	def from_media_pool_item(cls, item) -> typing.Self:
		"""Return a type for a given Media Pool Item"""
		
		return cls(item.GetClipProperty("Type"))