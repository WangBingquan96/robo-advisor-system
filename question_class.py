class risk_assessment():
    def __init__(self):
        super(RegisterErrorpage, self).__init__()
        self.init_ui()

    def init_ui(self):
        self.resize(500, 250)
        self.setWindowTitle('风险评估')

        all_v_layout = QVBoxLayout()
        # 下面和本页无关，保留作为你们写问卷的模板
        # 返回值用for循环

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
        choice_result = confirm_Btn.clicked.connect(self.returnchoice)
        all_v_layout.addWidget(confirm_Btn)

        self.setTabText(1, "消息中心")
        self.tab2.setLayout(all_v_layout)

    def returnchoice(self):
        choice_list = []
        for i in range(1, 10):
            question_id = 'q' + str(i)
            for j in range(4):
                choice_id = question_id + '_choice_' + str(j)
                choice_attr = getattr(self, choice_id)
                if choice_attr.isChecked():
                    choice_list.append(j)
        choice_score = risk_evaluation(choice_list)
        print('风险值为', choice_score)
        return choice_list

    def slot_btn_function(self):
        self.hide()
        self.s = Registerpage()
        self.s.show()


