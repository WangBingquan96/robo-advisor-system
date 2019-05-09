#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np


def risk_evaluation(risk_para):

    risk_score = []
    for i in risk_para:
        if i == 0:
            risk_score.append(0.25)
        elif i == 1:
            risk_score.append(0.5)
        elif i == 2:
            risk_score.append(0.75)
        elif i == 3:
            risk_score.append(1)

    true_risk = np.mean(risk_score)
    print('风险得分为：', risk_score)
    print('风险平均分为：', true_risk)
    return true_risk
