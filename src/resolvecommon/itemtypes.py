import enum, typing

class ItemTypes(enum.StrEnum):
	"""Media pool item (clip) types"""
	
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
	FUSION_COMP = "Fusion Composition"
	FUSION_TITLE= "Fusion Title"
	REF_COMP    = "Referenced Composition"
	PHOTO_ALBUM = "Photo Album"

	@classmethod
	def from_media_pool_item(cls, media_pool_item:object) -> typing.Self:
		"""Return a type for a given Media Pool Item"""
		
		return cls(media_pool_item.GetClipProperty("Type"))