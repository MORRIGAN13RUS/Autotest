import pytest
import yaml
from ssh_checkers import ssh_checkout
from ssh_checkers import ssh_getout
from ssh_checkers import upload_files
from conftest import save_log as log

with open('ssh_config.yaml', 'r') as f:
    data = yaml.safe_load(f)

arx = 'arx'
OK = 'Everything is Ok'


def test_positive_step0():
    res = []
    upload_files(data['host'], data['user'], data['passwd'],
                 f'{data["local_path"]}/p7zip-full.deb', f'{data["remote_path"]}/p7zip-full.deb')
    res.append(ssh_checkout(data['host'], data['user'], data['passwd'],
                            f'echo {data["passwd"]} | sudo -S dpkg -i {data["remote_path"]}/p7zip-full.deb',
                            'Настраивается пакет‚'))
    res.append(ssh_checkout(data['host'], data['user'], data['passwd'],
                            f'echo {data["passwd"]} | sudo -S dpkg -s p7zip-full',
                            'Status: install ok installed'))
    assert all(res), 'test0 FAIL'


def test_positive_step1(make_folders, clear_folders, make_files):
    # test1
    res = []
    res.append(ssh_checkout(data['host'], data['user'], data['passwd'],
                            f'cd {data["folder_in"]}; 7z a {data["folder_out"]}/{arx} -t{data["type"]}', OK))
    res.append(ssh_checkout(data['host'], data['user'], data['passwd'],
                            f'ls {data["folder_out"]}', f'{arx}.{data["type"]}'))
    assert all(res), 'rest1 FAIL'


def test_positive_step2(clear_folders, make_files):
    # test2
    res = []
    res.append(ssh_checkout(data['host'], data['user'], data['passwd'],
                            f'cd {data["folder_in"]}; 7z a {data["folder_out"]}/{arx} -t{data["type"]}', OK))
    res.append(ssh_checkout(data['host'], data['user'], data['passwd'],
                            f'cd {data["folder_out"]}; 7z e {arx}.{data["type"]} -o{data["folder_ext"]} -y', OK))
    for file_name in make_files:
        res.append(ssh_checkout(data['host'], data['user'], data['passwd'],
                                f'ls {data["folder_ext"]}', file_name))
    assert all(res), 'test2 FAIL'


def test_positive_step3(clear_folders, make_files):
    # test3
    res = []
    res.append(ssh_checkout(data['host'], data['user'], data['passwd'],
                            f'cd {data["folder_in"]}; 7z a {data["folder_out"]}/{arx} -t{data["type"]}', OK))
    res.append(ssh_checkout(data['host'], data['user'], data['passwd'],
                            f'cd {data["folder_out"]}; 7z t {arx}.{data["type"]}', OK))
    assert all(res), 'test3 FAIL'


def test_positive_step4():
    # test4
    assert ssh_checkout(data['host'], data['user'], data['passwd'],
                        f'cd {data["folder_out"]}; 7z d {arx}.{data["type"]}', OK), 'test4 FAIL'


def test_positive_step5():
    # test5
    assert ssh_checkout(data['host'], data['user'], data['passwd'],
                        f'cd {data["folder_in"]}; 7z u {data["folder_out"]}/{arx}.{data["type"]}', OK), 'test5 FAIL'


def test_positive_step6(clear_folders, make_files, make_subfolder):
    # test6
    res = []
    res.append(ssh_checkout(data['host'], data['user'], data['passwd'],
                            f'cd {data["folder_in"]}; 7z a {data["folder_out"]}/{arx} -t{data["type"]}', OK))
    res.append(ssh_checkout(data['host'], data['user'], data['passwd'],
                            f'cd {data["folder_out"]}; 7z x {arx}.{data["type"]} -o{data["folder_ext2"]} -y', OK))
    for file_name in make_files:
        res.append(ssh_checkout(data['host'], data['user'], data['passwd'],
                                f'ls {data["folder_ext2"]}', file_name))
    res.append(ssh_checkout(data['host'], data['user'], data['passwd'],
                            f'ls {data["folder_ext2"]}', make_subfolder[0]))
    res.append(ssh_checkout(data['host'], data['user'], data['passwd'],
                            f'ls {data["folder_ext2"]}/{make_subfolder[0]}', make_subfolder[1]))
    assert all(res), 'test6 FAIL'


def test_positive_step7(clear_folders, make_files):
    # test7
    res = []
    res.append(ssh_checkout(data['host'], data['user'], data['passwd'],
                            f'cd {data["folder_in"]}; 7z a {data["folder_out"]}/{arx} -t{data["type"]}', OK))
    for file_name in make_files:
        res.append(ssh_checkout(data['host'], data['user'], data['passwd'],
                                f'7z l {data["folder_out"]}/{arx}.{data["type"]}', file_name))
    assert all(res), 'test7 FAIL'


def test_positive_step8(clear_folders, make_files):
    # test8
    res = []
    for file_name in make_files:
        res.append(ssh_checkout(data['host'], data['user'], data['passwd'],
                                f'cd {data["folder_in"]}; 7z h {file_name}', OK))
        file_hash = ssh_getout(data['host'], data['user'], data['passwd'],
                               f'cd {data["folder_in"]}; crc32 {file_name}').upper()
        res.append(ssh_checkout(data['host'], data['user'], data['passwd'],
                                f'cd {data["folder_in"]}; 7z h {file_name}', file_hash))
    assert all(res), 'test8 FAIL'