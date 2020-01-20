# 处理
import xlrd
import pymysql

# 表格处理
# id = 1 处理上传文件/id = 2 处理下载文件
def handle_table(string, table_name, handle_id, file_id):
	if handle_id == 1 and handle_upload_table(string, table_name, file_id):
		return True

	if handle_id == 2 and handle_download_table(string):
		return True

	return False


# 处理表格上传
def handle_upload_table(string, table_name, file_id):
	if file_id == 1:
		if not handle_upload_excel(string, table_name):
			return False
	else:
		return False
	
	return True


# 处理表格下载
def handle_download_table(string):
	return False


# 处理excel文件上传
def handle_upload_excel(string, table_name):
	#打开文件句柄
	wb = xlrd.open_workbook(filename = None, file_contents = string)
	if wb:
		table = wb.sheets()[0]
		nrows = table.nrows
		#行为0返回失败
		if nrows == 0:
			return False

		#取首行数据，创建表
		head_values = table.row_values(0)
		if len(head_values) == 0:
			return False

		# 连接数据库，创建邮轮
		db = pymysql.connect("127.0.0.1", "root", "my_db", "my_db")
		cursor = db.cursor()

		sql = "CREATE TABLE IF NOT EXISTS " + table_name + "(";
		for i in range(0, len(head_values)):
			if i != len(head_values) - 1:
				sql += str(head_values[i]) + " TEXT,"
			else:
				sql += str(head_values[i]) + " TEXT"
		sql += ")ENGINE=InnoDB DEFAULT CHARSET=utf8;";
		cursor.execute(sql);
		sql = "INSERT INTO all_table VALUES(0, '" + table_name + "', 0, '', 'andy')"
		print(sql)
		cursor.execute(sql);

		#除首行外无其他数据则直接返回成功
		if nrows == 1:
			db.commit()
			db.close()
			return True

		#拼接插入记录
		try:
			for index in range(1, nrows):
				row_values = table.row_values(index)
				sql = "INSERT INTO " + table_name + " VALUES('"
				for u in range(0, len(row_values)):
					if u != len(row_values) - 1:
						sql += str(row_values[u]) + "', '"
					else:
						sql += str(row_values[u]) + "'"
				sql += ");"
				cursor.execute(sql);
		except Exception as e:
			db.commit()
			db.close()
			return False

	db.commit()
	db.close()
	return True


# 获取所有报表信息
def get_all_table():
	# 连接数据库，创建邮轮
	db = pymysql.connect("127.0.0.1", "root", "my_db", "my_db")
	cursor = db.cursor()

	ret = ""
	sql = "SELECT * FROM all_table;"
	cursor.execute(sql)
	results = cursor.fetchall()
	for row in results:
		ret += "<tr><td>"
		for field in row:
			if field != row[-1]:
				ret += str(field) + "</td><td>"
			else:
				ret += str(field) + "</td>"
		ret += "<td><a href=\"/system/observe?t=" + str(row[1]) + "\"><button \
			class=\"check_button\">查看</button></a></td><td><a href=\"/system/\
			remove?t=" + str(row[1]) + "\"><button class=\"check_button\">删除 \
			</button></a></td></tr>"

	db.close()
	return ret 


def get_one_table(name):
	# 连接数据库，创建邮轮
	db = pymysql.connect("127.0.0.1", "root", "my_db", "my_db")
	cursor = db.cursor()

	context = {'name': '', 'thead': [], 'tbody': []}
	context['name'] = name

	col_names = []
	sql = "SELECT COLUMN_NAME FROM information_schema.COLUMNS WHERE table_name \
		   = '" + name + "';"
	try:
		cursor.execute(sql)
		col_name = cursor.fetchall()
		for col in col_name:
			for col_field in col:
				col_names.append(col_field)
		context['thead'] = col_names
	except Exception as e:
		db.close()
		return context

	tbody = []
	sql = "SELECT * FROM " + name + ";"
	try:
		cursor.execute(sql)
		results = cursor.fetchall()
		for row in results:
			tbody.append(row)
		context['tbody'] = tbody
	except Exception as e:
		db.close()
		return context

	db.close()
	return context 


def delete_table(name):
	# 连接数据库，创建邮轮
	db = pymysql.connect("127.0.0.1", "root", "my_db", "my_db")
	cursor = db.cursor()

	try:
		sql = "DROP TABLE " + name + ";"
		cursor.execute(sql)
		sql = "DELETE FROM all_table WHERE name = '" + name + "';"
		cursor.execute(sql)
	except Exception as e:
		db.commit()
		db.close()
		return "failed"

	db.commit()
	db.close()
	return "ok"
