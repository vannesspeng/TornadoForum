#!/usr/bin/env python
#-*- coding:utf-8 -*-
# author:pyy
# datetime:2019/1/9 9:55
import functools

import jwt

from Myforum.Forum.settings import settings
from Myforum.apps.users.models import User


def authenticated_async(method):

    @functools.wraps(method)
    async def wrapper(self, *args, **kwargs):
        # 获取前端携带的JWT token
        tsessionid = self.request.headers["tsessionid"]
        # 解析JWT token
        if tsessionid:
            # 校验tsessionid
            """
                def decode(self,
                       jwt,  # type: str
                       key='',   # type: str
                       verify=True,  # type: bool
                       algorithms=None,  # type: List[str]
                       options=None,  # type: Dict
                       **kwargs):
            """
            try:
                send_data = jwt.decode(
                    tsessionid,
                    key=settings['secret_key'],
                    algorithms=['HS256'],
                    leeway=self.settings["jwt_expire"],
                    options={"verify_exp ": "True"}
                )
                user_id = send_data['id']
                # 从数据库中取出对应的User对象
                try:
                    user = await self.application.objects.get(User, id=user_id)
                    self._current_user = user

                    #此处很关键, 这里的method是一个协程方法，返回协程方法的时候不能使用return，要用await
                    await method(self, *args, **kwargs)
                except User.DoesNotExist as e:
                    self.set_status(401)
            except jwt.ExpiredSignatureError as e:
                self.set_status(401)
        else:
            self.set_status(401)
    return wrapper