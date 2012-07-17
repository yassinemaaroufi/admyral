#!/usr/bin/env python
"A web browser that will never exceed 128 lines of code. (not counting blanks)"

import sys
from PyQt4 import QtGui,QtCore,QtWebKit

class MainWindow(QtGui.QMainWindow):
	def __init__(self, url):
		QtGui.QMainWindow.__init__(self)
		self.sb=self.statusBar()

		self.pbar = QtGui.QProgressBar()
		self.pbar.setMaximumWidth(120)
		self.wb=QtWebKit.QWebView(loadProgress = self.pbar.setValue, loadFinished = self.pbar.hide, loadStarted = self.pbar.show, titleChanged = self.setWindowTitle)
		self.setCentralWidget(self.wb)

		self.tb=self.addToolBar("Main Toolbar")
		for a in (QtWebKit.QWebPage.Back, QtWebKit.QWebPage.Forward, QtWebKit.QWebPage.Reload):
			self.tb.addAction(self.wb.pageAction(a))

			self.url = QtGui.QLineEdit(returnPressed = lambda:self.wb.setUrl(QtCore.QUrl.fromUserInput(self.url.text())))
			self.tb.addWidget(self.url)

			self.wb.urlChanged.connect(lambda u: self.url.setText(u.toString()))
			self.wb.urlChanged.connect(lambda: self.url.setCompleter(QtGui.QCompleter(QtCore.QStringList([QtCore.QString(i.url().toString()) for i in self.wb.history().items()]), caseSensitivity = QtCore.Qt.CaseInsensitive)))

			self.wb.statusBarMessage.connect(self.sb.showMessage)
			self.wb.page().linkHovered.connect(lambda l: self.sb.showMessage(l, 3000))

			self.search = QtGui.QLineEdit(returnPressed = lambda: self.wb.findText(self.search.text()))
			self.search.hide()
			self.showSearch = QtGui.QShortcut("Ctrl+F", self, activated = lambda: (self.search.show() , self.search.setFocus()))
			self.hideSearch = QtGui.QShortcut("Esc", self, activated = lambda: (self.search.hide(), self.wb.setFocus()))

			self.quit = QtGui.QShortcut("Ctrl+Q", self, activated = self.close)
			self.zoomIn = QtGui.QShortcut("Ctrl++", self, activated = lambda: self.wb.setZoomFactor(self.wb.zoomFactor()+.2))
			self.zoomOut = QtGui.QShortcut("Ctrl+-", self, activated = lambda: self.wb.setZoomFactor(self.wb.zoomFactor()-.2))
			self.zoomOne = QtGui.QShortcut("Ctrl+=", self, activated = lambda: self.wb.setZoomFactor(1))
			self.wb.settings().setAttribute(QtWebKit.QWebSettings.PluginsEnabled, True)

			self.sb.addPermanentWidget(self.search)
			self.sb.addPermanentWidget(self.pbar)
			self.wb.load(url)


if __name__ == "__main__":
	app=QtGui.QApplication(sys.argv)
	if len(sys.argv) > 1:
		url = QtCore.QUrl.fromUserInput(sys.argv[1])
	else:
		url = QtCore.QUrl('http://www.python.org')
	wb=MainWindow(url)
	wb.show()
	sys.exit(app.exec_())
