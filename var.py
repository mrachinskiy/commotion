# ##### BEGIN GPL LICENSE BLOCK #####
#
#  Commotion motion graphics add-on for Blender.
#  Copyright (C) 2014-2020  Mikhail Rachinskiy
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
ADDON_CONFIG_DIR = ADDON_DIR


# mod_update
# --------------------------------


UPDATE_OPERATOR_ID_AFFIX = "commotion"
UPDATE_SAVE_STATE_FILEPATH = os.path.join(ADDON_CONFIG_DIR, "update_state.json")
UPDATE_URL_RELEASES = "https://api.github.com/repos/mrachinskiy/commotion/releases"
UPDATE_VERSION_CURRENT = None
UPDATE_VERSION_MAX = None

update_available = False
