from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle as PS
from reportlab.platypus import Paragraph, Image, Table, TableStyle, PageTemplate, BaseDocTemplate, PageBreak, Spacer
from reportlab.platypus.frames import Frame


from configs.configs import static
from .dims import *

styles = getSampleStyleSheet()
sub = PS(name='subtitle', alignment=1)
bodytext = PS(name='body', alignment=4)


class PageBuilder:

    def __init__(self, stories=None):
        self.stories = stories if isinstance(stories, list) else []

    def add_header(self, heading, level=1, title=False):
        style = 'Title' if title else f"Heading{level}"  # Title or f"Heading{level}"
        self.stories.append(Paragraph(heading, styles[style]))

    def add_body(self, body):
        self.stories.append(Paragraph(body, bodytext))

    def add_paragraph(self, body, p_styles=None, style=''):
        if p_styles is None: p_styles = {}
        style = styles[style] if style else PS(**p_styles)
        self.stories.append(Paragraph(body, style))

    def add_image(self, part, w=70, h=80, align='CENTER', kwn=True, cover=False):
        """
        Adds a part's image, it's caption and any accompanying text to the report
        :param part: {'name': 'Component Drawings', 'definition': '', 'files': 'Components 1.jpg'}
        :param w: The width of the image
        :param h: The height of the image
        :param align:
        :param kwn: keep with next
        :param cover: A boolean indicating that part will be a cover file for creating a cover image
        :return:
        """
        img = static(part['files'], 'img') if isinstance(part, dict) else static(part, 'img')
        w, h = px(w), px(h)
        img = Image(img, w, h)
        self.stories.append(img)
        if cover:
            return
        title = part['name']
        self.add_header(title, level=5)
        img.keepWithNext = kwn
        if body := part['definition']:
            self.add_body(body)

    def add_table(self, data, t_styles=None, **kwargs):
        if t_styles is None:
            t_styles = []
        t = Table(data, **kwargs)
        if t_styles:
            t.setStyle(TableStyle(t_styles))
        self.stories.append(t)

    def add_flowable(self, flow):
        self.stories.append(flow)


class BuildDoc(BaseDocTemplate):

    def __init__(self, result, file_name, **kw):
        self.allowSplitting = 0
        filename = file_name
        BaseDocTemplate.__init__(self, filename, **kw)
        padding = dict(leftPadding=px(5), bottomPadding=px(5), rightPadding=px(5), topPadding=px(5))
        page_template = PageTemplate('normal', [Frame(0, 0, px(100), py(100), **padding, id='F1'), Frame(px(95), py(95), px(5), py(5), id='F3')], onPage=self.add_page_number,
                                 onPageEnd=self.add_page_number)
        cover_template = PageTemplate('cover', [Frame(0, 0, px(100), py(100), **padding, id='F2')], onPage=self.add_author,
                                 onPageEnd=self.add_author, autoNextPageTemplate=1)
        self.addPageTemplates([cover_template, page_template])
        self.stories = []
        self.page_builder = PageBuilder(stories=self.stories)
        self.result = result
        self.cover()
        self.section()
        self.build(self.stories)

    @staticmethod
    def add_page_number(canvas, doc):
        canvas.saveState()
        canvas.setFont('Times-Roman', 10)
        page_number_text = "%d" % doc.page
        canvas.drawCentredString(px(50), py(2), page_number_text)
        canvas.restoreState()

    @staticmethod
    def add_author(canvas, doc):
        canvas.saveState()
        canvas.setFont('Times-Roman', 18)
        canvas.drawCentredString(px(50), py(2), "Oti Onyedikachi")
        canvas.restoreState()

    def cover(self):
        self.page_builder.add_header(self.result["cover"]['title'])
        self.page_builder.add_flowable(Spacer(dx(5), dy(15)))
        self.page_builder.add_image(self.result['cover']['image'], w=70, h=80, kwn=False, cover=True)
        self.page_builder.add_flowable(PageBreak())

    def section(self):
        """
        Build the report for each unit of the machine
        as defined in sections of the output dict
        :return:
        """
        for section in self.result['sections']:
            self.page_builder.add_header(section['title'], title=True)
            if section['data']:
                self.page_builder.add_table(section['data'], t_styles=[('BOX', (0,0), (-1,-1), 0.25, colors.black), ('INNERGRID', (0,0), (-1,-1), 0.25, colors.black)])
            self.page_builder.add_flowable(PageBreak())
            if parts := section['drawings']:
                for part in parts:
                    self.page_builder.add_image(part)
                    self.page_builder.add_flowable(PageBreak())







