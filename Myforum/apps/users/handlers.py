#!/usr/bin/env python
#-*- coding:utf-8 -*-
# author:pyy
# datetime:2018/12/29 10:33
import json
import os
import uuid
from datetime import datetime
from random import choices

import aiofiles
import jwt
from tornado.web import RequestHandler

from Myforum.Forum.handlers import RedisHandler, BaseHandler
from Myforum.Forum.settings import settings
from Myforum.apps.community.models import CommunityGroup, CommunityGroupMember
from Myforum.apps.question.models import Question, Answer
from Myforum.apps.users.forms import SmsCodeForm, RegisterForm, LoginForm, ChangeInfoForm, ChangePwdForm
from Myforum.apps.users.models import User
from Myforum.apps.utils.AsyncYunPian import AsyncYunPian
from Myforum.apps.utils.decorators import authenticated_async


class LoginHandler(BaseHandler):
    async def post(self, *args, **kwargs):
        # 声明返回的数据字典
        re_data = {}
        # 获取post参数请求
        param = self.request.body.decode("utf8")
        param = json.loads(param)
        # 新建login_form
        login_form = LoginForm.from_json(param)
        if login_form.validate():
            # 获取post参数数据
            mobile = login_form.mobile.data
            passoword = login_form.password.data
            #先判断用户是否存在
            try:
                # 数据库查询属于耗时IO操作，需要加上await关键字
                user = await self.application.objects.get(User, mobile=mobile)
                # 说明用户存在，接下来验证密码是否正确
                if not user.password.check_password(passoword):
                    self.set_status(400)
                    re_data["non_fields"] = "用户名或密码错误"
                else:
                    # 说明密码正确，登录成功
                    # 这里使用JWT进行验证
                    payload = {
                        "id": user.id,
                        "nickname": user.nick_name,
                        "exp": datetime.utcnow()
                    }
                    token = jwt.encode(payload, settings['secret_key'], algorithm='HS256')
                    re_data['id'] = user.id
                    if user.nick_name is not None:
                        re_data['nick_name'] = user.nick_name
                    else:
                        re_data['nick_name'] = user.mobile
                    re_data['token'] = token.decode("utf8")

            except User.DoesNotExist as e:
                # 说明查询用户结果是用户不存在
                self.set_status(400)
                re_data["mobile"] = "用户不存在"
        else:
            # 设置http状态码为400：参数错误
            self.set_status(400)
            for field in login_form.errors:
                re_data[field] = login_form.errors[field][0]
        self.finish(re_data)



class RegisterHandler(RedisHandler):
    async def post(self, *args, **kwargs):
        # 声明返回的数据字典
        re_data = {}
        # 获取post请求参数,此时的params为str
        param = self.request.body.decode("utf8")
        # 将params原始json数据转换为字典
        param = json.loads(param)
        register_form = RegisterForm.from_json(param)
        if register_form.validate():
            mobile = register_form.mobile.data
            code = register_form.code.data
            password = register_form.password.data

            # 在redis中查询验证码，来确定上传的验证码是否正确
            redis_key = "{}-{}".format(mobile, code)
            if not self.redis_conn.get(redis_key):
                # 说明验证码非法
                self.set_status(400)
                re_data['code'] = "验证码失效或者错误"
            else:
                # 验证正确，那么就需要验证用户是否存在
                try:
                    existed_users = await self.application.objects.get(User, mobile=mobile)
                    self.set_status(400)
                    re_data["mobile"] = "用户已经存在"
                except User.DoesNotExist as e:
                    user = await self.application.objects.create(User, mobile=mobile, password=password)
                    re_data['id'] = user.id
        else:
            self.set_status(400)
            for field in register_form.errors:
                re_data[field] = register_form.errors[field][0]
        self.finish(re_data)




class SmsHandler(RedisHandler):
    def general_code(self):
        """
        随机生成四位数的验证码
        :return:
        """
        seeds = "1234567890"
        random_str = []
        for i in range(4):
            random_str.append(choices(seeds)[0])
        return "".join(str(x) for x in random_str)


    async def post(self, *args, **kwargs):
        re_data = {}
        # 获取post的请求参数
        param = self.request.body.decode("utf-8")
        param = json.loads(param)
        sms_form = SmsCodeForm.from_json(param)
        if sms_form.validate():
            # 使用云片网api发送短信到指定的手机号码上
            # 发送单条短信
            # 这里使用tornado框架中的httpclient来发送网络请求
            mobile = sms_form.mobile.data
            code = self.general_code()
            yu_pian = AsyncYunPian("37a35942325be7af542ca05b22aa16ab")
            re_json = await yu_pian.send_single_sms(code, mobile)
            if re_json["code"] != 0:
                self.set_status(400)
                re_data["mobile"] = re_json["msg"]
            else:
                # 说明请求成功，将验证码写入redis数据库
                self.redis_conn.set("{}-{}".format(mobile, code), 1, 30*60)
                re_data["success"] = re_json["msg"]
        else:
            self.set_status(400)
            for field in sms_form.errors:
                re_data[field] = sms_form.errors[field][0]
        self.finish(re_data)


class InfoHandler(BaseHandler):
    @authenticated_async
    async def get(self, *args, **kwargs):
        re_data = {
            "mobile": self.current_user.mobile,
            "nick_name": self.current_user.nick_name,
            "gender": self.current_user.gender,
            "desc": self.current_user.desc,
            "address": self.current_user.address,
            "id": self.current_user.id
        }
        self.finish(re_data)

    @authenticated_async
    async def patch(self, *args, **kwargs):
        re_data = {}
        # 获取post请求参数
        param = self.request.body.decode("utf-8")
        param = json.loads(param)
        form = ChangeInfoForm.from_json(param)
        if form.validate():
            self.current_user.nick_name = form.nick_name.data
            self.current_user.gender = form.gender.data
            self.current_user.address = form.address.data
            self.current_user.desc = form.desc.data
            res = await self.application.objects.update(self.current_user)
        else:
            self.set_status(400)
            for field in form.errors:
                re_data[field] = form.errors[field][0]
        self.finish(re_data)


class HeadImageHandler(BaseHandler):
    @authenticated_async
    async def post(self, *args, **kwargs):
        re_data = {}
        # 获取图片文件
        files_meta = self.request.files.get("image", None)
        new_filename = ""
        if not files_meta:
            self.set_status(400)
            re_data["image"] = "请上传图片"
        else:
            # 保存上传图片
            for meta in files_meta:
                # 获取原文件名，生成新的文件名，并将保存的图片文件的完整路径存入到数据库
                file_name = meta["filename"]
                new_filename = "{uuid}_{filename}".format(uuid=uuid.uuid1(), filename=file_name)
                file_path = os.path.join(settings['MEDIA_ROOT'], new_filename)
                async with aiofiles.open(file_path, 'wb') as f:
                    await f.write(meta['body'])
            # 变更当前用户头像图片的url
            self.current_user.head_url = new_filename
            await self.application.objects.update(self.current_user)
            re_data["image"] = "/media/" + new_filename
        self.finish(re_data)


class PasswordHandler(BaseHandler):
    @authenticated_async
    async def post(self, *args, **kwargs):
        re_data = {}
        param = self.request.body.decode("utf-8")
        param = json.loads(param)
        change_pwd_form = ChangePwdForm.from_json(param)
        if change_pwd_form.validate():
            # 比对旧密码是否正确
            if not self.current_user.password.check_password(change_pwd_form.old_psw.data):
                self.set_status(400)
                re_data["old_password"] = "旧密码错误"
            # 比对新密码与新密码确认是否相同
            else:
                if change_pwd_form.new_psw.data != change_pwd_form.confirm_psw.data:
                    self.set_status(400)
                    re_data["new_password"] = "新密码两次输入不一致"
                else:
                    # 说明旧密码输入正确，新密码输入无误
                    self.current_user.password = change_pwd_form.confirm_psw.data
                    res = await self.application.objects.update(self.current_user)
        else:
            self.set_status(400)
            for field in change_pwd_form.errors:
                re_data[field] = change_pwd_form.errors[field][0]
        self.finish(re_data)


class UserGroupHanlder(BaseHandler):
    @authenticated_async
    async def get(self, user_id, *args, **kwargs):
        re_data = []
        # 获取到当前用户创建的group
        try:
            user = await self.application.objects.get(User, id=user_id)
            user_dict = {
                "nick_name": user.nick_name,
                "head_url": "/media/" + user.head_url,
            }
            re_data.append({"user": user_dict})
            create_groups = await self.application.objects.execute(CommunityGroup.select().where(CommunityGroup.creator_id == user_id))
            create_group = []
            for group in create_groups:
                create_group.append({
                    "group_id": group.id,
                    "front_image": group.front_image,
                    "name": group.name,
                    "desc": group.desc
                })
            re_data.append({"owner": create_group})
            join_group_members = await self.application.objects.execute(CommunityGroupMember.select().where(CommunityGroupMember.user_id == user_id, CommunityGroupMember.status == "agree"))
            join_group_ids = []
            for group_member in join_group_members:
                join_group_ids.append(group_member.community_id)
            join_groups = await self.application.objects.execute(
                CommunityGroup.select().where(CommunityGroup.id.in_(join_group_ids)))
            join_group = []
            for group in join_groups:
                join_group.append({
                    "group_id": group.id,
                    "front_image": group.front_image,
                    "name": group.name,
                    "desc": group.desc
                })
            re_data.append({"join": join_group})
        except User.DoesNotExist as e:
            self.set_status(400)
        self.finish(json.dumps(re_data))

class UserQuestionHanlder(BaseHandler):
    @authenticated_async
    async def get(self, user_id, *args, **kwargs):
        re_data = []
        # 获取到当前用户创建的question
        questions = await self.application.objects.execute(Question.select().where(Question.user_id == user_id))
        for question in questions:
            re_data.append({
                "question_id": question.id,
                "content": question.content,
                "add_time": question.add_time.strftime("%Y-%m-%d %H:%M:%S")
            })
        self.finish(json.dumps(re_data))


class UserAnswerHanlder(BaseHandler):
    @authenticated_async
    async def get(self, user_id, *args, **kwargs):
        re_data = []
        # 获取到当前用户创建的question
        answers = await self.application.objects.execute(Answer.select().where(Answer.user_id == user_id))
        for answer in answers:
            re_data.append({
                "question_id":answer.question_id,
                "content": answer.content,
                "add_time": answer.add_time.strftime("%Y-%m-%d %H:%M:%S")
            })
        self.finish(json.dumps(re_data))