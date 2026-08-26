import enum, typing

class ItemTypes(enum.StrEnum):
	
	VIDEO       = "Video"
	AUDIO       = "Audio"
	VIDEO_AUDIO = "Video + Audio"
	STILL       = "Still"
	MULTICAM    = "Multicam"
	TIMELINE    = "Timeline"
	COMPOUND    = "Compound"
	MATTE       = "Matte"
	REF_CLIP    = "Ref Clip"
	STEREO      = "Stereo"
	VFX_CONNECT = "VFX Connect"
	GENERATOR   = "Generator"
	FUSION      = "Fusion"
	REF_COMP    = "Referenced Composition"
	PHOTO_ALBUM = "Photo Album"

	@classmethod
	def from_media_pool_item(cls, item) -> typing.Self:
		"""Return a type for a given Media Pool Item"""
		
		return cls(item.GetClipProperty("Type"))