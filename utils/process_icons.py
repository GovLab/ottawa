import os
import glob

count = 0
for icon_file in glob.glob('/Users/sahuguet/Dropbox/PardonMyIcons/*.gif'):
    data = open(icon_file).read()
    new_icon_file = open('%03d.gif' % count, 'w+')
    new_icon_file.write(data)
    new_icon_file.close()
    count = count + 1
