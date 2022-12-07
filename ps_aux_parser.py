from datetime import datetime
from subprocess import Popen, PIPE


def get_ps_aux_result():
    return Popen(['ps', 'aux'], stdout=PIPE).stdout.readlines()


def get_formatted_data(_data_list):
    _keys = _data_list[0].decode("utf-8").split()
    _values_list = list(map(lambda item: item.decode("utf-8").split(), _data_list[1:]))
    return [dict(zip(_keys, values)) for values in _values_list]


def get_user_list(_formatted_data):
    return list(set(_item["USER"] for _item in _formatted_data))


def get_processes_count_by_user(_dicts_list, _user):
    _count = 0
    for item in _dicts_list:
        if item["USER"] == _user:
            _count += 1
    return _count


def get_sorted_processes_by_users(_formatted_data, _users):
    _counts_list = [get_processes_count_by_user(_formatted_data, _user) for _user in _users]
    _dict = dict(zip(_users, _counts_list))
    return dict(sorted(_dict.items(), key=lambda item: item[1], reverse=True))


def get_sum_by_key(_dicts_list, _key):
    return round(sum([float(item[_key]) for item in _dicts_list]), 1)


def get_command_with_max_value_by_key(_dicts_list, _key):
    return max(_dicts_list, key=lambda item: float(item[_key]))["COMMAND"][:20]


def generate_report(_formatted_data):
    users = get_user_list(_formatted_data)
    process_count = len(_formatted_data)
    sorted_processes_by_user = get_sorted_processes_by_users(_formatted_data, users)
    mem_usage = get_sum_by_key(_formatted_data, "%MEM")
    cpu_usage = get_sum_by_key(_formatted_data, "%CPU")
    command_with_max_of_mem = get_command_with_max_value_by_key(_formatted_data, "%MEM")
    command_with_max_of_cpu = get_command_with_max_value_by_key(_formatted_data, "%CPU")
    _report = list()
    _report.append("System status report:")
    _report.append(f"System users: {str(users)[1:-1]}")
    _report.append(f"Processes running: {process_count}")
    _report.append("User processes:")
    for key, value in sorted_processes_by_user.items():
        _report.append(f"{key}: {value}")
    _report.append(f"Total memory used: {mem_usage}%")
    _report.append(f"Total CPU used: {cpu_usage}%")
    _report.append(f"Uses the most memory: {command_with_max_of_mem}")
    _report.append(f"Most CPU used: {command_with_max_of_cpu}")
    return _report


def output_to_console(_report):
    print(*_report, sep="\n")


def write_to_file(_metrics):
    file_name = datetime.now().strftime("%d-%m-%Y-%H:%M-scan.txt")
    with open(file_name, 'w') as file:
        file.writelines(f"{item}\n" for item in report)


if __name__ == '__main__':
    ps_aux_result = get_ps_aux_result()
    formatted_data = get_formatted_data(ps_aux_result)
    report = generate_report(formatted_data)
    output_to_console(report)
    write_to_file(report)
