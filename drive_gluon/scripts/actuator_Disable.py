import innfos
guid = [0x01,0x02,0x03,0x04,0x05,0x06]
if(innfos.handshake() == 1):
    print('Actuator Connec Dectect')
    actNum = innfos.queryID(0x06)
    print('Actuator is connect: '+str(len(actNum)))
    print('Please wait for Disable Actuator...')
    if(innfos.disableact(guid)):
        print('Successfully...')
else :
    print('Actuator Not Connected')

