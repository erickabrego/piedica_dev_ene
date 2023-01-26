{
    'name': "Ajustes sitio web de Piédica",
    'summary': "Ajustes en el sitio web de Piédica",
    'description': """
        Realiza los siguientes ajustes en el sitio web:
            1) Modifica el snippet "image-text" para que en versión móvil se
            inviertan los elementos, es decir, muestre primero el texto y
            después la imagen.

            2) Agrega una etiqueta h1 a los títulos de los posts del blog.
    """,
    'author': 'M22',
    'category': 'Website/Website',
    'version': '14.0.1',
    'depends': ['website'],
    'data': [
        'views/assets.xml',
        'views/website_blog_templates.xml'
    ]
}
