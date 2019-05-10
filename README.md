# robo-advisor-system
用于给个人投资者提供量化投资建议的智能投顾平台
## 不同文件的介绍
1. main_UI 使我们的主要界面程序，其中构建了系统的注册登录界面，进入系统后还分为个人中心，消息中心和策略选择三个部分。其中个人中心展示了用户的部分信息，
消息中心为用户使用策略后给用户推送的交易信号（包含历史消息记录），策略选择为用户选择量化策略的界面 </br>
2. question class为在用户注册时为了调查用户的风险偏好所设置的调差问卷，用户也可以在个人个人中心通过重新填写问卷来修改个人风险偏好，风险偏好用于策略的选择 </br>
3. muti_factor_test为多因子策略，style_rotation为风格轮动策略，CTA为期货策略，这三个文件都会根据标的的交易或基本面数据输出信号和结果（包含回测信号和结果）</br>
4. strategy_result_summary是根据回测结果计算年化收益率， 波动率，最大回撤，夏普率等指标的文件</br>
5. update_strategy_main为每天更新所有策略的结果并产生交易信号
6. downloaddata1.0为从tushare上下载股票、指数、期货的行情以及基本面数据，并保存到本地，每天更新一次，形成一个本地的数据库，时间从20100101开始，为data文件。但是由于数据量较大作者没有将数据放到github中</br>

## 系统介绍
本系统的目的是给没有量化投资经验的投资者提供量化投资的建议。用户可以注册使用我们的系统，系统会根据用户的风险偏好、投资金额、投资年限等因素推荐适合用户的投资策略，用户如果选择使用该策略，那么该策略会每天在前一天交易数据的基础上更新交易信号，如果有新的交易信号产生就会在交易中心中输出给用户，用户可以根据该交易信号自行交易。 </br>
当用户打开系统时会看到如下界面，其中有我们的系统介绍，所使用的交易策略介绍以及团队介绍，同时还有注册和登录按钮</br>
![Image](https://github.com/WangBingquan96/robo-advisor-system/blob/master/pircture%201.png)  </br>
新用户开始注册一个账号时会看到如下界面</br>
![Image](https://github.com/WangBingquan96/robo-advisor-system/blob/master/pircture%202.png)</br>
账号注册完之后会直接进入风险评估界面，用户可以填写问卷来评估自己的风险偏好</br>
![Image](https://github.com/WangBingquan96/robo-advisor-system/blob/master/pircture%203.png)</br>
然后是个人中心界面，其中个人中心会显示用户的部分信息，并且用户可以修改密码和重新评估风险值</br>
![Image](https://github.com/WangBingquan96/robo-advisor-system/blob/master/pircture%204.png)</br>
在策略选择界面，用户可以输入投资金额，回测时间等参数，然后系统会根据用户的风险偏好给用户推荐两个最好的量化策略，并且输出策略的回测结果和匹配度，用户可以选择使用或者不使用这些策略</br>
![Image](https://github.com/WangBingquan96/robo-advisor-system/blob/master/pircture%205.png)</br>
如果用户使用了这个策略，那么在消息中心界面刷新之后就可以看大这个策略开始被使用</br>
![Image](https://github.com/WangBingquan96/robo-advisor-system/blob/master/pircture%206.png)</br>
点开该策略还可以看到具体的交易信息（如果使用当天恰好有交易信号的话），通常没有交易信号，所以这两张图展示了 一个历史账号的记录（从2018年开始使用）</br>
![Image](https://github.com/WangBingquan96/robo-advisor-system/blob/master/pircture%207.png)</br>
![Image](https://github.com/WangBingquan96/robo-advisor-system/blob/master/pircture%208.png)</br>

## 特别说明
1. 本系统由pycharm利用python开发，主要使用了pyqt5、numpy、pandas等扩展包，其中pyqt5是专门用来进行UI设计的扩展包 </br>
2. 上述文件缺少数据库以及策略回测结果文件（应当保存在nav_and_result和signal文件夹下），无法运行 </br>
3. 上述文件主要展示了多因子策略、CTA策略以及风格轮动策略的代码、构建平台的代码以及下载数据的代码，可以用作参考 </br>
4. 上述程序仅用于本地使用，还没有搭建服务器进行线上使用 </br>
5. 本程序是北京大学汇丰商学院软件工程课程的课程作业，不为商用 </br>


