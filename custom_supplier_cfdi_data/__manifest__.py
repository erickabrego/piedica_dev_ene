# -*- coding: utf-8 -*-
{
    'name': "Cambio de emisor CFDI",

    'summary': """
        Cambio del contacto de donde se obtiene la información del emisor para crear la factura.
    """,
    'description': """
        Cambio del contacto de donde se obtiene la información del emisor para crear la factura de cliente, agregando
        un campo nuevo en el catálogo de empresas.
    """,
    'author': "M22",
    'website': "http://www.m22.mx",
    'category': 'Contabilidad',
    'version': '14.0.1',
    'depends': ['base','l10n_mx_edi'],
    'data': ['views/res_company.xml'],
    'license': 'AGPL-3'

}
