from ..models import Post, Category, Tag
from django import template

register = template.Library()

@register.simple_tag
def get_recent_post(num=5):
    return Post.objects.all().order_by('-created_time')[:num]

@register.simple_tag
def archives():
    return Post.objects.dates('created_time', 'month', order='DESC')

@register.simple_tag
def get_categories():
    nums = []
    for category in Category.objects.all():
        nums.append(len(Post.objects.filter(category=category)))
    return zip(Category.objects.all(),nums)

@register.simple_tag
def get_tags():
	return Tag.objects.all()
