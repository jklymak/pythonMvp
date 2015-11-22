import time
import os
while 1:
    str= "rsync -av /Volumes/DC15b/ /Users/jklymak/DC15b/mvp/data/"
    print "Running " + str
    os.system(str)
    print "Done: sleeping 60 s"
    for i in range(3,60,3):
        print('.'),
        time.sleep(3)
