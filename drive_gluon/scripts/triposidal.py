import time
import sys
import innfos

### 1 = 10deg
actuID = [0x01, 0x02, 0x03, 0x04, 0x05, 0x06]
innfos.trapposmode(actuID)
innfos.trapposset(actuID, [1.5, 1.5, 1.5, 1.5, 1.5, 1.5], [.075, .075, .075, .075, .075, .075], [-1.5, -1.5, -1.5, -1.5, -1.5, -1.5])

time.sleep(0.5)

print(innfos.setpos(actuID,[0, 0, 0, 0,0, 0]))


