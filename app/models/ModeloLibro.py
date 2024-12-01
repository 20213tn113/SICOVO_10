from .entities.Autor import Autor
from .entities.Libro import Libro

class ModeloLibro:
    
    @classmethod
    def listar_libros(self, db):
        try:
            cursor=db.connection.cursor()
            sql="""SELECT LIB.isbn, LIB.titulo, LIB.anoedicion, LIB.precio,
                    AUT.apellidos, AUT.nombres
                    FROM libro LIB JOIN autor AUT ON LIB.autor_id = AUT.id
                    ORDER BY LIB.titulo ASC"""
            cursor.execute(sql)
            data=cursor.fetchall()
            libros=[]
            for row in data:
                aut = Autor(0, row[4], row[5])
                lib = Libro(row[0], row[1], aut, row[2], row[3], None, None ,None )
                libros.append(lib)
            return libros
        except Exception as ex:
            raise Exception(ex)
    
    
    @classmethod
    def leer_libro(self, db, isbn):
        try:
            cursor=db.connection.cursor()
            sql="""SELECT isbn, titulo, anoedicion, precio
                    FROM libro WHERE isbn = '{0}'""".format(isbn)
            cursor.execute(sql)
            data = cursor.fetchone()
            libro = Libro(data[0], data[1], None, data[2], data[3], None, None ,None )
            return libro
        except Exception as ex:
            raise Exception(ex)
    
    
    @classmethod
    def listar_libros_vendidos(self, db):
        try:
            cursor=db.connection.cursor()
            sql="""SELECT COM.libro_isbn, LIB.titulo, LIB.precio,
                        COUNT(COM.libro_isbn) AS Unidades_Vendidas
                        FROM compra COM JOIN libro LIB ON COM.libro_isbn = LIB.isbn
                        GROUP BY COM.libro_isbn ORDER BY 4 DESC, 2 ASC"""
            cursor.execute(sql)
            data=cursor.fetchall()
            libros=[]
            for row in data:
                lib = Libro(row[0], row[1], None, None, row[2], None, None ,None )
                lib.unidades_vendidas = int(row[3])
                libros.append(lib)
            return libros
        except Exception as ex:
            raise Exception(ex)

    @classmethod
    def obtener_libros(self, db):
        try:
            cursor = db.connection.cursor()
            cursor.callproc('obtener_libros')
            cursor.execute( 'SELECT * FROM vistalibros;')
            data = cursor.fetchall()
            libros = []
            for row in data:
                libro = Libro(row[0], row[1], row[2], row[3], row[4],row[5],row[6],row[7])
                # print(row[0], row[1], row[2], row[3], row[4],row[5],row[6],row[7])
                libros.append(libro)
            cursor.close()
            # print(libros[Libro.isbn])
            return libros
        except Exception as ex:
            raise Exception(ex)

    @classmethod
    def insert_libro(self,db,isbn,titulo, autor_id,fecha_edi, precio, descripcion, filename):
        try:
            print("INSERT_LIBRO")
            print(filename)
            print("1")
            cursor = db.connection.cursor()
            print("2")
            sql = """INSERT INTO libro (isbn, titulo, autor_id, anoedicion, precio, descripcion, imagen_portada) 
                             VALUES (%s, %s, %s, %s, %s, %s, %s)"""
            print("3")

            cursor.execute(sql, (isbn, titulo, autor_id, fecha_edi, precio, descripcion, filename))
            print("4")
            db.connection.commit()




            # sql = """INSERT INTO libro (isbn,titulo, autor_id,anoedicion, precio, descripcion, imagen_portada) VALUES
            #                 ('{0}', '{1}', '{2}', '{3}', '{4}', {5},  {6}) """.format(isbn, titulo, autor, fecha_edi, precio, descripcion, filename)
            print("3")
            # cursor.execute(sql)
            # print("4")
            # db.connection.commit()
            return True
        except Exception as ex:
            raise Exception(ex)