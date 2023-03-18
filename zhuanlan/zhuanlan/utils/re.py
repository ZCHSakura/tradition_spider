import re

aa = 'src="/uploadfile/201803/5/6212142732.jpg"'
print(aa)
bb = re.sub(r'src="/', "", aa)
print(bb)
