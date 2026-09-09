from __future__ import annotations
from os import PathLike
import logging, typing

from .itemtypes import ItemTypes

if typing.TYPE_CHECKING:
	import DaVinciResolveScript as bmd

def get_folder_from_path(path:PathLike[str], root_folder):
	
	current_folder = root_folder
	
	for search_folder_name in path.strip("/").split("/"):
		
		logging.getLogger(__name__).debug("In \"%s\" looking for \"%s\"", current_folder.GetName(), search_folder_name)
		
		try:
			current_folder = next(f for f in current_folder.GetSubFolderList() if f.GetName() == search_folder_name)
		except StopIteration:
			logging.getLogger(__name__).debug("Did not find \"%s\" in \"%s\"", search_folder_name, current_folder.GetName())
			raise FileNotFoundError(f"{search_folder_name} not in {current_folder.GetName()}")
		
		logging.getLogger(__name__).debug("Found \"%s\" in \"%s\"", search_folder_name, current_folder.GetName())
	
	return current_folder

def get_clips_from_folder_by_type(folder:bmd.Folder, clip_types:list[ItemTypes]|None=None, recursive:bool=False, ignore_folder:bmd.Folder|None=None):
	
	if ignore_folder and folder == ignore_folder:
		yield StopIteration

	clip_types = clip_types or ItemTypes
	
	yield from filter(lambda c: ItemTypes.from_media_pool_item(c) in clip_types, folder.GetClipList())

	if recursive:
		for subfolder in folder.GetSubFolderList():
			yield from get_clips_from_folder_by_type(subfolder, clip_types, recursive, ignore_folder=ignore_folder)