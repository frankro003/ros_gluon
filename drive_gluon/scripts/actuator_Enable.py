import innfos
guid = [0x01,0x02,0x03,0x04,0x05,0x06]
if(innfos.handshake() == 1):
    print('Actuator Connec Dectect')
    actNum = innfos.queryID(0x06)
    print('Actuator is connect: '+str(len(actNum)))
    print('Please wait for Enable Actuator...')
    if(innfos.enableact(guid)):
        print('Successfully...')
        innfos.trapposmode(guid)
        print(innfos.readpos(guid))
else :
    print('Actuator Not Connected')
