#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:pyy
# datetime:2018/12/29 10:33
import json
import os
import uuid

import aiofiles
from playhouse.shortcuts import model_to_dict

from Myforum.Forum.handlers import BaseHandler
from Myforum.apps.question.forms import QuestionForm
from Myforum.apps.question.models import Question
from Myforum.apps.utils.decorators import authenticated_async
from Myforum.apps.utils.util_func import json_serial


class QuestionHandler(BaseHandler):
    async def get(self, *args, **kwargs):
        re_data = []
        #获取所有的问题记录
        question_query = Question.extend()

        # 根据类别进行过滤
        c = self.get_argument("c", None)
        if c:
            question_query = question_query.filter(Question.category==c)

        # 根据参数进行排序
        order = self.get_argument("o", None)
        if order:
            if order == "new":
                question_query = question_query.order_by(Question.add_time.desc())
            elif order == "hot":
                question_query = question_query.order_by(Question.answer_nums.desc())

        questions = await self.application.objects.execute(question_query)
        for question in questions:
            question_dict = model_to_dict(question)
            question_dict["image"] = "{}/media/{}/".format(self.settings["SITE_URL"], question_dict["image"])
            question_dict["add_time"] = question_dict["add_time"].strftime("%Y-%m-%d %H:%M:%S")
            re_data.append(question_dict)

        self.finish(json.dumps(re_data, default=json_serial))

    @authenticated_async
    async def post(self, *args, **kwargs):
        # 添加问题
        # 不能使用json_form
        re_data = {}
        question_form = QuestionForm(self.request.body_arguments)
        if question_form.validate():
            # 完成图片字段验证
            files_meta = self.request.files.get("image", None)
            if not files_meta:
                self.set_status(400)
                re_data["image"] = "请上传图片"
            else:
                # 完成图片的保存并将图片路径设置给对应的记录
                # 通过aiofiles写文件
                # 1.文件名
                new_filename = ""
                for meta in files_meta:
                    filename = meta["filename"]
                    new_filename = "{uuid}_{filename}".format(uuid=uuid.uuid1(), filename=filename)
                    file_path = os.path.join(self.settings["MEDIA_ROOT"], new_filename)
                    async with aiofiles.open(file_path, "wb") as f:
                        await f.write(meta["body"])
                question = await self.application.objects.create(Question,
                                                                 user = self.current_user,
                                                                 category = question_form.category.data,
                                                                 title = question_form.title.data,
                                                                 content = question_form.content.data,
                                                                 image = new_filename)
                re_data["id"] = question.id
        else:
            self.set_status(400)
            for field in question_form.errors:
                re_data[field] = question_form.errors[field][0]
        self.finish(re_data)