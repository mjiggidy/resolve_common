import re

PAT_CAMERA_REEL_NAMES = {
	"Alexa 265"  : re.compile(r"^(?P<cam_letter>[a-z])_(?P<cam_card>[0-9]{4})C(?P<clip_number>[0-9]{3})_(?P<date>[0-9]{6})_(?P<unknown>[0-9]{6})_(?P<cam_id>[0-9a-z]{5})$", re.I),
	"Alexa Mini" : re.compile(r"^(?P<cam_letter>[a-z])(?P<cam_card>[0-9]{3})C(?P<clip_number>[0-9]{3})_(?P<date>[0-9]{6})_(?P<cam_id>[a-z0-9]{4})$", re.I),
	"RED"        : re.compile(r"^(?P<cam_letter>[a-z])(?P<cam_card>[0-9]{3})_C(?P<clip_number>[0-9]{3})_(?P<date>[0-9]{4})(?P<cam_id>[a-z0-9]{2})$", re.I),
	"DJI Inspire": re.compile(r"^(?P<cam_letter>[a-z])(?P<cam_card>[0-9]{3})C(?P<clip_number>[0-9]{4})_(?P<date>[0-9]{6})_(?P<cam_id>[a-z0-9]{6})$", re.I),
}