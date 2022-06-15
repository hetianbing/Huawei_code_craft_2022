from read_file import *
from heapq import *
from functions import *
import time

import matplotlib.pyplot as plt

debug_print = True

input_data = Input_datas('data')

site_history_arr = [[0 for j in range(input_data.all_times)] for i in range(input_data.site_cnt)]

output_path = 'output/solution.txt'

f = open(output_path)  # 返回一个文件对象
line = f.readline()  # 调用文件的 readline()方法

client_name_index = 0
times_index = 0

temp_client_sum = 0

is_test_res_ok = True


while line:
    # print(line, end = '') # 在 Python 3 中使用
    C_Ss = line.split(':')
    if len(C_Ss) != 2:
        print('error !')
        print(line)
        is_test_res_ok = False
        break
    if C_Ss[0] !=  input_data.client_names[client_name_index]:
        print('error - client names error ')
        print(line)
        print('client name is ', C_Ss[0])
        print(input_data.client_names[client_name_index])
        is_test_res_ok = False
        break

    depart_arr = C_Ss[1].split('>')
    temp_client_sum = 0
    for ever in depart_arr:
        dp = ever.lstrip(',<').split(',')
        if ever == '\n' or ever == '\r\n' or ever == '':
            continue
        if dp[0] not in input_data.site_names:
            print('error - site names error ')
            print(line)
            print('dp is', dp)
            print('site name is', dp[0])
            print(input_data.site_names)
            is_test_res_ok = False
            break
        request = int(dp[1])
        temp_client_sum += request
        site_index = input_data.site_names.index(dp[0])

        # check is connect
        if not input_data.bool_site_client[site_index][client_name_index]:
            print('error - site client not connect ')
            print(line)
            print('site name is', dp[0])
            is_test_res_ok = False
            break
        site_history_arr[site_index][times_index] += request
        # check site req is over to site max
        if site_history_arr[site_index][times_index] > input_data.site_max[site_index]:
            print(f'error - site {input_data.site_names[site_index]} over max ')
            print(site_history_arr[site_index][times_index])
            print(input_data.site_max[site_index])
            # print(line)
            is_test_res_ok = False
            break

    if not is_test_res_ok:
        break

    # check client is equal to client request
    if temp_client_sum != input_data.time_client_request[times_index][client_name_index]:
        print('error - client sum not equal to client request')
        print(temp_client_sum)
        print(input_data.time_client_request[times_index][input_data.client_cnt - 1])
        is_test_res_ok = False
        break

    line = f.readline()
    client_name_index += 1
    if client_name_index == input_data.client_cnt:
        client_name_index = 0
        times_index += 1

f.close()

if is_test_res_ok:
    print('\n--------------------------------\nres success!')
else:
    print('\n--------------------------------\nres error!')



res_index = input_data.all_times * 95 // 100
if input_data.all_times * 95 % 100 != 0:
    res_index += 1
res_index -= 1
print('final get index = ', res_index)

ans = 0


debug_draw_pic = True
if debug_draw_pic:
    # 多层柱状图
    fig, ax = plt.subplots(figsize=(10, 7))
    colors = ['res', 'green', 'blue']

for ever_list in site_history_arr:
    ever_list.sort()
    temp = ever_list[res_index]
    ans += temp
    # plt.plot([i for i in range(len(ever_list))], ever_list)
    if debug_draw_pic:
        ax.bar([i for i in range(len(ever_list))], ever_list)

if debug_draw_pic:
    ax.legend()
    plt.show()

print('final ans is ', ans)
























