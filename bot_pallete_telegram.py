import random
import matplotlib.pyplot as plt
from telegram import Update
from telegram.ext import Application, CommandHandler, CallbackContext, MessageHandler, filters
import os
import sqlite3
import matplotlib.colors as mcolors



TOKEN = os.environ.get("TOKENCHOCOLORS")

def obtener_categorias_de_base_de_datos():
    conexion = sqlite3.connect('Paletas.db')
    cursor = conexion.cursor()
    cursor.execute("SELECT DISTINCT categories FROM Categorized_pallettes")  # Suponiendo que tienes un campo 'category'
    categorias = [fila[0] for fila in cursor.fetchall()]
    conexion.close()
    return categorias

def obtener_pallette_por_categoria(categoria):
    conexion = sqlite3.connect('Paletas.db')
    cursor = conexion.cursor()
    cursor.execute("SELECT code FROM Categorized_pallettes WHERE categories = ? ORDER BY RANDOM() LIMIT 5", (categoria,))
    resultados = cursor.fetchall()
    conexion.close()

    return [hex_to_rgb(fila[0]) for fila in resultados] if resultados else None

def hex_to_rgb(hex_color):
    hex_color = hex_color.lstrip('#')
    return [int(hex_color[i:i+2], 16) / 255 for i in (0, 2, 4)]

def obtener_codigos_de_base_de_datos(tabla):
    conexion = sqlite3.connect('Paletas.db')
    cursor = conexion.cursor()
    cursor.execute(f"SELECT code FROM {tabla}")
    resultados = [fila[0] for fila in cursor.fetchall()]
    conexion.close()

    grupos_de_seis = [resultados[i:i+6] for i in range(0, len(resultados), 6)]
    return grupos_de_seis

def es_color_hexadecimal_valido(hex_color):
    if hex_color.startswith('#') and len(hex_color) == 7:
        try:
            int(hex_color[1:], 16)
            return True
        except ValueError:
            return False
    return False

def generar_paleta_desde_color(hex_color):
    base_color = mcolors.hex2color(hex_color)
    paleta = [base_color]
    for i in range(4):
        tono = [
            max(0, min(1, base_color[j] + random.uniform(-0.1, 0.1)))
            for j in range(3)
        ]
        paleta.append(tono)

    return paleta

async def paleta_hexadecimal(update: Update, context: CallbackContext):
    if context.args:
        hex_color = context.args[0]
        if es_color_hexadecimal_valido(hex_color):
            paleta_elegida = generar_paleta_desde_color(hex_color)
            plt.figure(figsize=(5, 1))
            plt.imshow([paleta_elegida], aspect='auto')
            plt.axis('off')

            plt.savefig('/tmp/paleta_hexadecimal.png', bbox_inches='tight', pad_inches=0)
            plt.close()

            await update.message.reply_photo(photo=open('/tmp/paleta_hexadecimal.png', 'rb'))

            colores_hexadecimales = [
                "#{:02x}{:02x}{:02x}".format(
                    int(color[0] * 255), int(color[1] * 255), int(color[2] * 255)
                )
                for color in paleta_elegida
            ]
            mensaje_colores = f"Paleta generada a partir del color {hex_color}:\n" + "\n".join(colores_hexadecimales)
            await update.message.reply_text(mensaje_colores)
        else:
            await update.message.reply_text(f"El código hexadecimal '{hex_color}' no es válido. Asegúrate de que el formato sea correcto (por ejemplo, #FF5733).")
    else:
        await update.message.reply_text("Por favor, proporciona un color hexadecimal como argumento, por ejemplo: /hexa #FF5733")

async def paleta_variable(update: Update, context: CallbackContext):
    if context.args:
        color = context.args[0]
        categorias = obtener_categorias_de_base_de_datos()
        if color in categorias:
            paleta_elegida = obtener_pallette_por_categoria(color)
            if paleta_elegida:
                plt.figure(figsize=(5, 1))
                plt.imshow([paleta_elegida], aspect='auto')
                plt.axis('off')

                plt.savefig('/tmp/paleta_variable.png', bbox_inches='tight', pad_inches=0)
                plt.close()

                await update.message.reply_photo(photo=open('/tmp/paleta_variable.png', 'rb'))

                colores_hexadecimales = [
                    "#{:02x}{:02x}{:02x}".format(
                        int(color[0] * 255), int(color[1] * 255), int(color[2] * 255)
                    )
                    for color in paleta_elegida
                ]
                mensaje_colores = f"Paleta de la categoría '{color.capitalize()}' generada :\n" + "\n".join(colores_hexadecimales)
                await update.message.reply_text(mensaje_colores)
            else:
                await update.message.reply_text(f"No se encontraron colores para la categoría '{color}'.")
        else:
            await update.message.reply_text(f"Lo siento, no puedo generar una paleta para la categoría '{color}'. Asegúrate de que la categoría exista.")
    else:
        await update.message.reply_text("Por favor, especifica una categoría después del comando, por ejemplo: /paleta_blue o /paleta_green")

async def categorias_comando(update: Update, context: CallbackContext):
    categorias = obtener_categorias_de_base_de_datos()
    if categorias:
        mensaje = "Categorías disponibles:\n" + "\n".join(categorias)
        await update.message.reply_text(mensaje)
    else:
        await update.message.reply_text("No se encontraron categorías disponibles en la base de datos.")

async def mostrar_codigos(update: Update, context: CallbackContext):
    tabla = context.args[0] if context.args else "Uncategorized_pallettes"
    try:
        grupos_de_codigos = obtener_codigos_de_base_de_datos(tabla)
        if grupos_de_codigos:
            mensaje = f"Código de colores de la tabla '{tabla}':\n\n"
            for grupo in grupos_de_codigos:
                mensaje += " | ".join(grupo) + "\n"
            await update.message.reply_text(mensaje)
        else:
            await update.message.reply_text(f"No se encontraron códigos en la tabla '{tabla}'")
    except sqlite3.OperationalError:
            await update.message.reply_text(f"La tabla '{tabla}'no existe")

def obtener_pallette_random_uncategorized():
    conexion = sqlite3.connect('Paletas.db')
    cursor = conexion.cursor()
    cursor.execute("SELECT Code FROM Uncategorized_pallettes ORDER BY RANDOM() LIMIT 5")  # Limitamos a 5 colores
    resultados = cursor.fetchall()

    if resultados:
        paleta =[hex_to_rgb(fila[0]) for fila in resultados]
    else:
        paleta = ["No se encontró ninguna paleta"]

    conexion.close()

    return paleta

def obtener_pallette_random_categorized():
    conexion = sqlite3.connect('Paletas.db')
    cursor = conexion.cursor()
    cursor.execute("SELECT code FROM Categorized_pallettes ORDER BY RANDOM() LIMIT 5")
    resultados = cursor.fetchall()

    if resultados:
        paleta = [hex_to_rgb(fila[0]) for fila in resultados]
    else:
        paleta = ["No se encontró ninguna paleta"]

    conexion.close()

    return paleta

async def paleta_random(update: Update, context: CallbackContext):
        if random.choice([True,False]):
            paleta_elegida = obtener_pallette_random_uncategorized()
            categoria = "Uncategorized"
        else:
            paleta_elegida = obtener_pallette_random_categorized()
            categoria = "Categorized"

        plt.figure(figsize=(5, 1))
        plt.imshow([paleta_elegida], aspect='auto')
        plt.axis('off')

        plt.savefig('/tmp/paleta_random.png', bbox_inches='tight', pad_inches=0)
        plt.close()


        await update.message.reply_photo(photo=open('/tmp/paleta_random.png', 'rb'))

        colores_hexadecimales = [
        "#{:02x}{:02x}{:02x}".format(
            int(color[0] * 255), int(color[1] * 255), int(color[2] * 255)
        )
        for color in paleta_elegida
    ]
        mensaje_colores = (
        f"Paleta generada :\n" +
        "\n".join(colores_hexadecimales)
    )
        await update.message.reply_text(mensaje_colores)

async def iniciar(update: Update, context:CallbackContext):
    await update.message.reply_text('Hola! Soy Chocolors y puedo ayudarte a elegir la mejor paleta de colores.Si necesitas más info, /help.')


async def ayuda(update: Update, context: CallbackContext):
    mensaje_ayuda = (
        "Aquí tienes una lista de comandos que puedes usar:\n"
        "/start - Inicia una conversación conmigo.\n"
        "/help - Muestra este mensaje de ayuda.\n"
        "/random - Genera y muestra una paleta de colores aleatoria.\n"
        "/paleta_ + color que quieras - Genera una paleta de colores partiendo de un color o tematica. Se divide en dos categorias:\n\n"
        "Colores disponibles:\n"
        "Gray, Yellow, Pink, Turquoise, Green, Violet, Blue, White, Brown, Black, Orange, Red\n\n"
        "Temática disponible:\n"
        "Pride, Halloween, Sunset, Christmas, Spring, Summer, Wedding, Gold, Winter, Autumn, Dark, Warm, Vintage, Gradient, Pastel, Monochromatic, Cold, Bright, Rainbow\n\n"
        "/hexa - Genera una paleta de colores a partir de un color hexadecimal.\n"
    )
    await update.message.reply_text(mensaje_ayuda)

def main():
    application = Application.builder().token(TOKEN).build()

    application.add_handler(CommandHandler("start", iniciar))
    application.add_handler(CommandHandler("random", paleta_random))
    application.add_handler(CommandHandler("help", ayuda))
    application.add_handler(CommandHandler("paleta", paleta_variable))
    application.add_handler(CommandHandler("hexa", paleta_hexadecimal))
    application.run_polling()

if __name__ == '__main__':
    main()
