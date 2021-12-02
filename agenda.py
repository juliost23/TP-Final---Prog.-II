from PyQt5.QtWidgets import QMainWindow, QApplication, QTableWidgetItem, QMessageBox
from PyQt5 import uic
import sqlite3


class MiVentana(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("tabla.ui", self)
        
        self.conexion = sqlite3.connect('agenda.db')
        self.cursor = self.conexion.cursor()
        self.operacion=''
        
        self.nuev.clicked.connect(self.agregar_contacto)
        self.delet.clicked.connect(self.eliminar_contacto)
        self.edit.clicked.connect(self.editar_contacto)
        self.cancel.clicked.connect(self.cancelar_cambios)
        self.acept.clicked.connect(self.aceptar_cambios)
        self.list.itemClicked.connect(self.clicks)
      
        
        self.cursor.execute('select * from contactos')
        
      
  #  lista BASE
        for i in self.cursor:
            self.id = str(i[0]) 
            self.nombre = str(i[1])
            self.apellido = str(i[2])
            
            self.list.addItem(self.id + " - " +self.nombre + ", " + self.apellido )     
    
    #BOTONES ACTIVOS E INACTIVOS
    def habilitar_desabilitar(self):            
        self.nuev.setEnabled(True)   
        self.edit.setEnabled(False)
        self.cancel.setEnabled(False)
        self.delet.setEnabled(False)
        self.acept.setEnabled(False)
        
        self.nombres.setEnabled(False)
        self.apellidos.setEnabled(False)
        self.emails.setEnabled(False)
        self.tel.setEnabled(False)
        self.direc.setEnabled(False)
        self.fecha_na.setEnabled(False)
        self.altur.setEnabled(False) 
        self.pes.setEnabled(False)
        
        self.nombres.setText('')
        self.apellidos.setText('')
        self.emails.setText('')
        self.tel.setText('')
        self.direc.setText('')
        self.fecha_na.setText('')
        self.altur.setText('')
        self.pes.setText('')
        
# HABILITA BOTONES PARA TRABAJAR CON LA OPERACIÓN AGREGAR_CON
    def agregar_contacto(self):
        self.operacion='Agregar_con'
        self.edit.setEnabled(False)
        self.cancel.setEnabled(True)
        self.nuev.setEnabled(False)
        self.nombres.setEnabled(True)
        self.apellidos.setEnabled(True)
        self.emails.setEnabled(True)
        self.tel.setEnabled(True)
        self.direc.setEnabled(True)
        self.fecha_na.setEnabled(True)
        self.altur.setEnabled(True) 
        self.pes.setEnabled(True)
        self.acept.setEnabled(True) 
        self.nombres.setText('')
        self.apellidos.setText('')
        self.emails.setText('')
        self.tel.setText('')
        self.direc.setText('')
        self.fecha_na.setText('')
        self.altur.setText('')
        self.pes.setText('')
        
#-----------------------------------------------------------#        
    
    def clicks(self):
        self.edit.setEnabled(True)
        self.cancel.setEnabled(True)
        self.nuev.setEnabled(True)
        self.acept.setEnabled(False)
        self.delet.setEnabled(True)
        self.conexion = sqlite3.connect('agenda.db')
        self.cursor = self.conexion.cursor()
        ind= self.list.currentItem().text()
        
        separador = ("-")
        contacto = ind.split(separador, 1)
        self.id_contacto=contacto[0]
        self.n_contacto=contacto[1]
        self.cursor.execute("select * from contactos  WHERE id = " + self.id_contacto)
        for i in self.cursor:
            
            self.nombres.setText(str(i[1]))
            self.apellidos.setText(str(i[2]))
            self.emails.setText(str(i[3]))
            self.tel.setText(str(i[4]))
            self.direc.setText(str(i[5]))
            self.fecha_na.setText(str(i[6])) 
            self.altur.setText(str(i[7])) 
            self.pes.setText(str(i[8])) 
            
           
    def editar_contacto(self):
        self.operacion='editar_con'
        self.nuev.setEnabled(False)
        self.delet.setEnabled(False)
        self.acept.setEnabled(True) 
        self.nombres.setEnabled(True)
        self.apellidos.setEnabled(True)
        self.emails.setEnabled(True)
        self.tel.setEnabled(True)
        self.direc.setEnabled(True)
        self.fecha_na.setEnabled(True)
        self.altur.setEnabled(True) 
        self.pes.setEnabled(True)
        
    def eliminar_contacto(self):
        self.conexion = sqlite3.connect('agenda.db')
        self.cursor = self.conexion.cursor()
        ret = QMessageBox.question (self, 'Quitar Contacto' , "Desea Quitar el contacto? '"+self.n_contacto+"'  Ok para confirmar" , QMessageBox.Ok | QMessageBox.No | QMessageBox.Cancel, QMessageBox.Cancel)
        if ret == QMessageBox.Ok: 
                self.cursor.execute("DELETE FROM contactos  WHERE id = " + self.id_contacto)
                self.conexion.commit()
                self.list.clear()
                self.cursor = self.conexion.cursor()
                self.cursor.execute('select * from contactos')
            # Se agregan los elementos al QListWidget
                for i in self.cursor:
                    self.id = str(i[0]) 
                    self.nombre = str(i[1])
                    self.apellido = str(i[2])
                    self.list.addItem(self.id + " - " +self.nombre + ", " + self.apellido ) 
        self.habilitar_desabilitar()
        
             
    
    def aceptar_cambios(self):  
        self.nombre = self.nombres.text()
        self.apellido = self.apellidos.text()
        self.email = self.emails.text()
        self.telefono = self.tel.text()
        self.direccion = self.direc.text()
        self.fecha_nac = self.fecha_na.text()
        self.altura = self.altur.text()
        self.peso = self.pes.text()
        
        if self.nombre=='' or self.apellido=='' :
            QMessageBox.information(self, '¡Atención!', "Ingresa Apellido y Nombre  ",QMessageBox.Ok)
       
            
        else:  
            self.conexion = sqlite3.connect('agenda.db')
            self.cursor = self.conexion.cursor()
                    
            
            if self.operacion=='Agregar_con':
                ret = QMessageBox.question (self, 'Agregar Contacto' , "Ok para Agendar" , QMessageBox.Ok | QMessageBox.No | QMessageBox.Cancel, QMessageBox.Cancel)
                if ret == QMessageBox.Ok: 
                    
                    self.cursor.execute("INSERT INTO contactos(nombre,apellido,email,telefono,direccion,fecha_nac,altura,peso) VALUES ('"+self.nombre+"','"+self.apellido+"','"+self.email+"', '"+self.telefono+"','"+self.direccion+"','"+self.fecha_nac+"','"+self.altura+"','"+self.peso+"')")
                        
                    self.conexion.commit() 
                    
                
            if self.operacion=='editar_con':
                ret = QMessageBox.question (self, 'Editar Contacto' , "Ok para guardar cambios" , QMessageBox.Ok | QMessageBox.No | QMessageBox.Cancel, QMessageBox.Cancel)
                if ret == QMessageBox.Ok: 
                    
                        
                    self.cursor.execute("UPDATE contactos SET nombre='"+self.nombre+"', apellido='"+self.apellido+"', email='"+self.email+"', telefono='"+self.telefono+"',direccion='"+self.direccion+"',fecha_nac='"+self.fecha_nac+"',altura='"+self.altura+"',peso='"+self.peso+"' WHERE id = " + self.id_contacto)
                    self.conexion.commit()
                    
                
                    
            if ret == QMessageBox.Ok:  
                self.list.clear()
                self.cursor = self.conexion.cursor()
                self.cursor.execute('select * from contactos')
                    # Se agregan los elementos al QListWidget
                for i in self.cursor:
                        self.id = str(i[0]) 
                        self.nombre = str(i[1])
                        self.apellido = str(i[2])
                        self.list.addItem(self.id + " - " +self.nombre + " - " + self.apellido ) 
            self.habilitar_desabilitar()
            

         
             
    def cancelar_cambios(self):
        self.habilitar_desabilitar()
           
        

app = QApplication([])
win = MiVentana()
win.show()
app.exec_()



