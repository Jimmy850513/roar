from django.db import models

# Create your models here.


class Active_Information(models.Model):
    #活動ID
    id = models.CharField(primary_key=True,max_length=200,null=False)
    #活動名稱
    title = models.CharField(max_length=300,null=False)
    #折扣資訊
    discount_info = models.CharField(max_length=200)
    #活動描述
    active_description = models.TextField()
    #活動推廣照片
    active_promo_image = models.CharField(max_length=500)
    #來源網站名稱
    source_web_name = models.CharField(max_length=200)
    #售票網址
    webSales = models.CharField(max_length=300)
    #活動起始日期
    start_date = models.DateField(null=False)
    #活動結束日期
    end_date = models.DateField(null=False)
    #活動備註
    comment = models.CharField(max_length=200,null=False)
    #活動點閱數
    hitRate = models.IntegerField(null=False,default=0)
    #使用找是否刪除
    is_deleted = models.BooleanField(default=True)
    
    class Meta:
        db_table = 'active_info'

class Active_Show_Information(models.Model):
    #活動ID
    active_info = models.ForeignKey(Active_Information,on_delete=models.CASCADE)
    #表演開始時間
    show_start_time = models.DateTimeField(null=False)
    #表演結束時間
    show_end_time = models.DateTimeField(null=False)
    #表演地點名稱
    show_location = models.CharField(max_length=200,null=False)
    #表演地點
    show_location_addr = models.CharField(max_length=200,null=False)
    #是否售票
    on_sale = models.BooleanField(default=False)
    #售票說明
    price = models.CharField(max_length=200)

    class Meta:
        db_table = 'active_show_info'

class Active_Category_Unit(models.Model):
    #活動ID
    active = models.ForeignKey(Active_Information,on_delete=models.CASCADE)
    #活動分類
    category = models.CharField(max_length=100,null=True)
    #演出單位
    show_unit = models.CharField(max_length=200,null=True)
    #主辦單位
    master_unit = models.CharField(max_length=200)
    #協辦單位
    sub_unit = models.CharField(max_length=200)
    #贊助單位
    support_unit = models.CharField(max_length=200)
    #其他單位
    other_unit = models.CharField(max_length=200)

    class Meta:
        db_table = 'active_category_info'
