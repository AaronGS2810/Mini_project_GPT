#!/usr/bin/env python3
"""
Asistente de comandos bash usando Ollama
Convierte lenguaje natural a comandos bash y los ejecuta
"""

import subprocess
import json
import requests
import os
import sys

class BashAssistant:
    def __init__(self, model_name="llama3.1"):
        self.model_name = model_name
        self.ollama_url = "http://localhost:11434/api/generate"
        
        # Prompt del sistema para entrenar el comportamiento
        self.system_prompt = """Eres un asistente que convierte instrucciones en lenguaje natural a comandos bash.

REGLAS IMPORTANTES:
1. Responde SOLO con el comando bash, sin explicaciones adicionales
2. Si no estás seguro del comando, responde "COMANDO_NO_CLARO"
3. No ejecutes comandos peligrosos (rm -rf, sudo sin confirmación, etc.)

EJEMPLOS:
Usuario: "crea la carpeta ayuda"
Respuesta: mkdir ayuda

Usuario: "muévete a la carpeta agua" 
Respuesta: cd agua

Usuario: "lista los archivos"
Respuesta: ls -la

Usuario: "elimina el archivo test.txt"
Respuesta: rm test.txt

Usuario: "copia archivo1.txt a archivo2.txt"
Respuesta: cp archivo1.txt archivo2.txt

Usuario: "muestra el contenido del archivo readme.txt"
Respuesta: cat readme.txt

Usuario: "busca archivos que contengan 'python'"
Respuesta: find . -name "*python*"

Convierte esta instrucción a comando bash:"""

    def check_ollama_connection(self):
        """Verifica si Ollama está corriendo"""
        try:
            response = requests.get("http://localhost:11434/api/tags")
            return response.status_code == 200
        except:
            return False

    def get_bash_command(self, natural_language_input):
        """Convierte lenguaje natural a comando bash usando Ollama"""
        
        if not self.check_ollama_connection():
            return "ERROR: Ollama no está corriendo. Ejecuta 'ollama serve' primero."
        
        payload = {
            "model": self.model_name,
            "prompt": f"{self.system_prompt}\n\nUsuario: \"{natural_language_input}\"",
            "stream": False,
            "options": {
                "temperature": 0.1,  # Baja temperatura para respuestas más precisas
                "top_p": 0.9,
                "max_tokens": 100
            }
        }
        
        try:
            response = requests.post(self.ollama_url, json=payload)
            if response.status_code == 200:
                result = response.json()
                command = result.get('response', '').strip()
                
                # Limpiar la respuesta
                if command.startswith('Respuesta:'):
                    command = command.replace('Respuesta:', '').strip()
                
                return command
            else:
                return f"ERROR: {response.status_code} - {response.text}"
                
        except Exception as e:
            return f"ERROR: {str(e)}"

    def is_safe_command(self, command):
        """Verifica si el comando es seguro de ejecutar"""
        dangerous_patterns = [
            'rm -rf /',
            'sudo rm',
            'mkfs',
            'dd if=',
            'chmod 777',
            'chown root',
            '> /dev/',
            'curl | sh',
            'wget | sh'
        ]
        
        for pattern in dangerous_patterns:
            if pattern in command.lower():
                return False
        return True

    def execute_command(self, command):
        """Ejecuta el comando bash de forma segura"""
        if not self.is_safe_command(command):
            return "COMANDO PELIGROSO: No se ejecutará por seguridad"
        
        if command == "COMANDO_NO_CLARO":
            return "No pude entender la instrucción. Por favor, sé más específico."
        
        try:
            # Para comandos cd, necesitamos manejarlos especialmente
            if command.startswith('cd '):
                directory = command[3:].strip()
                try:
                    os.chdir(directory)
                    return f"Cambiado al directorio: {os.getcwd()}"
                except FileNotFoundError:
                    return f"ERROR: El directorio '{directory}' no existe"
                except PermissionError:
                    return f"ERROR: No tienes permisos para acceder a '{directory}'"
            
            # Para otros comandos
            result = subprocess.run(
                command,
                shell=True,
                capture_output=True,
                text=True,
                timeout=30  # Timeout de 30 segundos
            )
            
            output = ""
            if result.stdout:
                output += f"Salida:\n{result.stdout}"
            if result.stderr:
                output += f"Errores:\n{result.stderr}"
            if result.returncode != 0:
                output += f"\nCódigo de salida: {result.returncode}"
            
            return output if output else "Comando ejecutado exitosamente (sin salida)"
            
        except subprocess.TimeoutExpired:
            return "ERROR: El comando tardó demasiado en ejecutarse"
        except Exception as e:
            return f"ERROR al ejecutar: {str(e)}"

    def interactive_mode(self):
        """Modo interactivo del asistente"""
        print("🤖 Asistente de Comandos Bash con Ollama")
        print("=" * 50)
        print("Escribe instrucciones en lenguaje natural y las convertiré a comandos bash")
        print("Comandos especiales:")
        print("  'salir' - Terminar el programa")
        print("  'pwd' - Mostrar directorio actual")
        print("  'ayuda' - Mostrar esta ayuda")
        print("=" * 50)
        
        while True:
            try:
                # Mostrar el directorio actual
                current_dir = os.getcwd()
                user_input = input(f"\n📁 {current_dir}\n💬 ¿Qué quieres hacer? ").strip()
                
                if user_input.lower() in ['salir', 'exit', 'quit']:
                    print("¡Até logo! 👋")
                    break
                
                if user_input.lower() == 'pwd':
                    print(f"Directorio actual: {os.getcwd()}")
                    continue
                
                if user_input.lower() == 'ayuda':
                    print("""
Ejemplos de uso:
- "crea la carpeta documentos"
- "muévete a la carpeta descargas"  
- "lista los archivos"
- "copia archivo.txt a backup.txt"
- "elimina el archivo temporal.log"
- "muestra el contenido de readme.txt"
                    """)
                    continue
                
                if not user_input:
                    continue
                
                print(f"\n🔍 Analizando: '{user_input}'")
                
                # Obtener comando bash
                bash_command = self.get_bash_command(user_input)
                
                if bash_command.startswith("ERROR"):
                    print(f"❌ {bash_command}")
                    continue
                
                print(f"⚡ Comando generado: {bash_command}")
                
                # Pedir confirmación para comandos potencialmente destructivos
                destructive_commands = ['rm', 'mv', 'cp']
                if any(cmd in bash_command for cmd in destructive_commands):
                    confirm = input("⚠️  ¿Ejecutar este comando? (s/N): ").lower()
                    if confirm not in ['s', 'si', 'sí', 'y', 'yes']:
                        print("Comando cancelado")
                        continue
                
                # Ejecutar comando
                print("🚀 Ejecutando...")
                result = self.execute_command(bash_command)
                print(f"📋 {result}")
                
            except KeyboardInterrupt:
                print("\n\n¡Hasta luego! 👋")
                break
            except Exception as e:
                print(f"❌ Error inesperado: {str(e)}")

def main():
    # Verificar argumentos de línea de comandos
    model_name = "llama3.1"  # Modelo por defecto
    
    if len(sys.argv) > 1:
        model_name = sys.argv[1]
    
    print(f"Usando modelo: {model_name}")
    
    assistant = BashAssistant(model_name)
    
    # Verificar conexión con Ollama
    if not assistant.check_ollama_connection():
        print("❌ ERROR: No se puede conectar con Ollama")
        print("Asegúrate de que Ollama esté corriendo: 'ollama serve'")
        print(f"Y que tengas el modelo '{model_name}' instalado: 'ollama pull {model_name}'")
        sys.exit(1)
    
    assistant.interactive_mode()

if __name__ == "__main__":
    main()