# import win32api
# import win32file
# import os
# import datetime
#
# my_drive = []
# DRIVE_REMOVABLE = 2
# drives = win32api.GetLogicalDriveStrings().split('\000')[::-1]
# for item in drives:
#     if win32file.GetDriveType(item) == DRIVE_REMOVABLE:
#         my_drive.append(item)
# if my_drive:
#     for item in my_drive:
#         if win32api.GetVolumeInformation(item[0:3])[0] == 'OSIPOV':
#             print(drives)