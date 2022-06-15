#coding=utf-8

from read_file import *
from node_class import *
from heapq import *
from functions import *
import time


start_time = time.time()

debug_print = True


# set env
output_path, input_path = set_env()

# input and output data
input_data = Input_datas(input_path)



spend_time = time.time() - start_time
print('read file: spend_time is ', spend_time)

# site数组和client数组
site_arr = set_site_arr(input_data)
client_arr = set_client_arr(input_data)

# 每个site最大次数，和平均每次的最大的site的个数
every_site_biggest_cnt, average_max = get_max_datas(input_data)

# 90分位
max_90_cnt = get_max_90(input_data)

origin_time_client_site = []
# 小规模场景，已经大规模场景的预处理
process_little(input_data, every_site_biggest_cnt, site_arr, client_arr, origin_time_client_site)


spend_time = time.time() - start_time
print('set little data: spend_time is ', spend_time)

if max_90_cnt >= 1:
    func_2(input_data, site_arr, client_arr, origin_time_client_site, every_site_biggest_cnt, max_90_cnt)


spend_time = time.time() - start_time
print('set biggest data: spend_time is ', spend_time)

write_into_file(origin_time_client_site, client_arr, site_arr, input_data, output_path)


spend_time = time.time() - start_time
print('write file: spend_time is ', spend_time)

# 重置时间
# input_data.reset_time()
#
# # 设置每次的最大的site数组
# max_site_times_arr, p_max_site_times_arr = set_max_turn_arr(input_data, every_site_biggest_cnt, site_arr, average_max)
# # 方式一 :final ans is  106300
# func_1(input_data, site_arr, client_arr, file_handle, max_site_times_arr, p_max_site_times_arr)
#
#
# 方式二 : 9609
# func_2(input_data, site_arr, client_arr, file_handle, origin_time_client_site, every_site_biggest_cnt)


#
# 方式三：每次都重新刷新全部值，出堆的时候和实时值不同的直接丢弃 --作废
# func_3(input_data, site_arr, client_arr, file_handle, origin_time_client_site, every_site_biggest_cnt)



#
# 方式四：每次新加max的时候，如果容量还有剩余，判断之前的max是否有不够分的情况。如果有，从共同的部分进行协调
# func_5(input_data, site_arr, client_arr, file_handle, origin_time_client_site, every_site_biggest_cnt, start_time)





spend_time = time.time() - start_time
print('spend_time is ', spend_time)
print('info:', 'C', input_data.client_cnt, 'S', input_data.site_cnt, 'T', input_data.all_times)




