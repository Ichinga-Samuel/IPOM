import sys
from reportlab.pdfgen.canvas import Canvas
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle as PS
from reportlab.lib.units import inch
from reportlab.platypus import Paragraph, Image, Table, TableStyle, PageTemplate, BaseDocTemplate, PageBreak, Spacer
from reportlab.platypus.frames import Frame
from reportlab.lib.pagesizes import A4

from configs.configs import static
from .dims import *

styles = getSampleStyleSheet()
sub = PS(name='subtitle', alignment=1)
bodytext = PS(name='body', alignment=4)


class PageBuilder:

    def __init__(self, stories=None):
        self.stories = stories if isinstance(stories, list) else []

    def add_header(self, heading, level=1, Title=False):
        style = 'Title' if Title else f"Heading{level}"  # Title or f"Heading{level}"
        self.stories.append(Paragraph(heading, styles[style]))

    def add_body(self, body):
        self.stories.append(Paragraph(body, bodytext))

    def add_paragraph(self, body, pstyles={}, style=''):
        style = styles[style] if style else PS(**pstyles)
        self.stories.append(Paragraph(body, style))

    def add_image(self, part, w=70, h=80, align='CENTER', kwn=True, cover=False):
        """
        Adds a part's image, it's caption and any accompanying text to the report
        :param part: {'name': 'Component Drawings', 'definition': '', 'files': 'Components 1.jpg'}
        :param w: The width of the image
        :param h: The height of the image
        :param align:
        :param kwn:
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
        # self.stories.append(Paragraph(title, sub))

    def add_table(self, data, tstyles=None, kwargs=None):
        if tstyles is None:
            tstyles = []
        if kwargs is None:
            kwargs = {}
        t = Table(data, **kwargs)
        if tstyles:
            t.setStyle(TableStyle(tstyles))
        self.stories.append(t)

    def add_flowable(self, flow):
        self.stories.append(flow)


class BuildDoc(BaseDocTemplate):

    def __init__(self, output, fname, **kw):
        self.allowSplitting = 0
        filename = fname
        BaseDocTemplate.__init__(self, filename, **kw)
        padding = dict(leftPadding=px(5), bottomPadding=px(5), rightPadding=px(5), topPadding=px(5))
        template2 = PageTemplate('normal', [Frame(0, 0, px(100), py(100), **padding, id='F1'), Frame(px(95), py(95), px(5), py(5), id='F3')], onPage=self.add_page_number,
                                 onPageEnd=self.add_page_number)
        template1 = PageTemplate('cover', [Frame(0, 0, px(100), py(100), **padding, id='F2')], onPage=self.add_author,
                                 onPageEnd=self.add_author, autoNextPageTemplate=1)
        self.addPageTemplates([template1, template2])
        self.stories = []
        self.PB = PageBuilder(stories=self.stories)
        self.output = output
        self.header = None
        self.cover()
        self.section()
        self.build(self.stories)

    @staticmethod
    def add_page_number(canvas, doc):
        canvas.saveState()
        canvas.setFont('Times-Roman', 10)
        page_number_text = "%d" % doc.page
        canvas.drawCentredString(
            px(50),
            py(2),
            page_number_text
        )
        canvas.restoreState()

    @staticmethod
    def add_author(canvas, doc):
        canvas.saveState()
        canvas.setFont('Times-Roman', 18)
        canvas.drawCentredString(px(50), py(2), "Oti Onyedikachi")
        canvas.restoreState()

    def cover(self):
        self.PB.add_header(self.output["cover"]['title'])
        self.PB.add_flowable(Spacer(dx(5), dy(15)))
        self.PB.add_image(self.output['cover']['image'], w=70, h=80, kwn=False, cover=True)
        self.PB.add_flowable(PageBreak())

    def handle_pageBegin(self):
        if (x := self.pageTemplate).id == 'normal':
            self.canv.drawCentredString(px(95), py(95), self.header)
        super(BuildDoc, self).handle_pageBegin()

    # def beforePage(self):
    #     if self.header:
    #         b = self.pageTemplate.frame[0]
    #
    #         self.canv.drawCentredString(px(95), py(95), self.header)

    def section(self):
        """
        Build the report for each unit of the machine
        as defined in sections of the output dict
        :return:
        """
        for section in self.output['sections']:
            self.header = section['title']
            self.PB.add_header(section['title'], Title=True)
            if section['data']:
                self.PB.add_table(section['data'], tstyles=[('BOX', (0,0), (-1,-1), 0.25, colors.black), ('INNERGRID', (0,0), (-1,-1), 0.25, colors.black)])
            self.PB.add_flowable(PageBreak())
            if parts := section['drawings']:
                for part in parts:
                    self.PB.add_image(part)
                    self.PB.add_flowable(PageBreak())







