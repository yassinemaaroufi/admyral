#!/usr/bin/python

# Browser name: VY
# i3 shortcut: Win+X

import sys

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.QtWebKit import *

TABS = []						# Tabs list

def closeWidget(parent, w):
	w.close()
	w.destroy()
	parent.setFocus()
	parent.focusPreviousChild()

def changeURL(parent, w):
	url = w.text()
	parent.setUrl(QUrl(url))
	w.close()
	w.destroy()


def URLBar(parent):
	w = QLineEdit(parent)
	#w.setText('http://')
	w.setText(parent.url().toString())
	#w.resize(1000,20)
	#w.resize(parent.width(), 20)
	w.resize(parent.width()/3, 20)
	w.move(parent.width()/3, parent.height()/2)
	w.setFocus()
	QShortcut("Esc", w, activated = lambda: closeWidget(parent, w))
	#QShortcut("F6", w, activated = lambda: closeWidget(parent, w))
	QObject.connect(w, SIGNAL('returnPressed()'), lambda: changeURL(parent, w))
	w.show()

def closeTab(parent):
	global TABS
	TABS[parent.tabPosition - 1].show()
	parent.close()
	TABS.pop(parent.tabPosition)

def closeTabs():
	for i in TABS:
		i.close()

def callNewTab(parent):
	initTab()
	parent.hide()

def nextTab(parent):
	global TABS
	n = 0 if (parent.tabPosition + 1 > len(TABS) - 1) else (parent.tabPosition + 1)
	TABS[n].show()
	parent.hide()

def prevTab(parent):
	global TABS
	n = len(TABS) - 1 if (parent.tabPosition - 1 < 0) else (parent.tabPosition - 1)
	TABS[n].show()
	parent.hide()

def initTab():
	global TABS
	v = QWebView()
	v.load(QUrl(url))
	v.setFocus()
	QShortcut("Ctrl+Q", v, activated = closeTabs)
	#QShortcut("Ctrl+W", v, activated = v.close)
	QShortcut("Ctrl+W", v, activated = lambda: closeTab(v))
	QShortcut("Ctrl+L", v, activated = lambda: URLBar(v))
	QShortcut("F6", v, activated = lambda: URLBar(v))
	#QShortcut("Ctrl+T", v, activated = initTab)
	QShortcut("Ctrl+T", v, activated = lambda: callNewTab(v))
	QShortcut("Ctrl+K", v, activated = lambda: nextTab(v))
	QShortcut("Ctrl+J", v, activated = lambda: prevTab(v))
	v.show()
	v.tabPosition = len(TABS)
	TABS += [v]


url = 'http://www.google.com'	# Default URL

app = QApplication(sys.argv)

initTab()

sys.exit(app.exec_())
