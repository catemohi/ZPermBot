from aiogram.dispatcher.filters import BoundFilter
from aiogram import types
from sheets import s



class AdminFilter(BoundFilter):
    key = 'is_admin'

    def __init__(self, is_admin):
        self.isin = is_admin

    async def check(self, message: types.Message):
        return s.admin_list(str(message.from_user.id))


class NotUserFilter(BoundFilter):
    key = 'is_not_user'

    def __init__(self, is_not_user):
        self.isin = is_not_user

    async def check(self, message: types.Message):
        return not str(message.from_user.id) in s.get_append_id()