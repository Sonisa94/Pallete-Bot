import random
import matplotlib.pyplot as plt
from telegram import Update
from telegram.ext import Application, CommandHandler, CallbackContext, MessageHandler, filters
import os

TOKEN = os.environ.get("TOKENCHOCOLORS")


paletas = {
    'paleta1':['#FF5733', '#33FF57', '#3357FF', '#F1C40F', '#8E44AD'],
    'paleta2':['#1ABC9C', '#2C3E50', '#E74C3C', '#F39C12', '#9B59B6'],
    'paleta3':['#FF5733', '#33FF57', '#C70039', '#900C3F', '#581845'],

}

async def enviar_paleta(update: Update, context: CallbackContext):
    paleta_elegida = random.choice(list(paletas.values()))

    plt.figure(figsize=(5,1))
    plt.imshow([paleta_elegida],aspect='auto')
    plt.axis('off')

    plt.savefig('/tmp/paleta.png', bbox_inches='tight', pad_inches=0)
    plt.close()

    await updater.message.reply_photo(photo=open('/tmp/paleta.png', 'rb'))

async def iniciar(update: Update, context:CallbackContext):
    await update.message.reply_text('Hola! Soy Chocolors, tu ayudante artificial.')

async def ver_paletas(update: Update, context: CallbackContext):
    paletas_listadas = "\n".join(paletas["paleta1"])
    await update.message.reply_text(f'Estas son las paletas que hay disponibles: \n{paletas_listadas}')

async def seleccionar_paleta(update: Update, context: CallbackContext):
    if context.args:
        nombre_paleta = context.arg[0]
        if nombre_paleta in paletas:
            paleta_elegida = paletas[nombre_paleta]
            plt.figure(figsize=(5,1))
            plt.imshow([paleta_elegida], aspect='auto')
            plt.axis('off')
            plt.savefig('/tmp/paleta_seleccionada.png',bbox_inches='tight', pad_inches=0)
            plt.close()
            await update.message.reply_photo(photo=open('/tmp/paleta_seleccionada.png', 'rb'))
        else:
            await update.message.reply_text(f'No existe paleta "{nombre_paleta}". Usa /ver_paletas para visualizar las disponibles')
    else:
        await update.message.reply_text('Por favor, especifica el nombre de la paleta. Usa /ver_paletas para ver disponibles.')

def main():
    application = Application.builder().token(TOKEN).build()

    application.add_handler(CommandHandler("start", iniciar))
    application.add_handler(CommandHandler("paleta", enviar_paleta))
    application.add_handler(CommandHandler("ver_paletas", ver_paletas))
    application.add_handler(CommandHandler("seleccionar_paleta", seleccionar_paleta))

    application.run_polling()

if __name__ == '__main__':
    main()
