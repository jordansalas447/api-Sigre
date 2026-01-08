
from copy import copy
import xlsxwriter

def copiar_formato(hoja,origen, row_destino,column_destino):
    for fila in origen:
        for celda in fila:
            destino_celda = hoja.cell(row=celda.row+row_destino, column=celda.column+column_destino)
            destino_celda.font = copy(celda.font)
            destino_celda.fill = copy(celda.fill)
            destino_celda.border = copy(celda.border)
            destino_celda.alignment = copy(celda.alignment)
            destino_celda.number_format = copy(celda.number_format)
            destino_celda.protection = copy(celda.protection)
            
def copiar(hoja,origen,row_destino,column_destino):
    for fila in origen:
        for celda in fila:
            destino_celda = hoja.cell(row=celda.row+row_destino, column=celda.column+column_destino)
            destino_celda.value = copy(celda.value)
            destino_celda.font = copy(celda.font)
            destino_celda.fill = copy(celda.fill)
            destino_celda.border = copy(celda.border)
            destino_celda.alignment = copy(celda.alignment)
            destino_celda.number_format = copy(celda.number_format)
            destino_celda.protection = copy(celda.protection)
            
def Unirceldas(hoja,Col1,Row1,Col2,Row2):
    Colum = xlsxwriter.utility.xl_col_to_name(Col1)
    Colum2 = xlsxwriter.utility.xl_col_to_name(Col2)
    hoja.merge_cells(Colum+str(Row1)+':'+Colum2+str(Row2))
    
def ConvertirNoneto0(value):
    if value is None:
        value = 0
        return value
    return value