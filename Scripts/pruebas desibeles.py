desibeles = input('Ingeres el valor en desibeles: ')

dic = {'Martillo neumatico': 130, 'Demalezadora a nafta':106, 'Alarma reloj':70, 'Tranquilo': 40}

for i in dic.keys():
    if desibeles == dic[i]:
        print(f'El ruido es de {i}')
        
if desibeles > dic['Martillo neumatico']:
    print(f'El ruido es superior al maximo de 140')
    
elif (dic['Martillo neumatico'] > desibeles > dic['Demalezadora a nafta']):
    print(f"El ruido se encuentra entre los valores de {dic['Martillo neumatico']} y {dic['Demalezadora a nafta']} db")

elif (dic['Demalezadora a nafta'] > desibeles > dic['Alarma reloj']):
    print(f'El ruido se encuentra entre los valores de {dic['Demalezadora a nafta']} y {dic['Alarma reloj']} dB')

elif (dic['Alarma reloj'] > desibeles > dic['Tranquilo']):
    print(f'El ruido se encuentra entre los valores de {dic['Alarma reloj']} y {dic['Tranquilo']} dB')

else:
    print('El valor es inferior a 40 dB, el cual corresponde a tranquilo')