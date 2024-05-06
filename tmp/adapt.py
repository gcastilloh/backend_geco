import sys
import re

def adaptar_y_convertir_sql(input_file, output_file):
    try:
        with open(input_file, 'r') as file:
            lines = file.readlines()
    except FileNotFoundError:
        print(f"Error: El archivo fuente '{input_file}' no existe.")
        sys.exit(1)

    start_copy = False
    table_name = ''
    columns = ''
    
    with open(output_file, 'w') as file:
        for line in lines:
            # Omitir comandos y comentarios no deseados
            if line.startswith('SET') or line.startswith('--') or "pg_catalog" in line:
                continue
            
            # Adaptar tipos de datos SERIAL
            if 'SERIAL' in line:
                line = line.replace('SERIAL', 'INTEGER AUTOINCREMENT')
            if 'public.' in line:
                line = line.replace('public.', '')

            # Manejo del comando COPY para conversión
            if line.startswith("COPY"):
                start_copy = True
                parts = re.match(r"COPY (.+?) \((.*?)\) FROM stdin;", line)
                table_name = parts.group(1)
                columns = parts.group(2)
                continue
            elif line.startswith("\\."):
                start_copy = False
                table_name = ''
                columns = ''
                continue
            
            if start_copy:
                # Convertir datos en un comando INSERT
                data = line.strip().split('\t')
                data = ["'" + x.replace("'", "''") + "'" for x in data]  # Escapar comillas simples de manera segura
                insert_statement = f"INSERT INTO {table_name} ({columns}) VALUES ({', '.join(data)});\n"
                if r"\N" in line:
                    insert_statement = insert_statement.replace(r"'\N'", 'NULL')
                file.write(insert_statement)
            else:
                # Escribir la línea adaptada si no está en modo COPY
                file.write(line)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Uso: python adapt.py <archivo_fuente> <archivo_destino>")
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_file = sys.argv[2]

    print(f"Entrada: {input_file}")
    print(f"Salida: {output_file}")
    adaptar_y_convertir_sql(input_file, output_file)
    print(f"Archivo adaptado y convertido con éxito de {input_file} a {output_file}")
