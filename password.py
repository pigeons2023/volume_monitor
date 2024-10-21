import datetime

# 密码：小时+日期+年份+月份
current_date = datetime.datetime.now()
date_str = current_date.strftime('%H%d%Y%m')
nowpassword = date_str

# 打印生成的密码
print(nowpassword)
