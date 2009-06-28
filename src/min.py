import sndobj
import time

jack = sndobj.SndJackIO('vizi')
thread = sndobj.SndThread()
thread.AddObj(jack, sndobj.SNDIO_OUT)
thread.ProcOn()
time.sleep(5)
