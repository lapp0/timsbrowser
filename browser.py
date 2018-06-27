import signal
import sys
from PyQt5 import QtCore, QtGui, QtWebEngineWidgets, QtWidgets


class Browser(QtWidgets.QMainWindow):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        self.current_zoom = 1.0
        self.current_rotation = 0
        self.resize(800, 800)
        self.centralwidget = QtWidgets.QWidget(self)
        self.current_scrollbar = 0
        self.scroll_area = QtWidgets.QScrollArea()
        self.slider = QtWidgets.QAbstractSlider(self)

        self.mainLayout = QtWidgets.QHBoxLayout(self.centralwidget)
        self.mainLayout.setSpacing(0)
        self.mainLayout.setContentsMargins(1, 1, 1, 1)

        self.frame = QtWidgets.QFrame(self.centralwidget)

        self.dblClick = QtGui.QMouseEvent

        self.gridLayout = QtWidgets.QVBoxLayout(self.frame)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setSpacing(0)

        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.tb_url = QtWidgets.QLineEdit(self.frame)
        self.bt_back = QtWidgets.QPushButton(self.frame)
        self.bt_ahead = QtWidgets.QPushButton(self.frame)
        self.increaseZoom = QtWidgets.QPushButton(self.frame)
        self.decreaseZoom = QtWidgets.QPushButton(self.frame)
        self.rotate90 = QtWidgets.QPushButton(self.frame)
        self.hideBar = QtWidgets.QPushButton(self.frame)

        self.bt_back.setText("🡸")
        self.bt_ahead.setText("🡺")
        self.increaseZoom.setText("+")
        self.decreaseZoom.setText("-")
        self.rotate90.setText("⤸")
        self.hideBar.setText("Hide")


        self.horizontalLayout.addWidget(self.bt_back)
        self.horizontalLayout.addWidget(self.bt_ahead)
        self.horizontalLayout.addWidget(self.tb_url)
        self.horizontalLayout.addWidget(self.increaseZoom)
        self.horizontalLayout.addWidget(self.decreaseZoom)
        self.horizontalLayout.addWidget(self.rotate90)
        self.horizontalLayout.addWidget(self.hideBar)
        self.gridLayout.addLayout(self.horizontalLayout)

        self.html = QtWebEngineWidgets.QWebEngineView()
        self.html.installEventFilter(self)

        if False:
            # put self.html in a QGraphicsView, this results in self.html
            # not taking up all the space available and being small
            self.scene = QtWidgets.QGraphicsScene()
            self.view = QtWidgets.QGraphicsView(self.scene)
            self.scene.addWidget(self.html)
            self.gridLayout.addWidget(self.view)
        else:
            # directly put self.html in self.gridLayout without a
            # QGraphicsScene inbetween them. This results in self.html
            # expanding to fit all available space
            self.gridLayout.addWidget(self.html)

        self.mainLayout.addWidget(self.frame)
        self.setCentralWidget(self.centralwidget)

        self.tb_url.returnPressed.connect(self.browse)
        self.bt_back.clicked.connect(self.html.back)
        self.bt_ahead.clicked.connect(self.html.forward)
        self.increaseZoom.clicked.connect(lambda: self.update_zoom_factor(True))
        self.decreaseZoom.clicked.connect(lambda: self.update_zoom_factor(False))
        self.rotate90.clicked.connect(lambda: self.update_rotation())
        self.hideBar.clicked.connect(lambda: self.toggle_widget(True))

        self.default_url = "http://www.google.com/webhp?complete=0&hl=en"
        self.tb_url.setText(self.default_url)
        self.browse()

    def toggle_widget(self, bln):
        list = [self.bt_ahead, self.bt_back, self.tb_url, self.increaseZoom, self.decreaseZoom, self.rotate90, self.hideBar]
        for widg in list:
            widg.setHidden(bln)

    def check_http(self, string):
        if "http://" not in string and "https://" not in string:
            return True

    def check_dom(self, string):
        tld = [".com", ".uk", ".net", ".org", ".edu", ".gov", ".ca"]
        for item in tld:
            if item in string:
                return True

    def browse(self):
        url = self.tb_url.text() if self.tb_url.text() else self.default_url

       # if url.find("http://") == -1:
        if self.check_http(url):
            if not self.check_dom(url):
                self.html.load(QtCore.QUrl("http://www.google.com/search?q=" + url))
            else:
                self.html.load(QtCore.QUrl("http://" + url))

        else:
            self.html.load(QtCore.QUrl(url))
        self.html.show()

    def update_zoom_factor(self, bln):
        if bln == True:
            self.current_zoom += 0.1
        if bln == False:
            self.current_zoom -= 0.1
        self.html.setZoomFactor(self.current_zoom)

    def update_rotation(self):
        self.view.rotate(90.0)

    def eventFilter(self, watched, event):
        if isinstance(event, QtGui.QMouseEvent):
            if event.type() == QtCore.QEvent.MouseButtonDblClick:

                print('tim this is where you should implement your double click logic')
                # self.toggle_widget(False)

        return super().eventFilter(watched, event)


if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    app = QtWidgets.QApplication(sys.argv)
    main = Browser()
    main.show()
    app.installEventFilter(main)

sys.exit(app.exec_())
