
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import BaseDocTemplate, Frame, Paragraph, NextPageTemplate, PageBreak, PageTemplate, Image
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

from dims import *
from configs.configs import static


# # base_dir = Path(__file__).resolve().parent.parent
capacity = ''
title = f'Design Manual for {capacity}kg .pdf'
cover_image = static('images/coverimage.jpg')
def foot1(canvas, doc):
    canvas.saveState()
    canvas.setFont('Times-Roman', 19)
    canvas.drawString(dx(6), py(6), "Oti Onyedikachi")
    canvas.restoreState()

v = ParagraphStyle(name='Heading1', alignment=4)

template1 = PageTemplate('cover', [Frame(px(5), py(5), px(95), py(95), id='F1')], onPage=foot1)
b=BaseDocTemplate('pop.pdf')
b.addPageTemplates(template1)
n=getSampleStyleSheet()

s=[Paragraph(title, n['Normal']), Image(cover_image, px(75), py(75)), Paragraph('dgdfgdfgdfgdfgrd', style=v)]

b.build(s)
# leftMargin=dx(22), rightMargin=dx(22), topMargin=py(30), bottomMargin=py(30),
# main_canvas = canvas.Canvas(title, pagesize=A4, pageCompression=1)
#
# main_canvas.drawCentredString(dx(50), dy(50), title)
#
# main_canvas.drawImage(cover_image, cx, cy)

# main_canvas.setAuthor('Oti Onyedikachi')
# main_canvas.setTitle(title[:-5])
# main_canvas.showPage()
# main_canvas.save()

# styles = ParagraphStyle('body')
#
# print(styles)
# print(n.list())
# #print(cover_image)
