from dark_cai_hong_pi.DarkCaiHongPi import dark_cai_hong_pi
from dark_chat.dark_jikipedia.DarkJiWordCloud import dark_ji_word_cloud
from dark_chat.dark_jikipedia.DarkJikipedia import dark_jikipedia
from dark_chat.zuan_chat.ZuAnChat import zuan_chat
from dark_guess_number.DarkGuessNumber import dark_guess_number
from dark_maze.DarkMaze import dark_maze
from dark_quiz.DarkQuiz import dark_quiz
from dark_show_hand.DarkShowHand import dark_show_hand
from dark_spy.DarkSpy import dark_spy
from dark_word_cloud.DarkWordCloud import dark_word_cloud
from juhe_api.JuheApi import juhe_api
from user.login.User_login import user_login
from user.ren_she.RenShe import ren_she_handler

# 菜单配置
# key:菜单项
# value:
#   |_path: 路径，机器人的可执行指令，可以定位到此
#   |hidden: 是否在菜单中隐藏
#   |children: 子菜单项，同父结构

default_menu = {
    '人设': {
        'path': '**人设',
        'children': {
            '显示': {
                'path': '**人设:显示',
                'children': ren_she_handler
            },
            '增加': {
                'path': '**人设:增加',
                'children': ren_she_handler
            }
        }
    },
    '骚词': {
        'path': '**骚词',
        'children': {
            '推荐': {
                'path': '**骚词:推荐',
                'children': dark_jikipedia
            }
        }
    },
    '词云': {
        'path': '**词云',
        'children': {
            '暗黑热搜': {
                'path': '**词云:暗黑热搜',
                'children': dark_word_cloud
            },
            '小鸡骚词': {
                'path': '**词云:小鸡骚词',
                'children': dark_ji_word_cloud
            }
        }
    },
    '注册': {
        'path': '**注册',
        'children': user_login
    },
    '祖安': {
        'path': '**祖安',
        'children': zuan_chat
    },
    '游戏': {
        'path': '**游戏',
        'children': {
            '迷宫': {
                'path': '**游戏:迷宫',
                'children': {
                    '开启': {
                        'path': '**游戏:迷宫:开启',
                        'children': dark_maze
                    },
                    '关闭': {
                        'path': '**游戏:迷宫:关闭',
                        'children': dark_maze
                    },
                    '行动': {
                        'path': '**游戏:迷宫:行动',
                        'children': dark_maze,
                        'hidden': True
                    }
                }
            },
            '谁是卧底': {
                'path': '**游戏:谁是卧底',
                'children': {
                    '开启': {
                        'path': '**游戏:谁是卧底:开启',
                        'children': dark_spy
                    },
                    '关闭': {
                        'path': '**游戏:谁是卧底:关闭',
                        'children': dark_spy
                    },
                    '调试': {
                        'path': '**游戏:谁是卧底:调试',
                        'children': {
                            '个人信息': {
                                'path': '**游戏:谁是卧底:调试:个人信息',
                                'children': dark_spy
                            },
                            '参加': {
                                'path': '**游戏:谁是卧底:调试:参加',
                                'children': dark_spy
                            },
                            '开始': {
                                'path': '**游戏:谁是卧底:调试:开始',
                                'children': dark_spy
                            },
                            '投票': {
                                'path': '**游戏:谁是卧底:调试:投票',
                                'children': dark_spy
                            }
                        },
                        'hidden': True
                    }
                }
            },
            '猜数字': {
                'path': '**游戏:猜数字',
                'children': {
                    '开启': {
                        'path': '**游戏:猜数字:开启',
                        'children': dark_guess_number
                    },
                    '关闭': {
                        'path': '**游戏:猜数字:关闭',
                        'children': dark_guess_number
                    },
                    '猜': {
                        'path': '**游戏:猜数字:猜',
                        'children': dark_guess_number,
                        'hidden': True
                    }
                }
            },
            '暗黑答题': {
                'path': '**游戏:暗黑答题',
                'children': {
                    '是非题(10金币)': {
                        'path': '**游戏:暗黑答题:是非题(10金币)',
                        'children': dark_quiz
                    },
                    '单选题(20金币)': {
                        'path': '**游戏:暗黑答题:单选题(20金币)',
                        'children': dark_quiz
                    },
                    '答题': {
                        'path': '**游戏:暗黑答题:答题',
                        'children': dark_quiz,
                        'hidden': True
                    }
                }
            },
            '暗黑梭哈': {
                'path': '**游戏:暗黑梭哈',
                'children': {
                    '来一把': {
                        'path': '**游戏:暗黑梭哈:来一把',
                        'children': dark_show_hand
                    },
                    '掀桌子': {
                        'path': '**游戏:暗黑梭哈:掀桌子',
                        'children': dark_show_hand
                    },
                    '操作': {
                        'path': '**游戏:暗黑梭哈:操作',
                        'children': dark_show_hand,
                        'hidden': True
                    }
                }
            }
        }
    },
    '小功能': {
        'path': '**小功能',
        'children': {
            '笑话': {
                'path': '**小功能:笑话',
                'children': juhe_api
            },
            '新闻': {
                'path': '**小功能:新闻',
                'children': juhe_api
            },
            '骚东西': {
                'path': '**小功能:骚东西',
                'children': juhe_api
            },
            '今日黄历': {
                'path': '**小功能:今日黄历',
                'children': juhe_api
            },
            '动图': {
                'path': '**小功能:动图',
                'children': juhe_api
            },
            '今天': {
                'path': '**小功能:今天',
                'children': juhe_api
            },
            '土味情话': {
                'path': '**小功能:土味情话',
                'children': juhe_api
            },
            '远哥语录': {
                'path': '**小功能:远哥语录',
                'children': dark_cai_hong_pi
            },
            '孟婆汤': {
                'path': '**小功能:孟婆汤',
                'children': juhe_api
            },
            '取名': {
                'path': '**小功能:取名',
                'children': juhe_api
            }
        }
    }

}

live_chat_menu = {
    '骚词': {
        'path': '**骚词',
        'children': {
            '推荐': {
                'path': '**骚词:推荐',
                'children': dark_jikipedia
            }
        }
    },
    '词云': {
        'path': '**词云',
        'children': {
            '小鸡骚词': {
                'path': '**词云:小鸡骚词',
                'children': dark_ji_word_cloud
            }
        }
    },
    '祖安': {
        'path': '**祖安',
        'children': zuan_chat
    },
    '游戏': {
        'path': '**游戏',
        'children': {
            '迷宫': {
                'path': '**游戏:迷宫',
                'children': {
                    '开启': {
                        'path': '**游戏:迷宫:开启',
                        'children': dark_maze
                    },
                    '关闭': {
                        'path': '**游戏:迷宫:关闭',
                        'children': dark_maze
                    },
                    '行动': {
                        'path': '**游戏:迷宫:行动',
                        'children': dark_maze,
                        'hidden': True
                    }
                }
            },
            '猜数字': {
                'path': '**游戏:猜数字',
                'children': {
                    '开启': {
                        'path': '**游戏:猜数字:开启',
                        'children': dark_guess_number
                    },
                    '关闭': {
                        'path': '**游戏:猜数字:关闭',
                        'children': dark_guess_number
                    },
                    '猜': {
                        'path': '**游戏:猜数字:猜',
                        'children': dark_guess_number,
                        'hidden': True
                    }
                }
            },
            '暗黑答题': {
                'path': '**游戏:暗黑答题',
                'children': {
                    '是非题(10金币)': {
                        'path': '**游戏:暗黑答题:是非题(10金币)',
                        'children': dark_quiz
                    },
                    '单选题(20金币)': {
                        'path': '**游戏:暗黑答题:单选题(20金币)',
                        'children': dark_quiz
                    },
                    '答题': {
                        'path': '**游戏:暗黑答题:答题',
                        'children': dark_quiz,
                        'hidden': True
                    }
                }
            },
            '暗黑梭哈': {
                'path': '**游戏:暗黑梭哈',
                'children': {
                    '来一把': {
                        'path': '**游戏:暗黑梭哈:来一把',
                        'children': dark_show_hand
                    },
                    '掀桌子': {
                        'path': '**游戏:暗黑梭哈:掀桌子',
                        'children': dark_show_hand
                    },
                    '操作': {
                        'path': '**游戏:暗黑梭哈:操作',
                        'children': dark_show_hand,
                        'hidden': True
                    }
                }
            }
        }
    },
    '小功能': {
        'path': '**小功能',
        'children': {
            '笑话': {
                'path': '**小功能:笑话',
                'children': juhe_api
            },
            '新闻': {
                'path': '**小功能:新闻',
                'children': juhe_api
            },
            '骚东西': {
                'path': '**小功能:骚东西',
                'children': juhe_api
            },
            '动图': {
                'path': '**小功能:动图',
                'children': juhe_api
            },
            '今天': {
                'path': '**小功能:今天',
                'children': juhe_api
            },
            '土味情话': {
                'path': '**小功能:土味情话',
                'children': juhe_api
            },
            '孟婆汤': {
                'path': '**小功能:孟婆汤',
                'children': juhe_api
            },
        }
    }
}
