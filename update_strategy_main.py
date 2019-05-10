#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author：Genie time:2019/4/14

import style_rotation
import multi_factor_test
import CTA


#更新策略的结果
def main():
    # 风格轮动
    style_rotation()

    #多因子
    multi_factor_test.multi_factor()
    
    # 期货策略
    CTA.cta()


if __name__ == "__main__":
    main()
