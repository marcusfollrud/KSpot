#!/bin/python
# -*- coding: utf-8 -*-
from PyKDE4.kdecore import ki18n,KAboutData, KCmdLineArgs
from PyKDE4.kdeui import KApplication,KMainWindow,KLineEdit,KPushButton,KListWidget,KMessageBox

from PyQt4.QtGui import QLabel,QListWidget
from PyQt4.QtCore import SIGNAL, Qt, QThread

from spytify import *
import sys
import time

runner = True
class SpotPlayFile(QThread):
	
	def __init__(self,parent,spyt,playlist,songID):
		QThread.__init__(self,parent)
		#parent.connect(self,SIGNAL("finished()"),callback)
		self.connect(self,SIGNAL("started()"),self.playSong)
		self.spyt = spyt
		self.playlist = playlist
		self.songID = songID
		self.parent = parent
	
	def run(self):
		self.exec_()
	
	def endProcess(self):
		self.spyt = None
		self.playlist = None
		self.songID = None
	
	def playSong(self):
		self.spyt.play(self.playlist.playlist.tracks[self.songID])
		##The song starts playing and goes all the way. However, we do have a freeze in the ui even though it's threaded!
		#FIXME: ^

global s
global result
s = Spytify("user","password")
result=None
global updateWindow
updateWindow=False

class MainWindow (KMainWindow):

	
	
	def __init__ (self):
		KMainWindow.__init__ (self)
		self.result = ""
		self.resize (640, 480)
		
		label = QLabel ("Search", self)
		label.setGeometry (10,10,200,20)
		
		self.searchBox = KLineEdit(self)
		self.searchBox.setGeometry(50,8,520,25)
		self.connect(self.searchBox, SIGNAL("returnPressed()"),self.search)
		
		searchButton = KPushButton(self)
		searchButton.setGeometry(570,6,70,25)
		searchButton.setText("Search")
		self.connect (searchButton, SIGNAL("clicked()"), self.search)
		
		self.resultList = KListWidget(self)
		self.resultList.setGeometry(10,50,620,400)
		self.connect(self.resultList, SIGNAL("itemDoubleClicked(QListWidgetItem*)"), self.playSelected)
	
		
	
	def formatResult(self,track):
		has_metadata = "un"
		if track.has_meta_data():
			has_metadata = ""

		return " %s - %s (%s), length: %d [%splayable]" % (", ".join((a.name for a in track.artists)),
                                                         track.title, track.album,
                                                         track.length, has_metadata)
	def playSelected(self):
		global s
		global result
		self.proc = SpotPlayFile(self,s,result,self.resultList.currentRow())
		self.proc.start()
		
		
	def doSomething(self):
		print("Doing something")
	
	def search(self):
		global result
		global s
		if self.searchBox.text() == "":
			KMessageBox.error(None,"Search for something...")
			return
		else:
			self.resultList.clear()
			result = s.search(str(self.searchBox.text()))
			if not result:
				self.resultList.addItem("Nothing found :(")
			else:
				for i in range(0,len(result.playlist.tracks)):
					tracktext = self.formatResult(result.playlist.tracks[i])
				#	tracktext = str(track)
					self.resultList.addItem(tracktext)
					
				#s.play(result.playlist.tracks.)
		return
			

	


#----------------------------Main------------------------
if __name__ == '__main__':
	appName = "KSpot"
	catalog = ""
	programName = ki18n ("KSpot")
	version = "0.1"
	description = ki18n ("Spotify for KDE")
	license = KAboutData.License_GPL
	copyright = ki18n ("Marcus Follrud")
	text = ki18n ("none")
	homePage = "http://marcusfollrud.net/kspot"
	bugEmail = "marcus.follrud@gmail.com"

	aboutData = KAboutData (appName,catalog,programName,version,description,license, copyright, text, homePage,bugEmail)
						
	KCmdLineArgs.init (sys.argv,aboutData)

	app = KApplication()
	mainWindow = MainWindow ()
	mainWindow.show()
	app.exec_ ()
	
	
