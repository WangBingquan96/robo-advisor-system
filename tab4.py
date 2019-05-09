def tab4UI(self):
    self.layout = QFormLayout()

    label1 = QLabel('您的风险偏好类型是：\t')
    label1text = QLabel('字符串格式化（改成问卷的输出）')
    self.layout.addRow(label1, label1text)

    label2 = QLabel('您的预期收益是：\t')
    # 对预期收益下拉框进行实例化
    choice_list1 = ['1%-5%', '5%-10%', '10%-15%', '15%-20%']
    self.combobox_1 = QComboBox(self)
    self.combobox_1.addItems(choice_list1)
    self.layout.addRow(label2, self.combobox_1)

    label3 = QLabel('您预期的投资金额（元）：')
    self.moneyLineEdit = QLineEdit()
    self.layout.addRow(label3, self.moneyLineEdit)

    label4 = QLabel('您预期的换仓频率是：')
    # 对换仓下拉框进行实例化
    choice_list2 = ['每周', '每月', '每季度']
    self.combobox_2 = QComboBox(self)
    self.combobox_2.addItems(choice_list2)
    self.layout.addRow(label4, self.combobox_2)

    label5 = QLabel('您预期的投资时间是：')
    # 对投资时间下拉框进行实例化
    choice_list3 = ['半年', '一年', '三年', '五年']
    self.combobox_3 = QComboBox(self)
    self.combobox_3.addItems(choice_list3)
    self.layout.addRow(label5, self.combobox_3)

    # 回测开始时间
    label6 = QLabel('策略回测开始时间：')
    choice_list4 = [str(num) for num in list(range(2010, 2018))]
    self.combobox_4 = QComboBox(self)
    self.combobox_4.addItems(choice_list4)
    self.layout.addRow(label6, self.combobox_4)

    # 回测结束时间
    label7 = QLabel('策略回测结束时间：')
    choice_list5 = [str(num) for num in list(range(2010, 2018))]
    self.combobox_5 = QComboBox(self)
    self.combobox_5.addItems(choice_list5)
    self.layout.addRow(label7, self.combobox_5)
    self.combobox_5.activated[str].connect(self.set_year)

    self.risk_factor = 1

    confirm_Btn = QPushButton('确认')
    confirm_Btn.clicked.connect(self.back_test)
    self.layout.addWidget(confirm_Btn)

    self.setTabText(3, "我的策略")  # 也可以在addTab时进行修改
    self.tab4.setLayout(self.layout)


def set_year(self):
    self.start_year = int(self.combobox_4.currentText())
    self.end_year = int(self.combobox_5.currentText())


def chose_strategy(self):
    if self.risk_factor > 0:
        self.strategy = 'style_rotation'


def back_test(self):
    self.chose_strategy()
    data = pd.read_csv('C:\\Users\\Shen Zimin\\Desktop\\' + self.strategy + '_nav.csv')
    data.trade_date = [dt.strptime(d, '%Y-%m-%d').date() for d in data.trade_date]
    data = data.set_index('trade_date')
    start_date = dt(self.start_year, 1, 1).date()
    end_date = dt(self.end_year, 1, 1).date()
    data = data[(data.index < end_date) & (data.index > start_date)]
    plot_figure(data)
    self.label6 = QLabel('投资曲线如下：')
    self.layout.addRow(self.label6)
    self.label8 = QLabel()
    self.label8.setPixmap(QPixmap('C:\\Users\\Shen Zimin\\Desktop\\temp.jpg'))
    self.layout.addWidget(self.label8)
    return


# def returnchoice(self):
#     choice_list = []
#     for i in range(1, 10):
#         question_id = 'q' + str(i)
#         for j in range(4):
#             choice_id = question_id + '_choice_' + str(j)
#             choice_attr = getattr(self, choice_id)
#             if choice_attr.isChecked():
#                 choice_list.append(j)
#     choice_score = risk_evaluation(choice_list)
#     print('风险值为', choice_score)
#     return choice_list