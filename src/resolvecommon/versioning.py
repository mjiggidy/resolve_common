import logging
import dataclasses, enum, typing, re

from . import itemtypes
from .session import resolve
from . import versioning


try:
	project = resolve.GetProjectManager().GetCurrentProject()
except Exception as e:
	logging.getLogger(__name__).critical("No project loaded: %s", str(e))

PAT_REEL_NAME = re.compile(r"^\s*(?P<show_name>.+)\s+REEL\s+(?P<reel_number>\d+)\s+v(?P<reel_version>[\d\.]+)", re.I)

class ReelNameError(ValueError):
	"""Invalid reel name given"""

class ReelVersionExistsError(FileExistsError):
	"""A reel with this version already exists"""

class VersionParts(enum.Enum):
	"""The parts of a Version"""
	
	MAJOR = enum.auto()
	"""Major version number (milestone)"""

	MINOR = enum.auto()
	"""Minor version number (length changes)"""

	PATCH = enum.auto()
	"""Patch version number (no length changes)"""

@dataclasses.dataclass(frozen=True)
class Version:
	
	major:int
	"""Major version number (milestone)"""

	minor:int = 0
	"""Minor version number (length changes)"""
	
	patch:int = 0
	"""Patch version number (no length changes)"""

	@classmethod
	def from_version_string(cls, version_string:str, /, delimiter:str=".") -> typing.Self:
		"""Parse a Version from a string"""
		
		version_parts  = [int(v) for v in version_string.split(delimiter)]
		version_padded = (version_parts + ([0]*3))[:3] # Pad parts with 0
		
		return cls(*version_padded)
	
	def to_version_string(self, /, delimiter:str=".") -> str:
		"""Format the Version as a string"""
		
		version_string = str(self.major) + delimiter + str(self.minor)

		if self.patch:
			version_string += delimiter + str(self.patch)
		
		return version_string
	
	def next_version(self, version_part:VersionParts=VersionParts.MAJOR) -> typing.Self:
		"""Increment the version number for a given part"""
		
		if version_part is VersionParts.MAJOR:
			return dataclasses.replace(self, major=self.major + 1, minor=0, patch=0)
		
		elif version_part is VersionParts.MINOR:
			return dataclasses.replace(self, minor=self.minor + 1, patch=0)
		
		elif version_part is VersionParts.PATCH:
			return dataclasses.replace(self, patch=self.patch + 1)
		
		else:
			raise ValueError(f"Invalid VersionPart: {repr(version_part)}")
		
	def parts(self) -> list[int]:
		"""Return the version parts as a list [major, minor, patch]"""
		
		return [self.major, self.minor, self.patch]
	
	def __str__(self) -> str:
		
		return self.to_version_string()
	
	def __lt__(self, other):
		
		if not isinstance(other, type(self)):
			raise TypeError
		
		return self.parts() < other.parts()


def build_next_reel_version_name(current_reel_name:str, /, version_part:VersionParts=VersionParts.MAJOR) -> str:
	"""Given the name of a reel, return a name with the next version"""

	# TODO: Maybe just pass a version and reformat for that

	reel_info = PAT_REEL_NAME.match(current_reel_name)

	if not reel_info:
		raise ReelNameError(f"Clip name not recognized as a valid reel name: {current_reel_name}")

	current_version_info = Version.from_version_string(reel_info.group("reel_version"))
	next_version_info    = current_version_info.next_version(version_part)

	next_version_clip_name = f"{reel_info.group("show_name")} REEL {reel_info.group("reel_number")} v{next_version_info}"

	return next_version_clip_name


def version_up_reel_timeline(current_timeline, /, version_part:VersionParts=VersionParts.PATCH):
	"""Given a reel timeline, duplicate it and version up"""

	current_timeline_name = current_timeline.GetName()
	next_timeline_name    = build_next_reel_version_name(current_timeline_name, version_part=version_part)

	if get_timeline_by_name(next_timeline_name):
		raise ReelVersionExistsError(f"Next version already exists: {next_timeline_name} (there can be only one)")

	next_timeline = current_timeline.DuplicateTimeline(next_timeline_name)

	if not next_timeline:
		raise RuntimeError(f"Resolve failed to duplicate timeline as {next_timeline_name}")

	return next_timeline


def version_up_selected_reels(version_part=versioning.VersionParts.PATCH):
	
	selected_items = project.GetMediaPool().GetSelectedClips()

	if not selected_items:

		logging.getLogger(__name__).info("No clips were selected.  Nothing to do.")
		return 1

	for item in selected_items:
		
		current_item_name = item.GetName()
		current_item_type = itemtypes.ItemTypes.from_media_pool_item(item)

		if not current_item_type is itemtypes.ItemTypes.TIMELINE:
		
			logging.getLogger(__name__).error("Skipping %s: Expected %s type, got %s", current_item_name, itemtypes.ItemTypes.TIMELINE, current_item_type)
			continue

		current_timeline = get_timeline_by_name(current_item_name)

		if not current_timeline:
			
			logging.getLogger(__name__).error("Skipping %s: Could not find timeline in current project...", current_item_name)
			continue
		
		try:
			versioned_up_timeline = versioning.version_up_reel_timeline(current_timeline, version_part)
		
		except Exception as e:
			
			logging.error("Skipping %s: %s", current_item_name, str(e))
			continue

		logging.getLogger(__name__).info("Successfully incremented %s to %s", current_item_name, str(versioned_up_timeline.GetName()))

def get_timeline_by_name(timeline_name:str) -> object:
	"""Find a timeline by name"""
	
	# Boy is this dumb
	
	for timeline in map(project.GetTimelineByIndex, range(1, project.GetTimelineCount()+1)):

		if timeline.GetName() == timeline_name:
			return timeline
		
def get_folder_by_path_elements(elements:list[str], root_folder:object|None=None) -> object:
	
	current_folder = root_folder or project.GetMediaPool().GetRootFolder()

	if not elements:
		return current_folder
	
	element = elements[0]

	for subfolder in current_folder.GetSubFolderList():
		
		if subfolder.GetName() == element:
			
			return get_folder_by_path_elements(elements[1:], subfolder)
	
	raise FileNotFoundError("Media pool folder was not found")

def get_latest_reel_version(reel_items:list[object]):
	
	valid_reels = filter(lambda r: PAT_REEL_NAME.match(r.GetName()), reel_items)

	if not valid_reels:
		return None

	return sorted(valid_reels, key=lambda r: Version.from_version_string(PAT_REEL_NAME.match(r.GetName()).group("reel_version")), reverse=True)[0]