Skip to main content
�����ļ�����
������������
�ӿ�˵��
������ͨ�� API ������������ĳ������û��������� Token�� ע�⣺

�����ļ���С���ܳ��� 200MB,�ļ�ҳ�������� 600 ҳ
ÿ���˺�ÿ������ 2000 ҳ������ȼ�������ȣ����� 2000 ҳ�Ĳ������ȼ�����
���������ƣ�github��aws �ȹ��� URL ������ʱ
�ýӿڲ�֧���ļ�ֱ���ϴ�
headerͷ����Ҫ���� Authorization �ֶΣ���ʽΪ Bearer + �ո� + Token
Python ����ʾ��
import requests

token = "���������api token"
url = "https://mineru.net/api/v4/extract/task"
header = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {token}"
}
data = {
    "url": "https://cdn-mineru.openxlab.org.cn/demo/example.pdf",
    "is_ocr": True,
    "enable_formula": False,
}

res = requests.post(url,headers=header,json=data)
print(res.status_code)
print(res.json())
print(res.json()["data"])

CURL ����ʾ��
curl --location --request POST 'https://mineru.net/api/v4/extract/task' \
--header 'Authorization: Bearer ***' \
--header 'Content-Type: application/json' \
--header 'Accept: */*' \
--data-raw '{
    "url": "https://cdn-mineru.openxlab.org.cn/demo/example.pdf",
    "is_ocr": true,
    "enable_formula": false
}'

���������˵��
����	����	�Ƿ��ѡ	ʾ��	����
url	string	��	https://static.openxlab.org.cn/
opendatalab/pdf/demo.pdf	�ļ� URL��֧��.pdf��.doc��.docx��.ppt��.pptx��.png��.jpg��.jpeg���ָ�ʽ
is_ocr	bool	��	false	�Ƿ����� ocr ���ܣ�Ĭ�� false
enable_formula	bool	��	true	�Ƿ�����ʽʶ��Ĭ�� true
enable_table	bool	��	true	�Ƿ������ʶ��Ĭ�� true
language	string	��	ch	ָ���ĵ����ԣ�Ĭ�� ch��������ѡֵ�б������https://www.paddleocr.ai/latest/en/version3.x/algorithm/PP-OCRv5/PP-OCRv5_multi_languages.html#4-supported-languages-and-abbreviations
data_id	string	��	abc**	���������Ӧ������ ID���ɴ�СдӢ����ĸ�����֡��»��ߣ�_�����̻��ߣ�-����Ӣ�ľ�ţ�.����ɣ������� 128 ���ַ�����������Ψһ��ʶ����ҵ�����ݡ�
callback	string	��	http://127.0.0.1/callback	��������ص�֪ͨ���� URL��֧��ʹ�� HTTP �� HTTPS Э��ĵ�ַ�����ֶ�Ϊ��ʱ�������붨ʱ��ѯ���������callback �ӿڱ���֧�� POST ������UTF-8 ���롢Content-Type:application/json �������ݣ��Լ����� checksum �� content�������ӿڰ������¹���͸�ʽ���� checksum �� content���������� callback �ӿڷ��ؼ������
checksum���ַ�����ʽ�����û� uid + seed + content ƴ���ַ�����ͨ�� SHA256 �㷨���ɡ��û� UID�����ڸ������Ĳ�ѯ��Ϊ���۸ģ��������ڻ�ȡ�����ͽ��ʱ���������㷨�����ַ������� checksum ��һ��У�顣
content��JSON �ַ�����ʽ�������н�����ת�� JSON ���󡣹��� content �����ʾ������μ������ѯ����ķ���ʾ������Ӧ�����ѯ����� data ���֡�
˵��:���ķ���� callback �ӿ��յ� Mineru �����������͵Ľ����������ص� HTTP ״̬��Ϊ 200�����ʾ���ճɹ��������� HTTP ״̬�����Ϊ����ʧ�ܡ�����ʧ��ʱ��mineru ������ظ����� 5 �μ������ֱ�����ճɹ����ظ����� 5 �κ���δ���ճɹ����������ͣ���������� callback �ӿڵ�״̬��
seed	string	��	abc**	����ַ�������ֵ���ڻص�֪ͨ�����е�ǩ������Ӣ����ĸ�����֡��»��ߣ�_����ɣ������� 64 ���ַ��������Զ��塣�����ڽ��յ����ݰ�ȫ�Ļص�֪ͨʱУ�������� Mineru ����������
˵������ʹ�� callback ʱ�����ֶα����ṩ��
extra_formats	[string]	��	["docx","html"]	markdown��jsonΪĬ�ϵ�����ʽ���������ã��ò�����֧��docx��html��latex���ָ�ʽ�е�һ������
page_ranges	string	��	1-600	ָ��ҳ�뷶Χ����ʽΪ���ŷָ����ַ��������磺"2,4-6"����ʾѡȡ��2ҳ����4ҳ����6ҳ������4��6�����Ϊ [2,4,5,6]����"2--2"����ʾ�ӵ�2ҳһֱѡȡ�������ڶ�ҳ������"-2"��ʾ�����ڶ�ҳ����
model_version	string	��	vlm	mineruģ�Ͱ汾������ѡ��:pipeline��vlm��Ĭ��pipeline��
������ʾ��
{
  "url": "https://static.openxlab.org.cn/opendatalab/pdf/demo.pdf",
  "is_ocr": true,
  "data_id": "abcd"
}

��Ӧ����˵��
����	����	ʾ��	˵��
code	int	0	�ӿ�״̬�룬�ɹ���0
msg	string	ok	�ӿڴ�����Ϣ���ɹ���"ok"
trace_id	string	c876cd60b202f2396de1f9e39a1b0172	���� ID
data.task_id	string	a90e6ab6-44f3-4554-b459-b62fe4c6b436	��ȡ���� id�������ڲ�ѯ������
��Ӧʾ��
{
  "code": 0,
  "data": {
    "task_id": "a90e6ab6-44f3-4554-b4***"
  },
  "msg": "ok",
  "trace_id": "c876cd60b202f2396de1f9e39a1b0172"
}

��ȡ������
�ӿ�˵��
ͨ�� task_id ��ѯ��ȡ����Ŀǰ�Ľ��ȣ���������ɺ󣬽ӿڻ���Ӧ��Ӧ����ȡ���顣

Python ����ʾ��
import requests

token = "���������api token"
url = f"https://mineru.net/api/v4/extract/task/{task_id}"
header = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {token}"
}

res = requests.get(url, headers=header)
print(res.status_code)
print(res.json())
print(res.json()["data"])

CURL ����ʾ��
curl --location --request GET 'https://mineru.net/api/v4/extract/task/{task_id}' \
--header 'Authorization: Bearer *****' \
--header 'Accept: */*'

��Ӧ����˵��
����	����	ʾ��	˵��
code	int	0	�ӿ�״̬�룬�ɹ���0
msg	string	ok	�ӿڴ�����Ϣ���ɹ���"ok"
trace_id	string	c876cd60b202f2396de1f9e39a1b0172	���� ID
data.task_id	string	abc**	���� ID
data.data_id	string	abc**	���������Ӧ������ ID��
˵��������ڽ�����������д����� data_id����˴����ض�Ӧ�� data_id��
data.state	string	done	������״̬�����:done��pending: �Ŷ��У�running: ���ڽ�����failed������ʧ�ܣ�converting����ʽת����
data.full_zip_url	string	https://cdn-mineru.openxlab.org.cn/
pdf/018e53ad-d4f1-475d-b380-36bf24db9914.zip	�ļ��������ѹ����
data.err_msg	string	�ļ���ʽ��֧�֣����ϴ�����Ҫ����ļ�����	����ʧ��ԭ�򣬵� state=failed ʱ��Ч
data.extract_progress.extracted_pages	int	1	�ĵ��ѽ���ҳ������state=runningʱ��Ч
data.extract_progress.start_time	string	2025-01-20 11:43:20	�ĵ�������ʼʱ�䣬��state=runningʱ��Ч
data.extract_progress.total_pages	int	2	�ĵ���ҳ������state=runningʱ��Ч
��Ӧʾ��
{
  "code": 0,
  "data": {
    "task_id": "47726b6e-46ca-4bb9-******",
    "state": "running",
    "err_msg": "",
    "extract_progress": {
      "extracted_pages": 1,
      "total_pages": 2,
      "start_time": "2025-01-20 11:43:20"
    }
  },
  "msg": "ok",
  "trace_id": "c876cd60b202f2396de1f9e39a1b0172"
}

{
  "code": 0,
  "data": {
    "task_id": "47726b6e-46ca-4bb9-******",
    "state": "done",
    "full_zip_url": "https://cdn-mineru.openxlab.org.cn/pdf/018e53ad-d4f1-475d-b380-36bf24db9914.zip",
    "err_msg": ""
  },
  "msg": "ok",
  "trace_id": "c876cd60b202f2396de1f9e39a1b0172"
}

�����ļ�����
�ļ������ϴ�����
�ӿ�˵��
�����ڱ����ļ��ϴ������ĳ�������ͨ���˽ӿ����������ļ��ϴ����ӣ��ϴ��ļ���ϵͳ���Զ��ύ�������� ע�⣺

������ļ��ϴ�������Ч��Ϊ 24 Сʱ��������Ч��������ļ��ϴ�
�ϴ��ļ�ʱ���������� Content-Type ����ͷ
�ļ��ϴ���ɺ���������ύ��������ӿڡ�ϵͳ���Զ�ɨ�����ϴ�����ļ��Զ��ύ��������
�����������Ӳ��ܳ��� 200 ��
headerͷ����Ҫ���� Authorization �ֶΣ���ʽΪ Bearer + �ո� + Token
Python ����ʾ��
import requests

token = "���������api token"
url = "https://mineru.net/api/v4/file-urls/batch"
header = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {token}"
}
data = {
    "enable_formula": True,
    "language": "ch",
    "enable_table": True,
    "files": [
        {"name":"demo.pdf", "is_ocr": True, "data_id": "abcd"}
    ]
}
file_path = ["demo.pdf"]
try:
    response = requests.post(url,headers=header,json=data)
    if response.status_code == 200:
        result = response.json()
        print('response success. result:{}'.format(result))
        if result["code"] == 0:
            batch_id = result["data"]["batch_id"]
            urls = result["data"]["file_urls"]
            print('batch_id:{},urls:{}'.format(batch_id, urls))
            for i in range(0, len(urls)):
                with open(file_path[i], 'rb') as f:
                    res_upload = requests.put(urls[i], data=f)
                    if res_upload.status_code == 200:
                        print(f"{urls[i]} upload success")
                    else:
                        print(f"{urls[i]} upload failed")
        else:
            print('apply upload url failed,reason:{}'.format(result.msg))
    else:
        print('response not success. status:{} ,result:{}'.format(response.status_code, response))
except Exception as err:
    print(err)

CURL ����ʾ��
curl --location --request POST 'https://mineru.net/api/v4/file-urls/batch' \
--header 'Authorization: Bearer ***' \
--header 'Content-Type: application/json' \
--header 'Accept: */*' \
--data-raw '{
    "enable_formula": true,
    "language": "ch",
    "enable_table": true,
    "files": [
        {"name":"demo.pdf", "is_ocr": true, "data_id": "abcd"}
    ]
}'

CURL �ļ��ϴ�ʾ��
curl -X PUT -T /path/to/your/file.pdf 'https://****'

���������˵��
����	����	�Ƿ��ѡ	ʾ��	����
enable_formula	bool	��	true	�Ƿ�����ʽʶ��Ĭ�� true
enable_table	bool	��	true	�Ƿ������ʶ��Ĭ�� true
language	string	��	ch	ָ���ĵ����ԣ�Ĭ�� ch��������ѡֵ�б������https://www.paddleocr.ai/latest/en/version3.x/algorithm/PP-OCRv5/PP-OCRv5_multi_languages.html#4-supported-languages-and-abbreviations
file.?name	string	��	demo.pdf	�ļ�����֧��.pdf��.doc��.docx��.ppt��.pptx��.png��.jpg��.jpeg���ָ�ʽ
file.is_ocr	bool	��	true	�Ƿ����� ocr ���ܣ�Ĭ�� false
file.data_id	string	��	abc**	���������Ӧ������ ID���ɴ�СдӢ����ĸ�����֡��»��ߣ�_�����̻��ߣ�-����Ӣ�ľ�ţ�.����ɣ������� 128 ���ַ�����������Ψһ��ʶ����ҵ�����ݡ�
file.page_ranges	string	��	1-600	ָ��ҳ�뷶Χ����ʽΪ���ŷָ����ַ��������磺"2,4-6"����ʾѡȡ��2ҳ����4ҳ����6ҳ������4��6�����Ϊ [2,4,5,6]����"2--2"����ʾ�ӵ�2ҳһֱѡȡ�������ڶ�ҳ������"-2"��ʾ�����ڶ�ҳ����
callback	string	��	http://127.0.0.1/callback	��������ص�֪ͨ���� URL��֧��ʹ�� HTTP �� HTTPS Э��ĵ�ַ�����ֶ�Ϊ��ʱ�������붨ʱ��ѯ���������callback �ӿڱ���֧�� POST ������UTF-8 ���롢Content-Type:application/json �������ݣ��Լ����� checksum �� content�������ӿڰ������¹���͸�ʽ���� checksum �� content���������� callback �ӿڷ��ؼ������
checksum���ַ�����ʽ�����û� uid + seed + content ƴ���ַ�����ͨ�� SHA256 �㷨���ɡ��û� UID�����ڸ������Ĳ�ѯ��Ϊ���۸ģ��������ڻ�ȡ�����ͽ��ʱ���������㷨�����ַ������� checksum ��һ��У�顣
content��JSON �ַ�����ʽ�������н�����ת�� JSON ���󡣹��� content �����ʾ������μ������ѯ����ķ���ʾ������Ӧ�����ѯ����� data ���֡�
˵��:���ķ���� callback �ӿ��յ� Mineru �����������͵Ľ����������ص� HTTP ״̬��Ϊ 200�����ʾ���ճɹ��������� HTTP ״̬�����Ϊ����ʧ�ܡ�����ʧ��ʱ��mineru ������ظ����� 5 �μ������ֱ�����ճɹ����ظ����� 5 �κ���δ���ճɹ����������ͣ���������� callback �ӿڵ�״̬��
seed	string	��	abc**	����ַ�������ֵ���ڻص�֪ͨ�����е�ǩ������Ӣ����ĸ�����֡��»��ߣ�_����ɣ������� 64 ���ַ��������Զ��壬�����ڽ��յ����ݰ�ȫ�Ļص�֪ͨʱУ�������� Mineru ����������
˵��:��ʹ�� callback ʱ�����ֶα����ṩ��
extra_formats	[string]	��	["docx","html"]	markdown��jsonΪĬ�ϵ�����ʽ���������ã��ò�����֧��docx��html��latex���ָ�ʽ�е�һ������
model_version	string	��	vlm	mineruģ�Ͱ汾������ѡ��:pipeline��vlm��Ĭ��pipeline��
������ʾ��
{
  "enable_formula": true,
  "language": "ch",
  "enable_table": true,
  "files": [{ "name": "demo.pdf", "is_ocr": true, "data_id": "abcd" }]
}

��Ӧ����˵��
����	����	ʾ��	˵��
code	int	0	�ӿ�״̬�룬�ɹ��� 0
msg	string	ok	�ӿڴ�����Ϣ���ɹ���"ok"
trace_id	string	c876cd60b202f2396de1f9e39a1b0172	���� ID
data.batch_id	string	2bb2f0ec-a336-4a0a-b61a-****	������ȡ���� id��������������ѯ�������
data.files	[string]	["https://mineru.oss-cn-shanghai.aliyuncs.com/api-upload/***"]	�ļ��ϴ�����
��Ӧʾ��
{
  "code": 0,
  "data": {
    "batch_id": "2bb2f0ec-a336-4a0a-b61a-241afaf9cc87",
    "file_urls": [
        "https://***"
    ]
  }
  "msg": "ok",
  "trace_id": "c876cd60b202f2396de1f9e39a1b0172"
}

url �����ϴ�����
�ӿ�˵��
������ͨ�� API ����������ȡ����ĳ��� ע�⣺

�����������Ӳ��ܳ��� 200 ��
�ļ���С���ܳ��� 200MB,�ļ�ҳ�������� 600 ҳ
���������ƣ�github��aws �ȹ��� URL ������ʱ
headerͷ����Ҫ���� Authorization �ֶΣ���ʽΪ Bearer + �ո� + Token
Python ����ʾ��
import requests

token = "���������api token"
url = "https://mineru.net/api/v4/extract/task/batch"
header = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {token}"
}
data = {
    "enable_formula": True,
    "language": "ch",
    "enable_table": True,
    "files": [
        {"url":"https://cdn-mineru.openxlab.org.cn/demo/example.pdf", "is_ocr": True, "data_id": "abcd"}
    ]
}
try:
    response = requests.post(url,headers=header,json=data)
    if response.status_code == 200:
        result = response.json()
        print('response success. result:{}'.format(result))
        if result["code"] == 0:
            batch_id = result["data"]["batch_id"]
            print('batch_id:{}'.format(batch_id))
        else:
            print('submit task failed,reason:{}'.format(result.msg))
    else:
        print('response not success. status:{} ,result:{}'.format(response.status_code, response))
except Exception as err:
    print(err)

CURL ����ʾ��
curl --location --request POST 'https://mineru.net/api/v4/extract/task/batch' \
--header 'Authorization: Bearer ***' \
--header 'Content-Type: application/json' \
--header 'Accept: */*' \
--data-raw '{
    "enable_formula": true,
    "language": "ch",
    "enable_table": true,
    "files": [
        {"url":"https://cdn-mineru.openxlab.org.cn/demo/example.pdf", "is_ocr": true, "data_id": "abcd"}
    ]
}'

���������˵��
����	����	�Ƿ��ѡ	ʾ��	����
enable_formula	bool	��	true	�Ƿ�����ʽʶ��Ĭ�� true
enable_table	bool	��	true	�Ƿ������ʶ��Ĭ�� true
language	string	��	ch	ָ���ĵ����ԣ�Ĭ�� ch��������ѡֵ�б������https://www.paddleocr.ai/latest/en/version3.x/algorithm/PP-OCRv5/PP-OCRv5_multi_languages.html#4-supported-languages-and-abbreviations
file.url	string	��	demo.pdf	�ļ����ӣ�֧��.pdf��.doc��.docx��.ppt��.pptx��.png��.jpg��.jpeg���ָ�ʽ
file.is_ocr	bool	��	true	�Ƿ����� ocr ���ܣ�Ĭ�� false
file.data_id	string	��	abc**	���������Ӧ������ ID���ɴ�СдӢ����ĸ�����֡��»��ߣ�_�����̻��ߣ�-����Ӣ�ľ�ţ�.����ɣ������� 128 ���ַ�����������Ψһ��ʶ����ҵ�����ݡ�
file.page_ranges	string	��	1-600	ָ��ҳ�뷶Χ����ʽΪ���ŷָ����ַ��������磺"2,4-6"����ʾѡȡ��2ҳ����4ҳ����6ҳ������4��6�����Ϊ [2,4,5,6]����"2--2"����ʾ�ӵ�2ҳһֱѡȡ�������ڶ�ҳ������"-2"��ʾ�����ڶ�ҳ����
callback	string	��	http://127.0.0.1/callback	��������ص�֪ͨ���� URL��֧��ʹ�� HTTP �� HTTPS Э��ĵ�ַ�����ֶ�Ϊ��ʱ�������붨ʱ��ѯ���������callback �ӿڱ���֧�� POST ������UTF-8 ���롢Content-Type:application/json �������ݣ��Լ����� checksum �� content�������ӿڰ������¹���͸�ʽ���� checksum �� content���������� callback �ӿڷ��ؼ������
checksum���ַ�����ʽ�����û� uid + seed + content ƴ���ַ�����ͨ�� SHA256 �㷨���ɡ��û� UID�����ڸ������Ĳ�ѯ��Ϊ���۸ģ��������ڻ�ȡ�����ͽ��ʱ���������㷨�����ַ������� checksum ��һ��У�顣
content��JSON �ַ�����ʽ�������н�����ת�� JSON ���󡣹��� content �����ʾ������μ������ѯ����ķ���ʾ������Ӧ�����ѯ����� data ���֡�
˵��:���ķ���� callback �ӿ��յ� Mineru �����������͵Ľ����������ص� HTTP ״̬��Ϊ 200�����ʾ���ճɹ��������� HTTP ״̬�����Ϊ����ʧ�ܡ�����ʧ��ʱ��mineru ������ظ����� 5 �μ������ֱ�����ճɹ����ظ����� 5 �κ���δ���ճɹ����������ͣ���������� callback �ӿڵ�״̬��
seed	string	��	abc**	����ַ�������ֵ���ڻص�֪ͨ�����е�ǩ������Ӣ����ĸ�����֡��»��ߣ�_����ɣ������� 64 ���ַ��������Զ��壬�����ڽ��յ����ݰ�ȫ�Ļص�֪ͨʱУ�������� Mineru ����������
˵������ʹ�� callback ʱ�����ֶα����ṩ��
extra_formats	[string]	��	["docx","html"]	markdown��jsonΪĬ�ϵ�����ʽ���������ã��ò�����֧��docx��html��latex���ָ�ʽ�е�һ������
model_version	string	��	vlm	mineruģ�Ͱ汾������ѡ��:pipeline��vlm��Ĭ��pipeline��
������ʾ��
{
    "enable_formula": true,
    "language": "ch",
    "enable_table": true,
    "files": [
        {"url":"https://cdn-mineru.openxlab.org.cn/demo/example.pdf", "is_ocr": true, "data_id": "abcd"}
    ]
}

��Ӧ����˵��
����	����	ʾ��	˵��
code	int	0	�ӿ�״̬�룬�ɹ���0
msg	string	ok	�ӿڴ�����Ϣ���ɹ���"ok"
trace_id	string	c876cd60b202f2396de1f9e39a1b0172	���� ID
data.batch_id	string	2bb2f0ec-a336-4a0a-b61a-****	������ȡ���� id��������������ѯ�������
��Ӧʾ��
{
  "code": 0,
  "data": {
    "batch_id": "2bb2f0ec-a336-4a0a-b61a-241afaf9cc87"
  },
  "msg": "ok",
  "trace_id": "c876cd60b202f2396de1f9e39a1b0172"
}

������ȡ������
�ӿ�˵��
ͨ�� batch_id ������ѯ��ȡ����Ľ��ȡ�

Python ����ʾ��
import requests

token = "���������api token"
url = f"https://mineru.net/api/v4/extract-results/batch/{batch_id}"
header = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {token}"
}

res = requests.get(url, headers=header)
print(res.status_code)
print(res.json())
print(res.json()["data"])

CURL ����ʾ��
curl --location --request GET 'https://mineru.net/api/v4/extract-results/batch/{batch_id}' \
--header 'Authorization: Bearer *****' \
--header 'Accept: */*'

��Ӧ����˵��
����	����	ʾ��	˵��
code	int	0	�ӿ�״̬�룬�ɹ���0
msg	string	ok	�ӿڴ�����Ϣ���ɹ���"ok"
trace_id	string	c876cd60b202f2396de1f9e39a1b0172	���� ID
data.batch_id	string	2bb2f0ec-a336-4a0a-b61a-241afaf9cc87	batch_id
data.extract_result.file_name	string	demo.pdf	�ļ���
data.extract_result.state	string	done	������״̬�����:done��waiting-file: �ȴ��ļ��ϴ��Ŷ��ύ���������У�pending: �Ŷ��У�running: ���ڽ�����failed������ʧ�ܣ�converting����ʽת����
data.extract_result.full_zip_url	string	https://cdn-mineru.openxlab.org.cn/pdf/018e53ad-d4f1-475d-b380-36bf24db9914.zip	�ļ��������ѹ����
data.extract_result.err_msg	string	�ļ���ʽ��֧�֣����ϴ�����Ҫ����ļ�����	����ʧ��ԭ�򣬵� state=failed ʱ����Ч
data.extract_result.data_id	string	abc**	���������Ӧ������ ID��
˵��������ڽ�����������д����� data_id����˴����ض�Ӧ�� data_id��
data.extract_result.extract_progress.extracted_pages	int	1	�ĵ��ѽ���ҳ������state=runningʱ��Ч
data.extract_result.extract_progress.start_time	string	2025-01-20 11:43:20	�ĵ�������ʼʱ�䣬��state=runningʱ��Ч
data.extract_result.extract_progress.total_pages	int	2	�ĵ���ҳ������state=runningʱ��Ч
��Ӧʾ��
{
  "code": 0,
  "data": {
    "batch_id": "2bb2f0ec-a336-4a0a-b61a-241afaf9cc87",
    "extract_result": [
      {
        "file_name": "example.pdf",
        "state": "done",
        "err_msg": "",
        "full_zip_url": "https://cdn-mineru.openxlab.org.cn/pdf/018e53ad-d4f1-475d-b380-36bf24db9914.zip"
      },
      {
        "file_name":"demo.pdf",
        "state": "running",
        "err_msg": "",
        "extract_progress": {
          "extracted_pages": 1,
          "total_pages": 2,
          "start_time": "2025-01-20 11:43:20"
        }
      }
    ]
  },
  "msg": "ok",
  "trace_id": "c876cd60b202f2396de1f9e39a1b0172"
}

����������
������	˵��	�������
A0202	Token ����	��� Token �Ƿ���ȷ�������Ƿ���Bearerǰ׺ ���߸����� Token
A0211	Token ����	������ Token
-500	���δ���	��ȷ���������ͼ�Content-Type��ȷ
-10001	�����쳣	���Ժ�����
-10002	�����������	������������ʽ
-60001	�����ϴ� URL ʧ�ܣ����Ժ�����	���Ժ�����
-60002	��ȡƥ����ļ���ʽʧ��	����ļ�����ʧ�ܣ�������ļ����������д�����ȷ�ĺ�׺�������ļ�Ϊ pdf,doc,docx,ppt,pptx,png,jp(e)g �е�һ��
-60003	�ļ���ȡʧ��	�����ļ��Ƿ��𻵲������ϴ�
-60004	���ļ�	���ϴ���Ч�ļ�
-60005	�ļ���С��������	����ļ���С�����֧�� 200MB
-60006	�ļ�ҳ����������	�����ļ�������
-60007	ģ�ͷ�����ʱ������	���Ժ����Ի���ϵ����֧��
-60008	�ļ���ȡ��ʱ	��� URL �ɷ���
-60009	�����ύ��������	���Ժ�����
-60010	����ʧ��	���Ժ�����
-60011	��ȡ��Ч�ļ�ʧ��	��ȷ���ļ����ϴ�
-60012	�Ҳ�������	��ȷ��task_id��Ч��δɾ��
-60013	û��Ȩ�޷��ʸ�����	ֻ�ܷ����Լ��ύ������
-60014	ɾ�������е�����	�����е������ݲ�֧��ɾ��
-60015	�ļ�ת��ʧ��	�����ֶ�תΪpdf���ϴ�
-60016	�ļ�ת��ʧ��	�ļ�ת��Ϊָ����ʽʧ�ܣ����Գ���������ʽ����������
�����ļ�����
������������
�ӿ�˵��
Python ����ʾ��
CURL ����ʾ��
���������˵��
������ʾ��
��Ӧ����˵��
��Ӧʾ��
��ȡ������
�ӿ�˵��
Python ����ʾ��
CURL ����ʾ��
��Ӧ����˵��
��Ӧʾ��
�����ļ�����
�ļ������ϴ�����
�ӿ�˵��
Python ����ʾ��
CURL ����ʾ��
CURL �ļ��ϴ�ʾ��
���������˵��
������ʾ��
��Ӧ����˵��
��Ӧʾ��
url �����ϴ�����
�ӿ�˵��
Python ����ʾ��
CURL ����ʾ��
���������˵��
������ʾ��
��Ӧ����˵��
��Ӧʾ��
������ȡ������
�ӿ�˵��
Python ����ʾ��
CURL ����ʾ��
��Ӧ����˵��
��Ӧʾ��
����������