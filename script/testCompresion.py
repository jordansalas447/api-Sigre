
from PIL import Image
import pyodbc 
import os

server = 'DESKTOP-54E82UI' 
database = 'sigre' 
username = 'sa' 
password = '3142' 
# ENCRYPT defaults to yes starting in ODBC Driver 18. It's good to always specify ENCRYPT=yes on the client side to avoid MITM attacks.
cnxn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+server+';DATABASE='+database+';Trusted_Connection=yes;UID='+username+';PWD='+ password)
cursor = cnxn.cursor()


def reduce_file_seal(cod_alimentador):
    base_path = "E:/PruebaCompress"  # Reemplaza con tu ruta base
    cursor.execute(" exec sp_ArchivosPorAlimentador " + str(cod_alimentador)) 
    folder = cursor.fetchone() 

    ancho = 800
    alto = 1067

    while folder: 
        path = os.path.join(base_path, folder[0])

        if os.path.isdir(path):
            files = os.listdir(path)

            for file in files:
                file_path = os.path.join(path, file)
             
                # Realizar la compresión de la imagen aquí
                # Puedes usar la biblioteca PIL para esto

                with Image.open(file_path) as img:
                     img_resized = img.resize((ancho, alto))
                     nueva_ruta = os.path.join(path, f"{file}")
                     print(path)
                     ruta_padre = os.path.dirname(path)
                     print(ruta_padre)
                     ruta_obsoluta = os.path.abspath(ruta_padre)
                     print(ruta_obsoluta)
                     img_resized.save(os.path.join(ruta_obsoluta,f"{file}"))
                     img.close()
                     

                # Eliminar el archivo original                              
                os.remove(file_path)
            # Eliminar el directorio vacío
            #os.rmdir(path)

            print(path)
        folder = cursor.fetchone() 

    print("Operacion finalizada")

  

if __name__=="__main__":
    reduce_file_seal(63)