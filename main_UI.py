#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author：Genie time:2019/4/13
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import pandas as pd
import numpy as np
from PyQt5.QtCore import *
from risk_evaluation import risk_evaluation
from style_rotation import plot_figure, performance
from datetime import datetime as dt
from pathlib import Path
import os
import time
from datetime import date, timedelta


# user_information = pd.DataFrame(columns=["user_name", "password", "phone_number", "risk_score", "risk_type", "strategy"])
# user_information.to_csv("user_information.csv")


# 设置主页
class Mainpage(QDialog):
    def __init__(self):
        super(Mainpage, self).__init__()
        self.init_ui()

    def init_ui(self):
        # 设置窗口的位置、大小、标题、icon
        self.setGeometry(100, 100, 1730, 880)  # 控制大窗口大小  行高 列高 长 宽
        self.setWindowTitle('智能投顾系统')
        self.setWindowIcon(QIcon('icon.jpg'))

        self.frame = QFrame(self)
        self.verticalLayout = QVBoxLayout(self.frame)
        label = QLabel()
        label.setPixmap(QPixmap('icon.jpg'))
        # label.setScaledContents(True)
        self.verticalLayout.addWidget(label)

        # 设置登录按钮
        btn1 = QPushButton('登录', self)
        btn1.setGeometry(1360, 414, 167, 88)
        # btn1.setStyleSheet('''QPushButton{background:#F3F3F5;border-radius:15px;font-size:18pt; font-weight:400;}
        # QPushButton:hover{border:2px solid #F3F3F5;background:darkGray;}''')
        # btn1.setStyleSheet('''QPushButton{background-color:rgb(62, 114, 242);border-radius:15px;font-size:18pt; font-weight:400;}
        # QPushButton:hover{border:2px solid #F3F3F5;background:darkGray;}''')
        btn1.setStyleSheet('''QPushButton{background-color:rgb(68, 107, 199);color:white; font-size:26pt; font-family:黑体;}
        QPushButton:hover{border:2px solid #F3F3F5;background:darkGray;}''')

        # 设置注册按钮56 76 102
        btn2 = QPushButton('立即注册', self)
        btn2.setGeometry(1125, 414, 222, 88)
        # btn2.setStyleSheet('''QPushButton{background:#F3F3F5; font-size:20pt; font-family:黑体;}
        # QPushButton:hover{border:2px solid #F3F3F5;background:darkGray;}''')
        btn2.setStyleSheet('''QPushButton{background-color:rgb(68, 107, 199);color:white; font-size:26pt; font-family:黑体;}
        QPushButton:hover{border:2px solid #F3F3F5;background:darkGray;}''')

        btn3 = QPushButton('策略广场', self)
        btn3.setGeometry(11, 13, 155, 70)
        btn3.setStyleSheet('''QPushButton{background-color:rgb(56, 76, 102); color:white; font-size:20pt; font-family:黑体;}
        QPushButton:hover{border:2px solid #F3F3F5;background:darkGray;}''')

        btn4 = QPushButton('团队介绍', self)
        btn4.setGeometry(11, 355, 155, 70)
        btn4.setStyleSheet('''QPushButton{background-color:rgb(56, 76, 102); color:white; font-size:20pt; font-family:黑体;}
        QPushButton:hover{border:2px solid #F3F3F5;background:darkGray;}''')

        btn5 = QPushButton('系统介绍', self)
        btn5.setGeometry(667, 178, 155, 70)
        btn5.setStyleSheet('''QPushButton{background-color:rgb(56, 76, 102); color:white; font-size:20pt; font-family:黑体;}
        QPushButton:hover{border:2px solid #F3F3F5;background:darkGray;}''')

        # 点击“登录”跳转到新界面
        btn1.clicked.connect(self.slot_btn1_function)

        # 点击“注册”跳转到新界面
        btn2.clicked.connect(self.slot_btn2_function)

        btn3.clicked.connect(self.slot_btn3_function)
        btn4.clicked.connect(self.slot_btn4_function)
        btn5.clicked.connect(self.slot_btn5_function)

    # 跳转到登录页的函数
    def slot_btn1_function(self):
        self.hide()
        self.s = Logpage()
        self.s.show()

    # 跳转到注册页的函数
    def slot_btn2_function(self):
        self.hide()
        self.s = Registerpage()
        self.s.show()

    # 跳转到策略广场页的函数
    def slot_btn3_function(self):
        self.hide()
        self.s = Strategypage()
        self.s.show()

    # 跳转系统介绍页的函数
    def slot_btn4_function(self):
        self.hide()
        self.s = Introductionpage()
        self.s.show()

    # 跳转到关于我们页的函数
    def slot_btn5_function(self):
        self.hide()
        self.s = AboutUspage()
        self.s.show()


# 设置登录页
class Logpage(QWidget):
    def __init__(self):
        super(Logpage, self).__init__()
        self.init_ui()
        self._user_information = pd.read_csv("user_information.csv", index_col=0, header=0,
                                             dtype={"user_name": str, "password": str, "phone_number": str,
                                                    "risk_score": str, "risk_type": str, "strategy": str})

    def init_ui(self):
        self.resize(500, 350)
        self.setWindowTitle('用户登录')
        self.setWindowIcon(QIcon('icon.jpg'))

        layout = QFormLayout()
        self.item1text = QLineEdit()
        self.item1text.setPlaceholderText("请输入用户名")
        layout.addRow(self.item1text)

        self.item2text = QLineEdit()
        self.item2text.setPlaceholderText("请输入密码")
        layout.addRow(self.item2text)

        self.btn1 = QPushButton('登录', self)
        self.btn1.setGeometry(100, 150, 100, 50)
        self.btn1.setStyleSheet('''QPushButton{background-color:rgb(62, 114, 242); color:white; border-radius:15px;font-size:18pt; font-weight:400;}
        QPushButton:hover{border:2px solid #F3F3F5;background:darkGray;}''')
        self.btn1.clicked.connect(self.slot_btn1_function)

        self.btn2 = QPushButton('返回', self)
        self.btn2.setGeometry(275, 150, 100, 50)
        self.btn2.setStyleSheet('''QPushButton{background-color:rgb(62, 114, 242); color:white; border-radius:15px;font-size:18pt; font-weight:400;}
        QPushButton:hover{border:2px solid #F3F3F5;background:darkGray;}''')
        self.btn2.clicked.connect(self.slot_btn2_function)

        self.setLayout(layout)

    def slot_btn1_function(self):
        user_name = str(self.item1text.text())
        password = str(self.item2text.text())

        if len(user_name) == 0:
            error = "请输入用户名！"
            self.hide()
            self.y = LogErrorpage(error)
            self.y.show()
        elif len(np.where(self._user_information["user_name"] == user_name)[0]) == 0:
            error = "用户名不存在！"
            self.hide()
            self.y = LogErrorpage(error)
            self.y.show()
        else:
            pos = np.where(self._user_information["user_name"] == user_name)[0][0]
            password_true = str(self._user_information.iloc[pos, 1])
            print(password)
            print(password_true)
            if password != password_true:
                error = "密码错误！"
                self.hide()
                self.y = LogErrorpage(error)
                self.y.show()
            else:
                self.hide()
                user_information_series = self._user_information[self._user_information['user_name'] == user_name]
                self.s = LogSucceedpage(user_information_series)
                self.s.show()

    def slot_btn2_function(self):
        self.hide()
        self.f = Mainpage()
        self.f.show()


# 设置注册页
class Registerpage(QWidget):
    def __init__(self):
        super(Registerpage, self).__init__()
        self.init_ui()
        self._user_information = pd.read_csv("user_information.csv", index_col=0, header=0,
                                             dtype={"user_name": str, "password": str, "phone_number": str,
                                                    "risk_score": str, "risk_type": str, "strategy": str})

    def init_ui(self):

        self.resize(500, 350)
        self.setWindowTitle('用户注册')
        self.setWindowIcon(QIcon('icon.jpg'))

        layout = QFormLayout()
        # 注册页正文
        item1 = QLabel('用户名：')
        self.item1text = QLineEdit()
        self.item1text.setPlaceholderText("用户名不得多于20位")
        layout.addRow(item1, self.item1text)

        item2 = QLabel('密码：')
        self.item2text = QLineEdit()
        layout.addRow(item2, self.item2text)

        item3 = QLabel('手机号：')
        self.item3text = QLineEdit()
        layout.addRow(item3, self.item3text)

        # (类似的还可以加其他许多条目，加了条目后记得在返回函数里面增加返回值)
        self.btn1 = QPushButton('提 交', self)
        self.btn1.setGeometry(100, 150, 100, 50)
        self.btn1.clicked.connect(self.slot_btn1_function)
        self.btn1.setStyleSheet('''QPushButton{background-color:rgb(62, 114, 242); color:white; border-radius:15px;font-size:18pt; font-weight:400;}
        QPushButton:hover{border:2px solid #F3F3F5;background:darkGray;}''')

        self.btn2 = QPushButton('返 回', self)
        self.btn2.setGeometry(275, 150, 100, 50)
        self.btn2.clicked.connect(self.slot_btn2_function)
        self.btn2.setStyleSheet('''QPushButton{background-color:rgb(62, 114, 242); color:white; border-radius:15px;font-size:18pt; font-weight:400;}
        QPushButton:hover{border:2px solid #F3F3F5;background:darkGray;}''')

        self.setLayout(layout)

    def slot_btn1_function(self):
        user_name = str(self.item1text.text())
        password = str(self.item2text.text())
        phone_number = str(self.item3text.text())

        if len(user_name) == 0:
            error = "用户名不能为空！"
            self.hide()
            self.y = RegisterErrorpage(error)
            self.y.show()
        elif len(user_name) > 20:
            error = "用户名不能大于20位！"
            self.hide()
            self.y = RegisterErrorpage(error)
            self.y.show()
        elif len(np.where(self._user_information["user_name"] == user_name)[0]) != 0:
            error = "用户名已存在！"
            self.hide()
            self.y = RegisterErrorpage(error)
            self.y.show()
        elif len(password) == 0:
            error = "密码不能为空！"
            self.hide()
            self.y = RegisterErrorpage(error)
            self.y.show()
        elif (len(phone_number) != 11) or (not phone_number.isdigit()):
            error = "手机号码不正确！"
            self.hide()
            self.y = RegisterErrorpage(error)
            self.y.show()
        else:
            risk_score = ""
            risk_type = ""
            strategy = ""
            temp = pd.DataFrame([[user_name, password, phone_number, risk_score, risk_type, strategy]],
                                columns=["user_name", "password", "phone_number", "risk_score", "risk_type", "strategy"])
            self._user_information.append(temp, ignore_index=True).to_csv("user_information.csv")

            self.hide()
            self.f = RegisterSucceedpage(user_name)
            self.f.show()

    def slot_btn2_function(self):
        self.hide()
        self.f = Mainpage()
        self.f.show()


# 设置策略广场页
class Strategypage(QWidget):
    def __init__(self):
        super(Strategypage, self).__init__()
        self.init_ui()

    def init_ui(self):

        # self.resize(1730, 880)
        self.setGeometry(100, 100, 1730, 880)
        self.setWindowTitle('策略广场')
        self.setWindowIcon(QIcon('icon.jpg'))

        layout = QVBoxLayout()

        ql = QLabel()
        font = QFont()
        font.setFamily('微软雅黑')
        font.setBold(True)
        font.setPointSize(14)
        font.setWeight(75)
        ql.setFont(font)
        ql.setText("<font color=black>%s</font>" % ('策略库之“多因子选股策略”'))

        self.textEdit1 = QTextEdit()
        self.textEdit1.setFontPointSize(15)
        layout.addWidget(ql)
        layout.addWidget(self.textEdit1)
        self.textEdit1.setPlainText('多因子策略是一种应用十分广泛的选股策略，其基本思构想是找到和收益率最相关的指标，并根据该指标，建一个股票组合，期望该组合在未来的一段时间大于或者小于指数。\n'
                                    '如果大于指数，则可以做多该组合，同时做空期指，如果小于指数，则可以做多期指，融券做空该正与向阿尔法收益组合，赚取反向阿尔法收益。\n'
                                    '多因子模型的关键是找到因子与收益率之间的关联性。\n'
                                    '影响价格走势的主要因子包括市场整体走势（市场因子，系统性风险）、估值因子（市盈率、市净率、市销率、市现率、企业价值倍数、PEG等）、\n'
                                    '成长因子（营业收入增长率、营业利润增长率、净利润增长率、每股收益增长率、净资产增长率、股东权益增长率、经营活动产生的现金流量金额增长率等）、\n'
                                    '盈利能力因子（销售净利率、毛利率、净资产收益率、资产收益率、营业费用比例、财务费用比例、息税前利润与营业总收入比等）、动量反转因子（前期涨跌幅等）、\n'
                                    '交投因子（前期换手率、量比等）、规模因子（流通市值、总市值、自由流通市值、流通股本、总股本等）、股价波动因子（前期股价振幅、日收益率标准差等）、\n'
                                    '分析师预测因子（预测净利润增长率、预测主营业务增长率、盈利预测调整等）。')

        ql = QLabel()
        ql.setFont(font)
        ql.setText("<font color=black>%s</font>" % ('策略库之“CTA策略”'))
        self.textEdit2 = QTextEdit()
        self.textEdit2.setFontPointSize(15)
        layout.addWidget(ql)
        layout.addWidget(self.textEdit2)
        self.textEdit2.setPlainText('CTA策略称为商品交易顾问策略，也称作管理期货。\n'
                                    '商品交易顾问对商品等投资标的走势做出预判，通过期货期权等衍生品在投资中进行做多、做空或多空双向的投资操作，为投资者获取来自于传统股票、债券等资产类别之外的投资回报。')

        ql = QLabel()
        ql.setFont(font)
        ql.setText("<font color=black>%s</font>" % ('策略库之“风格轮动策略”'))
        self.textEdit3 = QTextEdit()
        self.textEdit3.setFontPointSize(15)
        layout.addWidget(ql)
        layout.addWidget(self.textEdit3)
        self.textEdit3.setPlainText('风格轮动是指股票市场中具有对立分类属性的股票池的走势相对强弱随市场状况变化而变化的现象。\n'
                                    '因市场上的投资者存在偏好，如价值股，成长股，大盘股，小盘股等，这种不同的交易行为形成了市场风格。\n'
                                    '风格转换策略模型建立了一系列基本预测变量的基础上、寻找一个适用于风格转换的合理模型。\n'
                                    '主要有三类方法：\n'
                                    '（1）将风格相对收益率对相关变量进行回归。但由于建立精确关系较为困难，因此这种方法基本被排除。\n'
                                    '（2）Markov Switch模型。该模型主要关注相对收益率的历史表现（按照Levist的变量分类办法，这些指标主要是技术变量），并不关注其他基本经济变量，因此这种方法可能遗漏了很多可用信息。\n'
                                    '（3）Logistic概率模型。在任意时点，风格转换的结果无非有二种，即转换或不转换。如果预期下期某类风格占优，则将现有风格转化为占优的风格。\n'
                                    '在建立Logistic预测模型前，需要首先选择n个可能的影响因素（宏观、基本面、技术面等），可以通过逐步回归、主成分分析等方法选择。\n'
                                    '然后利用Y对n个解释变量建立多元Logistic回归模型。可采用Jackknife method等检验方法会多元Logistic模型进行稳定性检验，并确定模型最佳的判别点。\n'
                                    '比较按最佳判别点确定的风格转换策略所获得的收益是否大于任何简单的买入并持有策略，若难以超越，则认为简单的买入策略为最佳策略：\n'
                                    '若超过，则考虑交易成本后的最佳转换风格的交易策略。')
        layout.addStretch(0)
        # self.setLayout(layout)

        self.back_button = QPushButton('退出')
        self.back_button.setGeometry(100, 300, 100, 50)
        layout.addWidget(self.back_button)
        self.back_button.clicked.connect(self.back_button_function)

        self.setLayout(layout)

    def back_button_function(self):
        self.hide()
        self.s = Mainpage()
        self.s.show()


# 设置系统介绍页
class Introductionpage(QWidget):
    def __init__(self):
        super(Introductionpage, self).__init__()
        self.init_ui()

    def init_ui(self):

        self.setGeometry(100, 100, 1730, 880)
        self.setWindowTitle('Robo-Advisor')
        self.setWindowIcon(QIcon('icon.jpg'))

        layout = QVBoxLayout()

        ql = QLabel()
        font = QFont()
        font.setFamily('微软雅黑')
        font.setBold(True)
        font.setPointSize(14)
        font.setWeight(75)
        ql.setFont(font)
        ql.setText("<font color=black>%s</font>" % ('团队介绍'))
        layout.addWidget(ql)

        label = QLabel()
        label.setPixmap(QPixmap('team.jpg'))
        label.setScaledContents(True)
        layout.addWidget(label)

        layout.addStretch(0)

        self.back_button = QPushButton('退出')
        self.back_button.setGeometry(100, 300, 100, 50)
        layout.addWidget(self.back_button)
        self.back_button.clicked.connect(self.back_button_function)

        self.setLayout(layout)

    def back_button_function(self):
        self.hide()
        self.s = Mainpage()
        self.s.show()


# 设置关于我们页
class AboutUspage(QWidget):
    def __init__(self):
        super(AboutUspage, self).__init__()
        self.init_ui()

    def init_ui(self):

        self.setGeometry(100, 100, 1730, 880)
        self.setWindowTitle('Robo-Advisor')
        self.setWindowIcon(QIcon('icon.jpg'))

        layout = QVBoxLayout()

        ql = QLabel()
        font = QFont()
        font.setFamily('微软雅黑')
        font.setBold(True)
        font.setPointSize(14)
        font.setWeight(75)
        ql.setFont(font)
        ql.setText("<font color=black>%s</font>" % ('系统介绍'))
        layout.addWidget(ql)

        label = QLabel()
        label.setPixmap(QPixmap('about_us.jpg'))
        label.setScaledContents(True)
        layout.addWidget(label)

        layout.addStretch(0)

        self.back_button = QPushButton('退出')
        self.back_button.setGeometry(100, 300, 100, 50)
        layout.addWidget(self.back_button)
        self.back_button.clicked.connect(self.back_button_function)

        self.setLayout(layout)

    def back_button_function(self):
        self.hide()
        self.s = Mainpage()
        self.s.show()


# 设置登录成功页
class LogSucceedpage(QWidget):
    def __init__(self, user_information_series):
        super(LogSucceedpage, self).__init__()
        self.init_ui()
        self._user_information_series = user_information_series

    def init_ui(self):
        self.resize(500, 250)
        self.setWindowTitle('登录结果')
        self.setWindowIcon(QIcon('icon.jpg'))

        layout = QVBoxLayout()
        blank = QLabel("")
        layout.addWidget(blank)
        layout.addWidget(blank)

        self.centralWidget = QWidget(self)
        error = QLabel(self.centralWidget)
        font = QFont()
        font.setFamily('微软雅黑')
        font.setBold(True)
        font.setPointSize(14)
        font.setWeight(75)
        error.setFont(font)
        error.setText("<font color=black>%s</font>" % ("登录成功！"))
        layout.addWidget(error)
        error.setAlignment(Qt.AlignCenter)

        # error = QLabel("登录成功！")
        # layout.addWidget(error)
        # error.setAlignment(Qt.AlignCenter)

        self.btn = QPushButton('确定', self)
        self.btn.setGeometry(200, 150, 100, 50)
        self.btn.setStyleSheet('''QPushButton{background-color:rgb(62, 114, 242); color:white; border-radius:15px;font-size:18pt; font-weight:400;}
        QPushButton:hover{border:2px solid #F3F3F5;background:darkGray;}''')
        self.btn.clicked.connect(self.slot_btn_function)

        layout.addStretch(0)
        self.setLayout(layout)

    def slot_btn_function(self):
        self.hide()
        self.s = Infopage(self._user_information_series)
        self.s.show()


# 设置注册成功页
class RegisterSucceedpage(QWidget):
    def __init__(self, user_name):
        super(RegisterSucceedpage, self).__init__()
        self._user_name = user_name
        self.init_ui()

    def init_ui(self):
        self.resize(500, 250)
        self.setWindowTitle('注册结果')
        self.setWindowIcon(QIcon('icon.jpg'))

        layout = QVBoxLayout()
        blank = QLabel("")
        layout.addWidget(blank)
        layout.addWidget(blank)

        self.centralWidget = QWidget(self)
        error = QLabel(self.centralWidget)
        # error.setGeometry(QRect(60, 60, 591, 61))
        font = QFont()
        font.setFamily('微软雅黑')
        font.setBold(True)
        font.setPointSize(14)
        font.setWeight(75)
        error.setFont(font)
        error.setText("<font color=black>%s</font>" % ("注册成功！"))
        layout.addWidget(error)
        error.setAlignment(Qt.AlignCenter)

        # error = QLabel("注册成功！")
        # layout.addWidget(error)
        # error.setAlignment(Qt.AlignCenter)

        self.btn = QPushButton('确定', self)
        self.btn.setGeometry(200, 150, 100, 50)
        self.btn.clicked.connect(self.slot_btn_function)
        self.btn.setStyleSheet('''QPushButton{background-color:rgb(62, 114, 242); color:white; border-radius:15px;font-size:18pt; font-weight:400;}
        QPushButton:hover{border:2px solid #F3F3F5;background:darkGray;}''')

        layout.addStretch(0)
        self.setLayout(layout)

    def slot_btn_function(self):
        self.hide()
        self.s = RiskAssessment(self._user_name)
        self.s.show()


# 设置登录失败页
class LogErrorpage(QWidget):
    def __init__(self, error):
        super(LogErrorpage, self).__init__()
        self._error = error
        self.init_ui()

    def init_ui(self):
        self.resize(500, 250)
        self.setWindowTitle('登录失败')
        self.setWindowIcon(QIcon('icon.jpg'))

        layout = QVBoxLayout()
        blank = QLabel("")
        layout.addWidget(blank)
        layout.addWidget(blank)

        self.centralWidget = QWidget(self)
        error = QLabel(self.centralWidget)
        # error.setGeometry(QRect(60, 60, 591, 61))
        font = QFont()
        font.setFamily('微软雅黑')
        font.setBold(True)
        font.setPointSize(14)
        font.setWeight(75)
        error.setFont(font)
        error.setText("<font color=black>%s</font>" % (self._error))
        layout.addWidget(error)
        error.setAlignment(Qt.AlignCenter)

        self.btn = QPushButton('确定', self)
        self.btn.setGeometry(200, 150, 100, 50)
        font = QFont()
        font.setBold(True)
        self.btn.setFont(font)
        self.btn.setStyleSheet('''QPushButton{background-color:rgb(62, 114, 242); color:white; border-radius:15px;font-size:18pt; font-weight:400;}
        QPushButton:hover{border:2px solid #F3F3F5;background:darkGray;}''')
        self.btn.clicked.connect(self.slot_btn_function)

        layout.addStretch(0)
        self.setLayout(layout)

    def slot_btn_function(self):
        self.hide()
        self.s = Logpage()
        self.s.show()


# 设置注册失败页
class RegisterErrorpage(QWidget):
    def __init__(self, error):
        super(RegisterErrorpage, self).__init__()
        self._error = error
        self.init_ui()

    def init_ui(self):
        self.resize(500, 250)
        self.setWindowTitle('注册失败')
        self.setWindowIcon(QIcon('icon.jpg'))

        layout = QVBoxLayout()
        blank = QLabel("")
        layout.addWidget(blank)
        layout.addWidget(blank)

        self.centralWidget = QWidget(self)
        error = QLabel(self.centralWidget)
        # error.setGeometry(QRect(60, 60, 591, 61))
        font = QFont()
        font.setFamily('微软雅黑')
        font.setBold(True)
        font.setPointSize(14)
        font.setWeight(75)
        error.setFont(font)
        error.setText("<font color=black>%s</font>" % (self._error))
        layout.addWidget(error)
        error.setAlignment(Qt.AlignCenter)

        # error = QLabel(self._error)
        # layout.addWidget(error)
        # error.setAlignment(Qt.AlignCenter)

        self.btn = QPushButton('确定', self)
        self.btn.setGeometry(200, 150, 100, 50)
        self.btn.clicked.connect(self.slot_btn_function)
        self.btn.setStyleSheet('''QPushButton{background-color:rgb(62, 114, 242); color:white; border-radius:15px;font-size:18pt; font-weight:400;}
        QPushButton:hover{border:2px solid #F3F3F5;background:darkGray;}''')

        layout.addStretch(0)
        self.setLayout(layout)

    def slot_btn_function(self):
        self.hide()
        self.s = Registerpage()
        self.s.show()


# 风险评估页
class RiskAssessment(QWidget):
    def __init__(self, user_name):
        super(RiskAssessment, self).__init__()
        self.init_ui()
        self._user_name = user_name
        self._user_information = pd.read_csv("user_information.csv", index_col=0, header=0,
                                             dtype={"user_name": str, "password": str, "phone_number": str,
                                                    "risk_score": str, "risk_type": str, "strategy": str})

    def init_ui(self):

        self.resize(500, 250)
        self.setWindowTitle('风险评估')
        self.setWindowIcon(QIcon('icon.jpg'))

        all_v_layout = QVBoxLayout()

        # 1.年龄
        q1 = QHBoxLayout()
        q1.addWidget(QLabel('1 您的年龄是：\n'))
        self.q1_choice_0 = QRadioButton('A.18-25')
        self.q1_choice_1 = QRadioButton('B.25-40')
        self.q1_choice_2 = QRadioButton('C.40-60')
        self.q1_choice_3 = QRadioButton('D.> 60')
        q1.addWidget(self.q1_choice_0)
        q1.addWidget(self.q1_choice_1)
        q1.addWidget(self.q1_choice_2)
        q1.addWidget(self.q1_choice_3)
        groupbox_q1 = QGroupBox('Age')

        groupbox_q1.setLayout(q1)
        all_v_layout.addWidget(groupbox_q1)

        # 2.年收入
        q2 = QHBoxLayout()
        q2.addWidget(QLabel('2 您的年收入为：\n'))
        self.q2_choice_0 = QRadioButton('A.5万元以下')
        self.q2_choice_1 = QRadioButton('B.5至10万元')
        self.q2_choice_2 = QRadioButton('C.10-20万元')
        self.q2_choice_3 = QRadioButton('D.20万元以上')
        q2.addWidget(self.q2_choice_0)
        q2.addWidget(self.q2_choice_1)
        q2.addWidget(self.q2_choice_2)
        q2.addWidget(self.q2_choice_3)
        groupbox_q2 = QGroupBox('Income Flow')
        groupbox_q2.setLayout(q2)
        all_v_layout.addWidget(groupbox_q2)

        # 3.投资经验
        q3 = QHBoxLayout()
        q3.addWidget(QLabel('3 您有多少年投资股票、基金、外汇、期货、金融衍生品等风险资产'
                            '的经验（投资经历越长，您的风险承受能力越强）：\n'))
        self.q3_choice_0 = QRadioButton('A.没有经验')
        self.q3_choice_1 = QRadioButton('B.少于2年')
        self.q3_choice_2 = QRadioButton('C.2-5年')
        self.q3_choice_3 = QRadioButton('D.5年以上')
        q3.addWidget(self.q3_choice_0)
        q3.addWidget(self.q3_choice_1)
        q3.addWidget(self.q3_choice_2)
        q3.addWidget(self.q3_choice_3)
        groupbox_q3 = QGroupBox('Investment Experience')
        groupbox_q3.setLayout(q3)
        all_v_layout.addWidget(groupbox_q3)

        # 4.可用于投资资产
        q4 = QHBoxLayout()
        q4.addWidget(QLabel('4 在您每年的家庭收入中，可用于金融投资（储蓄存款除外）的比例为：\n'))
        self.q4_choice_0 = QRadioButton('A.小于10%')
        self.q4_choice_1 = QRadioButton('B.10%至20%')
        self.q4_choice_2 = QRadioButton('C.25%至50%')
        self.q4_choice_3 = QRadioButton('D.大于50%')
        q4.addWidget(self.q4_choice_0)
        q4.addWidget(self.q4_choice_1)
        q4.addWidget(self.q4_choice_2)
        q4.addWidget(self.q4_choice_3)
        groupbox_q4 = QGroupBox('Asset Liquidity')
        groupbox_q4.setLayout(q4)
        all_v_layout.addWidget(groupbox_q4)

        # 5.金融常识
        q5 = QHBoxLayout()
        q5.addWidget(QLabel('5 您的投资尝试掌握水平：\n'))
        self.q5_choice_0 = QRadioButton('A.缺乏投资基本知识')
        self.q5_choice_1 = QRadioButton('B.略有了解，但不懂投资技巧')
        self.q5_choice_2 = QRadioButton('C.有一定了解，懂一些投资技巧')
        self.q5_choice_3 = QRadioButton('D.认识充分，并懂得投资技巧')
        q5.addWidget(self.q5_choice_0)
        q5.addWidget(self.q5_choice_1)
        q5.addWidget(self.q5_choice_2)
        q5.addWidget(self.q5_choice_3)
        groupbox_q5 = QGroupBox('Financial Knowledge')
        groupbox_q5.setLayout(q5)
        all_v_layout.addWidget(groupbox_q5)

        # 6.金融常识
        q6 = QHBoxLayout()
        q6.addWidget(QLabel("6 您的投资目的是：\n"))
        self.q6_choice_0 = QRadioButton('A.资产保值')
        self.q6_choice_1 = QRadioButton('B.获取高于同期存款收益')
        self.q6_choice_2 = QRadioButton('C.保持资产稳健增长')
        self.q6_choice_3 = QRadioButton('D.实现资产迅速增长')
        q6.addWidget(self.q6_choice_0)
        q6.addWidget(self.q6_choice_1)
        q6.addWidget(self.q6_choice_2)
        q6.addWidget(self.q6_choice_3)
        groupbox_q6 = QGroupBox('Investment Aim')
        groupbox_q6.setLayout(q6)
        all_v_layout.addWidget(groupbox_q6)

        # 7.1.风险容忍度
        q7 = QHBoxLayout()
        q7.addWidget(QLabel("7.1 您如何看待投资亏损：\n"))
        self.q7_choice_0 = QRadioButton('A.很难接受，影响正常生活')
        self.q7_choice_1 = QRadioButton('B.受到一定的影响，但不影响正常生活')
        self.q7_choice_2 = QRadioButton('C.平常心看待，对情绪没有明显的影响')
        self.q7_choice_3 = QRadioButton('D.很理解，投资有风险，没有人只赚不赔')
        q7.addWidget(self.q7_choice_0)
        q7.addWidget(self.q7_choice_1)
        q7.addWidget(self.q7_choice_2)
        q7.addWidget(self.q7_choice_3)
        groupbox_q7 = QGroupBox('Risk Tolerance')
        groupbox_q7.setLayout(q7)
        all_v_layout.addWidget(groupbox_q7)

        # 7.2.风险容忍度
        q8 = QHBoxLayout()
        self.q8_choice_0 = QRadioButton('A.10%以内')
        self.q8_choice_1 = QRadioButton('B.10%-30%')
        self.q8_choice_2 = QRadioButton('C.30%-50%')
        self.q8_choice_3 = QRadioButton('D.50%以上')
        q8.addWidget(self.q8_choice_0)
        q8.addWidget(self.q8_choice_1)
        q8.addWidget(self.q8_choice_2)
        q8.addWidget(self.q8_choice_3)
        groupbox_q8 = QGroupBox('7.2 您进行投资时能承受的最大亏损比例是：\n')
        groupbox_q8.setLayout(q8)
        all_v_layout.addWidget(groupbox_q8)

        # 7.3.投资目的
        q9 = QHBoxLayout()
        self.q9_choice_0 = QRadioButton('A.确保资产的安全性，同时获得固定收益')
        self.q9_choice_1 = QRadioButton('B.希望投资能够获得一定的增值，同时获得波动适度的回报')
        self.q9_choice_2 = QRadioButton('C.倾向于长期成长，较少关心短期的回报和波动')
        self.q9_choice_3 = QRadioButton('D.只关心长期的高回报，能够接受短期的资产价值波动')
        q9.addWidget(self.q9_choice_0)
        q9.addWidget(self.q9_choice_1)
        q9.addWidget(self.q9_choice_2)
        q9.addWidget(self.q9_choice_3)
        groupbox_q9 = QGroupBox('7.3 您进行投资的主要目的是：\n')
        groupbox_q9.setLayout(q9)
        all_v_layout.addWidget(groupbox_q9)

        confirm_Btn = QPushButton('确认')
        confirm_Btn.clicked.connect(self.slot_btn_function)
        all_v_layout.addWidget(confirm_Btn)

        all_v_layout.addStretch(0)
        self.setLayout(all_v_layout)

    def slot_btn_function(self):
        choice_score = self.returnchoice()
        if choice_score:
            risk_type, risk_advise = self.get_risk_type(choice_score)
            print(self._user_information)
            print("-------------------------------------")
            print(self._user_information['user_name'])
            print(self._user_name)

            self._user_information["risk_score"][self._user_information['user_name'] == self._user_name] = choice_score
            self._user_information["risk_type"][self._user_information['user_name'] == self._user_name] = risk_type
            self._user_information.to_csv("user_information.csv")
            user_information_series = self._user_information[self._user_information['user_name'] == self._user_name]

            self.hide()
            self.s = ShowRiskAssessmentResultpage(user_information_series, risk_advise)
            self.s.show()
        else:
            return

    def returnchoice(self):
        choice_list = []
        for i in range(1, 10):
            question_id = 'q' + str(i)
            for j in range(4):
                choice_id = question_id + '_choice_' + str(j)
                choice_attr = getattr(self, choice_id)
                if choice_attr.isChecked():
                    choice_list.append(j)
        if len(choice_list) == 0:
            reply = QMessageBox.information(self, '提示', '请作答！', QMessageBox.Yes, QMessageBox.Yes)
            if reply == QMessageBox.Yes:
                print()
        else:
            choice_score = risk_evaluation(choice_list)
            return choice_score.round(2)

    def get_risk_type(self, choice_score):
        risk_type = ''
        risk_advise = ''
        if (choice_score > 0) & (choice_score <= 0.2):
            risk_type = '保守型'
            risk_advise = '不想承担任何风险，投资理财的目的在于保值，适合购买银行储蓄、货币基金、国债等产品'
        elif (choice_score > 0.2) & (choice_score <= 0.4):
            risk_type = '稳健型'
            risk_advise = '害怕风险，但是又希望保本的基础上有一定的收益，合适买债券、银行中短期理财产品等'
        elif (choice_score > 0.4) & (choice_score <= 0.6):
            risk_type = '平衡型'
            risk_advise = '综合考虑风险和收益，风险承受能力适中，可以尝试货币基金+股票/外汇等组合方式投资'
        elif (choice_score > 0.6) & (choice_score <= 0.8):
            risk_type = '积极型'
            risk_advise = '倾向于有风险高收益的理财投资，对风险并不惧怕，适合股票或偏股基金等投资方式'
        elif (choice_score > 0.8) & (choice_score <= 1.):
            risk_type = '激进型'
            risk_advise = '热衷在高风险中博取高收益，不怕本金损失，适合股票、外汇、数字货币等投资'
        return risk_type, risk_advise


# 显示风险评估结果页
class ShowRiskAssessmentResultpage(QWidget):
    def __init__(self, user_information_series, risk_advise):
        super(ShowRiskAssessmentResultpage, self).__init__()
        self._user_information_series = user_information_series
        self._risk_advise = risk_advise
        self.init_ui()

    def init_ui(self):
        self.resize(500, 250)
        self.setWindowTitle('风险评估结果')
        self.setWindowIcon(QIcon('icon.jpg'))

        layout = QVBoxLayout()
        blank = QLabel("")
        layout.addWidget(blank)
        layout.addWidget(blank)

        error = QLabel("您的风险评估值为" + str(self._user_information_series.risk_score.values))
        layout.addWidget(error)
        error.setAlignment(Qt.AlignCenter)

        error = QLabel("您的风险偏好为" + str(self._user_information_series.risk_type.values))
        layout.addWidget(error)
        error.setAlignment(Qt.AlignCenter)

        error = QLabel("该风险偏好的含义是：" + self._risk_advise)
        layout.addWidget(error)
        error.setAlignment(Qt.AlignCenter)

        self.btn1 = QPushButton('确定', self)
        self.btn1.setGeometry(110, 150, 100, 50)
        self.btn1.setStyleSheet('''QPushButton{background-color:rgb(62, 114, 242); color:white; border-radius:15px;font-size:18pt; font-weight:400;}
        QPushButton:hover{border:2px solid #F3F3F5;background:darkGray;}''')
        self.btn1.clicked.connect(self.slot_btn1_function)

        self.btn2 = QPushButton('重新评估', self)
        self.btn2.setGeometry(330, 150, 100, 50)
        self.btn2.setStyleSheet('''QPushButton{background-color:rgb(62, 114, 242); color:white; border-radius:15px;font-size:18pt; font-weight:400;}
        QPushButton:hover{border:2px solid #F3F3F5;background:darkGray;}''')
        self.btn2.clicked.connect(self.slot_btn2_function)

        layout.addStretch(0)
        self.setLayout(layout)

    def slot_btn1_function(self):
        self.hide()
        self.s = Infopage(self._user_information_series)
        self.s.show()

    def slot_btn2_function(self):
        self.hide()
        self.s = RiskAssessment(self._user_information_series.user_name.values[0])
        self.s.show()


# 设置个人中心页
class Infopage(QTabWidget):
    def __init__(self, user_information_series, parent=None):
        super(Infopage, self).__init__(parent)
        self._user_information = pd.read_csv("user_information.csv", index_col=0, header=0,
                                             dtype={"user_name": str, "password": str, "phone_number": str,
                                                    "risk_score": str, "risk_type": str, "strategy": str})
        self._user_information_series = user_information_series
        ID = list(user_information_series.index)[0]
        self.layout = QVBoxLayout()
        self.ID = str(ID)
        self.tab1 = QWidget()
        self.tab2 = QWidget()
        self.tab4 = QWidget()
        self.addTab(self.tab1, "个人中心")
        self.addTab(self.tab2, "消息中心")
        self.addTab(self.tab4, "策略定制")
        self.tab1UI()
        self.tab2UI()
        self.tab4UI()
        self.setWindowTitle("智能投顾系统")
        self.setWindowIcon(QIcon('icon.jpg'))
        self.setGeometry(100, 100, 1730, 880)

        self.font = QFont()
        self.font.setFamily('微软雅黑')
        self.font.setBold(True)
        self.font.setPointSize(14)
        self.font.setWeight(75)

    # 选项卡1：基本信息
    def tab1UI(self):
        layout = QFormLayout()

        # ql1 = QLabel()
        # ql1.setFont(self.font)
        # ql1.setText("<font color=black>%s</font>" % ('用户名：\t' + str(self._user_information_series.user_name.values[0])))
        # layout.addWidget(ql1)
        #
        # ql1 = QLabel()
        # ql1.setFont(self.font)
        # ql1.setText("<font color=black>%s</font>" % ('用户名：\t' + str(self._user_information_series.user_name.values[0])))
        # layout.addWidget(ql1)
        #
        # ql1 = QLabel()
        # ql1.setFont(self.font)
        # ql1.setText("<font color=black>%s</font>" % ('用户名：\t' + str(self._user_information_series.user_name.values[0])))
        # layout.addWidget(ql1)
        #
        # ql1 = QLabel()
        # ql1.setFont(self.font)
        # ql1.setText("<font color=black>%s</font>" % ('用户名：\t' + str(self._user_information_series.user_name.values[0])))
        # layout.addWidget(ql1)

        layout.addWidget(QLabel('用户名：\t' + str(self._user_information_series.user_name.values[0])))
        layout.addWidget(QLabel('手机号：\t' + str(self._user_information_series.phone_number.values[0])))
        layout.addWidget(QLabel('风险评估值：\t' + str(self._user_information_series.risk_score.values[0])))
        layout.addWidget(QLabel('风险偏好：\t' + str(self._user_information_series.risk_type.values[0])))

        self.back_button = QPushButton('退出登录')
        self.back_button.setGeometry(100, 300, 100, 50)
        layout.addWidget(self.back_button)
        self.back_button.clicked.connect(self.back_button_function)

        self.tab1.setLayout(layout)

    def back_button_function(self):
        self.hide()
        self.s = Mainpage()
        self.s.show()

    def tab2UI(self):
        layout = QFormLayout()
        self.updatepersonlsignal()
        # 根据用户ID查询用户历史策略
        address = self.ID + '_signal.csv'
        # 如果用户选择过策略
        if os.path.exists(address) == False:
            message = QLabel('暂无已选择策略')
            layout.addWidget(message)
        else:
            # 如果用户选择过策略
            self.strategy_data = pd.read_csv(address, index_col=0, encoding='gbk')
            strategy_list = self.strategy_data['strategy_name'].value_counts().index.sort_values()
            for i in strategy_list:
                # 根据用户选择过的策略设置按钮
                name = 'button' + str(i)
                setattr(self, name, QPushButton(i))
                getattr(self, name).setToolTip("查看策略消息详情")

                start_date = self.strategy_data['trade_date'][self.strategy_data['strategy_name'] == i].iloc[0]
                end_date = self.strategy_data['trade_date'][self.strategy_data['strategy_name'] == i].iloc[-1]
                period = str(start_date) + ' - ' + str(end_date)
                # 介绍策略时间
                intro = QLabel(('策略时间: ' + period))

                layout.addRow(intro, getattr(self, name))

                # self.statusBar()
                getattr(self, name).clicked.connect(self.check_button_function)

        self.refreshbutton = QPushButton('刷新')
        layout.addRow(self.refreshbutton)
        self.refreshbutton.clicked.connect(self.tab2refreshbutton_fun)

        # self.setTabText(1, "消息中心")
        self.tab2.setLayout(layout)

    def tab2refreshbutton_fun(self):
        self.removeTab(1)
        self.tab2 = self.tab2 = QWidget()
        self.insertTab(1, self.tab2, "消息提示")
        self.tab2UI()
        self.setCurrentIndex(1)


 # 链接消息中心中不同策略的槽函数
    def check_button_function(self):
        # 读取用户策略数据
        address = self.ID + '_signal.csv'
        self.strategy_data = pd.read_csv(address, index_col=0, encoding='gbk')
        # 查询用户使点击了哪个按钮
        sender = self.sender()
        # 显示该策略的历史消息
        self.s = strategymessagepage(sender.text(), self.strategy_data, self.ID)
        self.s.show()

# 选项卡3：我的策略
    # 选项卡3：我的策略
    def tab4UI(self):
        informationbox = QFormLayout()

        label1 = QLabel('您的风险偏好值是：\t')
        print(self._user_information_series.risk_score.values[0])
        label1text = QLabel(str(self._user_information_series.risk_score.values[0]))
        informationbox.addRow(label1, label1text)

        label1 = QLabel('您的风险偏好类型是：\t')
        label1text = QLabel(str(self._user_information_series.risk_type.values[0]))
        informationbox.addRow(label1, label1text)

        label2 = QLabel('您的预期收益是：\t')
        # 对预期收益下拉框进行实例化
        choice_list1 = ['1%-5%', '5%-10%', '10%-15%', '15%-20%']
        self.combobox_1 = QComboBox(self)
        self.combobox_1.addItems(choice_list1)
        informationbox.addRow(label2, self.combobox_1)

        label3 = QLabel('您预期的投资金额（元）：')
        self.moneyLineEdit = QLineEdit()
        informationbox.addRow(label3, self.moneyLineEdit)

        label4 = QLabel('您预期的换仓频率是：')
        # 对换仓下拉框进行实例化
        choice_list2 = ['每周', '每月', '每季度']
        self.combobox_2 = QComboBox(self)
        self.combobox_2.addItems(choice_list2)
        informationbox.addRow(label4, self.combobox_2)

        label5 = QLabel('您预期的投资时间是：')
        # 对投资时间下拉框进行实例化
        choice_list3 = ['半年', '一年', '三年', '五年']
        self.combobox_3 = QComboBox(self)
        self.combobox_3.addItems(choice_list3)
        informationbox.addRow(label5, self.combobox_3)

        # 回测开始时间
        label6 = QLabel('策略回测开始时间：')
        choice_list4 = [str(num) for num in list(range(2011, 2018))]
        self.combobox_4 = QComboBox(self)
        self.combobox_4.addItems(choice_list4)
        informationbox.addRow(label6, self.combobox_4)

        # 回测结束时间
        label7 = QLabel('策略回测结束时间：')
        choice_list5 = [str(num) for num in list(range(2011, 2018))]
        self.combobox_5 = QComboBox(self)
        self.combobox_5.addItems(choice_list5)
        informationbox.addRow(label7, self.combobox_5)
        self.combobox_5.activated[str].connect(self.set_year)

        self.risk_factor = float(self._user_information_series.risk_score.values[0])

        self.confirm_Btn = QPushButton('确认')
        informationbox.addWidget(self.confirm_Btn)
        self.confirm_Btn.clicked.connect(self.back_test)

        if int(self.combobox_5.currentText()) == 2011:
            self.confirm_Btn.setEnabled(False)

        # self.label6 = QLabel('投资曲线如下：')
        # self.layout.addRow(self.label6)

        # informationbox.addRow(self.label6,self.label8)

        self.layout.addLayout(informationbox)

        self.tab4.setLayout(self.layout)

    def set_year(self):

        self.start_year = int(self.combobox_4.currentText())
        self.end_year = int(self.combobox_5.currentText())
        if int(self.combobox_5.currentText()) > 2011:
            self.confirm_Btn.setEnabled(True)

    def chose_strategy(self):
        self.abspath = os.path.abspath(".")

        strategy_book = pd.read_csv(Path('nav_and_result/strategy_result_summary.csv'))
        strategy_book = strategy_book.sort_values(by='maximum_drawdown', axis=0, ascending=True)
        strategy_name = strategy_book.iloc[:, 0].values
        risk_factor = int(self.risk_factor * 10)
        self.strategy1 = strategy_name[risk_factor]
        print(self.strategy)

    def back_test(self):

        self.chose_strategy()
        data = pd.read_csv(Path("nav_and_result/" + self.strategy1 + '_nav.csv'))
        data.trade_date = [dt.strptime(d, '%Y-%m-%d').date() for d in data.trade_date]
        data = data.set_index('trade_date')
        start_date = dt(self.start_year, 1, 1).date()
        end_date = dt(self.end_year, 1, 1).date()
        data = data[(data.index < end_date) & (data.index > start_date)]
        money = int(self.moneyLineEdit.text())

        plot_figure(data, start_date, end_date)
        anual_profit, max_draw, final_nv, suit_rate, relative_profit = \
            performance(data, start_date, end_date, money, self.risk_factor)
        print(anual_profit, max_draw, final_nv, suit_rate, relative_profit)

        def judgestrategy(d):
            if d[:3] == 'CTA':
                strategy_name = 'CTA策略'
            elif d[:2] == 'mu':
                strategy_name = '多因子策略'
            elif d[:2] == 'in':
                strategy_name = '行业轮动策略'
            elif d[:2] == 'st':
                strategy_name = '风格轮动策略'
            return strategy_name

        strategy_name1 = judgestrategy(self.strategy)
        strategy_name2 = judgestrategy(self.strategy)

        self.label6 = QLabel('投资曲线如下：')
        # self.layout.addRow(self.label6)
        self.label7_1 = QLabel('为您选择的策略为：' + strategy_name1)
        self.label7_2 = QLabel('为您选择的策略为：' + strategy_name2)



        allpicturebox1 = QHBoxLayout()


        picturebox1 = QVBoxLayout()
        picturebox2 = QVBoxLayout()
        choosebox1 = QFormLayout()
        choosebox2 = QFormLayout()

        picturebox1.addWidget(self.label7_1)
        picturebox2.addWidget(self.label7_2)

        match_rate1 = '匹配度：' + '-'
        self.use_strategy1 = QPushButton('使用这个策略', self)
        choosebox1.addRow(QLabel(match_rate1), self.use_strategy1)
        self.use_strategy1.clicked.connect(self.use_strategy1_fun)

        match_rate2 = '匹配度：' + '-'
        self.use_strategy2 = QPushButton('使用这个策略', self)
        choosebox2.addRow(QLabel(match_rate2), self.use_strategy1)
        self.use_strategy2.clicked.connect(self.use_strategy2_fun)

        self.label8 = QLabel()
        self.label8.setPixmap(QPixmap('temp.png'))
        self.label8.setScaledContents(True)
        picturebox1.addWidget(self.label8)

        self.label9 = QLabel()
        self.label9.setPixmap(QPixmap('temp1.png'))
        self.label9.setScaledContents(True)
        picturebox2.addWidget(self.label9)

        resultbox1 = QGridLayout()
        resultbox1.addWidget(QLabel('收益率'), 0, 0)
        resultbox1.addWidget(QLabel('超额收益'), 0, 1)
        resultbox1.addWidget(QLabel('最大回撤'), 0, 2)
        resultbox1.addWidget(QLabel('资金量'), 0, 3)
        resultbox1.addWidget(QLabel('-'), 1, 0)
        resultbox1.addWidget(QLabel('-'), 1, 1)
        resultbox1.addWidget(QLabel('-'), 1, 2)
        resultbox1.addWidget(QLabel('-'), 1, 3)
        picturebox1.addLayout(resultbox1)
        picturebox1.addLayout(choosebox1)

        resultbox2 = QGridLayout()
        resultbox2.addWidget(QLabel('收益率'), 0, 0)
        resultbox2.addWidget(QLabel('超额收益'), 0, 1)
        resultbox2.addWidget(QLabel('最大回撤'), 0, 2)
        resultbox2.addWidget(QLabel('资金量'), 0, 3)
        resultbox2.addWidget(QLabel('-'), 1, 0)
        resultbox2.addWidget(QLabel('-'), 1, 1)
        resultbox2.addWidget(QLabel('-'), 1, 2)
        resultbox2.addWidget(QLabel('-'), 1, 3)

        picturebox2.addLayout(resultbox2)
        picturebox2.addLayout(choosebox2)

        allpicturebox1.addLayout(picturebox1)
        allpicturebox1.addLayout(picturebox2)
        self.layout.addLayout(allpicturebox1)

        self.not_use_strategy = QPushButton('重新选择', self)
        self.layout.addWidget(self.not_use_strategy)
        self.not_use_strategy.clicked.connect(self.not_use_strategy_func)

        # 刷新策略选择界面
        self.removeTab(2)
        self.tab4 = QWidget()
        self.insertTab(2, self.tab4, "策略定制")
        self.tab4.setLayout(self.layout)
        self.setCurrentIndex(2)
        self.confirm_Btn.setEnabled(False)

        return

    def use_strategy1_fun(self):
        print('use1')
        self.use_strategy_func(self.strategy)

    def use_strategy2_fun(self):
        print('use2')
        self.use_strategy_func(self.strategy)

    def use_strategy_func(self, strategy_name):
        print('use')
        temp_information = pd.read_csv("user_information.csv", index_col=0)
        existed_strategy = temp_information.iloc[int(self.ID), 5]
        if strategy_name == existed_strategy:
            reply = QMessageBox.information(self, '提示', '策略已经被使用', QMessageBox.Yes, QMessageBox.Yes)
            # if reply ==  QMessageBox.Yes:
            #    return (True)
        elif pd.isna(existed_strategy):
            #     self.createpersonlsignal()
            if (self.createpersonlsignal()):
                message = '开始使用' + strategy_name
                reply = QMessageBox.information(self, '提示', message, QMessageBox.Yes, QMessageBox.Yes)
                if reply == QMessageBox.Yes:
                    return (True)
            else:
                reply = QMessageBox.information(self, '提示', '使用策略出错', QMessageBox.Yes, QMessageBox.Yes)
                if reply == QMessageBox.Yes:
                    return (True)
        elif strategy_name != existed_strategy:
            message = (self._user_information_series['strategy'].values + '正在在使用\n是否使用新的策略')
            reply = QMessageBox.question(self, '提示', message, QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if reply == QMessageBox.Yes:
                if (self.createpersonlsignal()):
                    message = '开始使用' + strategy_name
                    reply = QMessageBox.information(self, '提示', message, QMessageBox.Yes, QMessageBox.Yes)
                    return (True)
                else:
                    reply = QMessageBox.information(self, '提示', '使用策略出错', QMessageBox.Yes, QMessageBox.Yes)
                    if reply == QMessageBox.Yes:
                        return (True)
            return (True)

    def use_strategy_func(self):
        print('use')
        temp_information = pd.read_csv("user_information.csv", index_col=0)
        existed_strategy = temp_information.iloc[int(self.ID), 5]
        if self.strategy == existed_strategy:
            reply = QMessageBox.information(self, '提示', '策略已经被使用', QMessageBox.Yes, QMessageBox.Yes)
            # if reply ==  QMessageBox.Yes:
            #    return (True)
        elif pd.isna(existed_strategy):
            #     self.createpersonlsignal()
            if (self.createpersonlsignal()):
                message = '开始使用' + self.strategy
                reply = QMessageBox.information(self, '提示', message, QMessageBox.Yes, QMessageBox.Yes)
                if reply == QMessageBox.Yes:
                    return (True)
            else:
                reply = QMessageBox.information(self, '提示', '使用策略出错', QMessageBox.Yes, QMessageBox.Yes)
                if reply == QMessageBox.Yes:
                    return (True)
        elif self.strategy != existed_strategy:
            message = (self._user_information_series['strategy'].values + '正在在使用\n是否使用新的策略')
            reply = QMessageBox.question(self, '提示', message, QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if reply == QMessageBox.Yes:
                if (self.createpersonlsignal()):
                    message = '开始使用' + self.strategy
                    reply = QMessageBox.information(self, '提示', message, QMessageBox.Yes, QMessageBox.Yes)
                    return (True)
                else:
                    reply = QMessageBox.information(self, '提示', '使用策略出错', QMessageBox.Yes, QMessageBox.Yes)
                    if reply == QMessageBox.Yes:
                        return (True)
            return (True)

    def not_use_strategy_func(self):
        self.removeTab(2)
        self.tab4 = QWidget()
        self.insertTab(2, self.tab4, "策略定制")
        self.layout = QVBoxLayout()
        self.tab4UI()
        self.confirm_Btn.setEnabled(True)

        self.setCurrentIndex(2)
        return

    def createpersonlsignal(self):
        try:
            ID = list(self._user_information_series.index)[0]
            temp_information = pd.read_csv("user_information.csv", index_col=0)
            temp_information.iloc[ID, 5] = self.strategy
            temp_information.to_csv("user_information.csv")
            yesterday = (date.today() + timedelta(days=-6)).strftime("%Y-%m-%d")
            print(yesterday)

            address = self.ID + '_signal.csv'
            signal_address = Path('signal/' + self.strategy + '_signal.csv')
            strategy_signal = pd.read_csv(signal_address, index_col=0, dtype={'trade_date': str})
            print(strategy_signal)
            # strategy_signal['trade_date'] = [dt.strptime(d, '%Y-%m-%d').date() for d in strategy_signal['trade_date'].trade_date]

            try:
                if os.path.exists(address) == False:  # 没有文件，生成文件
                    strategy_signal_now = pd.DataFrame(index=[0], columns=['trade_date', 'trade_code', 'signal',
                                                                           'strategy_name'])
                    strategy_signal_now['strategy_name'] = '1. ' + self.strategy
                    strategy_signal_now['trade_date'] = yesterday
                    strategy_signal_now['trade_code'] = ' '
                    strategy_signal_now['signal'] = '开始使用'

                    if yesterday not in strategy_signal['trade_date'].values:
                        strategy_signal_now.to_csv(address, encoding='gbk')
                    else:
                        strategy_signal = strategy_signal[strategy_signal['trade_date'] == yesterday]
                        strategy_signal['strategy_name'] = '1. ' + self.strategy
                        strategy_signal_now = pd.concat([strategy_signal_now, strategy_signal], axis=0)
                        strategy_signal_now.to_csv(address, encoding='gbk')
                    print('fresh')

                    return True
                else:  # 有文件
                    temp_data = pd.read_csv(address, index_col=0, encoding='gbk')

                    i = 1 + len(temp_data['strategy_name'].value_counts().index)
                    print(i)
                    strategy_signal_now = pd.DataFrame(index=[0, 1], columns=['trade_date', 'trade_code', 'signal',
                                                                              'strategy_name'])
                    strategy_signal_now.loc[0] = [yesterday, ' ', '停止使用', temp_data['strategy_name'].values[-1]]
                    strategy_signal_now.loc[1] = [yesterday, ' ', '开始使用', str(i) + '. ' + self.strategy]
                    strategy_signal_now = pd.concat([temp_data, strategy_signal_now], axis=0)
                    if yesterday not in strategy_signal['trade_date'].values:
                        strategy_signal_now.to_csv(address, encoding='gbk')
                    else:

                        strategy_signal = strategy_signal[strategy_signal['trade_date'] == yesterday]
                        strategy_signal_now = pd.concat([strategy_signal_now, strategy_signal], axis=0)

                        strategy_signal_now.to_csv(address, encoding='gbk')
                    print('add')

                    return True
            except:
                return (False)
                print('error1')
        except:
            print('error2')
            return (False)

    def updatepersonlsignal(self):
        try:
            ID = list(self._user_information_series.index)[0]
            temp_information = pd.read_csv("user_information.csv", index_col=0)
            existed_strategy = temp_information.iloc[ID, 5]
            if pd.isna(existed_strategy):
                print('no strategy used')
                return True
            else:
                print('strategy used')
                # existed_strategy = self._user_information_series['strategy'].values[0]
                address = self.ID + '_signal.csv'
                signal_address = Path('signal/' + existed_strategy + '_signal.csv')
                strategy_signal = pd.read_csv(signal_address, index_col=0)
                yesterday = (date.today() + timedelta(days=-6)).strftime("%Y-%m-%d")
                if os.path.exists(address) == True:
                    if yesterday == pd.read_csv(address, index_col=0, encoding='gbk')['trade_date'].values[0]:
                        print('updated before')
                        return True
                if yesterday in strategy_signal['trade_date'].values:
                    strategy_signal_now = strategy_signal[strategy_signal['trade_date'] == yesterday]
                    # start_date = yesterday
                    # end_date = strategy_signal['trade_date'].tail(1)
                    try:
                        if os.path.exists(address) == False:
                            strategy_signal_now['strategy_name'] = '1. ' + existed_strategy
                            strategy_signal_now.to_csv(address, encoding='gbk')
                            print('fresh')
                            return True
                        else:
                            temp_data = pd.read_csv(address, index_col=0, encoding='gbk')
                            i = len(temp_data['strategy_name'].value_counts().index)
                            print(i)
                            strategy_signal_now['strategy_name'] = str(i) + '. ' + existed_strategy
                            strategy_signal_now = pd.concat([temp_data, strategy_signal_now], axis=0)
                            strategy_signal_now.to_csv(address, encoding='gbk')
                            print('update')
                            return (True)
                    except:
                        print('error1')
                        return (False)
                else:
                    print('no signal getted')
                    return (True)
        except:
            print('error2')
            return (False)

# 单独策略消息展示界面
class strategymessagepage(QWidget):
    def __init__(self, strategy_name, strategy_data, ID):
        super(strategymessagepage, self).__init__()
        # 策略的名称
        self.strategy_name = strategy_name
        # 所有策略的数据
        self.strategy_data = strategy_data
        self.address = ID + '_signal.csv'
        self.ID = ID
        self.init_ui()

    def init_ui(self):

        # 取所有策略数据中所需单独策略的消息
        data = self.strategy_data[self.strategy_data['strategy_name'] == self.strategy_name]
        self.setWindowTitle(self.strategy_name)
        # self.setWindowIcon(QIcon('message.png'))
        self.setGeometry(100, 100, 1730, 880)
        # self.setStyleSheet("background-image: url(message.jpg)")
        # 依据要求排序栏
        data = data.loc[:, ['trade_date', 'trade_code', 'signal']]
        titles = ['日期', '股票列表', '仓位', '具体操作']
        self.table = QTableWidget()
        self.table.setRowCount(len(data.index))  # 行下标最大值
        self.table.setColumnCount(4)  # 列
        self.table.setHorizontalHeaderLabels(titles)

        palette = QPalette()
        background = QImage('message.png')
        palette.setBrush(self.backgroundRole(), QBrush(background))
        self.setPalette(palette)

        for i in range(len(data.index)):
            self.table.setRowHeight(i, 50)  # 设置i行的高度
            for j in range(len(data.columns)):
                values = str(data.iloc[i, j])
                self.table.setItem(i, j, QTableWidgetItem(values))
                if self.table.item(i, j):
                    self.table.item(i, j).setTextAlignment(Qt.AlignCenter)

            yesterday = dt.strptime(data.iloc[i, 0], '%Y-%m-%d').date()
            today = (yesterday + timedelta(days=1)).strftime('%Y/%m/%d')
            if data.iloc[i, 1] != ' ':
                message = 'Robo-Avisor建议您于' + today + '购买股票组合' + str(data.iloc[i, 1]) + '\n 每个标的资金量为总资金量的' + str(
                    data.iloc[i, 2])
                self.table.setItem(i, 3, QTableWidgetItem(message))
                self.table.item(i, 3).setTextAlignment(Qt.AlignCenter)
            else:
                message = ' '
                self.table.setItem(i, 3, QTableWidgetItem(message))
                self.table.item(i, 3).setTextAlignment(Qt.AlignCenter)

        # 设置股票代码那列的宽度
        self.table.setColumnWidth(1, 632)
        self.table.setColumnWidth(3, 948)
        # self.table.setFrameShape(QFrame.NoFrame)
        self.table.setShowGrid(False)
        self.table.setFixedHeight((len(data.index) + 1) * 50)

        self.table.verticalHeader().setVisible(False)  # 隐藏垂直表头

        self.stopbutton = QPushButton('停止使用')
        self.stopbutton.clicked.connect(self.stopbutton_fun)

        mainLayout = QFormLayout()
        mainLayout.addRow(QLabel('调仓策略通知'))
        mainLayout.addRow(self.table)
        mainLayout.addRow(self.stopbutton)
        self.setLayout(mainLayout)
        self.show()

    def stopbutton_fun(self):
        self._user_information = pd.read_csv("user_information.csv", index_col=0)
        if pd.isna(self._user_information.iloc[int(self.ID), 5]):
            reply = QMessageBox.information(self, '提示', '没有策略在使用', QMessageBox.Yes, QMessageBox.Yes)

            return True
        else:
            try:
                self._user_information.iloc[int(self.ID), 5] = ''
                self._user_information.to_csv("user_information.csv")

                temp_data = pd.read_csv(self.address, index_col=0, encoding='gbk')
                strategy_signal_now = pd.DataFrame(index=[0, 1], columns=['trade_date', 'trade_code', 'signal',
                                                                          'strategy_name'])
                today = (date.today()).strftime("%Y-%m-%d")
                strategy_signal_now.loc[0] = [today, ' ', '停止使用', self.strategy_name]
                strategy_signal_now = pd.concat([temp_data, strategy_signal_now], axis=0)
                strategy_signal_now.to_csv(self.address, encoding='gbk')
                reply = QMessageBox.information(self, '提示', '该策略已经被删除，请刷新界面查看', QMessageBox.Yes, QMessageBox.Yes)
                return True
            except:
                reply = QMessageBox.warning(self, '提示', '请求出错，请联系客服', QMessageBox.Yes, QMessageBox.Yes)
                return False


def main():
    app = QApplication(sys.argv)
    w = Mainpage()
    w.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()



