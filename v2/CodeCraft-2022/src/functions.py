#coding=utf-8
from node_class import *
from heapq import *
import time as t_time
import _thread

import sys,platform

def set_env():
    # set env
    if platform.system() == 'Windows':
        output_path = '../../../v2/output'
        input_path = '../../../v1/code/CodeCraft-2022/src/data'
    else:
        output_path = '/output'
        input_path = '/data'
    return output_path, input_path

def set_site_arr(input_data):
    site_arr = []
    for i in range(input_data.site_cnt):
        new_site = SITE()
        new_site.name = input_data.site_names[i]
        new_site.max_q = input_data.site_max[i]
        for j in range(input_data.client_cnt):
            if input_data.bool_site_client[i][j]:
                new_site.sons_index.append(j)
        new_site.sons_cnt = len(new_site.sons_index)
        site_arr.append(new_site)
    return site_arr


def set_client_arr(input_data):
    client_arr = []
    for i in range(input_data.client_cnt):
        new_client = MY_CLIENT()
        new_client.name = input_data.client_names[i]
        for j in range(input_data.site_cnt):
            if input_data.bool_site_client[j][i]:
                new_client.fathers_index.append(j)
        # print(new_client.fathers_index)
        new_client.father_cnt = len(new_client.fathers_index)
        client_arr.append(new_client)
    return client_arr


def get_max_datas(input_data):
    # final use time
    if input_data.all_times * 95 % 100 == 0:
        final_time = input_data.all_times * 95 // 100
    else:
        final_time = input_data.all_times * 95 // 100 + 1

    every_site_biggest_cnt = input_data.all_times - final_time

    average_max = every_site_biggest_cnt * input_data.site_cnt // input_data.all_times
    extr_max_cnt = every_site_biggest_cnt * input_data.site_cnt % input_data.all_times
    if extr_max_cnt != 0:
        average_max += 1

    return every_site_biggest_cnt, average_max

def get_max_90(input_data):
    # final use time
    if input_data.all_times * 90 % 100 == 0:
        final_time = input_data.all_times * 90 // 100
    else:
        final_time = input_data.all_times * 90 // 100 + 1

    every_site_biggest_cnt = input_data.all_times - final_time


    return every_site_biggest_cnt





# 重构版本
def process_little(input_data, every_site_biggest_cnt, site_arr, client_arr, origin_time_client_site):
    for tmp_time in range(input_data.all_times):
        here_client_stream_req = input_data.time_client_stream_req[tmp_time]

        ans_arr = [[-1 for i in range(input_data.time_stream_cnt[tmp_time])] for j in range(input_data.client_cnt)]

        sorted_client = []

        for i in range(input_data.client_cnt):
            client_arr[i].left_request = 0
            client_arr[i].req_list = []
            for st_idx in range(input_data.time_stream_cnt[tmp_time]):
                client_arr[i].req_list.append([here_client_stream_req[i][st_idx], st_idx])
                client_arr[i].left_request += here_client_stream_req[i][st_idx]
            sorted_client.append([client_arr[i].left_request, i])
            client_arr[i].req_list.sort()

        for i in range(input_data.site_cnt):
            site_arr[i].now_q = 0

        sorted_client.sort()


        while len(sorted_client) != 0:
            i = sorted_client.pop()[1]

            site_heap = []
            # base_cost
            for j in client_arr[i].fathers_index:
                heappush(site_heap,
                         [(site_arr[j].now_q - input_data.base_cost) * (1 - 1 / (site_arr[j].max_q + 1)),
                          j,
                          site_arr[j].max_q - site_arr[j].now_q])

            temp_site_heap = []

            while len(client_arr[i].req_list) != 0:
                [r, idx] = client_arr[i].req_list.pop()
                if r == 0:
                    continue

                while len(site_heap) != 0 and site_heap[0][2] < r:
                    temp_site_heap.append(heappop(site_heap))

                if len(site_heap) == 0:
                    print('error, cant over!')
                    bb = 0
                    ans = 1 // bb
                    exit()

                j = heappop(site_heap)[1]

                ans_arr[i][idx] = j
                site_arr[j].now_q += r
                if site_arr[j].now_q != site_arr[j].max_q:
                    heappush(site_heap,
                             [(site_arr[j].now_q - input_data.base_cost) * (1 - 1 / (site_arr[j].max_q + 1)),
                              j,
                              site_arr[j].max_q - site_arr[j].now_q])

            while len(temp_site_heap) != 0:
                heappush(site_heap, temp_site_heap.pop())

        origin_time_client_site.append(ans_arr)

        for i in range(input_data.site_cnt):
            site_arr[i].history_req.append(site_arr[i].now_q)

    return


def write_into_file(origin_time_client_site, client_arr, site_arr, input_data, output_path):
    file_handle = open(f'{output_path}/solution.txt', mode='w')

    tmp_time = 0


    cnt_90 = 0
    for i in range(input_data.site_cnt):
        if site_arr[i].is_90:
            file_handle.write(site_arr[i].name)
            if cnt_90 != 9:
                file_handle.write(',')
            else:
                file_handle.write('\n')
            cnt_90 += 1

    for ans_arr in origin_time_client_site:
        for i in range(input_data.client_cnt):
            output_buffer = client_arr[i].name
            output_buffer += ':'
            temp_arr = []
            for j in range(input_data.time_stream_cnt[tmp_time]):
                if ans_arr[i][j] != -1:
                    temp_arr.append(f'<{site_arr[ans_arr[i][j]].name},{input_data.time_stream_name[tmp_time][j]}>')
            # print(output_buffer + ','.join(temp_arr))
            if i == input_data.client_cnt - 1 and tmp_time == input_data.all_times - 1:
                file_handle.write(output_buffer + ','.join(temp_arr))
            else:
                file_handle.write(output_buffer + ','.join(temp_arr) + '\n')
        tmp_time += 1

    file_handle.close()
    return



# 重构版本
def func_2(input_data, site_arr, client_arr, origin_time_client_site, every_site_biggest_cnt, max_90_cnt):
    # 记录所有时间，那些site节点被设置为最大值节点（即超过95分位）
    max_site_times_arr = [[] for i in range(input_data.all_times)]

    # 更新的时间-client需求表
    times_client_request = []
    for t in range(input_data.all_times):
        times_client_request.append([])
        for c in range(input_data.client_cnt):
            times_client_request[t].append([0])
            for s_idx in range(input_data.time_stream_cnt[t]):
                if input_data.time_client_stream_req[t][c][s_idx] != 0:
                    times_client_request[t][c].append(s_idx)
                    times_client_request[t][c][0] += input_data.time_client_stream_req[t][c][s_idx]


    # 每次设置完max之后实时更新
    history_time_site = [[site_arr[j].history_req[i] for j in range(input_data.site_cnt)] for i in range(input_data.all_times)]

    another_heap_90 = []

    myHeap = []
    for time in range(input_data.all_times):
        for s_i in range(input_data.site_cnt):
            heappush(myHeap, [-history_time_site[time][s_i] * site_arr[s_i].max_q, history_time_site[time][s_i], time, s_i])
            # heappush(myHeap, [-history_time_site[time][s_i], history_time_site[time][s_i], time, s_i])

    # 记录每个site剩余的可以设置为max的个数
    cnt_site_max = [every_site_biggest_cnt for i in range(input_data.site_cnt)]


    already = 0
    all_already_cnt = input_data.site_cnt * every_site_biggest_cnt

    while already < all_already_cnt:
        here = heappop(myHeap)
        while here[1] != history_time_site[here[2]][here[3]] or cnt_site_max[here[3]] == 0:

            if cnt_site_max[here[3]] != 0:
                here[1] = history_time_site[here[2]][here[3]]
                # here[0] = -here[1]
                here[0] = - site_arr[here[3]].max_q * here[1]
                heappush(myHeap, here)
            else:
                another_heap_90.append(here)
            here = heappop(myHeap)

        time, site_index = here[2], here[3]
        cnt_site_max[site_index] -= 1

        max_site_times_arr[time].append(site_index)

        # sum_req 是 当前的site 对应的全部的client， 他们的剩余需求之和
        sum_req = 0
        for i in site_arr[site_index].sons_index:
            sum_req += times_client_request[time][i][0]

        # 如果剩余的需求小于等于当前的最大值，那么可以直接用当前的site来包含全部的下属client
        if sum_req <= site_arr[site_index].max_q:
            # enough
            # print("here")
            for i in site_arr[site_index].sons_index:
                if times_client_request[time][i][0] == 0:
                    continue
                for stream_idx in times_client_request[time][i][1:]:
                    other_site_idx = origin_time_client_site[time][i][stream_idx]
                    history_time_site[time][other_site_idx] -= input_data.time_client_stream_req[time][i][stream_idx]
                    origin_time_client_site[time][i][stream_idx] = site_index
                    history_time_site[time][site_index] += input_data.time_client_stream_req[time][i][stream_idx]
                times_client_request[time][i] = [0]
        else:
            left_use = site_arr[site_index].max_q - history_time_site[time][site_index]
            need_re_f_sum = 0
            for i in site_arr[site_index].sons_index:
                if times_client_request[time][i][0] == 0:
                    continue
                tmp_arr = [0]
                while len(times_client_request[time][i]) > 1:
                    here_stridx = times_client_request[time][i].pop()
                    if origin_time_client_site[time][i][here_stridx] == site_index:
                        #本来就是的
                        continue
                    tmp_arr.append(here_stridx)
                    tmp_arr[0] += input_data.time_client_stream_req[time][i][here_stridx]
                times_client_request[time][i] = tmp_arr
                need_re_f_sum += tmp_arr[0]

            for i in site_arr[site_index].sons_index:
                if times_client_request[time][i][0] == 0:
                    continue
                tmp_arr = [0]
                here_max_sum = left_use * times_client_request[time][i][0] // need_re_f_sum
                before_use_max = here_max_sum
                while len(times_client_request[time][i]) > 1:
                    here_stridx = times_client_request[time][i].pop()
                    if input_data.time_client_stream_req[time][i][here_stridx] <= here_max_sum:
                        other_site = origin_time_client_site[time][i][here_stridx]
                        origin_time_client_site[time][i][here_stridx] = site_index
                        history_time_site[time][other_site] -= input_data.time_client_stream_req[time][i][here_stridx]
                        history_time_site[time][site_index] += input_data.time_client_stream_req[time][i][here_stridx]
                        here_max_sum -= input_data.time_client_stream_req[time][i][here_stridx]
                    else:
                        tmp_arr.append(here_stridx)
                        tmp_arr[0] += input_data.time_client_stream_req[time][i][here_stridx]
                need_re_f_sum -= times_client_request[time][i][0]
                left_use -= before_use_max - here_max_sum
                times_client_request[time][i] = tmp_arr

        already += 1


    is_90_choose = [False for i in range(input_data.site_cnt)]
    cnt_90_max = 0

    more_than_95 = max_90_cnt - every_site_biggest_cnt

    all_already_cnt = 10 * more_than_95
    already = 0


    for every_used in another_heap_90:
        heappush(myHeap, every_used)

    while already < all_already_cnt:
        here = heappop(myHeap)
        while here[1] != history_time_site[here[2]][here[3]] or cnt_site_max[here[3]] == 0:
            if here[1] == history_time_site[here[2]][here[3]] and cnt_90_max < 10 and not is_90_choose[here[3]]:
                # cnt_site_max[here[3]] == 0:
                cnt_90_max += 1
                is_90_choose[here[3]] = True
                cnt_site_max[here[3]] += more_than_95
                site_arr[here[3]].is_90 = True
                if cnt_site_max[here[3]] != 0:
                    break

            if cnt_site_max[here[3]] != 0:
                here[1] = history_time_site[here[2]][here[3]]
                # here[0] = -here[1]
                here[0] = - site_arr[here[3]].max_q * here[1]
                heappush(myHeap, here)
            here = heappop(myHeap)

        time, site_index = here[2], here[3]
        cnt_site_max[site_index] -= 1

        max_site_times_arr[time].append(site_index)

        # sum_req 是 当前的site 对应的全部的client， 他们的剩余需求之和
        sum_req = 0
        for i in site_arr[site_index].sons_index:
            sum_req += times_client_request[time][i][0]

        # 如果剩余的需求小于等于当前的最大值，那么可以直接用当前的site来包含全部的下属client
        if sum_req <= site_arr[site_index].max_q:
            # enough
            # print("here")
            for i in site_arr[site_index].sons_index:
                if times_client_request[time][i][0] == 0:
                    continue
                for stream_idx in times_client_request[time][i][1:]:
                    other_site_idx = origin_time_client_site[time][i][stream_idx]
                    history_time_site[time][other_site_idx] -= input_data.time_client_stream_req[time][i][stream_idx]
                    origin_time_client_site[time][i][stream_idx] = site_index
                    history_time_site[time][site_index] += input_data.time_client_stream_req[time][i][stream_idx]
                times_client_request[time][i] = [0]
        else:
            left_use = site_arr[site_index].max_q - history_time_site[time][site_index]
            need_re_f_sum = 0
            for i in site_arr[site_index].sons_index:
                if times_client_request[time][i][0] == 0:
                    continue
                tmp_arr = [0]
                while len(times_client_request[time][i]) > 1:
                    here_stridx = times_client_request[time][i].pop()
                    if origin_time_client_site[time][i][here_stridx] == site_index:
                        #本来就是的
                        continue
                    tmp_arr.append(here_stridx)
                    tmp_arr[0] += input_data.time_client_stream_req[time][i][here_stridx]
                times_client_request[time][i] = tmp_arr
                need_re_f_sum += tmp_arr[0]

            for i in site_arr[site_index].sons_index:
                if times_client_request[time][i][0] == 0:
                    continue
                tmp_arr = [0]
                here_max_sum = left_use * times_client_request[time][i][0] // need_re_f_sum
                before_use_max = here_max_sum
                while len(times_client_request[time][i]) > 1:
                    here_stridx = times_client_request[time][i].pop()
                    if input_data.time_client_stream_req[time][i][here_stridx] <= here_max_sum:
                        other_site = origin_time_client_site[time][i][here_stridx]
                        origin_time_client_site[time][i][here_stridx] = site_index
                        history_time_site[time][other_site] -= input_data.time_client_stream_req[time][i][here_stridx]
                        history_time_site[time][site_index] += input_data.time_client_stream_req[time][i][here_stridx]
                        here_max_sum -= input_data.time_client_stream_req[time][i][here_stridx]
                    else:
                        tmp_arr.append(here_stridx)
                        tmp_arr[0] += input_data.time_client_stream_req[time][i][here_stridx]
                need_re_f_sum -= times_client_request[time][i][0]
                left_use -= before_use_max - here_max_sum
                times_client_request[time][i] = tmp_arr

        already += 1


    for tt in range(input_data.all_times):
        adjust_v2(origin_time_client_site[tt],
                      max_site_times_arr[tt],
                      history_time_site[tt],
                      site_arr,
                      client_arr,
                      input_data,
                      tt)


    return



# 每行开始，每个client依次分配
def adjust_v2(ans_arr, max_site_arr, history_time_site_t, site_arr, client_arr, input_data, now_time):

    is_site_max = [False for i in range(input_data.site_cnt)]
    for s_i in max_site_arr:
        is_site_max[s_i] = True

    site_arr_now_q = history_time_site_t
    site_arr_fp_val = [0 for i in range(input_data.site_cnt)]

    wanted_all_zero = [False for i in range(input_data.site_cnt)]

    all_zero_site = []

    # 缺口数量
    cap_cnt = 0
    for i in range(input_data.site_cnt):
        if is_site_max[i]:
            # 有剩余是负数，是缺口
            val = site_arr_now_q[i] - site_arr[i].max_q
        else:
            val = site_arr_now_q[i] - input_data.base_cost
            if site_arr[i].is_all_max_and_zero:
                val = site_arr_now_q[i]
                all_zero_site.append(i)
                wanted_all_zero[i] = True

        site_arr_fp_val[i] = val

        if val < 0:
            cap_cnt += 1

    adjust_accrod_to_fp_val(ans_arr, max_site_arr, history_time_site_t, site_arr, client_arr, input_data, now_time,
                            site_arr_fp_val)

    over_site_cnt = 0
    for value in site_arr_fp_val:
        if value > 0:
            over_site_cnt += 1

    while over_site_cnt != 0 and len(all_zero_site) > 0:

        this_change_index = get_wanted_index(ans_arr, max_site_arr, history_time_site_t, site_arr, client_arr, input_data, now_time, site_arr_fp_val, wanted_all_zero)
        # print('get change = ', this_change_index)

        if this_change_index == -1:
            break

        site_arr[this_change_index].is_all_max_and_zero = False

        all_zero_site.remove(this_change_index)
        wanted_all_zero[this_change_index] = False

        site_arr_fp_val[this_change_index] -= input_data.base_cost

        adjust_accrod_to_fp_val(ans_arr, max_site_arr, history_time_site_t, site_arr, client_arr, input_data,
                                now_time, site_arr_fp_val)

        over_site_cnt = 0
        for value in site_arr_fp_val:
            if value > 0:
                over_site_cnt += 1



    # print('finish , nowtime is ', now_time, 'all_zero_cnt = ', len(all_zero_site))
    # print(site_arr_fp_val)

    return




def adjust_accrod_to_fp_val(ans_arr, max_site_arr, history_time_site_t, site_arr, client_arr, input_data, now_time, site_arr_fp_val):
    for i in range(input_data.client_cnt):
        site_list = client_arr[i].fathers_index
        if len(site_list) == 0:
            continue
        si_index = 0
        all_len = len(site_list)
        for j in range(input_data.time_stream_cnt[now_time]):
            if ans_arr[i][j] == -1:
                continue
            if site_arr_fp_val[ans_arr[i][j]] > 0:
                while si_index != all_len and site_arr_fp_val[site_list[si_index]] + input_data.time_client_stream_req[now_time][i][j] > 0:
                    si_index += 1
                if si_index == all_len:
                    break
                site_arr_fp_val[site_list[si_index]] += input_data.time_client_stream_req[now_time][i][j]
                site_arr_fp_val[ans_arr[i][j]] -= input_data.time_client_stream_req[now_time][i][j]
                ans_arr[i][j] = site_list[si_index]

    return







def get_wanted_index(ans_arr, max_site_arr, history_time_site_t, site_arr, client_arr, input_data, now_time, site_arr_fp_val, wanted_all_zero):
    # print('here, now_time = ', now_time)
    site_need_cnt_arr = [0 for i in range(input_data.site_cnt)]
    for i in range(input_data.client_cnt):
        is_need = False
        for j in range(input_data.time_stream_cnt[now_time]):
            if ans_arr[i][j] != -1 and site_arr_fp_val[ans_arr[i][j]] > 0:
                is_need = True
                break
        if is_need:
            for index in client_arr[i].fathers_index:
                if wanted_all_zero[index]:
                    site_need_cnt_arr[index] += 1

    max_index = -1
    for i in range(input_data.site_cnt):
        if site_need_cnt_arr[i] > 0:
            if max_index == -1 or site_need_cnt_arr[i] > site_need_cnt_arr[max_index]:
                max_index = i


    return max_index











