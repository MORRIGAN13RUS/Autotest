import pytest
import yaml
from ssh_checkers import ssh_checkout_negative as ssh_nche

with open('ssh_config.yaml', 'r') as f:
    data = yaml.safe_load(f)

bad_arx = 'bad_arx'
bad_type = 'txt'
ERR = 'ERROR'


def test_negative_step1(make_folders, clear_folders, make_files, make_bad_arx):
    # test1
    res = ssh_nche(data['host'], data['user'], data['passwd'],
                   f'cd {data["folder_bad_out"]}; 7z e {bad_arx}.{data["type"]} -o{data["folder_ext"]} -y', ERR)
    assert res, 'test1 FAIL'


def test_negative_step2(clear_folders, make_files, make_bad_arx):
    # test2
    res = ssh_nche(data['host'], data['user'], data['passwd'],
                   f'cd {data["folder_bad_out"]}; 7z t {bad_arx}.{data["type"]}', ERR)
    assert res, 'test2 FAIL'


def test_negative_step3(clear_folders, make_files):
    # test3
    res = ssh_nche(data['host'], data['user'], data['passwd'],
                   f'cd {data["folder_in"]}; 7z a {data["folder_bad_out"]}/{bad_arx} -t{bad_type}', ERR)
    assert res, 'test3 FAIL'
