from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.template import loader 
from django.shortcuts import render

from . import handler

context = [{'template', ''}]
# Create your views here.

# test
def index(request):
	return HttpResponse('你好')


# 文件上传
@csrf_exempt
@require_http_methods(['POST'])
def upload(request):
	file_obj = request.FILES.get('csv_file')
	if file_obj:
		for chunk in file_obj.chunks():
			if len(chunk) > 100 * 1024 * 1024:
				return HttpResponse('文件过大(100M)')

			suffic = file_obj.name.split('.')[-1]
			table_name = file_obj.name.split('.')[0]
			if len(suffic) != 0 and suffic == 'xlsx':
				if not handler.handle_table(chunk, table_name, 1, 1):
					return HttpResponse("文件解析出错")
			elif len(suffic) != 0 and suffic == 'png':
				if not handler.handle_table(chunk, table_name, 1, 2):
					return HttpResponse("文件解析出错")
			else:
				return HttpResponse("文件格式异常")

		return HttpResponse('上传成功')


# 获取所有报表
def get_table(request):
	ret = handler.get_all_table()
	return HttpResponse(ret)


# 查看表格
@require_http_methods(['GET'])
def observe(request):
	context = handler.get_one_table(request.GET.get("t"))
	template = loader.get_template('table.html')
	html_str = template.render(context, request)
	return HttpResponse(html_str);


# 删除表格
@require_http_methods(['GET'])
def remove(request):
	handler.delete_table(request.GET.get("t"));
	return HttpResponse(open('static/basic-table.html', 'rb'), content_type='text/html');
