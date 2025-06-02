from transformers import T5Tokenizer, T5ForConditionalGeneration
import os

# Cargar el modelo desde la carpeta extraída
ruta_modelo = r"C:\Users\aaron\OneDrive\Escritorio\Reboot\Bloque_3\Deep_Learning\Mini_Project\t5_jarvis_model\content\t5_jarvis_model"

model = T5ForConditionalGeneration.from_pretrained(ruta_modelo)
tokenizer = T5Tokenizer.from_pretrained(ruta_modelo)

# Función para ejecutar comandos
def ejecutar_comando(texto_usuario):
    inputs = tokenizer(texto_usuario, return_tensors="pt", padding=True)
    output = model.generate(**inputs, max_length=32)
    comando = tokenizer.decode(output[0], skip_special_tokens=True)
    print(f"🗣️ Entrada: {texto_usuario}")
    print(f"🧠 Comando generado: {comando}")
    os.system(comando)  # ⚠️ Aquí se ejecuta realmente en tu PC

ejecutar_comando("Muestra el directorio de trabajo actual.")

