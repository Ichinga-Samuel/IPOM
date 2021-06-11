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
                             QSpacerItem, QMenu, QScrollArea, QFileDialog, QFrame, QLayout, QTabBar, QRadioButton, QSpinBox)

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
        main_layout = QVBoxLayout()   # Main layout containing the initial view
        inputs_layout = QHBoxLayout()   # layout for parameters configuration
        self.opp_form = QFormLayout()    # operational parameters Form
        opp_layout = QVBoxLayout()  # operational parameters layout
        opp_frame = QFrame()               # frame for operational parameters layout
        # self.opp_form.setFormAlignment(Qt.AlignLeft)
        opp_layout.addLayout(self.opp_form)

        # Operational Parameters Content
        # Speed of Motor
        speed_level_layout = QHBoxLayout()  # special layout for speed of motor
        speed_level_buttons_box = QGroupBox()    # group box for speed radio buttons
        speed_level_buttons_box.setTitle('Speed Level of Motor')
        speed_levels = ["High", "Medium", "Low"]
        self.speed_level_buttons = [QRadioButton(btn) for btn in speed_levels]  # speed radio buttons
        [(btn.clicked.connect(self.setSpeedLevel), speed_level_layout.addWidget(btn)) for btn in self.speed_level_buttons]
        speed_level_buttons_box.setLayout(speed_level_layout)

        motor_speed_layout = QHBoxLayout()  # layout for spinbox inputs
        high_speed = QSpinBox()
        high_speed.setSuffix(' rpm')
        high_speed.setEnabled(True)
        high_speed.valueChanged.connect(self.speedOfMotor)
        high_speed.setRange(2850, 3000)
        self.Nm = high_speed.value()
        medium_speed = QSpinBox()
        medium_speed.setSuffix(' rpm')
        medium_speed.setEnabled(False)
        medium_speed.valueChanged.connect(self.speedOfMotor)
        medium_speed.setRange(1440, 1480)
        low_speed = QSpinBox()
        low_speed.setSuffix(' rpm')
        low_speed.valueChanged.connect(self.speedOfMotor)
        low_speed.setEnabled(False)
        low_speed.setRange(950, 980)
        [motor_speed_layout.addWidget(w) for w in [high_speed, medium_speed, low_speed]]
        self.speed_input_widgets = {'High': high_speed, 'Medium': medium_speed, 'Low': low_speed}
        speed_input_box = QGroupBox()
        speed_input_box.setTitle('Select Speed Of Motor')
        speed_input_box.setLayout(motor_speed_layout)

        electric_motor_layout = QHBoxLayout()
        electric_motor_layout.addWidget(speed_level_buttons_box)
        electric_motor_layout.addWidget(speed_input_box)

        electric_motor_frame = QFrame()
        electric_motor_label = QLabel('Electric Motor Speed')
        electric_motor_frame.setLayout(electric_motor_layout)

        # opp_layout.addLayout(sil)
        opp_layout.addWidget(electric_motor_frame)
        opp_frame.setLayout(opp_layout)

        opp_form_title = QLabel("Set Operational Parameters")
        opp_form_title.setFont(QFont('Helvetica', 14))
        opp_form_title.setAlignment(Qt.AlignCenter)
        self.opp_form.addRow(opp_form_title)
        self.opp_form.setVerticalSpacing(20)
        opp_params = [('Nd', "Speed of Digester Shaft", '109'),
               ('Nc', "Speed of Cake Breaker Shaft", '109'), ('Na', "Speed of Auger Shaft", '218'),
               ('Nsp', "Speed of Screw Press Shaft", '60')]
        self.defaults_btn = QPushButton('Clear')
        self.defaults_btn.setToolTip('Toggle this button to use optimized values for Operational Parameters')
        self.defaults_btn.setCheckable(1)
        self.defaults_btn.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Maximum)
        self.defaults_btn.clicked.connect(self._defaults)
        self.opp_form.setFormAlignment(Qt.AlignCenter)
        for param in opp_params:
            param_input = QLineEdit()
            param_input.setAlignment(Qt.AlignCenter)
            param_input.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Maximum)
            param_input.setText(param[2])
            param_label = QLabel(param[1])
            param_label.setAlignment(Qt.AlignCenter)
            param_label.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Maximum)
            param_input.setPlaceholderText(param[1])
            param_input.setObjectName(param[0])
            param_input.setInputMask('>0000;_')
            self.opp_form.addRow(param_label, param_input)
        self.opp_form.addRow(self.defaults_btn)

        # Layout for Throughput input
        throughput_layout = QVBoxLayout()
        self.throughput_input = QLineEdit()
        self.throughput_input.setAlignment(Qt.AlignLeft | Qt.AlignCenter)
        self.throughput_input.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Maximum)
        throughput_validator = DV(280, 5650, 3, self.throughput_input)  # Validate throughput
        throughput_validator.setNotation(DV.StandardNotation)
        self.throughput_input.setValidator(throughput_validator)
        self.throughput_input.setPlaceholderText('Enter value between 280 and 5650')
        throughput_layout_title = QLabel("Set Throughput Capacity")
        throughput_layout_title.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Maximum)
        throughput_layout_title.setFont(QFont('Helvetica', 14))
        throughput_layout_title.setAlignment(Qt.AlignLeft | Qt.AlignCenter)
        throughput_layout.addWidget(throughput_layout_title)
        throughput_layout.addSpacing(15)
        throughput_layout.addWidget(self.throughput_input)
        throughput_layout.setAlignment(Qt.AlignLeft | Qt.AlignCenter)
        throughput_frame = QFrame()
        throughput_frame.setLayout(throughput_layout)
        throughput_frame.setObjectName('tpf')

        inputs_layout.addWidget(throughput_frame)
        inputs_layout.addSpacing(50)
        inputs_layout.addWidget(opp_frame)

        control_btns = QHBoxLayout()
        self.compute_btn = QPushButton('Compute')
        self.compute_btn.setCheckable(True)
        self.compute_btn.clicked.connect(self.run)

        self.reset_btn = QPushButton('Reset')
        self.reset_btn.setCheckable(True)
        self.reset_btn.clicked.connect(self._reset)
        self.reset_btn.setEnabled(False)

        self.report_btn = QPushButton('Generate Report')
        self.report_btn.setCheckable(True)
        self.report_btn.clicked.connect(self._generate)
        self.report_btn.setEnabled(False)

        control_btns.addWidget(self.compute_btn)
        control_btns.setSpacing(15)
        control_btns.addWidget(self.report_btn)
        control_btns.addWidget(self.reset_btn)
        control_btns.setAlignment(Qt.AlignCenter | Qt.AlignBottom)

        main_layout.addLayout(inputs_layout)
        main_layout.addSpacing(20)
        main_layout.addLayout(control_btns)
        main_layout.setAlignment(Qt.AlignCenter | Qt.AlignTop)

        main_frame = QFrame()
        main_frame.setLayout(main_layout)
        main_frame.setObjectName('main')
        main_frame.setFrameShape(QFrame.StyledPanel)
        main_frame.setFrameStyle(QFrame.Raised | QFrame.Panel)
        main_frame.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Maximum)
        main_frame.setContentsMargins(0, 50, 0, 0)

        self.tabs = QTabWidget()
        self.tabs.setTabPosition(QTabWidget.North)
        self.tabs.setMovable(True)

        self.tabs.insertTab(0, main_frame, 'Results')

    def setSpeedLevel(self, s):
        for btn in self.speed_level_buttons:
            if btn.isChecked():
                level = btn.text()
                sp = self.speed_input_widgets[level]
                sp.setEnabled(True)
                [v.setEnabled(False) for k, v in self.speed_input_widgets.items() if k!=level]

    def speedOfMotor(self, speed):
        self.Nm = speed

    def _defaults(self, state):
        default_values = {'Nd': '109', 'Nc': '109', 'Na': '218', 'Nsp': '60'}
        num = self.opp_form.count()
        if state:
            self.defaults_btn.setText('Defaults')
        else:
            self.defaults_btn.setText('Clear')
        for i in range(num):
            child = self.opp_form.itemAt(i).widget()
            if isinstance(child, QLineEdit):
                if state:
                    child.setText('')
                else:
                    child.setText(default_values[child.objectName()])

    def _generate(self):
        path = homedir('m')   # obtain path for creating storing pdf file
        path = str(path / self.parameters['filename'])
        file, _ = QFileDialog.getSaveFileName(self.report_btn, 'Save Manual', path, "PDF Format (*.pdf)")

        if file:
            BuildDoc(self.parameters, file)

    def run(self, state):
        res = self.validate()
        if res['status']:
            tpd, op = res['results'][0], res['results'][1:]
            output = model(tpd, op)
            self.parameters = format_results(output, tpd)
            self.buildTables()
            self.showImages()
            self.compute_btn.setDisabled(True)
            self.reset_btn.setEnabled(True)
            self.report_btn.setEnabled(True)
        else:
            self.msgBox(res['err'])

    def _reset(self, state):
        self.compute_btn.setDisabled(False)
        while self.tabs.count() > 1:
            self.tabs.removeTab(1)
        self.reset_btn.setEnabled(False)
        self.report_btn.setEnabled(False)

    def validate(self):
        err = ''
        inputs = []
        try:
            if (i := self.throughput_input.text()) and (280 <= int(i) <= 5650):
                inputs.append(int(i))
            else:
                err = 'ThroughPut value falls outside acceptable range'
                self.throughput_input.setFocus()
                raise ValueError('')

            num = self.opp_form.count()
            for i in range(num):
                child = self.opp_form.itemAt(i).widget()
                if isinstance(child, QLineEdit) and not (value:= child.text()):
                    err = f"{child.objectName()} Value is not Valid"
                    child.setFocus()
                    raise ValueError('')
                elif isinstance(child, QLabel) or isinstance(child, QPushButton):
                    continue
                else:
                    inputs.append(int(value))
            inputs.insert(1, self.Nm)

        except ValueError:
            return {'status': False, 'err': err}
        else:
            return {'status': True, 'results': inputs}

    def msgBox(self, msg):
        msg_box = QMessageBox()
        msg_box.setWindowTitle('Invalid Input(s)')
        msg_box.setText(msg)
        msg_box.setIcon(QMessageBox.Warning)
        msg_box.setStandardButtons(QMessageBox.Ok)
        style = msg_box.style()
        ico = style.standardIcon(QStyle.SP_MessageBoxCritical)
        msg_box.setWindowIcon(ico)
        msg_box.exec_()

    def buildTables(self):
        for section in self.parameters['sections']:
            if section['data']:
                table = DataLayout(section)
                table.setAccessibleName(section['title'])
                self.tabs.addTab(table, section['title'])

    def showImages(self):
        for section in self.parameters['sections']:
            if not section['drawings']:
                continue
            page = [(i['files'], i['name']) for i in section['drawings']]
            main = Display(page)
            main.setAccessibleName(section['title'])
            self.tabs.addTab(main, section['title'])


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

        table_label = QLabel(self.unit['title'])
        table_label.setAlignment(Qt.AlignCenter)
        table_label.setFont(QFont('Helvetica', 18))

        table_layout = QVBoxLayout()
        table_layout.setAlignment(Qt.AlignCenter | Qt.AlignTop)
        table_layout.setContentsMargins(20, 20, 20, 20)
        table_layout.addWidget(table_label)
        table_layout.addSpacing(20)
        table_layout.addWidget(self.table)

        self.build_table()
        self.table.resizeColumnsToContents()
        self.table.resizeRowsToContents()
        self.setLayout(table_layout)

    def build_table(self):
        data = self.unit['data']
        self.table.setRowCount(len(data[1:]))
        self.table.setColumnCount(3)

        # set the header of the table
        [self.table.setHorizontalHeaderItem(index, QTableWidgetItem(str(header))) for index, header in enumerate(data[0])]
        for index, param in enumerate(data[1:]):
            [self.table.setItem(index, pos, QTableWidgetItem(str(value))) for pos, value in enumerate(param)]


class Display(QScrollArea):
    def __init__(self, parts):
        super().__init__()

        self.parts = parts   # Part files of the unit
        self.num = len(parts)
        self.counter = 0

        # main layout of the tab
        main_layout = QHBoxLayout()

        # Contains the drawing on display and button stack for traversing the drawings and the caption of the image on display
        display_layout = QVBoxLayout()

        # Contains the thumbnails of all images available for that unit
        self.thumbnails_layout = QVBoxLayout()
        self.thumbnails_layout.setContentsMargins(0, 20, 0, 20)
        self.create_thumbnails()
        thumbnails_scroll = QScrollArea()

        thumbnails_widget = QWidget()
        thumbnails_widget.setLayout(self.thumbnails_layout)
        thumbnails_scroll.setWidget(thumbnails_widget)
        thumbnails_scroll.setMaximumWidth(150)
        thumbnails_scroll.setWidgetResizable(True)
        thumbnails_scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        thumbnails_scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        thumbnails_scroll.setFrameStyle(0)

        # The buttons for traversing the drawings of the unit are in the layout bstack
        control_buttons = QHBoxLayout()
        self.next_btn = QPushButton(QIcon(static('arrow.png', 'ico')), 'Next')
        self.previous_btn = QPushButton(QIcon(static('arrow-180.png', 'ico')), 'Previous')
        self.previous_btn.clicked.connect(self.previous)
        self.next_btn.clicked.connect(self._next)
        control_buttons.addStretch()
        control_buttons.addWidget(self.previous_btn, 0, Qt.AlignLeft)
        control_buttons.addSpacing(50)
        control_buttons.addWidget(self.next_btn, 0, Qt.AlignRight)
        control_buttons.addStretch()

        # A widget to display the drawings for that component
        self.image_display = QLabel()
        self.image_display.setMaximumSize(900, 900)
        self.image_display.setAlignment(Qt.AlignCenter)
        # self.image_display.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)
        self.image = QImage(self.size(), QImage.Format_RGB32)

        self.image_display.setPixmap(QPixmap(static(parts[0][0], 'img')).scaled(self.image_display.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation))
        self.image_display.setScaledContents(True)

        # Implements a context menu for interacting with the displayed image
        self.image_display.setContextMenuPolicy(Qt.CustomContextMenu)
        self.image_display.customContextMenuRequested.connect(self.context_menu)

        # A description and title of the displayed image
        self.image_caption = QLabel(parts[0][1])
        self.image_caption.setAccessibleName(parts[0][0])
        self.image_caption.setFont(QFont('Helvetica', 18))
        self.image_caption.setAlignment(Qt.AlignCenter)

        # TODO: Can image be made to popup and show in full?

        display_layout.addWidget(self.image_display, 0, Qt.AlignCenter)
        display_layout.addSpacing(20)
        display_layout.setContentsMargins(0, 20, 0, 20)
        display_layout.addWidget(self.image_caption)
        display_layout.addSpacing(20)
        display_layout.addLayout(control_buttons)
        display_layout.addStretch()

        main_layout.addStretch()
        main_layout.addLayout(display_layout)
        main_layout.addStretch()
        main_layout.addWidget(thumbnails_scroll)

        self.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.check_btns()
        self.setAlignment(Qt.AlignCenter)
        self.setLayout(main_layout)
        self.setWidgetResizable(True)

    def _next(self):
        self.counter += 1
        self.image_slide()

    def previous(self):

        self.counter -= 1
        self.image_slide()

    def image_slide(self):
        self.check_btns()
        self.image_caption.setText(self.parts[self.counter][1])
        self.image_caption.setAccessibleName(self.parts[self.counter][0])
        self.image_display.setPixmap(QPixmap(static(self.parts[self.counter][0], 'img')))

    def check_btns(self):
        if self.num <= self.counter + 1:
            self.next_btn.setEnabled(False)
        else:
            self.next_btn.setEnabled(True)

        if self.counter <= 0:
            self.previous_btn.setEnabled(False)
        else:
            self.previous_btn.setEnabled(True)

    def goto_image(self, index=0):
        self.counter = index
        self.image_slide()

    def create_thumbnails(self):
        """
        Populate the thumbnails layout tstack with 100X100 thumbnails of the drawings for the unit
        :param self:
        :return:
        """
        for image, caption in self.parts:
            index = self.parts.index((image, caption))
            img_label = QLabel()
            img_label.setMaximumSize(100, 100)
            # i.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)
            img_label.setPixmap(QPixmap(static(image, 'img')).scaled(image.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation))
            img_label.setScaledContents(True)
            view_btn = QPushButton(caption)
            view_btn.pressed.connect(lambda: self.goto_image(index=index))
            self.thumbnails_layout.addWidget(img_label, 0, Qt.AlignCenter)
            self.thumbnails_layout.addWidget(view_btn, 0, Qt.AlignCenter)
            self.thumbnails_layout.addSpacing(5)
        self.thumbnails_layout.addStretch()

    def context_menu(self, pos):
        context = QMenu(self.image_display)
        self.save_action = QAction("save", self.image_display)
        self.save_action.triggered.connect(self.save_image)
        self.print_action = QAction("print", self.image_display)
        self.print_action.triggered.connect(self.print_image)
        context.addAction(self.save_action)
        context.addAction(self.print_action)
        context.exec_(self.image_display.mapToGlobal(pos))

    def save_image(self):
        path = str(homedir('i') / self.image_caption.accessibleName())
        image_file, _ = QFileDialog.getSaveFileName(self, "Save Image", path, "JPG Files (*.jpeg *.jpg );;PNG Files (*.png);;Bitmap Files (*.bmp)")
        if image_file:  # and self.image.isNull() == False:
            self.image_display.pixmap().save(image_file)
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
            size = QSize(self.image_display.pixmap().size())
            size.scale(rect.size(), Qt.KeepAspectRatio)

            painter.setViewport(rect.x(), rect.y(), size.width(), size.height())
            painter.setWindow(self.image_display.pixmap().rect())
            # Scale the image_label to fit the rect source (0, 0)
            painter.drawPixmap(0, 0, self.image_display.pixmap())
            # End painting
            painter.end()


app = QApplication(sys.argv)
qtmodern.styles.dark(app)
win = MainWindow()

mw = qtmodern.windows.ModernWindow(win)
mw.show()

app.exec_()
