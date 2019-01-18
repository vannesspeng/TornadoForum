#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:pyy
# datetime:2018/12/28 15:30
import json
import os
import uuid

import aiofiles
from playhouse.shortcuts import model_to_dict

from Myforum.Forum.handlers import BaseHandler
from Myforum.Forum.settings import settings
from Myforum.apps.community.forms import CommunityGroupForm, GroupApplyForm
from Myforum.apps.community.models import CommunityGroup, CommunityGroupMember
from Myforum.apps.utils.decorators import authenticated_async
from Myforum.apps.utils.util_func import json_serial


class GroupHandler(BaseHandler):
    async def get(self, *args, **kwargs):
        re_data = []
        # 先获取所有的小组
        # 这里解释一下为什么不直接使用CommunityGroup.select()，因为
        community_query = CommunityGroup.extend()

        # 根据分类进行过滤
        c = self.get_argument("c", None)
        if c:
            community_query = community_query.filter(CommunityGroup.category==c)

        # 根据参数进行排序
        order = self.get_argument("o", None)
        if order:
            if order == "new":
                community_query = community_query.order_by(CommunityGroup.add_time.desc())
            elif order == "hot":
                community_query = community_query.order_by(CommunityGroup.member_nums.desc())

        # limit
        limit = self.get_argument("limit", None)
        if limit:
            community_query = community_query.limit(int(limit))

        groups = await self.application.objects.execute(community_query)

        for group in groups:
            # model to dict
            group_dict = model_to_dict(group)
            group_dict["front_image"] = "{}/media/{}".format(settings["SITE_URL"], group_dict["front_image"])

            re_data.append(group_dict)
        self.finish(json.dumps(re_data, default=json_serial))


    @authenticated_async
    async def post(self, *args, **kwargs):
        re_data = {}
        # 这里不能使用form.form_json()方法，因为这个参数里面包含文件参数
        group_form = CommunityGroupForm(self.request.body_arguments)
        new_filename = ""
        if group_form.validate():
            files_meta = self.request.files.get("front_image", None)
            if not files_meta:
                self.set_status(400)
                re_data["front_image"] = "请上传图片"
            else:
                for meta in files_meta:
                    # 获取原文件名，生成新的文件名，并将保存的图片文件的完整路径存入到数据库
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


class GroupMemberHandler(BaseHandler):
    @authenticated_async
    async def post(self, group_id, *args, **kwargs):
        re_data = {}
        # 获取前端post请求数据
        param = self.request.body.decode("utf8")
        param = json.loads(param)
        form = GroupApplyForm.from_json(param)
        if form.validate():
            try:
                # 获取要加入的group对象
                group = await self.application.objects.get(CommunityGroup, id=int(group_id))
                # 如果group存在，说明用户已经加入到该group
                existed = await self.application.objects.get(CommunityGroupMember, user=self.current_user, community=group)
                self.set_status(400)
                re_data["non_fields"] = "用户已经加入"

            except CommunityGroup.DoesNotExist as e:
                self.set_status(400)
            except CommunityGroupMember.DoesNotExist as e:
                community_member = await self.application.objects.create(CommunityGroupMember, user=self.current_user, community=group,
                                                      apply_reason = form.apply_reason.data)
                group.member_nums += 1
                result = await self.application.objects.update(group, ["member_nums"])
                # 该小组的成员数加1


                re_data["id"] = community_member.id
        else:
            self.set_status(400)
            for field in form.errors:
                re_data[field] = form.errors[field][0]
        self.finish(re_data)