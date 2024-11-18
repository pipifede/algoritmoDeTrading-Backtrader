import pandas as pd
import csv
def transformar_y_eliminar_comillas(input_file, output_file):
    # Leer el archivo CSV original
    df = pd.read_csv(input_file)
    
    # Seleccionar solo las columnas que necesitamos
    df = df[["Date", "Open", "High", "Low", "Close", "Volume"]]
    
    # Convertir la columna 'Date' al formato requerido: 'YYYY-MM-DD'
    df['Date'] = pd.to_datetime(df['Date']).dt.strftime('%Y-%m-%d')
    df['Volume'] = df['Volume'].replace({',': ''}, regex=True).astype(int)
    # Crear la columna 'Adj Close' igual a 'Close'
    df['Adj Close'] = df['Close']
    
    # Reordenar las columnas según el formato requerido
    df = df[["Date", "Open", "High", "Low", "Close", "Adj Close", "Volume"]]
    
    # Guardar el archivo en formato CSV
    df.to_csv(output_file, index=False)
    
    print(f"Archivo transformado y guardado en: {output_file}")

instrumento = "YPF.F" 
transformar_y_eliminar_comillas(f"./Data/-{instrumento}.csv", f"./Data/{instrumento}.csv")
    
