from decimal import Decimal
from PyQt5 import QtCore
from PyQt5.QtGui import QTextCursor
from PyQt5.QtWidgets import QApplication, QWidget, QTextEdit, QVBoxLayout, QPushButton, QLineEdit
from src.GUI.product_script import *
from src.analysis.code_variable import *
import sys


class CodeEvaluationPage(QWidget):
    def __init__(self, parent=None):
        super(CodeEvaluationPage, self).__init__(parent)
        self.setWindowTitle('代码命名评估界面')

        # 定义窗口的初始大小
        self.resize(900, 500)
        # 创建多行文本框
        self.textEdit = QTextEdit()
        self.textEdit.setText('# 在此处输入代码\n')
        self.lineEdit = QLineEdit()
        self.lineEdit.setFocusPolicy(QtCore.Qt.NoFocus)
        # 创建提交按钮
        self.upload_button = QPushButton('提交')

        # 实例化垂直布局
        layout = QVBoxLayout()
        # 相关控件添加到垂直布局中
        layout.addWidget(self.textEdit)
        layout.addWidget(self.lineEdit)
        layout.addWidget(self.upload_button)

        # 设置布局
        self.setLayout(layout)

        # 将按钮的点击信号与相关的槽函数进行绑定，点击即触发
        self.upload_button.clicked.connect(self.upload_button_action)

    def upload_button_action(self):
        # 将文本框内的代码转化成字符串形式
        content = str(self.textEdit.toPlainText())
        answer = evaluation(content)
        self.lineEdit.setText('这段代码的得分为：' + str(Decimal(answer['all']).quantize(Decimal('0.00'))) + ' 变量: ' + str(
            Decimal(answer['variable']).quantize(Decimal('0.00'))) + ' 复用:' + str(
            Decimal(answer['reuse']).quantize(Decimal('0.00'))) + ' 分布: ' + str(
            Decimal(answer['initiation']).quantize(Decimal('0.00'))))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = CodeEvaluationPage()
    win.show()
    sys.exit(app.exec_())
