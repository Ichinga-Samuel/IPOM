from pathlib import Path
import sys

from PyQt5 import QtWidgets
from PyQt5.QtCore import QSize, Qt, QRegExp, QRect, QPoint
from PyQt5.QtGui import QColor, QPalette, QPixmap, QFont, QIntValidator as IV, QDoubleValidator as DV, \
    QRegExpValidator as RV, QIcon, QTextItem, QPainter, QImage
from PyQt5.QtPrintSupport import QPrinter, QPrintDialog
from PyQt5.QtWidgets import (QApplication, QWidget, QLineEdit, QMainWindow, QPushButton, QLabel, QVBoxLayout,
                             QHBoxLayout, QGridLayout, QToolBar, QAction, QFormLayout, QDialog, QMessageBox, QStyle,
                             QTabWidget, QTableWidget, QTableWidgetItem, QStackedLayout, QGroupBox, QSizePolicy,
                             QSpacerItem, QMenu, QScrollArea, QFileDialog, QFrame, QLayout, QTabBar)

import qtmodern.styles
import qtmodern.windows

from configs.configs import static, homedir
from model.model import model, tabulate, format_results
from stylesheets.style import style
from report.report_builder import BuildDoc

root = Path()
if getattr(sys, 'frozen', False):
    root = Path(sys._MEIPASS)
    qtmodern.styles._STYLESHEET = root / 'qtmodern/style.qss'
    qtmodern.windows._FL_STYLESHEET = root / 'qtmodern/frameless.qss'

homedir(typ='')


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Integrated Palm Oil Machine Designer")
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.lo = MainLayout()
        self.setCentralWidget(self.lo.tabs)
        self.setStyleSheet(style('style1'))

    def createDialog(self, info):
        dlg = QDialog()
        dlg.setWindowTitle('Invalid Input')
        dlg.setWindowIcon(static('exclamation-red.png', 'ico'))


class MainLayout:
    def __init__(self):

        self.parameters = {}
        self.main = QVBoxLayout()
        container = QHBoxLayout()
        self.opf = QFormLayout()

        title = QLabel("Set Operational Parameters")
        title.setFont(QFont('Helvetica', 14))
        title.setAlignment(Qt.AlignCenter)
        self.opf.addRow(title)
        self.opf.setVerticalSpacing(20)
        ops = [('Nm', "Speed of Motor", '1450'), ('Nd', "Speed of Digester Shaft", '109'),
               ('Nc', "Speed of Cake Breaker Shaft", '109'), ('Na', "Speed of Auger Shaft", '218'),
               ('Nsp', "Speed of Screw Press Shaft", '60')]
        self.defaults = QPushButton('Clear')
        self.defaults.setToolTip('Toggle this button to use optimized values for Operational Parameters')
        self.defaults.setCheckable(1)
        self.defaults.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Maximum)
        self.defaults.toggled.connect(self._defaults)
        dl = QLabel('Reset')
        dl.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Maximum)
        for op in ops:
            opp = QLineEdit()
            opp.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Maximum)
            opp.setText(op[2])
            lb = QLabel(op[1])
            lb.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Maximum)
            opp.setPlaceholderText(op[1])
            opp.setObjectName(op[1])
            opp.setAccessibleName(op[0])
            opp.setInputMask('>0000;_')
            self.opf.addRow(lb, opp)
        self.opf.addRow(dl, self.defaults)

        frame = QFrame()
        frame.setLayout(self.opf)
        frame.setObjectName('opf')

        # Layout for Throughput input
        tpf = QVBoxLayout()
        self.capacity = QLineEdit()
        self.capacity.setAlignment(Qt.AlignLeft | Qt.AlignCenter)
        self.capacity.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Maximum)
        dv = DV(280, 5650, 3, self.capacity)
        dv.setNotation(DV.StandardNotation)
        self.capacity.setValidator(dv)
        self.capacity.setPlaceholderText('Enter value between 280 and 5650')
        title = QLabel("Set Throughput Capacity")
        title.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Maximum)
        title.setFont(QFont('Helvetica', 14))
        title.setAlignment(Qt.AlignLeft | Qt.AlignCenter)
        tpf.addWidget(title)
        tpf.addSpacing(15)
        tpf.addWidget(self.capacity)
        tpf.setAlignment(Qt.AlignLeft | Qt.AlignCenter)
        frame1 = QFrame()
        frame1.setLayout(tpf)
        frame1.setObjectName('tpf')

        container.addWidget(frame1)
        container.addSpacing(50)
        container.addWidget(frame)

        self.bs = QHBoxLayout()
        self.compute = QPushButton('Compute')
        self.compute.setCheckable(True)
        self.compute.clicked.connect(self.run)

        self.reset = QPushButton('Reset')
        self.reset.setCheckable(True)
        self.reset.clicked.connect(self._reset)
        self.reset.setEnabled(False)

        self.report = QPushButton('Generate Report')
        self.report.setCheckable(True)
        self.report.clicked.connect(self._generate)
        self.report.setEnabled(False)

        self.bs.addWidget(self.compute)
        self.bs.setSpacing(15)
        self.bs.addWidget(self.report)
        self.bs.addWidget(self.reset)
        self.bs.setAlignment(Qt.AlignCenter | Qt.AlignBottom)

        self.main.addLayout(container)
        self.main.addSpacing(20)
        self.main.addLayout(self.bs)

        mframe = QFrame()
        mframe.setLayout(self.main)
        mframe.setObjectName('main')
        mframe.setFrameShape(QFrame.StyledPanel)
        mframe.setFrameStyle(QFrame.Raised | QFrame.Panel)
        mframe.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Maximum)

        ml = QVBoxLayout()
        ml.addWidget(mframe)
        ml.setAlignment(Qt.AlignCenter | Qt.AlignTop)

        self.tabs = QTabWidget()
        self.tabs.setTabPosition(QTabWidget.North)
        self.tabs.setMovable(True)

        self.widget = QWidget()
        self.widget.setObjectName('mainf')
        self.widget.setContentsMargins(0, 50, 0, 0)
        self.widget.setLayout(ml)
        self.tabs.insertTab(0, self.widget, 'Results')

    def _defaults(self, s):
        dp = {'Nm': '1450', 'Nd': '109', 'Nc': '109', 'Na': '218', 'Nsp': '60'}
        num = self.opf.count()
        if s:
            self.defaults.setText('Defaults')
        else:
            self.defaults.setText('Clear')
        for i in range(num):
            child = self.opf.itemAt(i).widget()
            if isinstance(child, QLineEdit):
                if s:
                    child.setText('')
                else:
                    child.setText(dp[child.accessibleName()])

    def _generate(self):
        path = homedir('m')
        path = str(path / self.parameters['filename'])
        file, _ = QFileDialog.getSaveFileName(self.report, 'Save Manual', path, "PDF Format (*.pdf)")

        if file:
            BuildDoc(self.parameters, file)

    def run(self, s):
        res = self.validate()
        if res['status']:
            tpd, op = res['results'][0], res['results'][1:]
            output = model(tpd, op)
            self.parameters = format_results(output, tpd)
            self.buiildTables()
            self.showImages()
            self.compute.setDisabled(True)
            self.reset.setEnabled(True)
            self.report.setEnabled(True)
        else:
            self.msgBox(res['err'])

    def _reset(self, r):
        self.compute.setDisabled(False)
        while self.tabs.count() > 1:
            self.tabs.removeTab(1)
        self.reset.setEnabled(False)
        self.report.setEnabled(False)

    def validate(self):
        err = ''
        inputs = []
        try:
            if (i := self.capacity.text()) and (280 <= int(i) <= 5650):
                inputs.append(int(i))
            else:
                err = 'ThroughPut value falls outside acceptable range'
                self.capacity.setFocus()
                raise ValueError('')

            num = self.opf.count()
            for i in range(num):
                child = self.opf.itemAt(i).widget()
                if isinstance(child, QLineEdit) and not (j := child.text()):
                    err = f"{child.objectName()} Value is not Valid"
                    child.setFocus()
                    raise ValueError('')
                elif isinstance(child, QLabel) or isinstance(child, QPushButton):
                    continue
                else:
                    inputs.append(int(j))

        except ValueError:
            return {'status': False, 'err': err}
        else:
            return {'status': True, 'results': inputs}

    def msgBox(self, msg):
        mb = QMessageBox()
        mb.setWindowTitle('Invalid Input(s)')
        mb.setText(msg)
        mb.setIcon(QMessageBox.Warning)
        mb.setStandardButtons(QMessageBox.Ok)
        s = mb.style()
        ico = s.standardIcon(QStyle.SP_MessageBoxCritical)
        mb.setWindowIcon(ico)
        mb.exec_()

    def buiildTables(self):
        for section in self.parameters['sections']:
            if section['data']:
                table = DataLayout(section)
                table.setAccessibleName(section['title'])
                self.tabs.addTab(table, section['title'])

    def showImages(self):
        for s in self.parameters['sections']:
            if not s['drawings']:
                continue
            p = [(i['files'], i['name']) for i in s['drawings']]
            main = Display(p)
            main.setAccessibleName(s['title'])
            self.tabs.addTab(main, s['title'])


class DataLayout(QWidget):

    def __init__(self, unit):
        super(DataLayout, self).__init__()
        self.unit = unit

        self.table = QTableWidget()
        self.table.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.table.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.table.setSizeAdjustPolicy(QTableWidget.AdjustToContents)
        self.table.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Maximum)
        self.table.setFrameStyle(2)

        l = QLabel(self.unit['title'])
        l.setAlignment(Qt.AlignCenter)
        l.setFont(QFont('Helvetica', 18))

        lo = QVBoxLayout()
        lo.setAlignment(Qt.AlignCenter | Qt.AlignTop)
        lo.setContentsMargins(20, 20, 20, 20)
        lo.addWidget(l)
        lo.addSpacing(20)
        lo.addWidget(self.table)

        self.build()
        self.table.resizeColumnsToContents()
        self.table.resizeRowsToContents()
        self.setLayout(lo)

    def build(self):
        data = self.unit['data']
        self.table.setRowCount(len(data[1:]))
        self.table.setColumnCount(3)

        # set the header of the table
        [self.table.setHorizontalHeaderItem(k, QTableWidgetItem(str(j))) for k, j in enumerate(data[0])]
        for i, d in enumerate(data[1:]):
            [self.table.setItem(i, k, QTableWidgetItem(str(j))) for k, j in enumerate(d)]


class Display(QScrollArea):
    def __init__(self, parts):
        super().__init__()

        self.parts = parts   # Part files of the unit
        self.num = len(parts)
        self.counter = 0

        # main layout of the tab
        mstack = QHBoxLayout()

        # Contains the drawing on display and button stack for traversing the drawings and the caption of the image on display
        dstack = QVBoxLayout()

        # Contains the thumbnails of all images available for that unit
        self.tstack = QVBoxLayout()
        self.tstack.setContentsMargins(0, 20, 0, 20)
        self.create_tstack()
        tscroll = QScrollArea()
        twidget = QWidget()
        twidget.setLayout(self.tstack)
        tscroll.setWidget(twidget)
        tscroll.setMaximumWidth(150)
        tscroll.setWidgetResizable(True)
        tscroll.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        tscroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        tscroll.setFrameStyle(0)

        # The buttons for traversing the drawings of the unit are in the layout bstack
        bstack = QHBoxLayout()
        self.next_ = QPushButton(QIcon(static('arrow.png', 'ico')), 'Next')
        self.prev = QPushButton(QIcon(static('arrow-180.png', 'ico')), 'Previous')
        self.prev.clicked.connect(self._prev)
        self.next_.clicked.connect(self._next)
        bstack.addStretch()
        bstack.addWidget(self.prev, 0, Qt.AlignLeft)
        bstack.addSpacing(50)
        bstack.addWidget(self.next_, 0, Qt.AlignRight)
        bstack.addStretch()

        # A widget to display the drawings for that component
        self.display = QLabel()
        self.display.setMaximumSize(900, 900)
        self.display.setAlignment(Qt.AlignCenter)
        # self.display.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)
        self.image = QImage(self.size(), QImage.Format_RGB32)

        self.display.setPixmap(QPixmap(static(parts[0][0], 'img')).scaled(self.display.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation))
        self.display.setScaledContents(True)

        # Implements a context menu for interacting with the displayed image
        self.display.setContextMenuPolicy(Qt.CustomContextMenu)
        self.display.customContextMenuRequested.connect(self.context_menu)

        # A description and title of the displayed image
        self.caption = QLabel(parts[0][1])
        self.caption.setAccessibleName(parts[0][0])
        self.caption.setFont(QFont('Helvetica', 18))
        self.caption.setAlignment(Qt.AlignCenter)

        # TODO: Can image be made to popup and show in full?

        dstack.addWidget(self.display, 0, Qt.AlignCenter)
        dstack.addSpacing(20)
        dstack.setContentsMargins(0, 20, 0, 20)
        dstack.addWidget(self.caption)
        dstack.addSpacing(20)
        dstack.addLayout(bstack)
        dstack.addStretch()

        mstack.addStretch()
        mstack.addLayout(dstack)
        mstack.addStretch()
        mstack.addWidget(tscroll)

        self.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.chkbtns()
        mwidget = QWidget()
        mwidget.setLayout(mstack)
        self.setAlignment(Qt.AlignCenter)
        self.setWidget(mwidget)
        self.setWidgetResizable(True)

    def _next(self):
        self.counter += 1
        self.slide()

    def _prev(self):

        self.counter -= 1
        self.slide()

    def slide(self):
        self.chkbtns()
        self.caption.setText(self.parts[self.counter][1])
        self.caption.setAccessibleName(self.parts[self.counter][0])
        self.display.setPixmap(QPixmap(static(self.parts[self.counter][0], 'img')))

    def chkbtns(self):
        if self.num <= self.counter + 1:
            self.next_.setEnabled(False)
        else:
            self.next_.setEnabled(True)

        if self.counter <= 0:
            self.prev.setEnabled(False)
        else:
            self.prev.setEnabled(True)

    def goto(self, x=0):
        self.counter = x
        self.slide()

    def create_tstack(self):
        """
        Populate the thumbnails layout tstack with 100X100 thumbnails of the drawings for the unit
        :param self:
        :return:
        """
        for f, c in self.parts:
            tindex = self.parts.index((f, c))
            i = QLabel()
            i.setMaximumSize(100, 100)
            # i.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)
            i.setPixmap(QPixmap(static(f, 'img')).scaled(i.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation))
            i.setScaledContents(True)
            c = QPushButton(c)
            c.pressed.connect(lambda x=tindex: self.goto(x=x))
            self.tstack.addWidget(i, 0, Qt.AlignCenter)
            self.tstack.addWidget(c, 0, Qt.AlignCenter)
            self.tstack.addSpacing(5)
        self.tstack.addStretch()

    def context_menu(self, pos):
        context = QMenu(self.display)
        self.save = QAction("save", self.display)
        self.save.triggered.connect(self.save_image)
        self.print = QAction("print", self.display)
        self.print.triggered.connect(self.print_image)
        context.addAction(self.save)
        context.addAction(self.print)
        context.exec_(self.display.mapToGlobal(pos))

    def save_image(self):
        path = str(homedir('i') / self.caption.accessibleName())
        image_file, _ = QFileDialog.getSaveFileName(self, "Save Image", path, "JPG Files (*.jpeg *.jpg );;PNG Files (*.png);;Bitmap Files (*.bmp)")
        if image_file:  # and self.image.isNull() == False:
            self.display.pixmap().save(image_file)
        else:
            QMessageBox.information(self, "Error", "Unable to save image.", QMessageBox.Ok)

    def print_image(self):
        printer = QPrinter()
        printer.setOutputFormat(QPrinter.NativeFormat)

        # Create printer dialog to configure printer
        print_dialog = QPrintDialog(printer)

        if print_dialog.exec_() == QPrintDialog.Accepted:
            # Use QPainter to output a PDF file
            painter = QPainter()
            # Begin painting device
            painter.begin(printer)
            # Set QRect to hold painter's current viewport, which is the display
            rect = QRect(painter.viewport())
            # Get the size of display and use it to set the size of the viewport
            size = QSize(self.display.pixmap().size())
            size.scale(rect.size(), Qt.KeepAspectRatio)

            painter.setViewport(rect.x(), rect.y(), size.width(), size.height())
            painter.setWindow(self.display.pixmap().rect())
            # Scale the image_label to fit the rect source (0, 0)
            painter.drawPixmap(0, 0, self.display.pixmap())
            # End painting
            painter.end()


app = QApplication(sys.argv)
qtmodern.styles.dark(app)
win = MainWindow()

mw = qtmodern.windows.ModernWindow(win)
mw.show()

app.exec_()
