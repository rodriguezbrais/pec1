# PRA1: Web Scraping de TripAdvisor con Python
### Composición del grupo
* Nombre: Brais Rodríguez Martínez, usuario: brodmar
### Ficheros asociados al proyecto
* hotel_scraping.py: el archivo principal donde se concentra todo el código desarrollado. Este script consta de varias partes y métodos:
  * **Imports:** primera sección del script donde se especifican todas las dependencias del script.
  * **Parámetros y variables:** sección donde se especifica toda la información básica y estática que se va a usar en el proyecto. El único parámetro dinámico sería **hotel_link** y **nHotels**, donde el primero especifica la zona de la que se quiere hacer scraping y la segunda el número de hoteles más destacados de esa zona. La creación de las variables estáticas se ha hecho para evitar el **hardcoding** y facilitar futuros evolutivos en caso de que la web cambie.
  * **Métodos:** a continuación, se comentan los métodos usados.
    * get_points_from_class(review_element): es un método de conversión de las clases css que usa TripAdvisor para representar la puntuación de los hoteles, con burbujas y medias burbujas verdes, a número decimales: 4 para 4 bolas, 2.5 para 2 bolas y media, etc.
    * format_date(date): se encarga de formatear las fechas de tipo texto, en formato "Fecha de la estancia: MMM de YYYY", a formato de fecha MM-YYYY.
    * format_review_count(hotel_review_count): convierte los datos de número de reviews de texto a entero.
    * extract_hotels(hotels_html): método principal que realiza la extracción de la información a partir del html de la página. Recorre los n primeros hoteles más destacados obteniendo el nombre, el contador de reviews y asignándole un id incremental. Para cada uno de ellos, accede a su URL y, por cada página, recoge 5 reviews de ese hotel. Todo ello dejando una pausa de entre 1 y 5 segundos entre páginas para no sobrecargar la página.
    * set_user_agent(): de la lista de agentes web, selecciona uno aleatorio para cada petición que se hace del html.
    * generate_csv(): a partir de la información de las listas de hoteles y reviews, genera los datasets finales.
    * check_reviews_number(hotel_review_count): comprueba si el hotel tiene reviews, si no tiene ya no realiza la petición de su URL.
### DOI de Zenodo
https://zenodo.org/record/5614241
