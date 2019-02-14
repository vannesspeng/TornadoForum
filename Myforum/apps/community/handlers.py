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
from Myforum.apps.community.forms import CommunityGroupForm, GroupApplyForm, PostForm, PostComentForm, CommentReplyForm
from Myforum.apps.community.models import CommunityGroup, CommunityGroupMember, Post, PostComment, CommentLike
from Myforum.apps.users.models import User
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
            community_query = community_query.filter(CommunityGroup.category == c)

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
                                                              add_user=self.current_user, name=group_form.name.data,
                                                              category=group_form.category.data,
                                                              desc=group_form.desc.data,
                                                              notice=group_form.notice.data, from_image=new_filename)
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
                existed = await self.application.objects.get(CommunityGroupMember, user=self.current_user,
                                                             community=group)
                self.set_status(400)
                re_data["non_fields"] = "用户已经加入"

            except CommunityGroup.DoesNotExist as e:
                self.set_status(400)
            except CommunityGroupMember.DoesNotExist as e:
                community_member = await self.application.objects.create(CommunityGroupMember, user=self.current_user,
                                                                         community=group,
                                                                         apply_reason=form.apply_reason.data)
                group.member_nums += 1
                result = await self.application.objects.update(group, ["member_nums"])
                # 该小组的成员数加1
                re_data["id"] = community_member.id
        else:
            self.set_status(400)
            for field in form.errors:
                re_data[field] = form.errors[field][0]
        self.finish(re_data)


class GroupDetailHanlder(BaseHandler):
    @authenticated_async
    async def get(self, group_id, *args, **kwargs):
        # 获取group基本信息
        re_data = {}
        try:
            group = await self.application.objects.get(CommunityGroup, id=int(group_id))
            item_dict = {}
            item_dict["name"] = group.name
            item_dict["id"] = group.id
            item_dict["desc"] = group.desc
            item_dict["notice"] = group.notice
            item_dict["member_nums"] = group.member_nums
            item_dict["post_nums"] = group.post_nums
            item_dict["front_image"] = "{}/media/{}".format(self.settings["SITE_URL"], group.front_image)
            re_data = item_dict
        except CommunityGroup.DoesNotExist as e:
            self.set_status(400)

        self.finish(re_data)


class PostHandler(BaseHandler):
    @authenticated_async
    async def get(self, group_id, *args, **kwargs):
        post_list = []
        # 查询group是否存在
        try:
            group = await self.application.objects.get(CommunityGroup, id=int(group_id))
            # 查询当前用户是否为当前组的组员，只有组员才能查看
            group_member = await self.application.objects.get(CommunityGroupMember, user=self.current_user,
                                                              community=group, status="agree")

            posts_query = Post.extend()
            c = self.get_argument("cate", None)
            if c == "hot":
                posts_query = posts_query.filter(Post.is_hot == True)
            if c == "excellent":
                posts_query = posts_query.filter(Post.is_excellent == True)
            posts = await self.application.objects.execute(posts_query)

            for post in posts:
                item_dict = {
                    "user": {
                        "id": post.user.id,
                        "nick_name": post.user.nick_name
                    },
                    "id": post.id,
                    "title": post.title,
                    "content": post.content,
                    "comment_nums": post.comment_nums,
                    "add_time": post.add_time.strftime("%Y-%m-%d %H:%M:%S")
                }
                post_list.append(item_dict)
        except CommunityGroup.DoesNotExist as e:
            self.set_status(403)
        except CommunityGroupMember.DoesNotExist as e:
            self.set_status(404)
        self.finish(json.dumps(post_list, default=json_serial))

    @authenticated_async
    async def post(self, group_id, *args, **kwargs):
        re_data = {}
        params = self.request.body.decode("utf8")
        params = json.loads(params)
        form = PostForm.from_json(params)
        if form.validate():
            # 查询用户发帖的小组
            try:
                group = await self.application.objects.get(CommunityGroup, id=int(group_id))
                # 在处理发帖之前要校验一下，用户是否为小组成员
                group_member = await self.application.objects.get(CommunityGroupMember, user=self.current_user,
                                                                  community=group, status="agree")
                post = await self.application.objects.create(Post, user=self.current_user, group=group,
                                                             title=form.title.data, content=form.content.data)
                re_data["id"] = post.id
            except CommunityGroup.DoesNotExist as e:
                self.set_status(404)
            except CommunityGroupMember.DoesNotExist as e:
                self.set_status(403)
        else:
            self.set_status(400)
            for field in form.errors:
                re_data[field] = form.errors[field][0]
        self.finish(re_data)


class PostDetailHandler(BaseHandler):
    @authenticated_async
    async def get(self, post_id, *args, **kwargs):
        # 获取某一个帖子的详情
        re_data = {}
        post_details = await self.application.objects.execute(Post.extend().where(Post.id == int(post_id)))
        re_count = 0
        for data in post_details:
            item_dict = {}
            item_dict["user"] = model_to_dict(data.user)
            item_dict["title"] = data.title
            item_dict["content"] = data.content
            item_dict["comment_nums"] = data.comment_nums
            item_dict["add_time"] = data.add_time.strftime("%Y-%m-%d %H:%M:%S")
            re_data = item_dict

            re_count += 1

        if re_count == 0:
            self.set_status(404)

        self.finish(json.dumps(re_data, default=json_serial))


class PostCommentHanlder(BaseHandler):
    @authenticated_async
    async def get(self, post_id, *args, **kwargs):
        re_data = []
        try:
            post = await self.application.objects.get(Post, id=int(post_id))
            post_coments = await self.application.objects.execute(
                PostComment.extend().where(PostComment.post == post, PostComment.parent_comment.is_null(True)).order_by(
                    PostComment.add_time.desc())
            )
            for item in post_coments:
                has_liked = False
                try:
                    comments_like = await self.application.objects.get(CommentLike, post_comment_id=item.id,
                                                                       user_id=self.current_user.id)
                    has_liked = True
                except CommentLike.DoesNotExist:
                    pass

                item_dict = {
                    "user": model_to_dict(item.user),
                    "content": item.content,
                    "reply_nums": item.reply_nums,
                    "like_nums": item.like_nums,
                    "has_liked": has_liked,
                    "id": item.id,
                }

                re_data.append(item_dict)
        except Post.DoesNotExist as e:
            self.set_status(404)
        self.finish(json.dumps(re_data, default=json_serial))

    @authenticated_async
    async def post(self, post_id, *args, **kwargs):
        re_data = {}
        param = self.request.body.decode("utf8")
        param = json.loads(param)
        form = PostComentForm.from_json(param)
        if form.validate():
            try:
                # 获取对应的帖子实体
                post = await self.application.objects.get(Post, id=int(post_id))
                # 数据库中创建评论记录
                post_comment = await self.application.objects.create(PostComment, user=self.current_user, post=post,
                                                                     content=form.content.data)
                # 帖子的评论数要加1
                post.comment_nums += 1
                await self.application.objects.update(post)
                re_data["id"] = post_comment.id
                # 这里这样处理，是剔除掉User中的datetime类型，这样序列化的时候就不会报错了
                re_data["user"] = {}
                re_data["user"]["nick_name"] = self.current_user.nick_name
                re_data["user"]["id"] = self.current_user.id
            except Post.DoesNotExist as e:
                self.set_status(404)
        else:
            self.set_status(400)
            for field in form.errors:
                re_data[field] = form.errors[field][0]
        self.finish(re_data)


class CommentReplyHandler(BaseHandler):
    @authenticated_async
    async def get(self, comment_id, *args, **kwargs):
        re_data = []
        # 获取某一条评论的所有回复
        comment_replys = await self.application.objects.execute(
            PostComment.extend().where(PostComment.parent_comment_id == int(comment_id)))
        # 遍历所有的评论回复返回前端需要的json数据
        for item in comment_replys:
            item_dict = {
                "user": model_to_dict(item.user),
                "content": item.content,
                "reply_nums": item.reply_nums,
                "add_time": item.add_time.strftime("%Y-%m-%d"),
                "id": item.id
            }
            re_data.append(item_dict)
        self.finish(json.dumps(re_data, default=json_serial))

    @authenticated_async
    async def post(self, comment_id, *args, **kwargs):
        re_data = {}
        # 1、校验评论回复表单
        params = self.request.body.decode("utf8")
        params = json.loads(params)
        form = CommentReplyForm.from_json(params)
        if form.validate():

            try:
                # 1、找到comment实体,帖子实体
                comment = await self.application.objects.get(PostComment, id=int(comment_id))
                post = await self.application.objects.get(Post, id=comment.post_id)
                # 2、找出回复的目标用户
                reply_user = await self.application.objects.get(User, id=int(form.replyed_user.data))
                # 3、创建评论回复的记录
                reply = await self.application.objects.create(PostComment, user=self.current_user, post=post,
                                                              parent_comment=comment, reply_user=reply_user,
                                                              content=form.content.data)
                # 4、更新coment的回复数
                comment.reply_nums += 1
                await self.application.objects.update(comment)

                re_data["id"] = reply.id
                re_data["user"] = {
                    "id": self.current_user.id,
                    "nick_name": self.current_user.nick_name
                }

            except PostComment.DoesNotExist:
                self.set_status(404)
            except User.DoesNotExist as e:
                self.set_status(400)
                re_data["replyed_user"] = "用户不存在"
        else:
            self.set_status(400)
            for field in form.errors:
                re_data[field] = form.errors[field][0]
        self.finish(re_data)


class CommentsLikeHanlder(BaseHandler):
    @authenticated_async
    async def post(self, comment_id, *args, **kwargs):
        re_data = {}
        # 查询对应的comment
        try:
            comment = await self.application.objects.get(PostComment, id=int(comment_id))
            # 创建一条点赞记录
            comment_like = await self.application.objects.create(CommentLike, user=self.current_user,
                                                                 post_comment=comment)
            # 更新评论的点赞数量
            comment.like_nums += 1
            await self.application.objects.update(comment)
            re_data["id"] = comment_like.id
        except PostComment.DoesNotExist as e:
            self.set_status(404)
        self.finish(re_data)
