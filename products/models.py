from django.db import models
from users.models import Consumer, Farmer
from django.core.exceptions import ObjectDoesNotExist
# Create your models here.


def check_rate(rate_num):
    if rate_num is 1:
        return 2
    elif rate_num is 3:
        return 1
    else:
        return 0


class Product(models.Model):
    title = models.CharField(max_length=50)
    sub_title = models.CharField(max_length=100)
    main_image = models.ImageField(upload_to="product_main_image/%Y/%m/%d/")
    open = models.BooleanField(default=False)

    sell_price = models.IntegerField(default=0, help_text="현재 판매가")
    weight = models.FloatField()
    stock = models.IntegerField(default=0, help_text="총 재고 수량")
    sales_count = models.IntegerField(
        default=0, help_text="총 판매 수량", blank=True)
    sales_rate = models.FloatField(default=0, blank=True)

    instruction = models.TextField(blank=True)

    desc_image = models.ImageField(
        upload_to="product_desc_image/%Y/%m/%d/", null=True, blank=True)
    desc = models.TextField(blank=True)

    total_rating_avg = models.FloatField(default=0)

    update_at = models.DateTimeField(auto_now=True)
    create_at = models.DateTimeField(auto_now_add=True)

    farmer = models.ForeignKey(
        Farmer, related_name="products", on_delete=models.CASCADE)
    category = models.ForeignKey(
        'Category', related_name='products', on_delete=models.CASCADE)
    #editor_review = models.ForeignKey(editor_review)

    def save(self, *args, **kwargs):
        self.weight = round(self.weight, 1)
        self.sales_count = round(self.sales_count, 2)
        super(Product, self).save(*args, **kwargs)

    def sold(self):
        if self.stock > 0:
            self.stock -= 1
            self.sales_count += 1
        else:
            self.open = False
        return

    def calculate_sale_rate(self):
        rate = self.sales_count / (self.stock + self.sales_count)
        self.sales_rate = rate
        return self.sales_rate

    def calculate_total_rating_avg(self):
        sum = 0
        try:
            comments = self.product_comments.all()
            if comments.exists() is False:
                raise ObjectDoesNotExist
            comments_num = comments.count()
            print(comments_num)
            for comment in comments:
                sum += comment.avg
            print(sum)
            self.total_rating_avg = round(sum/comments_num, 1)
            return self.total_rating_avg
        except ObjectDoesNotExist:
            return 0

    def check_rate(rate_num):
        if rate_num is 1:
            return 2
        elif rate_num is 3:
            return 1
        else:
            return 0

    def calculate_specific_rating(self):
        freshness_array = [0, 0, 0]
        flavor_array = [0, 0, 0]
        cost_performance_array = [0, 0, 0]
        result = []
        try:
            comments = self.product_comments.all()
            if comments.exists() is False:
                raise ObjectDoesNotExist
            ratio = 100/comments.count()
            for comment in comments:
                freshness_array[check_rate(comment.freshness)] += 1
                flavor_array[check_rate(comment.flavor)] += 1
                cost_performance_array[check_rate(
                    comment.cost_performance)] += 1

            for i in range(0, 3):
                freshness_array[i] = round(freshness_array[i] * ratio)
                flavor_array[i] = round(flavor_array[i] * ratio)
                cost_performance_array[i] = round(
                    cost_performance_array[i] * ratio)
            print(freshness_array)
            print(flavor_array)
            print(cost_performance_array)
            result.append(freshness_array)
            result.append(flavor_array)
            result.append(cost_performance_array)
            return result
        except ObjectDoesNotExist:
            result.append(freshness_array)
            result.append(flavor_array)
            result.append(cost_performance_array)
            return result

    def __str__(self):
        return self.title


class Product_Image(models.Model):
    product = models.ForeignKey(
        Product, related_name='product_images', on_delete=models.CASCADE)

    image = models.ImageField(
        upload_to="product_images/%Y/%m/%d/")

    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)


class Category(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField()
    parent = models.ForeignKey(
        'self', blank=True, null=True, related_name="children", on_delete=models.CASCADE)

    def __str__(self):
        full_path = [self.name]
        k = self.parent
        while k is not None:
            full_path.append(k.name)
            k = k.parent
        return '->'.join(full_path[::-1])


class Question(models.Model):
    status = (
        (True, '답변 완료'),
        (False, '답변 대기'),
    )
    title = models.CharField(max_length=50)
    content = models.TextField()
    image = models.ImageField(upload_to="question_image/%Y/%m/%d/")

    status = models.BooleanField(default=False, choices=status)

    update_at = models.DateTimeField(auto_now=True)
    create_at = models.DateTimeField(auto_now_add=True)

    consumer = models.ForeignKey(
        Consumer, related_name='QnAs', on_delete=models.CASCADE)
    product = models.ForeignKey(
        Product, related_name='QnAs', on_delete=models.CASCADE)

    def __str__(self):
        return self.product.title.join('-Q from ', self.consumer.user.nickname)


class Answer(models.Model):
    title = models.CharField(max_length=50)
    content = models.TextField()
    question = models.OneToOneField(Question, on_delete=models.CASCADE)

    update_at = models.DateTimeField(auto_now=True)
    create_at = models.DateTimeField(auto_now_add=True)

    farmer = models.ForeignKey('users.Farmer', on_delete=models.CASCADE)

    def __str__(self):
        return self.question.__str__().join('에 대한 답변')


def get_delete_product():
    return Product.objects.get_or_create(title="삭제된 상품")[0]
