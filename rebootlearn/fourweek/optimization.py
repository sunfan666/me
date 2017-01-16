#coding:utf-8
def statistics_file(file_name):
    res_dict = {}
    with open(file_name) as f:
        for line in f:
            if line =='\n':
                continue
            temp = line.split()
            tup = (temp[0],temp[6],temp[8])
            res_dict[tup] = res_dict.get(tup,0)+1
    return res_dict
def generate_html(res_list):
    html_str = '<table border="1">'
    tr_tmpl = '<tr><td>%s</td><td>%s</td><td>%s</td></tr>'
    html_str += tr_tmpl%('IP','staus','count')
    for (ip,status),count in  res_list[-10:]:
        html_str+=tr_tmpl%(ip,status,count)
    html_str+='</table>'
    with open('res111.html','w') as html_f:
        html_f.write(html_str)


res_dict = statistics_file('www_access_20140823.log')
res_list = sorted(res_dict.items(),key=lambda x:x[1])
generate_html(res_list)




