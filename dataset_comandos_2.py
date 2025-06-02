import csv
import random

# Dataset con comandos COMPLETOS incluyendo parámetros
commands_with_parameters = [
    # CD con diferentes parámetros
    ["cd ..", "Ir a la carpeta anterior"],
    ["cd ..", "Volver al directorio padre"],
    ["cd ..", "Subir un nivel en el directorio"],
    ["cd ..", "Ir hacia atrás en la estructura"],
    ["cd ..", "Regresar a la carpeta superior"],
    ["cd ..", "Moverse al directorio padre"],
    ["cd ..", "Ir al directorio anterior"],
    ["cd ..", "Subir una carpeta"],
    ["cd ..", "Volver hacia atrás"],
    ["cd ..", "Ir un nivel arriba"],
    
    ["cd ~", "Ir al directorio home"],
    ["cd ~", "Volver a mi carpeta personal"],
    ["cd ~", "Ir a la carpeta de usuario"],
    ["cd ~", "Moverse al directorio principal"],
    ["cd ~", "Ir a mi directorio personal"],
    ["cd ~", "Volver al home"],
    ["cd ~", "Ir a la carpeta raíz del usuario"],
    
    ["cd /", "Ir al directorio raíz"],
    ["cd /", "Moverse a la raíz del sistema"],
    ["cd /", "Ir al directorio principal del sistema"],
    ["cd /", "Volver a la raíz"],
    
    # Ejemplos con nombres de carpetas específicas
    ["cd Documentos", "Ir a la carpeta Documentos"],
    ["cd Documentos", "Entrar en Documentos"],
    ["cd Documentos", "Moverse a Documentos"],
    ["cd Documentos", "Acceder a la carpeta Documentos"],
    
    ["cd Proyecto", "Ir a la carpeta Proyecto"],
    ["cd Proyecto", "Entrar en Proyecto"],
    ["cd Proyecto", "Moverse a Proyecto"],
    ["cd Proyecto", "Acceder a Proyecto"],
    
    ["cd Descargas", "Ir a Descargas"],
    ["cd Descargas", "Entrar en la carpeta Descargas"],
    ["cd Descargas", "Moverse a Descargas"],
    
    # LS con parámetros
    ["ls -l", "Lista detallada de archivos"],
    ["ls -l", "Mostrar archivos con detalles"],
    ["ls -l", "Ver archivos en formato largo"],
    ["ls -l", "Lista completa de archivos"],
    ["ls -l", "Mostrar información detallada"],
    
    ["ls -la", "Mostrar todos los archivos incluidos ocultos"],
    ["ls -la", "Listar archivos ocultos también"],
    ["ls -la", "Ver todos los archivos con detalles"],
    ["ls -la", "Mostrar archivos ocultos y detalles"],
    
    ["ls -lh", "Mostrar archivos con tamaños legibles"],
    ["ls -lh", "Lista con tamaños en formato humano"],
    ["ls -lh", "Ver archivos con tamaños fáciles de leer"],
    
    # MKDIR con nombres específicos
    ["mkdir nueva_carpeta", "Crear carpeta llamada nueva_carpeta"],
    ["mkdir nueva_carpeta", "Hacer una carpeta nueva_carpeta"],
    ["mkdir nueva_carpeta", "Crear directorio nueva_carpeta"],
    
    ["mkdir Proyecto", "Crear carpeta Proyecto"],
    ["mkdir Proyecto", "Hacer directorio Proyecto"],
    ["mkdir Proyecto", "Crear la carpeta Proyecto"],
    
    ["mkdir -p ruta/completa/nueva", "Crear ruta completa de directorios"],
    ["mkdir -p ruta/completa/nueva", "Crear directorios anidados"],
    ["mkdir -p ruta/completa/nueva", "Hacer estructura de carpetas completa"],
    
    # RM con parámetros
    ["rm archivo.txt", "Eliminar archivo.txt"],
    ["rm archivo.txt", "Borrar el archivo archivo.txt"],
    ["rm archivo.txt", "Quitar archivo.txt"],
    
    ["rm -r carpeta", "Eliminar carpeta y su contenido"],
    ["rm -r carpeta", "Borrar carpeta recursivamente"],
    ["rm -r carpeta", "Eliminar directorio completo"],
    
    ["rm -rf carpeta", "Forzar eliminación de carpeta"],
    ["rm -rf carpeta", "Borrar carpeta sin preguntar"],
    ["rm -rf carpeta", "Eliminar carpeta forzadamente"],
    
    # CP con parámetros
    ["cp archivo.txt copia.txt", "Copiar archivo.txt como copia.txt"],
    ["cp archivo.txt copia.txt", "Duplicar archivo.txt a copia.txt"],
    ["cp archivo.txt copia.txt", "Hacer copia de archivo.txt"],
    
    ["cp -r carpeta carpeta_copia", "Copiar carpeta completa"],
    ["cp -r carpeta carpeta_copia", "Duplicar directorio carpeta"],
    ["cp -r carpeta carpeta_copia", "Copiar carpeta recursivamente"],
    
    # MV con parámetros
    ["mv archivo.txt nuevo_nombre.txt", "Renombrar archivo.txt a nuevo_nombre.txt"],
    ["mv archivo.txt nuevo_nombre.txt", "Cambiar nombre de archivo.txt"],
    ["mv archivo.txt nuevo_nombre.txt", "Mover archivo.txt a nuevo_nombre.txt"],
    
    ["mv archivo.txt /otra/carpeta/", "Mover archivo.txt a otra carpeta"],
    ["mv archivo.txt /otra/carpeta/", "Trasladar archivo.txt"],
    ["mv archivo.txt /otra/carpeta/", "Cambiar ubicación de archivo.txt"],
    
    # CAT con archivos específicos
    ["cat archivo.txt", "Mostrar contenido de archivo.txt"],
    ["cat archivo.txt", "Leer archivo.txt"],
    ["cat archivo.txt", "Ver el texto de archivo.txt"],
    
    ["cat archivo1.txt archivo2.txt", "Mostrar contenido de múltiples archivos"],
    ["cat archivo1.txt archivo2.txt", "Leer varios archivos juntos"],
    
    # GREP con parámetros
    ["grep 'texto' archivo.txt", "Buscar 'texto' en archivo.txt"],
    ["grep 'texto' archivo.txt", "Encontrar 'texto' en archivo.txt"],
    ["grep 'texto' archivo.txt", "Localizar 'texto' en archivo.txt"],
    
    ["grep -r 'texto' .", "Buscar 'texto' en todos los archivos"],
    ["grep -r 'texto' .", "Buscar 'texto' recursivamente"],
    ["grep -r 'texto' .", "Encontrar 'texto' en carpeta actual"],
    
    ["grep -i 'texto' archivo.txt", "Buscar 'texto' sin importar mayúsculas"],
    ["grep -i 'texto' archivo.txt", "Buscar 'texto' ignorando mayúsculas"],
    
    # FIND con parámetros
    ["find . -name '*.txt'", "Buscar archivos .txt"],
    ["find . -name '*.txt'", "Encontrar archivos de texto"],
    ["find . -name '*.txt'", "Localizar archivos .txt"],
    
    ["find . -name 'archivo*'", "Buscar archivos que empiecen con 'archivo'"],
    ["find . -name 'archivo*'", "Encontrar archivos con nombre 'archivo'"],
    
    ["find /home -type d", "Buscar solo directorios en /home"],
    ["find /home -type d", "Encontrar carpetas en /home"],
    
    # CHMOD con parámetros específicos
    ["chmod 755 archivo.txt", "Dar permisos 755 a archivo.txt"],
    ["chmod 755 archivo.txt", "Cambiar permisos de archivo.txt a 755"],
    ["chmod 755 archivo.txt", "Establecer permisos ejecutables"],
    
    ["chmod +x script.sh", "Hacer ejecutable script.sh"],
    ["chmod +x script.sh", "Dar permisos de ejecución a script.sh"],
    ["chmod +x script.sh", "Permitir ejecutar script.sh"],
    
    # TAR con parámetros
    ["tar -czf archivo.tar.gz carpeta/", "Comprimir carpeta en archivo.tar.gz"],
    ["tar -czf archivo.tar.gz carpeta/", "Crear archivo comprimido de carpeta"],
    ["tar -czf archivo.tar.gz carpeta/", "Empaquetar carpeta en tar.gz"],
    
    ["tar -xzf archivo.tar.gz", "Extraer archivo.tar.gz"],
    ["tar -xzf archivo.tar.gz", "Descomprimir archivo.tar.gz"],
    ["tar -xzf archivo.tar.gz", "Desempaquetar archivo.tar.gz"],
    
    # ZIP con archivos específicos
    ["zip archivo.zip *.txt", "Comprimir archivos .txt en archivo.zip"],
    ["zip archivo.zip *.txt", "Crear zip con archivos de texto"],
    ["zip archivo.zip *.txt", "Empaquetar archivos .txt"],
    
    ["unzip archivo.zip", "Descomprimir archivo.zip"],
    ["unzip archivo.zip", "Extraer contenido de archivo.zip"],
    
    # SSH con parámetros
    ["ssh usuario@servidor.com", "Conectar a servidor.com como usuario"],
    ["ssh usuario@servidor.com", "Acceder por SSH a servidor.com"],
    ["ssh usuario@192.168.1.100", "Conectar a IP 192.168.1.100"],
    
    # SCP con archivos específicos
    ["scp archivo.txt usuario@servidor:/ruta/", "Copiar archivo.txt al servidor"],
    ["scp archivo.txt usuario@servidor:/ruta/", "Transferir archivo.txt por SSH"],
    
    # WGET con URLs
    ["wget https://ejemplo.com/archivo.zip", "Descargar archivo desde ejemplo.com"],
    ["wget https://ejemplo.com/archivo.zip", "Bajar archivo.zip de la web"],
    
    # NANO/VIM con archivos
    ["nano archivo.txt", "Editar archivo.txt con nano"],
    ["nano archivo.txt", "Abrir archivo.txt en nano"],
    
    ["vim archivo.txt", "Editar archivo.txt con vim"],
    ["vim archivo.txt", "Abrir archivo.txt en vim"],
    
    # PS con parámetros
    ["ps aux", "Mostrar todos los procesos"],
    ["ps aux", "Ver procesos de todos los usuarios"],
    ["ps aux", "Listar procesos completos"],
    
    # KILL con PID específico
    ["kill 1234", "Terminar proceso con ID 1234"],
    ["kill 1234", "Matar proceso 1234"],
    ["kill -9 1234", "Forzar terminación del proceso 1234"],
    
    # Comandos con tuberías y redirección
    ["ls > lista.txt", "Guardar lista de archivos en lista.txt"],
    ["ls > lista.txt", "Escribir lista de archivos a archivo"],
    
    ["cat archivo.txt | grep 'texto'", "Buscar 'texto' en archivo.txt"],
    ["cat archivo.txt | grep 'texto'", "Filtrar 'texto' del archivo.txt"],
]

def create_enhanced_dataset():
    """Crea el dataset con comandos completos y parámetros"""
    
    # Agregar más variaciones dinámicas
    extended_dataset = []
    extended_dataset.append(['comando', 'descripcion_variacion'])  # Header
    
    # Agregar todos los comandos base
    for comando, descripcion in commands_with_parameters:
        extended_dataset.append([comando, descripcion])
    
    # Generar variaciones adicionales con plantillas
    folder_names = ['Documentos', 'Proyecto', 'Descargas', 'Imagenes', 'Videos', 'Musica', 'src', 'build', 'test', 'config']
    file_names = ['archivo.txt', 'documento.pdf', 'imagen.jpg', 'script.py', 'config.json', 'readme.md', 'index.html']
    
    # Más variaciones de CD con diferentes carpetas
    cd_descriptions = [
        "Ir a la carpeta {folder}",
        "Entrar en {folder}",
        "Moverse a {folder}",
        "Acceder a la carpeta {folder}",
        "Cambiar a {folder}",
        "Navegar a {folder}",
        "Dirigirse a {folder}",
        "Abrir carpeta {folder}",
        "Ir hacia {folder}",
        "Entrar a {folder}"
    ]
    
    for folder in folder_names:
        for desc_template in cd_descriptions[:5]:  # Limitar para no hacer dataset gigante
            comando = f"cd {folder}"
            descripcion = desc_template.format(folder=folder)
            extended_dataset.append([comando, descripcion])
    
    # Más variaciones de comandos con archivos
    file_commands = [
        ("rm {file}", ["Eliminar {file}", "Borrar {file}", "Quitar {file}"]),
        ("cat {file}", ["Mostrar contenido de {file}", "Leer {file}", "Ver {file}"]),
        ("nano {file}", ["Editar {file} con nano", "Abrir {file} en nano", "Modificar {file}"]),
        ("vim {file}", ["Editar {file} con vim", "Abrir {file} en vim", "Modificar {file} con vim"]),
    ]
    
    for file_name in file_names[:3]:  # Limitar archivos
        for cmd_template, desc_templates in file_commands:
            for desc_template in desc_templates:
                comando = cmd_template.format(file=file_name)
                descripcion = desc_template.format(file=file_name)
                extended_dataset.append([comando, descripcion])
    
    return extended_dataset

def save_enhanced_dataset(dataset, filename='comandos_linux_completos.csv'):
    """Guarda el dataset mejorado"""
    with open(filename, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerows(dataset)
    
    print(f"Dataset guardado en {filename}")
    print(f"Total de líneas: {len(dataset)-1}")
    
    # Mostrar algunos ejemplos
    print("\n=== EJEMPLOS DEL DATASET ===")
    for i in range(1, min(11, len(dataset))):
        print(f"{dataset[i][0]} | {dataset[i][1]}")

# Crear y guardar el dataset mejorado
enhanced_dataset = create_enhanced_dataset()
save_enhanced_dataset(enhanced_dataset)

print(f"\n=== ESTADÍSTICAS ===")
print(f"Dataset creado con comandos COMPLETOS incluyendo parámetros")
print(f"Ahora el modelo aprenderá a generar 'cd ..' no solo 'cd'")
print(f"Incluye ejemplos con nombres de carpetas y archivos específicos")