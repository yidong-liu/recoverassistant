from django.db import models


# Create nurse models here.


class UserInfo(models.Model):
    """用户模型"""
    id = models.AutoField(primary_key=True)
    name = models.CharField('姓名', max_length=20, null=False, blank=False, unique=True)
    phone = models.CharField('电话', max_length=11, null=False, blank=False, unique=True)
    password = models.CharField('密码', max_length=256, null=False, blank=False)
    authority = models.IntegerField('权限', default=0, null=False)
    create_time = models.DateTimeField('创建时间', auto_now_add=True)

    class Meta:
        db_table = 't_user'
        verbose_name = '用户表'
        verbose_name_plural = verbose_name
        ordering = ['id']

    def __str__(self):
        return self.name


class FeedbackInfo(models.Model):
    """反馈信息模型"""
    id = models.AutoField(primary_key=True)
    description = models.CharField('描述', max_length=256, null=True)
    collection = models.BooleanField('是否查看', default=False)
    # 设置一个外键，将题目与上传人对应起来
    uploader = models.ForeignKey(UserInfo, on_delete=models.CASCADE, null=True)
    pub_time = models.DateTimeField('日期', auto_now_add=True)

    class Meta:
        db_table = 't_feedback'
        verbose_name = '反馈信息表'
        verbose_name_plural = verbose_name
        ordering = ['id']

    def __str__(self):
        return self.id


class QueryLog(models.Model):
    """日志信息模型"""
    id = models.AutoField(primary_key=True)
    query_text = models.TextField()
    query_timestamp = models.DateTimeField(auto_now_add=True)
    response_text = models.TextField()
    response_timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 't_log'
        verbose_name = '日志表'
        verbose_name_plural = verbose_name
        ordering = ['id']

    def __str__(self):
        return self.id
