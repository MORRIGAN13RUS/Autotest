import pytest
import yaml
import random
import string
from datetime import datetime
from ssh_checkers import ssh_checkout as che
from ssh_checkers import ssh_getout

with open('ssh_config.yaml', 'r') as f:
    data = yaml.safe_load(f)

bad_arx = 'bad_arx'
OK = 'Everything is Ok'


@pytest.fixture()
def make_folders():
    return che(data['host'], data['user'], data['passwd'],
               f'mkdir {data["folder_in"]} {data["folder_out"]} {data["folder_ext"]} {data["folder_ext2"]} {data["folder_bad_out"]}',
               '')


@pytest.fixture()
def clear_folders():
    return che(data['host'], data['user'], data['passwd'],
               f'rm -rf {data["folder_in"]}/* {data["folder_out"]}/* {data["folder_ext"]}/* {data["folder_ext2"]}/* {data["folder_bad_out"]}/*',
               '')


@pytest.fixture()
def make_files():
    list_off_files = []
    for i in range(data["count"]):
        filename = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
        if che(data['host'], data['user'], data['passwd'],
               f'cd {data["folder_in"]}; dd if=/dev/urandom of={filename} bs={data["bs"]} count=1 iflag=fullblock', ''):
            list_off_files.append(filename)
    return list_off_files


@pytest.fixture()
def make_subfolder():
    subfoldername = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
    testfilename = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
    if not che(data['host'], data['user'], data['passwd'],
               f'cd {data["folder_in"]}; mkdir {subfoldername}', ''):
        return [None, None]
    if not che(data['host'], data['user'], data['passwd'],
               f'cd {data["folder_in"]}/{subfoldername}; dd if=/dev/urandom of={testfilename} bs={data["bs"]} count=1 iflag=fullblock',
               ''):
        return [subfoldername, None]
    return [subfoldername, testfilename]


@pytest.fixture(autouse=True)
def print_time():
    print(f'Start test: {datetime.now().strftime("%H:%M:%S.%f")}')
    yield
    print(f'End test: {datetime.now().strftime("%H:%M:%S.%f")}')


@pytest.fixture()
def make_bad_arx():
    che(data['host'], data['user'], data['passwd'],
        f'cd {data["folder_in"]}; 7z a {data["folder_bad_out"]}/{bad_arx} -t{data["type"]}', OK)
    che(data['host'], data['user'], data['passwd'],
        f'truncate -s 1 {data["folder_bad_out"]}/{bad_arx}.{data["type"]}', OK)
    # yield
    # che(f'rm -f {data["folder_bad_out"]}/{bad_arx}.{data["type"]}', '')


@pytest.fixture()
def start_time():
    return datetime.now().strftime('%y-%m-%d %H:%M:%S')


def save_log(time, file_name):
    log = ssh_getout(data['host'], data['user'], data['passwd'],
                     f'journal --since={time}')
    with open(file_name, 'w', encoding='utf-8') as f:
        f.writelines(log)
    return True
