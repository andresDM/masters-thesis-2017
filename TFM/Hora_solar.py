import ephem
from datetime import datetime

def solicitarPermiso():

	Permiso_apertura = False

	observatorio = ephem.Observer()
	observatorio.lat, observatorio.lon = '40.406161', '-3.838485'


	 
	i = datetime.utcnow()
	 
	hora = i.strftime('%H:%M:%S')

	observatorio.date = i


	h_amanecer = observatorio.previous_rising(ephem.Sun())
	h_anochecer = observatorio.next_setting(ephem.Sun())
	"""h_Luna = observatorio.previous_rising(ephem.Moon())
	h_anochecer2 = observatorio.next_setting(ephem.Moon())"""

	#Calcular twilight
	observatorio.horizon = '-18'
	h_PrimeraLuz = observatorio.previous_rising(ephem.Sun(), use_center=True)
	h_UltimaLuz = observatorio.next_setting(ephem.Sun(), use_center=True)

        #Pasamos a segundos totales
        #hora_secsTot=int(hora)
        #h_UltimaLuz_secsTot=int(h_UltimaLuz.strftime('%s'))
        #h_PrimeraLuz_secsTot=int(h_PrimeraLuz.strftime('%s'))
	if hora > h_UltimaLuz and hora < h_PrimeraLuz:
	
		Permiso_apertura = True


	print h_amanecer, h_PrimeraLuz
	print h_anochecer, h_UltimaLuz

	print hora, Permiso_apertura

	return Permiso_apertura
