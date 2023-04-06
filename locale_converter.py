inp = '''CPU Usage Percentage
CPU Times
CPU Frequency
CPU Usage Percentage Min
CPU Usage Percentage Min
Average network throughputs
CPU Load
Average disk usage
Memory Usage
Network activity
Disk Usage
Browser Used & Traffic Reports
Sessions
Channel
Browser
User Activivites
Name
Email
Timestamp
Processes
Memory'''
out = '''CPU пайдалану пайызы
CPU уақыттары
CPU жиілігі
CPU пайдалану пайызы Мин
CPU пайдалану пайызы Мин
Желінің орташа өткізу қабілеті
CPU жүктемесі
Дискіні орташа пайдалану
Жедел Жадты пайдалану
Желі әрекеті
Дискіні пайдалану
Браузер пайдаланылған және трафик есептері
Сеанстар
Арна
Браузер
Пайдаланушы әрекеттері
Аты
Электрондық пошта
Уақыт белгісі
Процестер
Жедел Жад'''

inp = inp.split('\n')
out = out.split('\n')
out = [f'msgid "{inp[i]}" \nmsgstr "{out[i]}"\n' for i in range(len(inp))]
print('\n'.join(out))