from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import sys
from os.path import join, isfile
import json
from galaxy_generator import generate


class GalaxyGenerator(QMainWindow):
	def __init__(self):
		super().__init__()
		self.lang = json.load(open('lang.json', 'r'))['English']
		self.initUI()
	
	
	def initUI(self):
		self.setObjectName('win')
		self.setFixedSize(528, 292)
		self.main_win = QWidget(self)
		self.main_win.setObjectName(u'main_win')

		self.btn_open = QPushButton(self.main_win)
		self.btn_open.setObjectName(u'btn_open')
		self.btn_open.setGeometry(QRect(20, 260, 111, 23))
		self.btn_open.pressed.connect(self.find_game)

		self.btn_gen = QPushButton(self.main_win)
		self.btn_gen.setObjectName(u'btn_gen')
		self.btn_gen.setGeometry(QRect(210, 260, 111, 23))
		self.btn_gen.setEnabled(False)
		self.btn_gen.pressed.connect(self.gen)

		self.btn_close = QPushButton(self.main_win)
		self.btn_close.setObjectName(u'btn_close')
		self.btn_close.setGeometry(QRect(400, 260, 111, 23))
		self.btn_close.pressed.connect(self.close)

		self.cb_balance_tech = QCheckBox(self.main_win)
		self.cb_balance_tech.setObjectName(u'cb_balance_tech')
		self.cb_balance_tech.setGeometry(QRect(210, 70, 181, 21))

		self.cb_colors = QCheckBox(self.main_win)
		self.cb_colors.setObjectName(u'cb_colors')
		self.cb_colors.setGeometry(QRect(10, 70, 181, 21))
		self.cb_colors.setChecked(True)

		self.g_factions = QGroupBox(self.main_win)
		self.g_factions.setObjectName(u'g_factions')
		self.g_factions.setGeometry(QRect(10, 100, 511, 151))

		self.cb_faction1 = QCheckBox(self.g_factions)
		self.cb_faction1.setObjectName(u'cb_faction1')
		self.cb_faction1.setGeometry(QRect(10, 30, 131, 21))
		self.cb_faction1.setChecked(True)

		self.cb_faction2 = QCheckBox(self.g_factions)
		self.cb_faction2.setObjectName(u'cb_faction2')
		self.cb_faction2.setGeometry(QRect(10, 60, 131, 21))
		self.cb_faction2.setChecked(True)

		self.cb_faction3 = QCheckBox(self.g_factions)
		self.cb_faction3.setObjectName(u'cb_faction3')
		self.cb_faction3.setGeometry(QRect(10, 90, 181, 21))
		self.cb_faction3.setChecked(True)

		self.cb_faction4 = QCheckBox(self.g_factions)
		self.cb_faction4.setObjectName(u'cb_faction4')
		self.cb_faction4.setGeometry(QRect(10, 120, 131, 21))
		self.cb_faction4.setChecked(True)

		self.cb_faction5 = QCheckBox(self.g_factions)
		self.cb_faction5.setObjectName(u'cb_faction5')
		self.cb_faction5.setGeometry(QRect(230, 30, 151, 21))

		self.lbl_faction5_min = QLabel(self.g_factions)
		self.lbl_faction5_min.setObjectName(u'lbl_faction5_min')
		self.lbl_faction5_min.setGeometry(QRect(230, 60, 201, 21))

		self.lbl_faction5_max = QLabel(self.g_factions)
		self.lbl_faction5_max.setObjectName(u'lbl_faction5_max')
		self.lbl_faction5_max.setGeometry(QRect(230, 90, 201, 21))

		self.num_faction5_min = QSpinBox(self.g_factions)
		self.num_faction5_min.setObjectName(u'num_faction5_min')
		self.num_faction5_min.setGeometry(QRect(430, 58, 71, 24))
		self.num_faction5_min.setMinimum(1)
		self.num_faction5_min.setMaximum(999)

		self.num_faction5_max = QSpinBox(self.g_factions)
		self.num_faction5_max.setObjectName(u'num_faction5_max')
		self.num_faction5_max.setGeometry(QRect(430, 88, 71, 24))
		self.num_faction5_max.setMinimum(1)
		self.num_faction5_max.setMaximum(999)

		self.cb_faction5_coldrock = QCheckBox(self.g_factions)
		self.cb_faction5_coldrock.setObjectName(u'cb_faction5_coldrock')
		self.cb_faction5_coldrock.setGeometry(QRect(230, 120, 271, 21))
		self.cb_faction5_coldrock.setChecked(True)

		self.dropdown_gen = QComboBox(self.main_win)
		self.dropdown_gen.setObjectName(u'dropdown_gen')
		self.dropdown_gen.setGeometry(QRect(250, 10, 151, 23))
		self.dropdown_gen.addItems(self.lang["dropdown_gen"])
		self.dropdown_gen.activated.connect(self.on_dropdown_changed)

		self.lbl_gen = QLabel(self.main_win)
		self.lbl_gen.setObjectName(u'lbl_gen')
		self.lbl_gen.setGeometry(QRect(140, 12, 121, 16))

		self.cb_standard_tech = QCheckBox(self.main_win)
		self.cb_standard_tech.setObjectName(u'cb_standard_tech')
		self.cb_standard_tech.setGeometry(QRect(210, 40, 171, 21))
		self.cb_standard_tech.setChecked(True)

		self.lbl_stations = QLabel(self.main_win)
		self.lbl_stations.setObjectName(u'lbl_stations')
		self.lbl_stations.setGeometry(QRect(10, 40, 191, 16))

		self.num_stations = QSpinBox(self.main_win)
		self.num_stations.setObjectName(u'num_stations')
		self.num_stations.setGeometry(QRect(120, 36, 71, 24))
		self.num_stations.setMinimum(1)
		self.num_stations.setMaximum(999)
		self.num_stations.setValue(75)

		self.progress_gen = QProgressBar(self.main_win)
		self.progress_gen.setObjectName(u'progress_gen')
		self.progress_gen.setGeometry(QRect(400, 68, 118, 23))
		self.progress_gen.setValue(0)

		self.lbl_progress = QLabel(self.main_win)
		self.lbl_progress.setObjectName(u'lbl_progress')
		self.lbl_progress.setGeometry(QRect(396, 45, 121, 20))
		self.lbl_progress.setAlignment(Qt.AlignCenter)

		self.translateUI()

		self.setCentralWidget(self.main_win)
		QMetaObject.connectSlotsByName(self)
		self.center()
		self.show()

	def translateUI(self):
		self.setWindowTitle(QCoreApplication.translate('win', self.lang['window_title'], None))
		self.btn_open.setText(QCoreApplication.translate('win', self.lang['btn_open'], None))
		self.btn_gen.setText(QCoreApplication.translate('win', self.lang['btn_gen'], None))
		self.btn_close.setText(QCoreApplication.translate('win', self.lang['btn_close'], None))
		self.lbl_gen.setText(QCoreApplication.translate('win', self.lang['lbl_gen'], None))
		self.lbl_stations.setText(QCoreApplication.translate('win', self.lang['lbl_stations'], None))
		self.cb_colors.setText(QCoreApplication.translate('win', self.lang['cb_colors'], None))
		self.cb_standard_tech.setText(QCoreApplication.translate('win', self.lang['cb_standard_tech'], None))
		self.cb_balance_tech.setText(QCoreApplication.translate('win', self.lang['cb_balance_tech'], None))
		self.lbl_progress.setText(QCoreApplication.translate('win', self.lang['progress_none'], None))
		self.g_factions.setTitle(QCoreApplication.translate('win', self.lang['g_factions'], None))
		self.cb_faction1.setText(QCoreApplication.translate('win', self.lang['cb_faction1'], None))
		self.cb_faction2.setText(QCoreApplication.translate('win', self.lang['cb_faction2'], None))
		self.cb_faction3.setText(QCoreApplication.translate('win', self.lang['cb_faction3'], None))
		self.cb_faction4.setText(QCoreApplication.translate('win', self.lang['cb_faction4'], None))
		self.cb_faction5.setText(QCoreApplication.translate('win', self.lang['cb_faction5'], None))
		self.lbl_faction5_min.setText(QCoreApplication.translate('win', self.lang['lbl_faction5_min'], None))
		self.lbl_faction5_max.setText(QCoreApplication.translate('win', self.lang['lbl_faction5_max'], None))
		self.cb_faction5_coldrock.setText(QCoreApplication.translate('win', self.lang['cb_faction5_coldrock'], None))


	def center(self):
		qr = self.frameGeometry()
		cp = QDesktopWidget().availableGeometry().center()
		qr.moveCenter(cp)
		self.move(qr.topLeft())


	def load_galaxy_settings(self, galaxy_json):
		print('woo')


	def find_game(self):
		self.game_dir = str(QFileDialog.getExistingDirectory(None, 'Locate Game Directory'))
		if isfile(join(self.game_dir, 'Heat_Signature.exe')):
			self.btn_gen.setEnabled(True)
		else:
			QMessageBox.critical(None, self.lang['error_no_game_title'], self.lang['error_no_game_desc'])


	def on_dropdown_changed(self, value):
		if self.dropdown_gen.currentText() == 'Predefined':
			galaxy_file = QFileDialog.getOpenFileName(None, 'Open Galaxy Definition File', filter='*.json')[0]
			if isfile(galaxy_file):
				self.load_galaxy_settings(galaxy_file)


	def gen(self):
		save_dir = QFileDialog.getSaveFileName(None, 'Save Galaxy As...', '', '.txt')
		if save_dir == ('', ''):
			return
		save_dir = str(save_dir[0] + save_dir[1])
		wanted_factions = []
		if self.cb_faction1.isChecked():
			wanted_factions.append(0)
		if self.cb_faction2.isChecked():
			wanted_factions.append(1)
		if self.cb_faction3.isChecked():
			wanted_factions.append(2)
		if self.cb_faction4.isChecked():
			wanted_factions.append(3)
		if self.cb_faction5.isChecked():
			wanted_factions.append(4)
			
		generate(self, self.game_dir, save_dir, self.dropdown_gen.currentText().lower(), self.cb_balance_tech.isChecked(), self.cb_colors.isChecked(),
				self.num_stations.value(), wanted_factions, self.cb_faction5_coldrock.isChecked(), self.num_faction5_min.value(),
				self.num_faction5_max.value())


	def update_progress(self, value: int, text: str):
		self.lbl_progress.setText(text)
		self.progress_gen.setValue(value)


if __name__ == '__main__':
	app = QApplication(sys.argv)
	font = QFont()
	font.setFamily("DejaVu Sans")
	font.setPointSize(9)
	app.setFont(font)
	app.setStyle('Fusion')
	ex = GalaxyGenerator()
	sys.exit(app.exec_())