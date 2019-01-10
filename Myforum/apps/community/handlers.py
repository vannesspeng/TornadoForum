#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:pyy
# datetime:2018/12/28 15:30
import os
import uuid

import aiofiles
import jwt
from tornado.web import authenticated

from Myforum.Forum.handlers import BaseHandler
from Myforum.Forum.settings import settings
from Myforum.apps.community.forms import CommunityGroupForm
from Myforum.apps.community.models import CommunityGroup
from Myforum.apps.utils.decorators import authenticated_async



class GroupHandler(BaseHandler):
    async def get(self, *args, **kwargs):
        re_data = {}
        pass

    @authenticated_async
    async def post(self, *args, **kwargs):
        re_data = {}
        # 这里不能使用form.form_json()方法，因为这个参数里面包含文件参数
        group_form = CommunityGroupForm(self.request.body_arguments)
        new_filename = ""
        if group_form.validate():
            # 获取文件名，生成新的文件名，并将保存的图片文件的完整路径存入到数据库
            files_meta = self.request.files.get("front_image", None)
            if not files_meta:
                self.set_status(400)
                re_data["front_image"] = "请上传图片"
            else:
                for meta in files_meta:
                    file_name = meta["filename"]
                    new_filename = "{uuid}_{filename}".format(uuid=uuid.uuid1(), filename=file_name)
                    file_path = os.path.join(settings['MEDIA_ROOT'], new_filename)
                    async with aiofiles.open(file_path, 'wb') as f:
                        await f.write(meta['body'])
                group = await self.application.objects.create(CommunityGroup,
                                                        creator=self.current_user,
                                                        category=group_form.category.data,
                                                        desc=group_form.desc.data,
                                                        notice=group_form.notice.data,
                                                        front_image=new_filename)
                re_data["id"] = group.id
        else:
            self.set_status(400)
            for field in group_form.errors:
                re_data['field'] = group_form.errors[field][0]
        self.finish(re_data)

