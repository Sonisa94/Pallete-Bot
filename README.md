# Pallete-Bot

"Chocolors" is a Telegram bot that helps you create and explore color palettes easily.

***Features***:
- Generate random color palettes.
- Create palettes from a specific hexadecimal color.
- Explore palettes by category or theme (e.g., Sunset, Pastel, Christmas).
- Simple commands for quick interaction.

***Commands***:
- **/start** – Start the bot.
- **/help** – Show a list of commands.
- **/random** – Generate a random color palette.
- **/paleta [category]** – Generate a palette for a specific category.
    - *Categories include*:
      - ***Colors**: Gray, Yellow, Pink, Turquoise, Green, Violet, Blue, White, Brown, Black, Orange, Red*
      - ***Themes**: Pride, Halloween, Sunset, Christmas, Spring, Summer, Wedding, Gold, Winter, Autumn, Dark, Warm, Vintage, Gradient, Pastel, Monochromatic,               Cold,Bright, Rainbow.*
 - /hexa [#HEXCODE] - Create a pallette from a hexadecimal code (example: /hexa #FF573)

***Requirements***:
- Python
- Telegram Bot Token
- SQLite database (In this case, I provide a uncategorized database sample to test the bot. **IMPORTANT**: You'll need to rename the sample file to Paletas.db and need to create a table with "Categorized" colors in database,otherwise, you'll only be able to use the command /random)
