from datetime import datetime
from subprocess import Popen, PIPE


def get_run_ps_aux_result():
    return Popen(['ps', 'aux'], stdout=PIPE).stdout.readlines()


def get_formatted_data(data_list):
    keys = data_list[0].decode("utf-8").split()
    values_list = list(map(lambda item: item.decode("utf-8").split(), data_list[1:]))
    return [dict(zip(keys, values)) for values in values_list]


def get_processes_count_by_user(dicts_list, user):
    counter = 0
    for item in dicts_list:
        if item["USER"] == user:
            counter += 1
    return counter


def get_sum_by_key(dicts_list, key):
    return round(sum([float(item[key]) for item in dicts_list]), 1)


def get_command_with_max_value_by_key(dicts_list, key):
    return max(dicts_list, key=lambda item: float(item[key]))["COMMAND"][:20]


formatted_data = get_formatted_data(get_run_ps_aux_result())

users = list(set(x["USER"] for x in formatted_data))
process_count = len(formatted_data)
mem_usage = get_sum_by_key(formatted_data, "%MEM")
cpu_usage = get_sum_by_key(formatted_data, "%CPU")
command_with_max_of_mem = get_command_with_max_value_by_key(formatted_data, "%MEM")
command_with_max_of_cpu = get_command_with_max_value_by_key(formatted_data, "%CPU")

report = []
report.append("Отчёт о состоянии системы:")
report.append(f"Пользователи системы: {users}")
report.append(f"Процессов запущено: {process_count}")
report.append("Пользовательских процессов:")
for u in users:
    report.append(f"{u}: {get_processes_count_by_user(formatted_data, u)}")
report.append(f"Всего памяти используется: {mem_usage}%")
report.append(f"Всего CPU используется: {cpu_usage}%")
report.append(f"Больше всего памяти использует: {command_with_max_of_mem}")
report.append(f"Больше всего CPU использует: {command_with_max_of_cpu}")

print(*report, sep="\n")

file_name = datetime.now().strftime("%d-%m-%Y-%H:%M-scan.txt")
with open(file_name, 'w') as file:
    file.writelines(f"{item}\n" for item in report)
