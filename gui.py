from PyQt5.QtWidgets import QWidget, QTextBrowser, QPushButton, QVBoxLayout, QFileDialog, QApplication
from PyQt5.QtCore import Qt
from sys import argv
import wc

# 图形化界面
class Gui(QWidget):
    def __init__(self, wc_exe, args):
        self.wc_exe = wc_exe
        self.args = args
        super().__init__()
        self.setGeometry(800, 300, 500, 350)
        self.setWindowTitle('WC.exe')
        self.setWindowFlag(Qt.WindowStaysOnTopHint)
        self.textbox = QTextBrowser(self)
        self.btn = QPushButton('Choose File', self)
        self.btn.clicked.connect(self.choose_file)
        vbox = QVBoxLayout()
        vbox.addWidget(self.textbox)
        vbox.addWidget(self.btn)
        self.setLayout(vbox)
        self.show()

    def choose_file(self):
        # 获取选择的文件
        self.files, files_type = QFileDialog.getOpenFileNames()
        if len(self.files) > 0:
            # 文件单选的情况
            if len(self.files) == 1:
                self.wc_exe.args.directory = self.files[0]
            # 文件多选的情况
            else:
                self.wc_exe.flag = False
                self.wc_exe.args.directory = self.files[0]
                for file in self.files:
                    self.wc_exe.file_list.append(file)
            info = self.wc_exe.main()
            # 清除原来的文件，防止重复检测
            self.wc_exe.file_list.clear()
            self.textbox.setText("\n".join(info))
        else:
            self.textbox.setText("未选择文件.")


def GUI(args):
    app = QApplication(argv)
    Wc = wc.WC(args)
    ex = Gui(Wc, args)
    app.exit(app.exec_())