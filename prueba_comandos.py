#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
import subprocess
import os
import platform
from typing import Optional, Tuple

class CommandInterpreter:
    def __init__(self):
        # Detectar sistema operativo
        self.is_windows = platform.system().lower() == 'windows'
        
        # Comandos multiplataforma
        if self.is_windows:
            self.commands = {
                # Comandos de directorios
                r"crea(?:r|me)?\s+(?:una?\s+)?carpeta\s+(?:llamada?\s+)?(['\"]?)([a-zA-Z0-9_\s-]+)\1(?:\s+en\s+(?:el\s+)?(\w+))?": self._crear_carpeta_win,
                r"mu[eé]vete\s+a\s+(?:la\s+)?carpeta\s+(['\"]?)([a-zA-Z0-9_\s/-]+)\1": "cd /d {0}",
                r"elimina(?:r)?\s+(?:la\s+)?carpeta\s+(['\"]?)([a-zA-Z0-9_\s-]+)\1": "rmdir /s /q {0}",
                
                # Comandos de archivos
                r"crea(?:r)?\s+(?:el\s+|un\s+)?archivo\s+(?:llamado\s+)?(['\"]?)([a-zA-Z0-9_.\s-]+)\1": "echo. > {0}",
                r"elimina(?:r)?\s+(?:el\s+)?archivo\s+(['\"]?)([a-zA-Z0-9_.\s-]+)\1": "del {0}",
                r"copia(?:r)?\s+(['\"]?)([a-zA-Z0-9_.\s-]+)\1\s+a\s+(['\"]?)([a-zA-Z0-9_.\s-]+)\3": "copy {0} {1}",
                r"mueve\s+(['\"]?)([a-zA-Z0-9_.\s-]+)\1\s+a\s+(['\"]?)([a-zA-Z0-9_.\s-]+)\3": "move {0} {1}",
                
                # Comandos de listado y navegación
                r"(?:lista(?:r)?|muestra(?:r|me)?)\s+(?:los\s+|las\s+)?(?:archivos?|carpetas?)": "dir",
                r"(?:lista(?:r)?|muestra(?:r|me)?)\s+(?:los\s+|las\s+)?(?:archivos?|carpetas?)\s+(?:del\s+)?(?:directorio\s+)?(?:actual)?": "dir",
                r"(?:d[oó]nde\s+estoy|ubicaci[oó]n\s+actual|carpeta\s+actual|directorio\s+actual)": "cd",
                r"vuelve\s+atr[aá]s": "cd ..",
                r"ve\s+al\s+(?:inicio|home)": "cd %USERPROFILE%",
                
                # Comandos de contenido
                r"muestra(?:r|me)?\s+(?:el\s+)?contenido\s+de\s+(['\"]?)([a-zA-Z0-9_.\s-]+)\1": "type {0}",
                r"edita(?:r)?\s+(?:el\s+)?archivo\s+(['\"]?)([a-zA-Z0-9_.\s-]+)\1": "notepad {0}",
                
                # Comandos de búsqueda
                r"busca(?:r)?\s+(?:el\s+|los\s+)?archivos?\s+(['\"]?)([a-zA-Z0-9_.*\s-]+)\1": "dir /s *{0}*",
                r"busca(?:r)?\s+(?:el\s+)?texto\s+(['\"]?)([^'\"]+)\1\s+en\s+(['\"]?)([a-zA-Z0-9_.\s-]+)\3": "findstr \"{0}\" {1}",
            }
        else:
            self.commands = {
                # Comandos Unix/Linux (código original mejorado)
                r"crea(?:r|me)?\s+(?:una?\s+)?carpeta\s+(?:llamada?\s+)?(['\"]?)([a-zA-Z0-9_\s-]+)\1(?:\s+en\s+(?:el\s+)?(\w+))?": self._crear_carpeta_unix,
                r"mu[eé]vete\s+a\s+(?:la\s+)?carpeta\s+(['\"]?)([a-zA-Z0-9_\s/-]+)\1": "cd {0}",
                r"elimina(?:r)?\s+(?:la\s+)?carpeta\s+(['\"]?)([a-zA-Z0-9_\s-]+)\1": "rmdir {0}",
                
                # Resto de comandos Unix...
                r"crea(?:r)?\s+(?:el\s+|un\s+)?archivo\s+(?:llamado\s+)?(['\"]?)([a-zA-Z0-9_.\s-]+)\1": "touch {0}",
                r"elimina(?:r)?\s+(?:el\s+)?archivo\s+(['\"]?)([a-zA-Z0-9_.\s-]+)\1": "rm {0}",
                r"copia(?:r)?\s+(['\"]?)([a-zA-Z0-9_.\s-]+)\1\s+a\s+(['\"]?)([a-zA-Z0-9_.\s-]+)\3": "cp {0} {1}",
                r"mueve\s+(['\"]?)([a-zA-Z0-9_.\s-]+)\1\s+a\s+(['\"]?)([a-zA-Z0-9_.\s-]+)\3": "mv {0} {1}",
                
                r"(?:lista(?:r)?|muestra(?:r|me)?)\s+(?:los\s+|las\s+)?(?:archivos?|carpetas?)": "ls",
                r"(?:lista(?:r)?|muestra(?:r|me)?)\s+(?:los\s+|las\s+)?(?:archivos?|carpetas?)\s+(?:del\s+)?(?:directorio\s+)?(?:actual)?": "ls -la",
                r"(?:d[oó]nde\s+estoy|ubicaci[oó]n\s+actual|carpeta\s+actual|directorio\s+actual)": "pwd",
                r"vuelve\s+atr[aá]s": "cd ..",
                r"ve\s+al\s+(?:inicio|home)": "cd ~",
                
                r"muestra(?:r|me)?\s+(?:el\s+)?contenido\s+de\s+(['\"]?)([a-zA-Z0-9_.\s-]+)\1": "cat {0}",
                r"edita(?:r)?\s+(?:el\s+)?archivo\s+(['\"]?)([a-zA-Z0-9_.\s-]+)\1": "nano {0}",
                
                r"busca(?:r)?\s+(?:el\s+|los\s+)?archivos?\s+(['\"]?)([a-zA-Z0-9_.*\s-]+)\1": "find . -name '*{0}*'",
                r"busca(?:r)?\s+(?:el\s+)?texto\s+(['\"]?)([^'\"]+)\1\s+en\s+(['\"]?)([a-zA-Z0-9_.\s-]+)\3": "grep '{0}' {1}",
            }
    
    def _crear_carpeta_win(self, match_groups):
        """Crear carpeta en Windows con soporte para ubicaciones específicas"""
        grupos = [g for g in match_groups if g and g not in ["'", '"']]
        nombre_carpeta = grupos[0].strip()
        ubicacion = grupos[1] if len(grupos) > 1 else None
        
        if ubicacion and ubicacion.lower() == 'escritorio':
            # Crear en el escritorio
            return f'mkdir "%USERPROFILE%\\Desktop\\{nombre_carpeta}"'
        else:
            return f'mkdir "{nombre_carpeta}"'
    
    def _crear_carpeta_unix(self, match_groups):
        """Crear carpeta en Unix con soporte para ubicaciones específicas"""
        grupos = [g for g in match_groups if g and g not in ["'", '"']]
        nombre_carpeta = grupos[0].strip()
        ubicacion = grupos[1] if len(grupos) > 1 else None
        
        if ubicacion and ubicacion.lower() == 'escritorio':
            return f'mkdir ~/Desktop/"{nombre_carpeta}"'
        else:
            return f'mkdir "{nombre_carpeta}"'
    
    def interpretar_comando(self, texto_natural: str) -> Optional[str]:
        """
        Convierte un comando en lenguaje natural al comando del sistema correspondiente
        """
        texto_limpio = texto_natural.strip().lower()
        
        for patron, template in self.commands.items():
            match = re.search(patron, texto_limpio, re.IGNORECASE)
            if match:
                # Si es una función personalizada
                if callable(template):
                    return template(match.groups())
                
                # Extraer grupos capturados, filtrando comillas
                grupos = [g for g in match.groups() if g and g not in ["'", '"']]
                
                try:
                    # Limpiar nombres de archivos/carpetas
                    grupos_limpios = [g.strip() for g in grupos]
                    comando = template.format(*grupos_limpios)
                    return comando
                except (IndexError, KeyError):
                    # Si no hay suficientes grupos, usar el template sin formatear
                    return template if isinstance(template, str) else None
        
        return None
    
    def ejecutar_comando(self, comando: str, directorio_trabajo: str = None) -> Tuple[str, str, int]:
        """
        Ejecuta un comando del sistema y devuelve (stdout, stderr, codigo_salida)
        """
        try:
            # Cambiar directorio si es necesario
            if directorio_trabajo:
                os.chdir(directorio_trabajo)
            
            # Manejar el comando 'cd' especialmente para Windows
            if self.is_windows and comando.startswith('cd '):
                try:
                    nuevo_dir = comando[3:].strip()
                    if nuevo_dir == '..':
                        os.chdir('..')
                    elif nuevo_dir.startswith('%USERPROFILE%'):
                        nuevo_dir = nuevo_dir.replace('%USERPROFILE%', os.path.expanduser('~'))
                        os.chdir(nuevo_dir)
                    else:
                        # Remover comillas si las hay
                        nuevo_dir = nuevo_dir.strip('"')
                        os.chdir(nuevo_dir)
                    return f"Cambiado a directorio: {os.getcwd()}", "", 0
                except FileNotFoundError:
                    return "", f"Error: Directorio '{nuevo_dir}' no encontrado", 1
                except PermissionError:
                    return "", f"Error: Sin permisos para acceder a '{nuevo_dir}'", 1
            
            # Para Unix/Linux, manejar cd también
            elif not self.is_windows and comando.startswith('cd '):
                try:
                    nuevo_dir = comando[3:].strip()
                    if nuevo_dir == '..':
                        os.chdir('..')
                    elif nuevo_dir == '~':
                        os.chdir(os.path.expanduser('~'))
                    else:
                        nuevo_dir = nuevo_dir.strip('"')
                        os.chdir(nuevo_dir)
                    return f"Cambiado a directorio: {os.getcwd()}", "", 0
                except FileNotFoundError:
                    return "", f"Error: Directorio '{nuevo_dir}' no encontrado", 1
                except PermissionError:
                    return "", f"Error: Sin permisos para acceder a '{nuevo_dir}'", 1
            
            # Ejecutar otros comandos
            if self.is_windows:
                # En Windows, usar cmd /c para comandos
                resultado = subprocess.run(
                    comando, 
                    shell=True, 
                    capture_output=True, 
                    text=True,
                    timeout=30,
                    encoding='cp1252'  # Codificación para Windows español
                )
            else:
                resultado = subprocess.run(
                    comando, 
                    shell=True, 
                    capture_output=True, 
                    text=True,
                    timeout=30
                )
            
            return resultado.stdout, resultado.stderr, resultado.returncode
            
        except subprocess.TimeoutExpired:
            return "", "Error: Comando excedió tiempo límite (30s)", 1
        except UnicodeDecodeError:
            return "", "Error: Problema de codificación de caracteres", 1
        except Exception as e:
            return "", f"Error ejecutando comando: {str(e)}", 1
    
    def procesar_solicitud(self, texto_natural: str, ejecutar: bool = False) -> dict:
        """
        Procesa una solicitud completa: interpreta y opcionalmente ejecuta
        """
        comando = self.interpretar_comando(texto_natural)
        
        resultado = {
            'texto_original': texto_natural,
            'comando': comando,
            'interpretado': comando is not None,
            'sistema': 'Windows' if self.is_windows else 'Unix/Linux'
        }
        
        if comando:
            print(f"🔍 Comando interpretado: {comando}")
            print(f"💻 Sistema: {'Windows' if self.is_windows else 'Unix/Linux'}")
            
            if ejecutar:
                stdout, stderr, codigo = self.ejecutar_comando(comando)
                resultado.update({
                    'ejecutado': True,
                    'stdout': stdout,
                    'stderr': stderr,
                    'codigo_salida': codigo,
                    'exito': codigo == 0
                })
                
                if codigo == 0:
                    print(f"✅ Ejecutado exitosamente")
                    if stdout:
                        print(f"📤 Salida:\n{stdout}")
                else:
                    print(f"❌ Error en ejecución: {stderr}")
            else:
                resultado['ejecutado'] = False
                print("ℹ️  Usa ejecutar=True para ejecutar el comando")
        else:
            resultado['ejecutado'] = False
            print("❌ No se pudo interpretar el comando")
            print("💡 Prueba variaciones como:")
            if self.is_windows:
                print("   - 'crea la carpeta ayuda'")
                print("   - 'muestra los archivos'")
                print("   - 'creame una carpeta llamada test en el escritorio'")
            else:
                print("   - 'crea la carpeta ayuda'")
                print("   - 'lista los archivos'")
                print("   - 'muévete a la carpeta documentos'")
        
        return resultado


# Ejemplo de uso
if __name__ == "__main__":
    interprete = CommandInterpreter()
    
    print(f"🖥️  Sistema detectado: {'Windows' if interprete.is_windows else 'Unix/Linux'}")
    
    # Ejemplos de prueba según el sistema
    if interprete.is_windows:
        comandos_prueba = [
            "creame una carpeta llamada ayuda en el escritorio",
            "muestrame las carpetas del directorio actual", 
            "lista los archivos",
            "crea el archivo test.txt",
            "muestra el contenido de test.txt",
            "dónde estoy",
            "busca archivos txt"
        ]
    else:
        comandos_prueba = [
            "crea la carpeta ayuda",
            "muévete a la carpeta agua", 
            "lista los archivos",
            "crea el archivo test.txt",
            "muestra el contenido de test.txt",
            "dónde estoy"
        ]
    
    print("\n=== PRUEBAS DE INTERPRETACIÓN ===\n")
    
    for comando in comandos_prueba:
        print(f"🗣️  '{comando}'")
        resultado = interprete.procesar_solicitud(comando, ejecutar=False)
        print("-" * 50)
    
    print("\n=== MODO INTERACTIVO ===")
    print("Escribe comandos en lenguaje natural (escribe 'salir' para terminar):")
    
    while True:
        try:
            entrada = input("\n👤 ")
            if entrada.lower() in ['salir', 'exit', 'quit']:
                break
            
            # Preguntar si ejecutar
            ejecutar = input("¿Ejecutar comando? (s/N): ").lower().startswith('s')
            
            resultado = interprete.procesar_solicitud(entrada, ejecutar=ejecutar)
            
        except KeyboardInterrupt:
            print("\n👋 ¡Hasta luego!")
            break
        except Exception as e:
            print(f"❌ Error: {e}")