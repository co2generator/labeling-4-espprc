# **********************************************************
# * Author        : CO2MAKER
# * Email         : 429401330@qq.com
# * Create time   : 2023/1/16 10:53 AM
# * Filename      : ORException
# * Description   :
# **********************************************************

class NotEqual(Exception):

    """Class for not equal exception."""

    def __init__(self, msg: str):
        self.msg = msg

    def __str__(self):
        return self.msg
