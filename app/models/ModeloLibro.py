from .entities.Autor import Autor
from .entities.Libro import Libro

class ModeloLibro:
    
    @classmethod
    def listar_libros(self, db):
        try:
            cursor=db.connection.cursor()
            sql="""SELECT LIB.isbn, LIB.titulo, LIB.anoedicion, LIB.precio,
                    AUT.apellidos, AUT.nombres, LIB.imagen_portada
                    FROM libro LIB JOIN autor AUT ON LIB.autor_id = AUT.id
                    ORDER BY LIB.titulo ASC"""
            cursor.execute(sql)
            data=cursor.fetchall()
            libros=[]
            for row in data:
                aut = Autor(0, row[4], row[5])
                lib = Libro(row[0], row[1], aut, row[2], row[3], None, row[6] ,None )
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
            print("Listar_libros_vendidos")
            cursor = db.connection.cursor()
            sql = """SELECT COM.libro_isbn, LIB.titulo, LIB.precio,
                                    COUNT(COM.libro_isbn) AS Unidades_Vendidas
                                    FROM compra COM JOIN libro LIB ON COM.libro_isbn = LIB.isbn
                                    GROUP BY COM.libro_isbn ORDER BY 4 DESC, 2 ASC"""
            cursor.execute(sql)
            data = cursor.fetchall()
            print("2")
            libros = []
            for row in data:
                lib = Libro(row[0], row[1], None, None, row[2], None, None, None)
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
            cursor = db.connection.cursor()
            sql = """INSERT INTO libro (isbn, titulo, autor_id, anoedicion, precio, descripcion, imagen_portada) 
                             VALUES (%s, %s, %s, %s, %s, %s, %s)"""

            cursor.execute(sql, (isbn, titulo, autor_id, fecha_edi, precio, descripcion, filename))
            db.connection.commit()

            return True
        except Exception as ex:
            raise Exception(ex)

    @classmethod
    def insert_autor(self, db,nombre_autor,apellido_autor,fecha_nacimiento):
        try:
            cursor = db.connection.cursor()
            sql = """INSERT INTO autor (apellidos, nombres, fechanacimiento) 
                                        VALUES (%s, %s, %s)"""

            cursor.execute(sql, (apellido_autor, nombre_autor, fecha_nacimiento))
            db.connection.commit()
            nuevo_id = cursor.lastrowid

            return nuevo_id
        except Exception as ex:
            raise Exception(ex)

    @classmethod
    def borrarlibro(self, db, isbn):
        try:
            cursor = db.connection.cursor()
            sql = """DELETE FROM libro WHERE isbn = %s"""
            cursor.execute(sql, (isbn,))
            db.connection.commit()

            return True
        except Exception as ex:
            raise Exception(ex)

    @classmethod
    def cargarlibro(self, db, isbn):
        try:
            cursor = db.connection.cursor()
            sql = """SELECT * FROM libro WHERE isbn = %s"""
            cursor.execute(sql, (isbn,))
            libro = cursor.fetchone()
            if libro:
                return libro  # Devuelve la tupla del libro encontrado
            return None  # Si no se encuentra el libro, retorna None
        except Exception as ex:
            raise Exception(f"Error al cargar el libro: {str(ex)}")

    @classmethod
    def editarS(self, db, isbn, titulo, autor_id, fecha_edi, precio, descripcion,isbn_org):
        try:
            print("Update sin imagen")
            cursor = db.connection.cursor()
            print("ISBN", isbn)
            print("ISBN_org", isbn_org)


            sql = """UPDATE libro SET isbn = %s, titulo = %s,autor_id = %s,anoedicion = %s,precio = %s,descripcion = %s 
                    WHERE isbn = %s"""

            cursor.execute(sql, (isbn,titulo, autor_id, fecha_edi, precio, descripcion,isbn_org))
            db.connection.commit()

            return True
        except Exception as ex:
            raise Exception(ex)

    @classmethod
    def editarC(self, db, isbn, titulo, autor_id, fecha_edi, precio, descripcion, filename,isbn_org):
        try:
            print("Update con imagen")
            cursor = db.connection.cursor()
            print("ISBN", isbn)
            print("ISBN_org", isbn_org)
            sql = """UPDATE libro SET isbn = %s, titulo = %s,autor_id = %s,anoedicion = %s,precio = %s,descripcion = %s,imagen_portada = %s 
                                WHERE isbn = %s"""

            cursor.execute(sql, (isbn, titulo, autor_id, fecha_edi, precio, descripcion, filename,isbn_org))
            db.connection.commit()

            return True
        except Exception as ex:
            raise Exception(ex)