from .requester import test_route
from colorama import init, Fore, Back, Style
import os
from .config import cfg


def test_accounts():
    tests = [
    {'description': 'LOGIN with incorrect email',
                    'url': '/login',
                    'method': 'post',
                    'data': {"email": "root", "password": "1234"},
                    'valid_code': '<Response [404]>',
                    'valid_data': {'error': 'Invalid user'},
                    'need_decision': False,
                    'cookie': 'none',
                    'get_cookie': False
    },
    {'description': 'LOGIN with incorrect password',
                    'url': '/login',
                    'method': 'post',
                    'data': {"email": cfg.SUPER_ADMIN_MAIL, "password": "123456789"},
                    'valid_code': '<Response [422]>',
                    'valid_data': {'error': 'Invalid password'},
                    'need_decision': False,
                    'cookie': 'none',
                    'get_cookie': False
    },
    {'description': 'LOGIN with incorrect keys',
                    'url': '/login',
                    'method': 'post',
                    'data': {"mail": cfg.SUPER_ADMIN_MAIL, "password": "1234"},
                    'valid_code': '<Response [400]>',
                    'valid_data': {'error': 'Wrong json key(s)'},
                    'need_decision': False,
                    'cookie': 'none',
                    'get_cookie': False
    },
    {'description': 'LOGIN correct',
                    'url': '/login',
                    'method': 'post',
                    'data': {"email": cfg.SUPER_ADMIN_MAIL, "password": "1234"},
                    'valid_code': '<Response [200]>',
                    'valid_data': {'description': 'User was logined', 'name': 'Super', 'surname': 'Admin'},
                    'need_decision': False,
                    'cookie': 'none',
                    'get_cookie': True,
                    'to_cookie': 'admin'
    },
    {'description': 'GET CURRENT USER STATUS',
                    'url': '/status',
                    'method': 'get',
                    'data': {},
                    'valid_code': '<Response [200]>',
                    'valid_data': {'service_status': 'superadmin'},
                    'need_decision': False,
                    'cookie': 'admin',
                    'get_cookie': False
    },
    {'description': 'LOGIN repeat correct',
                    'url': '/login',
                    'method': 'post',
                    'data': {"email": cfg.SUPER_ADMIN_MAIL, "password": "1234"},
                    'valid_code': '<Response [409]>',
                    'valid_data': {'error': 'User is currently authenticated'},
                    'need_decision': False,
                    'cookie': 'admin',
                    'get_cookie': False
    },
    {'description': 'LOGOUT correct',
                    'url': '/logout',
                    'method': 'get',
                    'data': {},
                    'valid_code': '<Response [200]>',
                    'valid_data': {'description': 'User was logouted'},
                    'need_decision': False,
                    'cookie': 'admin',
                    'get_cookie': False
    },
    {'description': 'REGISTER correct',
                    'url': '/register',
                    'method': 'post',
                    'data': {"email": "mail@mail.mail", "name": "naaaaaaaame", "surname": "surnaaaaaaaame", "password": "1234"},
                    'valid_code': '<Response [201]>',
                    'valid_data': {'description': 'User was registered'},
                    'need_decision': False,
                    'cookie': 'none',
                    'get_cookie': False
    },
    {'description': 'REGISTER user exists',
                    'url': '/register',
                    'method': 'post',
                    'data': {"email": cfg.SUPER_ADMIN_MAIL, "name": "naaaaaaaame", "surname": "surnaaaaaaaame", "password": "1234"},
                    'valid_code': '<Response [409]>',
                    'valid_data': {'error': 'Trying to register existing user'},
                    'need_decision': False,
                    'cookie': 'none',
                    'get_cookie': False
    },
    {'description': 'REGISTER then login',
                    'url': '/register',
                    'method': 'post',
                    'data': {"email": cfg.SUPER_ADMIN_MAIL, "password": "1234"},
                    'valid_code': '<Response [409]>',
                    'valid_data': {'error': 'User is currently authenticated'},
                    'need_decision': False,
                    'cookie': 'admin',
                    'get_cookie': False
    },
    {'description': 'LOGIN mail@mail.mail',
                    'url': '/login',
                    'method': 'post',
                    'data': {"email": "mail@mail.mail", "password": "1234"},
                    'valid_code': '<Response [200]>',
                    'valid_data': {'description': 'User was logined', 'name': 'naaaaaaaame', 'surname': 'surnaaaaaaaame'},
                    'need_decision': False,
                    'cookie': 'none',
                    'get_cookie': True,
                    'to_cookie': 'user'
    },
    {'description': 'CHANGE PASSWORD incorrect old password',
                    'url': '/change_password',
                    'method': 'post',
                    'data': {"old_password": "12345", "new_password": "12345678"},
                    'valid_code': '<Response [422]>',
                    'valid_data': {'error': 'Invalid password'},
                    'need_decision': False,
                    'cookie': 'user',
                    'get_cookie': False
    },
    {'description': 'CHANGE PASSWORD correct',
                    'url': '/change_password',
                    'method': 'post',
                    'data': {"old_password": "1234", "new_password": "12345678"},
                    'valid_code': '<Response [200]>',
                    'valid_data': {'description': 'Password has beed changed'},
                    'need_decision': False,
                    'cookie': 'user',
                    'get_cookie': True,
                    'to_cookie': 'tmp'
    },
    {'description': 'CHANGE PASSWORD old cookie try',
                    'url': '/change_password',
                    'method': 'post',
                    'data': {"old_password": "12345678", "new_password": "1234567890"},
                    'valid_code': '<Response [401]>',
                    'valid_data': {'error': 'Unauthorized'},
                    'need_decision': False,
                    'cookie': 'user',
                    'get_cookie': False
    },
    {'description': 'CHANGE PASSWORD correct with new cookies',
                    'url': '/change_password',
                    'method': 'post',
                    'data': {"old_password": "12345678", "new_password": "1234"},
                    'valid_code': '<Response [200]>',
                    'valid_data': {'description': 'Password has beed changed'},
                    'need_decision': False,
                    'cookie': 'tmp',
                    'get_cookie': True,
                    'to_cookie': 'user'
    },
    {'description': 'CLOSE ALL SESSIONS correct',
                    'url': '/close_all_sessions',
                    'method': 'post',
                    'data': {"password": "1234"},
                    'valid_code': '<Response [200]>',
                    'valid_data': {'description': 'Logout from all other sessions'},
                    'need_decision': False,
                    'cookie': 'user',
                    'get_cookie': True,
                    'to_cookie': 'user'
    },
    {'description': 'SELF DELETE correct',
                    'url': '/delete',
                    'method': 'post',
                    'data': {"password": "1234"},
                    'valid_code': '<Response [200]>',
                    'valid_data': {'description': 'Successfully delete account'},
                    'need_decision': False,
                    'cookie': 'user',
                    'get_cookie': False
    },
    {'description': 'LOGIN REQUIRED ROUTE AFTER SELF DELETE',
                    'url': '/change_password',
                    'method': 'post',
                    'data': {"old_password": "12345678", "new_password": "1234567890"},
                    'valid_code': '<Response [401]>',
                    'valid_data': {'error': 'Unauthorized'},
                    'need_decision': False,
                    'cookie': 'user',
                    'get_cookie': False
    },
    {'description': 'LOGIN AFTER SELF DELETE',
                    'url': '/login',
                    'method': 'post',
                    'data': {"email": "mail@mail.mail", "password": "1234"},
                    'valid_code': '<Response [404]>', # move to 409 deleted
                    'valid_data': {'error': 'Invalid user'},
                    'need_decision': False,
                    'cookie': 'none',
                    'get_cookie': False
    },
    {'description': 'REGISTER AFTER SELF DELETE',
                    'url': '/register',
                    'method': 'post',
                    'data': {"email": "mail@mail.mail", "name": "name", "surname": "surname", "password": "1234"},
                    'valid_code': '<Response [201]>',
                    'valid_data': {'description': 'User was registered'},
                    'need_decision': False,
                    'cookie': 'none',
                    'get_cookie': False
    },
    {'description': 'LOGIN AFTER SELF DELETE AND REREGISTERING',
                    'url': '/login',
                    'method': 'post',
                    'data': {"email": "mail@mail.mail", "password": "1234"},
                    'valid_code': '<Response [200]>',
                    'valid_data': {'description': 'User was logined', 'name': 'name', 'surname': 'surname'},
                    'need_decision': False,
                    'cookie': 'none',
                    'get_cookie': True,
                    'to_cookie': 'user'
    },
    {'description': 'USER BAN USER',
                    'url': '/user/2/ban',
                    'method': 'get',
                    'data': {},
                    'valid_code': '<Response [403]>',
                    'valid_data':  {'error': 'No rights'},
                    'need_decision': False,
                    'cookie': 'user',
                    'get_cookie': False
    },
    {'description': 'ADMIN BAN 404 USER',
                    'url': '/user/10/ban',
                    'method': 'get',
                    'data': {},
                    'valid_code': '<Response [404]>',
                    'valid_data':  {'error': 'No user with this id'},
                    'need_decision': False,
                    'cookie': 'admin',
                    'get_cookie': False
    },
    {'description': 'ADMIN BAN USER',
                    'url': '/user/2/ban',
                    'method': 'get',
                    'data': {},
                    'valid_code': '<Response [200]>',
                    'valid_data':  {'description': 'Successfully baned this user'},
                    'need_decision': False,
                    'cookie': 'admin',
                    'get_cookie': False
    },
    {'description': 'LOGIN BANNED USER',
                    'url': '/login',
                    'method': 'post',
                    'data': {"email": "mail@mail.mail", "password": "1234"},
                    'valid_code': '<Response [409]>',
                    'valid_data': {'error': 'Trying to login banned user'},
                    'need_decision': False,
                    'cookie': 'none',
                    'get_cookie': False
    },
    {'description': 'REGISTER BANNED USER',
                    'url': '/register',
                    'method': 'post',
                    'data': {"email": "mail@mail.mail", "name": "name", "surname": "surname", "password": "1234"},
                    'valid_code': '<Response [409]>',
                    'valid_data':  {'error': 'User with this email was banned'},
                    'need_decision': False,
                    'cookie': 'none',
                    'get_cookie': False
    },
    {'description': 'REGISTER new user correct',
                    'url': '/register',
                    'method': 'post',
                    'data': {"email": "mail@mail", "name": "Name", "surname": "Surname", "password": "1234"},
                    'valid_code': '<Response [201]>',
                    'valid_data':  {'description': 'User was registered'},
                    'need_decision': False,
                    'cookie': 'none',
                    'get_cookie': False
    },
    {'description': 'LOGIN new user correct',
                    'url': '/login',
                    'method': 'post',
                    'data': {"email": "mail@mail", "password": "1234"},
                    'valid_code': '<Response [200]>',
                    'valid_data':  {'description': 'User was logined', 'name': 'Name', 'surname': 'Surname'},
                    'need_decision': False,
                    'cookie': 'none',
                    'get_cookie': True,
                    'to_cookie': 'user'
    },
    {'description': 'User try to change privileges',
                    'url': '/user/1/role/moderator',
                    'method': 'get',
                    'data': {},
                    'valid_code': '<Response [403]>',
                    'valid_data':  {'error': 'No rights'},
                    'need_decision': False,
                    'cookie': 'user',
                    'get_cookie': False
    },
    {'description': 'Admin try to change privileges no user',
                    'url': '/user/10/role/moderator',
                    'method': 'get',
                    'data': {},
                    'valid_code': '<Response [404]>',
                    'valid_data':  {'error': 'No user with this id'},
                    'need_decision': False,
                    'cookie': 'admin',
                    'get_cookie': False
    },
    {'description': 'Admin change privileges',
                    'url': '/user/3/role/admin',
                    'method': 'get',
                    'data': {},
                    'valid_code': '<Response [200]>',
                    'valid_data':  {'description': 'Successfully changed privilegy of user'},
                    'need_decision': False,
                    'cookie': 'admin',
                    'get_cookie': False
    },
    {'description': 'GET CURRENT USER NEW STATUS',
                    'url': '/status',
                    'method': 'get',
                    'data': {},
                    'valid_code': '<Response [200]>',
                    'valid_data': {'service_status': 'admin'},
                    'need_decision': False,
                    'cookie': 'user',
                    'get_cookie': False
    },
    {'description': 'User become moder try to change admin',
                    'url': '/user/1/role/moderator',
                    'method': 'get',
                    'data': {},
                    'valid_code': '<Response [404]>',
                    'valid_data':  {'error': 'No user with this id'},
                    'need_decision': False,
                    'cookie': 'user',
                    'get_cookie': False
    },
    {'description': 'Admin change privileges to user',
                    'url': '/user/3/role/user',
                    'method': 'get',
                    'data': {},
                    'valid_code': '<Response [200]>',
                    'valid_data':  {'description': 'Successfully changed privilegy of user'},
                    'need_decision': False,
                    'cookie': 'admin',
                    'get_cookie': False
    },
    {'description': 'GET CURRENT USER NEW NEW STATUS',
                    'url': '/status',
                    'method': 'get',
                    'data': {},
                    'valid_code': '<Response [200]>',
                    'valid_data': {'service_status': 'user'},
                    'need_decision': False,
                    'cookie': 'user',
                    'get_cookie': False
    },
    ]

    cookies = {'admin': '',
               'user': '',
               'tmp': '',
               'none': ''
    }

    i = 0
    code_passed = 0
    data_passed = 0

    print(Fore.BLACK + Back.WHITE + '=========================( TESTS ACCOUNT )=========================' + Style.RESET_ALL)
    print()

    for test in tests:
        if test['get_cookie']:
            i, code_passed, data_passed, cookies[test['to_cookie']] = test_route(i, code_passed, data_passed,
                                                                    test['description'],
                                                                    test['url'],
                                                                    test['method'],
                                                                    test['data'],
                                                                    test['valid_code'],
                                                                    test['valid_data'],
                                                                    test['need_decision'],
                                                                    cookies[test['cookie']],
                                                                    test['get_cookie']
            )
        else:
            i, code_passed, data_passed = test_route(i, code_passed, data_passed,
                                                                    test['description'],
                                                                    test['url'],
                                                                    test['method'],
                                                                    test['data'],
                                                                    test['valid_code'],
                                                                    test['valid_data'],
                                                                    test['need_decision'],
                                                                    cookies[test['cookie']],
                                                                    test['get_cookie']
            )

    print(Fore.BLACK + Back.WHITE + '=====================( TESTS ACCOUNT FINISHED )====================' + Style.RESET_ALL)
    print('TESTS: ' + str(i))
    print('CODE:' + "      " + Back.GREEN + 'passed: ' + str(code_passed) + Style.RESET_ALL + "      " + Back.RED + 'failed: ' + str(i - code_passed) + Style.RESET_ALL)
    print('DATA:' + "      " + Back.GREEN + 'passed: ' + str(data_passed) + Style.RESET_ALL + "      " + Back.RED + 'failed: ' + str(i - data_passed) + Style.RESET_ALL)
    print()

    return i, code_passed, data_passed, cookies