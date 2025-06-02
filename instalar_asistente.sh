#!/bin/bash

# Script de instalación para el Asistente de Comandos Bash con Ollama

echo "🚀 Configurando Asistente de Comandos Bash con Ollama"
echo "=================================================="

# Verificar si Python está instalado
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 no está instalado"
    echo "Instala Python3 primero: sudo apt install python3 python3-pip"
    exit 1
fi

# Instalar dependencias de Python
echo "📦 Instalando dependencias de Python..."
pip3 install requests

# Verificar si Ollama está instalado
if ! command -v ollama &> /dev/null; then
    echo "📥 Ollama no está instalado. Instalando..."
    curl -fsSL https://ollama.ai/install.sh | sh
else
    echo "✅ Ollama ya está instalado"
fi

# Iniciar Ollama en segundo plano
echo "🔧 Iniciando Ollama..."
if ! pgrep -f "ollama serve" > /dev/null; then
    ollama serve &
    sleep 3
    echo "✅ Ollama iniciado"
else
    echo "✅ Ollama ya está corriendo"
fi

# Instalar modelo por defecto
echo "📥 Descargando modelo llama3.1..."
ollama pull llama3.1

# Crear script de inicio rápido
cat > bash_assistant_start.sh << 'EOF'
#!/bin/bash
# Script de inicio rápido para el asistente

# Verificar si Ollama está corriendo
if ! pgrep -f "ollama serve" > /dev/null; then
    echo "Iniciando Ollama..."
    ollama serve &
    sleep 3
fi

# Ejecutar el asistente
python3 bash_assistant.py
EOF

chmod +x bash_assistant_start.sh

echo ""
echo "✅ ¡Instalación completada!"
echo ""
echo "Para usar el asistente:"
echo "1. Ejecuta: python3 bash_assistant.py"
echo "2. O usa el script rápido: ./bash_assistant_start.sh"
echo ""
echo "Ejemplos de uso:"
echo "- 'crea la carpeta ayuda'"
echo "- 'muévete a la carpeta agua'"
echo "- 'lista los archivos'"
echo "- 'copia archivo1.txt a backup.txt'"
echo ""
echo "Modelos disponibles para probar:"
echo "- llama3.1 (por defecto)"
echo "- llama3.2"
echo "- mistral"
echo "- codellama"
echo ""
echo "Para usar otro modelo: python3 bash_assistant.py nombre_del_modelo"

