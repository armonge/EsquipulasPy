# -*- coding: utf-8 -*-
'''
Created on 14/07/2010

@author: armonge
'''
from PyQt4.QtSql import QSqlQuery, QSqlDatabase
from PyQt4.QtCore import Qt, QModelIndex, QAbstractItemModel
     
class CategoryItem(object):
    def __init__(self, data, parent=None):
        self.parentItem = parent
        self.itemData = data
        self.childItems = []
        
        
    def child(self, row):
        return self.childItems[row]

    def childCount(self):
        return len(self.childItems)

    def childNumber(self):
        if self.parentItem != None:
            return self.parentItem.childItems.index(self)
        return 0

    def columnCount(self):
        return len(self.itemData)

    def data(self, column):
        if column == 1:
            print self.itemData[column]
        return self.itemData[column]

    def insertChildren(self, position, count, columns):
        if position < 0 :
            return False
        if not (self.parent() is None or self.parent().parent() is None):
            return False
        
        
        for row in range(count):
            data = columns
            if type(columns) == int:             
                query = QSqlQuery()
                try:
                    if not QSqlDatabase.database().isOpen():
                        if not QSqlDatabase.database().open():
                            raise Exception("No se pudo conectar con la base de datos")
                    if self.parentItem is None:
                        if not query.prepare("""
                        INSERT INTO categorias (nombre) VALUES ( :nombre)
                        """ ):
                            raise Exception("No se pudo preparar la consulta para insertar la categoria")
                        
                    else:
                        if not query.prepare("""
                        INSERT INTO categorias (nombre, padre) VALUES ( :nombre, %d)
                        """ % self.data(1) ):
                            raise Exception("No se pudo preparar la consulta para insertar la categoria")
                        
                    query.bindValue(":nombre", "tmp")    
                    if not query.exec_():
                        raise Exception("No se pudo insertar la categoria")
                    
                    data = ["tmp", query.lastInsertId().toInt()[0]]
                except Exception as inst:
                    print inst
                    return False
            elif data[0]==0:
                query = QSqlQuery()
                try:
                    if type(self.itemData[0])==int:
                        if not query.prepare("""
                        INSERT INTO categorias (padre, nombre) VALUES (%d, :nombre)
                        """ % self.itemData[0]):
                            raise Exception("No se pudo preparar la consulta para insertar la categoria")
                    else:
                        if not query.prepare("""
                        INSERT INTO categorias (nombre) VALUES ( :nombre)
                        """ ):
                            raise Exception("No se pudo preparar la consulta para insertar la categoria")
                    query.bindValue(":nombre", data[1].strip())
                    if not query.exec_():
                        raise Exception("No se pudo insertar la categoria")
                except Exception as inst:
                    print inst
                    return False

                
                
            item = CategoryItem(data, self)
            self.childItems.insert(position, item)
        
        return True


    def parent(self):
        return self.parentItem

    def removeChildren(self, position, count):
        if position < 0 or position + count > len(self.childItems):
            return False
        database = QSqlDatabase.database()
        query = QSqlQuery()
        try:
            if not QSqlDatabase.database().isOpen():
                if not QSqlDatabase.database().open():
                    raise Exception("No se pudo conectar con la base de datos")
            if not database.transaction():
                raise Exception("No se pudo iniciar la transacción para borrar las categorias")
            for row in range(count):
                print self.childItems[position].itemData
                if not query.exec_("DELETE FROM categorias WHERE padre = %d" % self.childItems[position].itemData[1]):
                    raise Exception("No se pudieron borrar los hijos de la categoria: %s con id: %d" % (self.childItems[position].itemData[1], self.childItems[position].itemData[1] ))
                    print query.executedQuery()
                if not query.exec_("DELETE FROM categorias WHERE idcategoria = %d" % self.childItems[position].itemData[1]):
                    raise Exception("No se pudo borrar la categoria: %s con id: %d" % (self.childItems[position].itemData[1], self.childItems[position].itemData[1] ))
                    print query.executedQuery()
                self.childItems.pop(position)
            
            if not database.commit():
                raise Exception("No se pudieron borrar las categorias")
            
            return True
        
        except Exception as inst:
            print inst
            print query.lastError().text()
            database.rollback()
            return False
    

    def setData(self, column, value):
        if column < 0:
            return False
        if column == 0:
            try:
                if not QSqlDatabase.database().isOpen():
                    if not QSqlDatabase.database().open():
                        raise Exception("No se pudo conectar con la base de datos")
                query = QSqlQuery()
                if not query.prepare("""
                UPDATE categorias SET nombre = :nombre
                WHERE idcategoria = %d 
                """ % self.itemData[1]):
                    raise Exception("No se pudo preparar la consulta para actualizar la categoria")

                query.bindValue(":nombre", value[column].strip())
                if not query.exec_():
                    raise Exception("No se pudo actualizar la categoria")
                
                
            except Exception as inst:
                print inst
                return False
            self.itemData[column] = value[column]
        return True


class CategoriesModel(QAbstractItemModel):
    def __init__(self, parent=None):
        super(CategoriesModel, self).__init__(parent)

        rootData  = ("Nombre","Id")
        self.rootItem = CategoryItem(rootData)
        if not self.setupModelData( self.rootItem):
            raise Exception("No se pudieron recuperar las categorias")

    def columnCount(self, parent=QModelIndex()):
        return 2

    def data(self, index, role):
        if not index.isValid():
            return None

        if role != Qt.DisplayRole and role != Qt.EditRole:
            return None

        item = self.getItem(index)
        return item.data(index.column())

    def flags(self, index):
        if not index.isValid():
            return 0

        return Qt.ItemIsEditable | Qt.ItemIsEnabled | Qt.ItemIsSelectable

    def getItem(self, index):
        if index.isValid():
            item = index.internalPointer()
            if item:
                return item

        return self.rootItem

    def headerData(self, section, orientation, role=Qt.DisplayRole):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return self.rootItem.data(section)

        return None

    def index(self, row, column, parent=QModelIndex()):
        if parent.isValid() and parent.column() != 0:
            return QModelIndex()

        parentItem = self.getItem(parent)
        childItem = parentItem.child(row)
        if childItem:
            return self.createIndex(row, column, childItem)
        else:
            return QModelIndex()


    def insertRows(self, position, rows, parent=QModelIndex()):
        parentItem = self.getItem(parent)
        self.beginInsertRows(parent, position, position + rows - 1)
        success = parentItem.insertChildren(position, rows, self.rootItem.columnCount())
        self.endInsertRows()

        return success

    def parent(self, index):
        if not index.isValid():
            return QModelIndex()

        childItem = self.getItem(index)
        parentItem = childItem.parent()

        if parentItem == self.rootItem:
            return QModelIndex()

        return self.createIndex(parentItem.childNumber(), 0, parentItem)


    def removeRows(self, position, rows, parent=QModelIndex()):
        parentItem = self.getItem(parent)
        
        self.beginRemoveRows(parent, position, position + rows - 1)
        success = parentItem.removeChildren(position, rows)
        self.endRemoveRows()

        return success

    def rowCount(self, parent=QModelIndex()):
        parentItem = self.getItem(parent)

        return parentItem.childCount()

    def setData(self, index, value, role=Qt.EditRole):
        if role != Qt.EditRole:
            return False

        item = self.getItem(index)
        result = item.setData(index.column(), value)

        if result:
            self.dataChanged.emit(index, index)

        return result



    def setupModelData(self,  parent):
        try:
            if not QSqlDatabase.database().isOpen():
                if not QSqlDatabase.database().open():
                    raise Exception("No se pudo conectar con la base de datos")
            parents=[parent]
            query = """
             SELECT
                 p.nombre, 
                p.idcategoria,
                COUNT(h.idcategoria) as hijos 
            FROM categorias p
            LEFT JOIN categorias h ON p.idcategoria = h.padre
            WHERE p.padre IS NULL
            GROUP BY p.idcategoria    
            """
            query = QSqlQuery(query)
            if not query.exec_():
                raise Exception("No se pudieron recuperar las categorias")
    
            x = 0
            while query.next():
                parent = parents[-1]
                parent.insertChildren(x,1,[query.value(0).toString(), query.value(1).toInt()[0]])
                
                
                if query.value(2) > 0:
                    y = 0
                    childquery =  """SELECT
                        p.nombre ,
                        p.idcategoria 
                    FROM categorias p
                    WHERE p.padre = %d 
                    """ % query.value(1).toInt()[0]
                    childquery = QSqlQuery(childquery)
                    childquery.exec_()
                    while childquery.next():
                        parent.child(x).insertChildren(y,1,[childquery.value(0).toString(), childquery.value(1).toInt()[0]])
                        
                        y +=1
                x +=1
            return True
        except Exception as inst:
            print inst
            return False

