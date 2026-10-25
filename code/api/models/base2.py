# import json
# import os
# from datetime import datetime, timezone

# class Actions:
    
#     DATA_FILE = ""  # het pad van het bestand op een manier
#     DEBUG_DATA = None 
    
#     def __init__(self, root_path, is_debug=False):
#         self.data_path = os.path.join(root_path, self.DATA_FILE)
#         self.data = []
#         self.load(is_debug)

#     def load(self, is_debug):
#         if is_debug:
#             self.data = self.DEBUG_DATA if self.DEBUG_DATA is not None else []
#         else:
#             with open(self.data_path, "r") as f:
#                 self.data = json.load(f)
    
    