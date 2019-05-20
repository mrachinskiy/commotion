# ##### BEGIN GPL LICENSE BLOCK #####
#
#  Commotion motion graphics add-on for Blender.
#  Copyright (C) 2014-2019  Mikhail Rachinskiy
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <https://www.gnu.org/licenses/>.
#
# ##### END GPL LICENSE BLOCK #####


import os


ADDON_ID = __package__
ADDON_DIR = os.path.dirname(__file__)


# mod_update
# --------------------------------


UPDATE_OPERATOR_ID_AFFIX = "commotion"
UPDATE_SAVE_STATE_FILEPATH = os.path.join(ADDON_DIR, "update_state.json")
UPDATE_RELEASES_URL = "https://api.github.com/repos/mrachinskiy/commotion/releases"
UPDATE_MAX_VERSION = None
UPDATE_CURRENT_VERSION = None

update_available = False
update_in_progress = False
update_completed = False
update_days_passed = None
update_version = ""
update_download_url = ""
update_html_url = ""
