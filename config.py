servers = {
        'freenode': dict (
            encoding='utf8',
            host='irc.freenode.net', port=6667,
            nickname='lalita',
            channels= {
                '#not-grulic': dict (plugins={}),
            },
            plugins= {
                'register.Register': { 'password': 'zaraza' },
            },
        ),
        'perrito':{
            'encoding': 'utf8',
            'host' : "10.100.0.156",
            'port' : 6667,
            'nickname' : "morelia",
            'channels':{
                'humites':{
                    '#plugins':{
                        'url.Url': dict (
                            database= 'url_public',
                        )
                    },
                    'encoding': 'utf8',
                    },
                'perrites':{
                    'encoding': 'utf8',
                    '#plugins':{
                        'url.Url': dict (
                            database= 'url_perrites_private',
                        )
                    },
                    },
                },
            'plugins':{
                'url.Url': dict (
                    database= 'url_public',
                )
                }
            },
        'testbot-a':{
            'encoding': 'utf8',
            'host' : "10.100.0.175",
            'port' : 6667,
            'nickname' : "itchy",
            'channels':{
                '#humites':{
                    'plugins': {}
                    },
                },
            'plugins':{
                'testbot.TestPlugin': {'other': 'scratchy'}
                },
            'plugins_dir': "./core/tests/plugins",
            },
        'testbot-b':{
            'encoding': 'utf8',
            'host' : "10.100.0.175",
            'port' : 6667,
            'nickname' : "scratchy",
            'channels':{
                '#humites':{
                    'plugins': {}
                    },
                },
            'plugins':{
                'testbot.TestPlugin': {'other':'itchy'}
                },
            'plugins_dir': "./core/tests/plugins",
            },
        'perrito1':{
            'encoding': 'utf8',
            'host' : "10.100.0.194",
            'port' : 6668,
            'nickname' : "lolita",
                'channels':{
                    '#humites':{
                        'plugins':{ 'Log':{} },
                        'encoding': 'utf8',
                        },
                    '#perrites':{
                        'plugins':{ 'Log':{} }
                        }
                    },
                'plugins':{
                    'Log': {}
                    }
                },
        'javito':{
            'encoding': 'utf8',
            'host' : "10.100.0.175",
            'port' : 6667,
            'nickname' : "manyula",
            'channels':{
                '#humites':{
                    'plugins':{ 'Log':{} , 'moin_search.MoinSearch': {'fruta': 'banana'}},
                    'encoding': 'utf8',
                    },
                '#perrites':{
                    'plugins':{ 'Log':{'arbol':5} },
                    'encoding': 'utf8',
                    }
                },
            'plugins':{
                    'Log': {}
                    }
                }
        }
