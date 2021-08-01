'''
Created on 29 ago. 2017

@author: AndresDiaz
'''
from mecanismo import mecanismo
from tinydb import TinyDB, Query
import json
from threading import Thread, Timer
import Hora_solar

class managerMecanismo(object):
    '''
    classdocs
    '''
    revisando = False
    revisar = True

    #Base de datos
    db = TinyDB('database.json')
    tasks = db.table('tasks')
    positions = db.table('positions')
    query = Query()

    mecanismo = None
    def __init__(self):
        '''
        Constructor
        '''
       
        self.mecanismo = mecanismo(self.positions, self.query)
        
        pass
    
    # Devuelve el estado del telescopio en json
    def getStatus(self):
        [abierto, cerrado, automaticMode, manualMode] = self.mecanismo.getStatus()
        return {'estado':{'abierto':abierto, 'cerrado': cerrado, 'automaticMode': automaticMode,
                                      'modoManual': manualMode
                                      }}
    def getTasks(self):
        return self.tasks.all
    def insertTask(self, task):
        self.tasks.insert(task)

    def getTask(self, iden):
        return self.tasks.search(self.query.id == iden)

    def tasksReview(self):
        self.revisar = True
        if self.revisando == False:
            self.revisando = True
            th = Thread(target = self.petitionsProcess())
            th.start()
            

    def petitionsProcess(self):
        while self.revisar:
            self.revisar = False
            for task in self.tasks.search(self.query.done == False):
                self.taskProcess(task)
        self.revisando = False
        
    def setResult(self, resultado, iden):
        print resultado
        print iden
        self.tasks.update({'resultado': resultado, 'done': True}, self.query.id == iden)

    
        
    # Identifica que debe hacer el telescopio
    def taskProcess(self, peticion):
        print('Procesar una peticion')
        # Anadimos la tarea a la base de datos
        iden = peticion['id']
        # Nos centramos en la orden a realizar
        orden = peticion['orden']
        
        resultado = False
        #Comprobamos las posibles ordenes
        if orden == 'modoAutomatico':
            resultado=self.mecanismo.setAutomaticMode()

        elif orden == 'modoManual':
            resultado=self.mecanismo.setManualMode()

        elif orden == 'Abrir':
            permiso=Hora_solar.solicitarPermiso()
            if permiso or mecanismo.manualMode:
                resultado=self.mecanismo.openCover()

        elif orden == 'Cerrar':
            resultado=self.mecanismo.closeCover()

        
            
                
                   
        # Actualizamos la tarea y finalizamos su procesamiento
        if resultado != True:
            self.setResult(resultado, iden)

        print('Final del procesado')
        return resultado
        
