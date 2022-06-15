from node_class import *
from heapq import *
import time as t_time

import sys,platform

def set_env():
    # set env
    if platform.system() == 'Windows':
        output_path = 'output'
        input_path = 'data'
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




def process_little(input_data, every_site_biggest_cnt, site_arr, client_arr, file_handle, origin_time_client_site):
    tmp_debug_print = False
    while input_data.get_next_time():
        if tmp_debug_print:
            print("-------------------------------------------------------------------------------")
            print(input_data.now_time_client_request)

        ans_arr = [[0 for i in range(input_data.site_cnt)] for j in range(input_data.client_cnt)]
        temp_heap = []

        for i in range(input_data.client_cnt):
            client_arr[i].left_request = input_data.now_time_client_request[i]
            # client_arr[i].min_depart = client_arr[i].left_request / step
            # client_arr[i].show()
            heappush(temp_heap, [-client_arr[i].left_request, i])
        for i in range(input_data.site_cnt):
            site_arr[i].now_q = 0
            # site_arr[i].show()

        while len(temp_heap) != 0:
            aaa = heappop(temp_heap)
            i = aaa[1]
            sum_power = 0
            left_res = client_arr[i].left_request
            for j in client_arr[i].fathers_index:
                site_arr[j].last_power = (site_arr[j].max_q - site_arr[j].now_q)
                # site_arr[j].last_power = max(0, 1 - site_arr[j].now_q / site_arr[j].max_q - 0.01)
                sum_power += site_arr[j].last_power
            for j in client_arr[i].fathers_index:
                if j == client_arr[i].fathers_index[-1]:
                    ans_arr[i][j] = left_res
                    site_arr[j].now_q += left_res
                else:
                    ans_arr[i][j] = client_arr[i].left_request * site_arr[j].last_power // sum_power
                    site_arr[j].now_q += ans_arr[i][j]
                    left_res -= ans_arr[i][j]

        # before adjust
        if tmp_debug_print :
            print('\n---------------------------before adjust-------------------------------\nshow arr:')
            for i in range(input_data.client_cnt):
                print(ans_arr[i], end = '      sum = ')
                print(sum(ans_arr[i]))
            for j in range(input_data.site_cnt):
                tmp = 0
                for i in range(input_data.client_cnt):
                    tmp += ans_arr[i][j]
                print(tmp, end = '   ')
            print('\n----------------------------------------------------------:')

        if True:
            for i in range(input_data.client_cnt):
                # adjust for every line
                if input_data.now_time_client_request[i] == 0:
                    continue

                not_max_list = []
                over_max_list = []

                need_up_val = 0
                need_down_val = 0

                for j in range(input_data.site_cnt):
                    if ans_arr[i][j] != 0:
                        if site_arr[j].now_q > site_arr[j].history_max:
                            need_down_val += min(ans_arr[i][j], site_arr[j].now_q - site_arr[j].history_max)
                            over_max_list.append([min(ans_arr[i][j], site_arr[j].now_q - site_arr[j].history_max), j])
                        else:
                            need_up_val += site_arr[j].history_max - site_arr[j].now_q
                            not_max_list.append([site_arr[j].history_max - site_arr[j].now_q, j])
                if need_up_val >= need_down_val:
                    # good , all
                    if need_down_val != 0:
                        if tmp_debug_print:
                            print('adjust -- all down -- line ', i)
                        for j in range(input_data.site_cnt):
                            if ans_arr[i][j] != 0:
                                if site_arr[j].now_q > site_arr[j].history_max:
                                    one_down_val = min(ans_arr[i][j], site_arr[j].now_q - site_arr[j].history_max)
                                    ans_arr[i][j] -= one_down_val
                                    site_arr[j].now_q -= one_down_val
                                else:
                                    if need_up_val != 0:
                                        old_req = site_arr[j].now_q
                                        one_up_val = need_down_val * (site_arr[j].history_max - site_arr[j].now_q) // need_up_val
                                        ans_arr[i][j] += one_up_val
                                        site_arr[j].now_q += one_up_val
                                        need_down_val -= one_up_val
                                        need_up_val -= site_arr[j].history_max - old_req
                    else:
                        if tmp_debug_print:
                            print("all is lower than history max")
                else:
                    if tmp_debug_print:
                        print('not good, adjust step by step')
                        print(need_up_val, need_down_val)
                    if need_up_val == 0:
                        # no val can be up
                        if tmp_debug_print:
                            print('---no val can be up')
                    else:
                        if tmp_debug_print:
                            print('adjust - all up --line ', i)
                        for j in range(input_data.site_cnt):
                            if ans_arr[i][j] != 0:
                                if site_arr[j].now_q > site_arr[j].history_max:
                                    if need_down_val != 0:
                                        old_power = min(ans_arr[i][j], site_arr[j].now_q - site_arr[j].history_max)
                                        one_down_val = need_up_val * min(ans_arr[i][j], site_arr[j].now_q - site_arr[j].history_max) // need_down_val
                                        ans_arr[i][j] -= one_down_val
                                        site_arr[j].now_q -= one_down_val
                                        need_up_val -= one_down_val
                                        need_down_val -= old_power
                                else:
                                    one_up_val = site_arr[j].history_max - site_arr[j].now_q
                                    ans_arr[i][j] += one_up_val
                                    site_arr[j].now_q += one_up_val

        # after adjust
        if tmp_debug_print:
            print('\n---------------------------after adjust-------------------------------\nshow arr:')
            for i in range(input_data.client_cnt):
                print(ans_arr[i], end = '      sum = ')
                print(sum(ans_arr[i]))
            for j in range(input_data.site_cnt):
                tmp = 0
                for i in range(input_data.client_cnt):
                    tmp += ans_arr[i][j]
                print(tmp, end = '   ')
            print('\n----------------------------------------------------------:')

        # 直接写入的部分
        if every_site_biggest_cnt < 1:
            for i in range(input_data.client_cnt):
                output_buffer = client_arr[i].name
                output_buffer += ':'
                temp_arr = []
                for j in range(input_data.site_cnt):
                    if ans_arr[i][j] < 0:
                        print("error !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
                        print(ans_arr[i][j])
                    if ans_arr[i][j] != 0:
                        temp_arr.append(f'<{site_arr[j].name},{str(ans_arr[i][j])}>')
                # print(output_buffer + ','.join(temp_arr))
                if i == input_data.client_cnt - 1 and input_data.now_time == input_data.all_times - 1:
                    file_handle.write(output_buffer + ','.join(temp_arr))
                else:
                    file_handle.write(output_buffer + ','.join(temp_arr) + '\n')

        origin_time_client_site.append(ans_arr)

        for i in range(input_data.site_cnt):
            if site_arr[i].now_q > site_arr[i].history_max:
                site_arr[i].history_max = site_arr[i].now_q
            site_arr[i].history_req.append([site_arr[i].now_q, site_arr[i].times])
            site_arr[i].times += 1

    return




def set_max_turn_arr(input_data, every_site_biggest_cnt, site_arr, average_max):
    max_site_times_arr = [[] for i in range(input_data.all_times)]
    cnt_max = [every_site_biggest_cnt for i in range(input_data.site_cnt)]
    sort_max_arr = []
    for i in range(input_data.site_cnt):
        for j in range(input_data.all_times):
            sort_max_arr.append([-site_arr[i].history_req[j][0], i, j])
    sort_max_arr.sort()
    for [_req, i, j] in sort_max_arr:
        if cnt_max[i] == 0:
            continue
        if len(max_site_times_arr[j]) >= average_max:
            continue
        max_site_times_arr[j].append(i)
        cnt_max[i] -= 1
    p_max_site_times_arr = 0
    #
    # for ever in max_site_times_arr:
    #     print(ever)
    return max_site_times_arr, p_max_site_times_arr



def func_1(input_data, site_arr, client_arr, file_handle, max_site_times_arr, p_max_site_times_arr):
    """方式一，直接事先排列好，然后直接按照设置来进行"""
    here_debug_print = False
    while input_data.get_next_time():
        if here_debug_print:
            print("-------------------------------------------------------------------------------")
            print(input_data.now_time_client_request)

        ans_arr = [[0 for i in range(input_data.site_cnt)] for j in range(input_data.client_cnt)]
        temp_heap = []

        for i in range(input_data.client_cnt):
            client_arr[i].left_request = input_data.now_time_client_request[i]
            heappush(temp_heap, [-client_arr[i].left_request, i])
        for i in range(input_data.site_cnt):
            site_arr[i].now_q = 0

        max_site_list = max_site_times_arr[p_max_site_times_arr]
        p_max_site_times_arr += 1
        for i in max_site_list:
            site_arr[i].is_max_this_time = True

        # from max to min
        while len(temp_heap) != 0:
            aaa = heappop(temp_heap)
            i = aaa[1]
            sum_power = 0
            left_res = client_arr[i].left_request
            if left_res == 0:
                continue

            for j in client_arr[i].fathers_index:
                if site_arr[j].is_max_this_time:
                    site_arr[j].last_power = (site_arr[j].max_q - site_arr[j].now_q)
                    sum_power += site_arr[j].last_power

            if sum_power != 0:
                last_j = -1
                for j in client_arr[i].fathers_index:
                    if site_arr[j].is_max_this_time:
                        htb_a, htb_b, htb_c = min(left_res, site_arr[j].max_q - site_arr[j].now_q), site_arr[
                            j].now_q, left_res
                        ans_arr[i][j] = min(client_arr[i].left_request * site_arr[j].last_power // sum_power,
                                            site_arr[j].max_q - site_arr[j].now_q)
                        site_arr[j].now_q += ans_arr[i][j]
                        # ans_trans_f[i][j] += client_arr[i].min_depart * site_arr[j].last_power / sum_power
                        left_res -= ans_arr[i][j]
                        last_j = j
                if last_j != -1:
                    ans_arr[i][last_j] = htb_a
                    site_arr[last_j].now_q = htb_b + htb_a
                    left_res = htb_c - htb_a

                client_arr[i].left_request = left_res

            if left_res == 0:
                continue

            sum_power = 0
            for j in client_arr[i].fathers_index:
                if not site_arr[j].is_max_this_time:
                    site_arr[j].last_power = (site_arr[j].max_q - site_arr[j].now_q)
                    sum_power += site_arr[j].last_power

            if sum_power < left_res:
                print('error, sum_power < left_res')
                out = 0
                bb = 2 / out
            last_j = -1
            for j in client_arr[i].fathers_index:
                if not site_arr[j].is_max_this_time:
                    htb_a, htb_b, htb_c = min(left_res, site_arr[j].max_q - site_arr[j].now_q), site_arr[
                        j].now_q, left_res
                    ans_arr[i][j] = min(client_arr[i].left_request * site_arr[j].last_power // sum_power,
                                        site_arr[j].max_q - site_arr[j].now_q)
                    site_arr[j].now_q += ans_arr[i][j]
                    # ans_trans_f[i][j] += client_arr[i].min_depart * site_arr[j].last_power / sum_power
                    left_res -= ans_arr[i][j]
                    last_j = j
            if last_j != -1:
                ans_arr[i][last_j] = htb_a
                site_arr[last_j].now_q = htb_b + htb_a
                left_res = htb_c - htb_a

        if here_debug_print:
            print('\n----------------------------------------------------------\nshow arr:')
            for i in range(input_data.client_cnt):
                print(ans_arr[i], end='      sum = ')
                print(sum(ans_arr[i]))
            for j in range(input_data.site_cnt):
                tmp = 0
                for i in range(input_data.client_cnt):
                    tmp += ans_arr[i][j]
                print(tmp, end='   ')
            print('\n----------------------------------------------------------:')

        # write into file
        output_buffer = ''
        for i in range(input_data.client_cnt):
            output_buffer = client_arr[i].name
            output_buffer += ':'
            temp_arr = []
            for j in range(input_data.site_cnt):
                if ans_arr[i][j] < 0:
                    print("error !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
                    print(ans_arr[i][j])
                if ans_arr[i][j] != 0:
                    temp_arr.append(f'<{site_arr[j].name},{str(ans_arr[i][j])}>')
            # print(output_buffer + ','.join(temp_arr))
            if i == input_data.client_cnt - 1 and input_data.now_time == input_data.all_times - 1:
                file_handle.write(output_buffer + ','.join(temp_arr))
            else:
                file_handle.write(output_buffer + ','.join(temp_arr) + '\n')

        if here_debug_print:
            for i in range(input_data.site_cnt):
                tttt = 0
                for j in range(input_data.client_cnt):
                    tttt += ans_arr[j][i]
                if tttt > site_arr[i].max_q:
                    print('site: tttt = ', tttt, ' real = ', site_arr[i].max_q)

            for i in range(input_data.client_cnt):
                tttt = 0
                for j in range(input_data.site_cnt):
                    tttt += ans_arr[i][j]
                if tttt != input_data.now_time_client_request[i]:
                    print('client: tttt = ', tttt, ' real = ', input_data.now_time_client_request[i])

        # reset max_site
        if len(max_site_list) != 0:
            for i in max_site_list:
                site_arr[i].is_max_this_time = False
    return




def func_2(input_data, site_arr, client_arr, file_handle, origin_time_client_site, every_site_biggest_cnt):
    for t in origin_time_client_site:
        for i in t:
            for j in i:
                if j < 0:
                    print('input not correct')
                    return

    max_site_times_arr = [[] for i in range(input_data.all_times)]

    # 固定值（拉倒极限的部分)
    ter_arr = [[[0 for k in range(input_data.site_cnt)] for j in range(input_data.client_cnt)] for i in range(input_data.all_times)]

    # 更新的时间-client需求表
    times_client_request = []
    for t in range(input_data.all_times):
        times_client_request.append([])
        for c in range(input_data.client_cnt):
            times_client_request[t].append(input_data.time_client_request[t][c])

    # 每次设置完max之后实时更新
    history_time_site = [[site_arr[j].history_req[i][0] for j in range(input_data.site_cnt)] for i in range(input_data.all_times)]

    myHeap = []
    for time in range(input_data.all_times):
        for s_i in range(input_data.site_cnt):
            heappush(myHeap, [-history_time_site[time][s_i], time, s_i])

    cnt_site_max = [every_site_biggest_cnt for i in range(input_data.site_cnt)]

    # if True:
    #     ter_arr[0][0][0] = 199
    #     origin_time_client_site[0][0][0] = 200
    #     return


    already = 0
    while already < input_data.site_cnt * every_site_biggest_cnt:
        here = heappop(myHeap)
        while here[0] != -history_time_site[here[1]][here[2]] or cnt_site_max[here[2]] == 0:
            if cnt_site_max[here[2]] != 0:
                here[0] = -history_time_site[here[1]][here[2]]
                heappush(myHeap, here)
            here = heappop(myHeap)

        time, site_index = here[1], here[2]
        cnt_site_max[site_index] -= 1

        max_site_times_arr[time].append(site_index)

        # sum_req 是 当前的site 对应的全部的client， 他们的剩余需求之和
        sum_req = 0
        for i in site_arr[site_index].sons_index:
            sum_req += times_client_request[time][i]

        # 如果剩余的需求小于等于当前的最大值，那么可以直接用当前的site来包含全部的下属client
        if sum_req <= site_arr[site_index].max_q:
            # enough
            for i in site_arr[site_index].sons_index:
                for j in client_arr[i].fathers_index:
                    # 不管是不是，全部置为0
                    history_time_site[time][j] -= origin_time_client_site[time][i][j]
                    origin_time_client_site[time][i][j] = 0
                # full
                ter_arr[time][i][site_index] = times_client_request[time][i]
                times_client_request[time][i] = 0

            already += 1
            continue

        # print('here', 'time = ', time, 'site_index = ', site_index)

        # 按比例分配, 当前的不变，剩余的按比例分配
        # sum_power是权重，是 每一个client 根据他们 剩余的需求 和 在当前site之下的差 、的和
        sum_power = 0
        site_max = site_arr[site_index].max_q
        for i in site_arr[site_index].sons_index:
            sum_power += times_client_request[time][i] - origin_time_client_site[time][i][site_index]


        all_can_add_to = site_arr[site_index].max_q - history_time_site[time][site_index]
        for i in site_arr[site_index].sons_index:
            # 先求出每一行（每一个client）可以在当前site下增加多少；this_client_add
            if len(client_arr[i].fathers_index) <= 1:
                ter_arr[time][i][site_index] = origin_time_client_site[time][i][site_index]
                origin_time_client_site[time][i][site_index] = 0
                times_client_request[time][i] -= ter_arr[time][i][site_index]
                if times_client_request[time][i] < 0:
                    print('error -here 115')
                    return
                continue
            # sum_i_rest_site 是当前比重
            sum_i_rest_site = times_client_request[time][i] - origin_time_client_site[time][i][site_index]
            if sum_i_rest_site == 0:
                ter_arr[time][i][site_index] = origin_time_client_site[time][i][site_index]
                origin_time_client_site[time][i][site_index] = 0
                times_client_request[time][i] -= ter_arr[time][i][site_index]
                if times_client_request[time][i] < 0:
                    print('error -here 114')
                    return
                continue
            if sum_i_rest_site < 0:
                print('error !-- req < real')
                print(times_client_request[time])
                print(origin_time_client_site[time][i])
                print('i = ', i, 'site_index = ', site_index)
                bb = 0
                aa = 1 // bb
                exit()
            if i != site_arr[site_index].sons_index[-1]:
                this_client_add = sum_i_rest_site * all_can_add_to // sum_power
                sum_power -= sum_i_rest_site
                all_can_add_to -= this_client_add
            else:
                this_client_add = all_can_add_to
            ter_arr[time][i][site_index] = origin_time_client_site[time][i][site_index] + this_client_add
            origin_time_client_site[time][i][site_index] = 0
            times_client_request[time][i] -= ter_arr[time][i][site_index]
            if times_client_request[time][i] < 0:
                print('error -here 113')
                print(times_client_request[time][i],ter_arr[time][i][site_index])
                print(time, i, site_index)
                print(origin_time_client_site[time])
                print('this_client_add = ', this_client_add)
                return


            # 非site_index依次减少
            # 加权平分 this_client_add
            if this_client_add == 0:
                continue
            if this_client_add < 0:
                print('error --33')
                return
            for j in client_arr[i].fathers_index:
                if j == site_index:
                    continue
                if sum_i_rest_site == 0:
                    break
                if (j == client_arr[i].fathers_index[-2] and site_index == client_arr[i].fathers_index[-1]) or j == client_arr[i].fathers_index[-1]:
                    tmp_del = this_client_add
                    origin_time_client_site[time][i][j] -= tmp_del
                    if origin_time_client_site[time][i][j] < 0:
                        print('here-- 111')
                        print(tmp_del)
                        print(origin_time_client_site[time][i])
                        print(time,i,j)
                        return
                else:
                    tmp_del = origin_time_client_site[time][i][j] * this_client_add // sum_i_rest_site
                    sum_i_rest_site -= origin_time_client_site[time][i][j]
                    origin_time_client_site[time][i][j] -= tmp_del
                    this_client_add -= tmp_del
                    if origin_time_client_site[time][i][j] < 0:
                        print('here-- 112')
                        return
                history_time_site[time][j] -= tmp_del
                if history_time_site[time][j] < 0:
                    print('here -- 116')
            # if True:
            #     return # --v7 -运行失败
        #
        # if True:
        #     return
        #  -- v6 -运行失败
        already += 1
    # if True:
    #     return
    #  -- v5 -运行失败

    # 清除历史：history
    for s in range(input_data.site_cnt):
        site_arr[s].history_max = 0

    for t in range(input_data.all_times):
        for i in range(input_data.client_cnt):
            for j in range(input_data.site_cnt):
                origin_time_client_site[t][i][j] += ter_arr[t][i][j]
        for j in range(input_data.site_cnt):
            n_q = 0
            for i in range(input_data.client_cnt):
                n_q += origin_time_client_site[t][i][j]
            site_arr[j].now_q = n_q
        adjust_except_max(input_data, origin_time_client_site[t], max_site_times_arr[t], site_arr)

    # 清除历史：history
    for s in range(input_data.site_cnt):
        site_arr[s].history_max = 0
    for t in range(input_data.all_times):
        for j in range(input_data.site_cnt):
            n_q = 0
            for i in range(input_data.client_cnt):
                n_q += origin_time_client_site[t][i][j]
            site_arr[j].now_q = n_q
        adjust_to_max(input_data, origin_time_client_site[t], max_site_times_arr[t], site_arr)


    for t in range(input_data.all_times):
        for i in range(input_data.client_cnt):
            output_buffer = client_arr[i].name
            output_buffer += ':'
            temp_arr = []
            for j in range(input_data.site_cnt):
                val = origin_time_client_site[t][i][j]
                if val < 0:
                    print("error !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
                    print(val)
                if val != 0:
                    temp_arr.append(f'<{site_arr[j].name},{str(val)}>')
            # print(output_buffer + ','.join(temp_arr))
            if i == input_data.client_cnt - 1 and t == input_data.all_times - 1:
                file_handle.write(output_buffer + ','.join(temp_arr))
            else:
                file_handle.write(output_buffer + ','.join(temp_arr) + '\n')


    return


def adjust(input_data, ans_arr, max_list, site_arr):
    tmp_debug_print = False
    for i in range(input_data.client_cnt):
        # adjust for every line
        if input_data.now_time_client_request[i] == 0:
            continue

        not_max_list = []
        over_max_list = []

        need_up_val = 0
        need_down_val = 0

        for j in range(input_data.site_cnt):
            if ans_arr[i][j] != 0:
                if site_arr[j].now_q > site_arr[j].history_max:
                    need_down_val += min(ans_arr[i][j], site_arr[j].now_q - site_arr[j].history_max)
                    over_max_list.append([min(ans_arr[i][j], site_arr[j].now_q - site_arr[j].history_max), j])
                else:
                    need_up_val += site_arr[j].history_max - site_arr[j].now_q
                    not_max_list.append([site_arr[j].history_max - site_arr[j].now_q, j])
        if need_up_val >= need_down_val:
            # good , all
            if need_down_val != 0:
                if tmp_debug_print:
                    print('adjust -- all down -- line ', i)
                for j in range(input_data.site_cnt):
                    if ans_arr[i][j] != 0:
                        if site_arr[j].now_q > site_arr[j].history_max:
                            one_down_val = min(ans_arr[i][j], site_arr[j].now_q - site_arr[j].history_max)
                            ans_arr[i][j] -= one_down_val
                            site_arr[j].now_q -= one_down_val
                        else:
                            if need_up_val != 0:
                                old_req = site_arr[j].now_q
                                one_up_val = need_down_val * (
                                            site_arr[j].history_max - site_arr[j].now_q) // need_up_val
                                ans_arr[i][j] += one_up_val
                                site_arr[j].now_q += one_up_val
                                need_down_val -= one_up_val
                                need_up_val -= site_arr[j].history_max - old_req
            else:
                if tmp_debug_print:
                    print("all is lower than history max")
        else:
            if tmp_debug_print:
                print('not good, adjust step by step')
                print(need_up_val, need_down_val)
            if need_up_val == 0:
                # no val can be up
                if tmp_debug_print:
                    print('---no val can be up')
            else:
                if tmp_debug_print:
                    print('adjust - all up --line ', i)
                for j in range(input_data.site_cnt):
                    if ans_arr[i][j] != 0:
                        if site_arr[j].now_q > site_arr[j].history_max:
                            if need_down_val != 0:
                                old_power = min(ans_arr[i][j], site_arr[j].now_q - site_arr[j].history_max)
                                one_down_val = need_up_val * min(ans_arr[i][j], site_arr[j].now_q - site_arr[
                                    j].history_max) // need_down_val
                                ans_arr[i][j] -= one_down_val
                                site_arr[j].now_q -= one_down_val
                                need_up_val -= one_down_val
                                need_down_val -= old_power
                        else:
                            one_up_val = site_arr[j].history_max - site_arr[j].now_q
                            ans_arr[i][j] += one_up_val
                            site_arr[j].now_q += one_up_val

    for s_i in range(input_data.site_cnt):
        if s_i in max_list:
            continue
        sums = 0
        for i in range(input_data.client_cnt):
            sums += ans_arr[i][s_i]
        if sums > site_arr[s_i].history_max:
            site_arr[s_i].history_max = sums

def adjust_except_max(input_data, ans_arr, max_list, site_arr):
    tmp_debug_print = False

    for index in max_list:
        site_arr[index].is_max_this_time = True

    for i in range(input_data.client_cnt):
        # adjust for every line
        if input_data.now_time_client_request[i] == 0:
            continue

        not_max_list = []
        over_max_list = []

        need_up_val = 0
        need_down_val = 0

        for j in range(input_data.site_cnt):
            if site_arr[j].is_max_this_time:
                continue
            if ans_arr[i][j] != 0:
                if site_arr[j].now_q > site_arr[j].history_max:
                    need_down_val += min(ans_arr[i][j], site_arr[j].now_q - site_arr[j].history_max)
                    over_max_list.append([min(ans_arr[i][j], site_arr[j].now_q - site_arr[j].history_max), j])
                else:
                    need_up_val += site_arr[j].history_max - site_arr[j].now_q
                    not_max_list.append([site_arr[j].history_max - site_arr[j].now_q, j])
        if need_up_val >= need_down_val:
            # good , all
            if need_down_val != 0:
                if tmp_debug_print:
                    print('adjust -- all down -- line ', i)
                for j in range(input_data.site_cnt):
                    if site_arr[j].is_max_this_time:
                        continue
                    if ans_arr[i][j] != 0:
                        if site_arr[j].now_q > site_arr[j].history_max:
                            one_down_val = min(ans_arr[i][j], site_arr[j].now_q - site_arr[j].history_max)
                            ans_arr[i][j] -= one_down_val
                            site_arr[j].now_q -= one_down_val
                        else:
                            if need_up_val != 0:
                                old_req = site_arr[j].now_q
                                one_up_val = need_down_val * (
                                            site_arr[j].history_max - site_arr[j].now_q) // need_up_val
                                ans_arr[i][j] += one_up_val
                                site_arr[j].now_q += one_up_val
                                need_down_val -= one_up_val
                                need_up_val -= site_arr[j].history_max - old_req
            else:
                if tmp_debug_print:
                    print("all is lower than history max")
        else:
            if tmp_debug_print:
                print('not good, adjust step by step')
                print(need_up_val, need_down_val)
            if need_up_val == 0:
                # no val can be up
                if tmp_debug_print:
                    print('---no val can be up')
            else:
                if tmp_debug_print:
                    print('adjust - all up --line ', i)
                for j in range(input_data.site_cnt):
                    if site_arr[j].is_max_this_time:
                        continue
                    if ans_arr[i][j] != 0:
                        if site_arr[j].now_q > site_arr[j].history_max:
                            if need_down_val != 0:
                                old_power = min(ans_arr[i][j], site_arr[j].now_q - site_arr[j].history_max)
                                one_down_val = need_up_val * min(ans_arr[i][j], site_arr[j].now_q - site_arr[
                                    j].history_max) // need_down_val
                                ans_arr[i][j] -= one_down_val
                                site_arr[j].now_q -= one_down_val
                                need_up_val -= one_down_val
                                need_down_val -= old_power
                        else:
                            one_up_val = site_arr[j].history_max - site_arr[j].now_q
                            ans_arr[i][j] += one_up_val
                            site_arr[j].now_q += one_up_val


    for index in max_list:
        site_arr[index].is_max_this_time = False

    for s_i in range(input_data.site_cnt):
        if s_i in max_list:
            continue
        sums = 0
        for i in range(input_data.client_cnt):
            sums += ans_arr[i][s_i]
        if sums > site_arr[s_i].history_max:
            site_arr[s_i].history_max = sums


# 调整到最大的site中
def adjust_to_max(input_data, ans_arr, max_list, site_arr):
    tmp_debug_print = False

    for index in max_list:
        site_arr[index].is_max_this_time = True

    for i in range(input_data.client_cnt):
        # adjust for every line
        if input_data.now_time_client_request[i] == 0:
            continue

        not_max_list = []
        over_max_list = []

        need_up_val = 0
        need_down_val = 0

        for j in range(input_data.site_cnt):
            if site_arr[j].is_max_this_time:
                if site_arr[j].max_q - site_arr[j].now_q != 0 and input_data.bool_site_client[j][i]:
                    need_up_val += site_arr[j].max_q - site_arr[j].now_q
                    not_max_list.append([site_arr[j].history_max - site_arr[j].now_q, j])
            else:
                if site_arr[j].now_q - site_arr[j].history_max > 0:
                    need_down_val += min(ans_arr[i][j], site_arr[j].now_q - site_arr[j].history_max)
                    over_max_list.append([min(ans_arr[i][j], site_arr[j].now_q - site_arr[j].history_max), j])


        if need_up_val >= need_down_val:
            # good , all
            if need_down_val != 0:
                if tmp_debug_print:
                    print('adjust -- all down -- line ', i)
                for j in range(input_data.site_cnt):
                    if site_arr[j].is_max_this_time:
                        if need_up_val != 0 and site_arr[j].max_q - site_arr[j].now_q != 0 and input_data.bool_site_client[j][i]:
                            old_req = site_arr[j].now_q
                            one_up_val = need_down_val * (
                                    site_arr[j].max_q - site_arr[j].now_q) // need_up_val
                            ans_arr[i][j] += one_up_val
                            site_arr[j].now_q += one_up_val
                            need_down_val -= one_up_val
                            need_up_val -= site_arr[j].max_q - old_req
                    elif ans_arr[i][j] != 0:
                        if site_arr[j].now_q > site_arr[j].history_max:
                            one_down_val = min(ans_arr[i][j], site_arr[j].now_q - site_arr[j].history_max)
                            ans_arr[i][j] -= one_down_val
                            site_arr[j].now_q -= one_down_val
            else:
                if tmp_debug_print:
                    print("all is lower than history max")
        else:
            if tmp_debug_print:
                print('not good, adjust step by step')
                print(need_up_val, need_down_val)
            if need_up_val == 0:
                # no val can be up
                if tmp_debug_print:
                    print('---no val can be up')
            else:
                if tmp_debug_print:
                    print('adjust - all up --line ', i)
                for j in range(input_data.site_cnt):
                    if site_arr[j].is_max_this_time:
                        if input_data.bool_site_client[j][i]:
                            one_up_val = site_arr[j].max_q - site_arr[j].now_q
                            ans_arr[i][j] += one_up_val
                            site_arr[j].now_q += one_up_val
                    elif ans_arr[i][j] != 0:
                        if site_arr[j].now_q > site_arr[j].history_max:
                            if need_down_val != 0:
                                old_power = min(ans_arr[i][j], site_arr[j].now_q - site_arr[j].history_max)
                                one_down_val = need_up_val * min(ans_arr[i][j], site_arr[j].now_q - site_arr[
                                    j].history_max) // need_down_val
                                ans_arr[i][j] -= one_down_val
                                site_arr[j].now_q -= one_down_val
                                need_up_val -= one_down_val
                                need_down_val -= old_power



    for index in max_list:
        site_arr[index].is_max_this_time = False

    for s_i in range(input_data.site_cnt):
        if s_i in max_list:
            continue
        sums = 0
        for i in range(input_data.client_cnt):
            sums += ans_arr[i][s_i]
        if sums > site_arr[s_i].history_max:
            site_arr[s_i].history_max = sums







# 调整到最大的site中
def adjust_mix_all(input_data, ans_arr, max_list, site_arr):
    tmp_debug_print = False

    res_flag = False

    for index in max_list:
        site_arr[index].is_max_this_time = True

    for i in range(input_data.client_cnt):
        # adjust for every line
        if input_data.now_time_client_request[i] == 0:
            continue

        not_max_list = []
        over_max_list = []

        need_up_val = 0
        need_down_val = 0

        for j in range(input_data.site_cnt):
            if site_arr[j].is_max_this_time:
                if site_arr[j].max_q - site_arr[j].now_q != 0 and input_data.bool_site_client[j][i]:
                    need_up_val += site_arr[j].max_q - site_arr[j].now_q
                    not_max_list.append([site_arr[j].history_max - site_arr[j].now_q, j])
            else:
                if site_arr[j].now_q - site_arr[j].history_max < 0 and input_data.bool_site_client[j][i]:
                    need_up_val += site_arr[j].history_max - site_arr[j].now_q
                    not_max_list.append([site_arr[j].history_max - site_arr[j].now_q, j])
                elif site_arr[j].now_q - site_arr[j].history_max > 0:
                    need_down_val += min(ans_arr[i][j], site_arr[j].now_q - site_arr[j].history_max)
                    over_max_list.append([min(ans_arr[i][j], site_arr[j].now_q - site_arr[j].history_max), j])


        if need_down_val == 0 or need_up_val == 0:
            continue

        res_flag = True

        if need_up_val >= need_down_val:
            # good, all
            if tmp_debug_print:
                print('adjust -- all down -- line ', i)
            for j in range(input_data.site_cnt):
                if site_arr[j].is_max_this_time:
                    if need_up_val != 0 and site_arr[j].max_q - site_arr[j].now_q != 0 and input_data.bool_site_client[j][i]:
                        old_req = site_arr[j].now_q
                        one_up_val = need_down_val * (
                                site_arr[j].max_q - site_arr[j].now_q) // need_up_val
                        ans_arr[i][j] += one_up_val
                        site_arr[j].now_q += one_up_val
                        need_down_val -= one_up_val
                        need_up_val -= site_arr[j].max_q - old_req
                else:
                    if site_arr[j].now_q - site_arr[j].history_max < 0 and input_data.bool_site_client[j][i]:
                        old_req = site_arr[j].now_q
                        one_up_val = need_down_val * (
                                site_arr[j].history_max - site_arr[j].now_q) // need_up_val
                        ans_arr[i][j] += one_up_val
                        site_arr[j].now_q += one_up_val
                        need_down_val -= one_up_val
                        need_up_val -= site_arr[j].history_max - old_req
                    elif site_arr[j].now_q > site_arr[j].history_max:
                        one_down_val = min(ans_arr[i][j], site_arr[j].now_q - site_arr[j].history_max)
                        ans_arr[i][j] -= one_down_val
                        site_arr[j].now_q -= one_down_val
        else:
            if tmp_debug_print:
                print('not good, adjust step by step')
                print(need_up_val, need_down_val)
                print('adjust - all up --line ', i)
            for j in range(input_data.site_cnt):
                if site_arr[j].is_max_this_time:
                    if input_data.bool_site_client[j][i]:
                        one_up_val = site_arr[j].max_q - site_arr[j].now_q
                        ans_arr[i][j] += one_up_val
                        site_arr[j].now_q += one_up_val
                else:
                    if site_arr[j].now_q - site_arr[j].history_max < 0:
                        if input_data.bool_site_client[j][i]:
                            one_up_val = site_arr[j].history_max - site_arr[j].now_q
                            ans_arr[i][j] += one_up_val
                            site_arr[j].now_q += one_up_val
                    elif site_arr[j].now_q - site_arr[j].history_max > 0:
                        if need_down_val != 0:
                            old_power = min(ans_arr[i][j], site_arr[j].now_q - site_arr[j].history_max)
                            one_down_val = need_up_val * min(ans_arr[i][j], site_arr[j].now_q - site_arr[
                                j].history_max) // need_down_val
                            ans_arr[i][j] -= one_down_val
                            site_arr[j].now_q -= one_down_val
                            need_up_val -= one_down_val
                            need_down_val -= old_power



    for index in max_list:
        site_arr[index].is_max_this_time = False

    for s_i in range(input_data.site_cnt):
        if s_i in max_list:
            continue
        sums = 0
        for i in range(input_data.client_cnt):
            sums += ans_arr[i][s_i]
        if sums > site_arr[s_i].history_max:
            site_arr[s_i].history_max = sums

    return res_flag
























# 已经作废不用
def func_3(input_data, site_arr, client_arr, file_handle, origin_time_client_site, every_site_biggest_cnt):
    for t in origin_time_client_site:
        for i in t:
            for j in i:
                if j < 0:
                    print('input not correct')
                    return

    # 最大值的时间表
    max_site_times_arr = [[] for i in range(input_data.all_times)]

    # 固定值（拉倒极限的部分)
    ter_arr = [[[0 for k in range(input_data.site_cnt)] for j in range(input_data.client_cnt)] for i in range(input_data.all_times)]

    # 更新的时间-client需求表
    times_client_request = []
    for t in range(input_data.all_times):
        times_client_request.append([])
        for c in range(input_data.client_cnt):
            times_client_request[t].append(input_data.time_client_request[t][c])

    # 每次设置完max之后实时更新
    history_time_site = [[site_arr[j].history_req[i][0] for j in range(input_data.site_cnt)] for i in range(input_data.all_times)]

    myHeap = []
    for time in range(input_data.all_times):
        for s_i in range(input_data.site_cnt):
            heappush(myHeap, [-history_time_site[time][s_i], time, s_i])

    cnt_site_max = [every_site_biggest_cnt for i in range(input_data.site_cnt)]

    # if True:
    #     ter_arr[0][0][0] = 199
    #     origin_time_client_site[0][0][0] = 200
    #     return


    already = 0
    while already < input_data.site_cnt * every_site_biggest_cnt:
        here = heappop(myHeap)
        while here[0] != -history_time_site[here[1]][here[2]] or cnt_site_max[here[2]] == 0 or here[2] in max_site_times_arr[here[1]]:
            here = heappop(myHeap)

        time, site_index = here[1], here[2]
        cnt_site_max[site_index] -= 1

        max_site_times_arr[time].append(site_index)

        # 这里是重新计算的部分
        set_ans_arr_by_max(input_data, site_arr, client_arr, origin_time_client_site[time], max_site_times_arr[time], times_client_request[time])
        # 重新计算结束

        for j in range(input_data.site_cnt):
            his = 0
            if j in max_site_times_arr[time]:
                continue
            for i in range(input_data.client_cnt):
                his += origin_time_client_site[time][i][j]
            heappush(myHeap, [-his, time, j])


        already += 1
    # if True:
    #     return
    #  -- v5 -运行失败
    #
    # for v in max_site_times_arr:
    #     print(v)

    # 清除历史：history
    for s in range(input_data.site_cnt):
        site_arr[s].history_max = 0

    for t in range(input_data.all_times):
        for i in range(input_data.client_cnt):
            for j in range(input_data.site_cnt):
                origin_time_client_site[t][i][j] += ter_arr[t][i][j]
        for j in range(input_data.site_cnt):
            n_q = 0
            for i in range(input_data.client_cnt):
                n_q += origin_time_client_site[t][i][j]
            site_arr[j].now_q = n_q
        adjust_except_max(input_data, origin_time_client_site[t], max_site_times_arr[t], site_arr)

    for t in range(input_data.all_times):
        for i in range(input_data.client_cnt):
            output_buffer = client_arr[i].name
            output_buffer += ':'
            temp_arr = []
            for j in range(input_data.site_cnt):
                val = origin_time_client_site[t][i][j]
                if val < 0:
                    print("error !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
                    print(val)
                if val != 0:
                    temp_arr.append(f'<{site_arr[j].name},{str(val)}>')
            # print(output_buffer + ','.join(temp_arr))
            if i == input_data.client_cnt - 1 and t == input_data.all_times - 1:
                file_handle.write(output_buffer + ','.join(temp_arr))
            else:
                file_handle.write(output_buffer + ','.join(temp_arr) + '\n')

    return
# 已经作废不用
def set_ans_arr_by_max(input_data, site_arr, client_arr, ans_arr, max_list, req_list):
    """按照max_list 来设置最优解"""
    here_debug_print = False
    if here_debug_print:
        print("-------------------------------------------------------------------------------")
        print(req_list)

    for i in range(input_data.client_cnt):
        for j in range(input_data.site_cnt):
            ans_arr[i][j] = 0

    temp_heap = []

    for i in range(input_data.client_cnt):
        client_arr[i].left_request = req_list[i]
        heappush(temp_heap, [-client_arr[i].left_request, i])
    for i in range(input_data.site_cnt):
        site_arr[i].now_q = 0

    for i in max_list:
        site_arr[i].is_max_this_time = True

    # from max to min
    while len(temp_heap) != 0:
        aaa = heappop(temp_heap)
        i = aaa[1]
        sum_power = 0
        left_res = client_arr[i].left_request
        if left_res == 0:
            continue

        for j in client_arr[i].fathers_index:
            if site_arr[j].is_max_this_time:
                site_arr[j].last_power = (site_arr[j].max_q - site_arr[j].now_q)
                sum_power += site_arr[j].last_power

        if sum_power != 0:
            last_j = -1
            for j in client_arr[i].fathers_index:
                if site_arr[j].is_max_this_time:
                    htb_a, htb_b, htb_c = min(left_res, site_arr[j].max_q - site_arr[j].now_q), site_arr[
                        j].now_q, left_res
                    ans_arr[i][j] = min(client_arr[i].left_request * site_arr[j].last_power // sum_power,
                                        site_arr[j].max_q - site_arr[j].now_q)
                    site_arr[j].now_q += ans_arr[i][j]
                    # ans_trans_f[i][j] += client_arr[i].min_depart * site_arr[j].last_power / sum_power
                    left_res -= ans_arr[i][j]
                    last_j = j
            if last_j != -1:
                ans_arr[i][last_j] = htb_a
                site_arr[last_j].now_q = htb_b + htb_a
                left_res = htb_c - htb_a

            client_arr[i].left_request = left_res

        if left_res == 0:
            continue

        sum_power = 0
        for j in client_arr[i].fathers_index:
            if not site_arr[j].is_max_this_time:
                site_arr[j].last_power = (site_arr[j].max_q - site_arr[j].now_q)
                sum_power += site_arr[j].last_power

        if sum_power < left_res:
            print('error, sum_power < left_res')
            out = 0
            bb = 2 / out
        last_j = -1
        for j in client_arr[i].fathers_index:
            if not site_arr[j].is_max_this_time:
                htb_a, htb_b, htb_c = min(left_res, site_arr[j].max_q - site_arr[j].now_q), site_arr[
                    j].now_q, left_res
                ans_arr[i][j] = min(client_arr[i].left_request * site_arr[j].last_power // sum_power,
                                    site_arr[j].max_q - site_arr[j].now_q)
                site_arr[j].now_q += ans_arr[i][j]
                # ans_trans_f[i][j] += client_arr[i].min_depart * site_arr[j].last_power / sum_power
                left_res -= ans_arr[i][j]
                last_j = j
        if last_j != -1:
            ans_arr[i][last_j] = htb_a
            site_arr[last_j].now_q = htb_b + htb_a
            left_res = htb_c - htb_a

    if here_debug_print:
        print('\n----------------------------------------------------------\nshow arr:')
        for i in range(input_data.client_cnt):
            print(ans_arr[i], end='      sum = ')
            print(sum(ans_arr[i]))
        for j in range(input_data.site_cnt):
            tmp = 0
            for i in range(input_data.client_cnt):
                tmp += ans_arr[i][j]
            print(tmp, end='   ')
        print('\n----------------------------------------------------------:')

    if here_debug_print:
        for i in range(input_data.site_cnt):
            tttt = 0
            for j in range(input_data.client_cnt):
                tttt += ans_arr[j][i]
            if tttt > site_arr[i].max_q:
                print('site: tttt = ', tttt, ' real = ', site_arr[i].max_q)

        for i in range(input_data.client_cnt):
            tttt = 0
            for j in range(input_data.site_cnt):
                tttt += ans_arr[i][j]
            if tttt != input_data.now_time_client_request[i]:
                print('client: tttt = ', tttt, ' real = ', input_data.now_time_client_request[i])

    # reset max_site
    if len(max_list) != 0:
        for i in max_list:
            site_arr[i].is_max_this_time = False
    return










# 和 func2相同
def func_4(input_data, site_arr, client_arr, file_handle, origin_time_client_site, every_site_biggest_cnt, start_time):
    for t in origin_time_client_site:
        for i in t:
            for j in i:
                if j < 0:
                    print('input not correct')
                    return

    # 记录每个时间的最大值site下标
    max_site_times_arr = [[] for i in range(input_data.all_times)]

    over_max_site_time_arr = [[] for i in range(input_data.all_times)]

    # 固定值（拉倒极限的部分)
    ter_arr = [[[0 for k in range(input_data.site_cnt)] for j in range(input_data.client_cnt)] for i in range(input_data.all_times)]

    # 更新的时间-client需求表
    times_client_request = []
    for t in range(input_data.all_times):
        times_client_request.append([])
        for c in range(input_data.client_cnt):
            times_client_request[t].append(input_data.time_client_request[t][c])

    # 每次设置完max之后实时更新
    history_time_site = [[site_arr[j].history_req[i][0] for j in range(input_data.site_cnt)] for i in range(input_data.all_times)]

    myHeap = []
    for time in range(input_data.all_times):
        for s_i in range(input_data.site_cnt):
            heappush(myHeap, [-history_time_site[time][s_i], time, s_i])

    cnt_site_max = [every_site_biggest_cnt for i in range(input_data.site_cnt)]

    # if True:
    #     ter_arr[0][0][0] = 199
    #     origin_time_client_site[0][0][0] = 200
    #     return


    already = 0
    while already < input_data.site_cnt * every_site_biggest_cnt:
        here = heappop(myHeap)
        while here[0] != -history_time_site[here[1]][here[2]] or cnt_site_max[here[2]] == 0:
            if cnt_site_max[here[2]] != 0:
                here[0] = -history_time_site[here[1]][here[2]]
                heappush(myHeap, here)
            here = heappop(myHeap)

        time, site_index = here[1], here[2]
        cnt_site_max[site_index] -= 1

        max_site_times_arr[time].append(site_index)

        # sum_req 是 当前的site 对应的全部的client， 他们的剩余需求之和
        sum_req = 0
        for i in site_arr[site_index].sons_index:
            sum_req += times_client_request[time][i]

        # 如果剩余的需求小于等于当前的最大值，那么可以直接用当前的site来包含全部的下属client
        if sum_req <= site_arr[site_index].max_q:
            # enough
            for i in site_arr[site_index].sons_index:
                for j in client_arr[i].fathers_index:
                    # 不管是不是，全部置为0
                    history_time_site[time][j] -= origin_time_client_site[time][i][j]
                    origin_time_client_site[time][i][j] = 0
                # full
                ter_arr[time][i][site_index] = times_client_request[time][i]
                times_client_request[time][i] = 0

            left_max = site_arr[site_index].max_q - sum_req
            if left_max != 0 and len(over_max_site_time_arr[time]) != 0:
                changed_list = []
                while left_max != 0 and len(over_max_site_time_arr[time]) != 0:
                    new_max_site_index = over_max_site_time_arr[time].pop()
                    new_include_val = 0
                    new_need_val = 0
                    for c_idx in site_arr[new_max_site_index].sons_index:
                        new_need_val += times_client_request[time][c_idx]
                    if new_need_val == 0:
                        # 无需再调剂
                        continue
                    for c_idx in site_arr[site_index].sons_index:
                        if ter_arr[time][c_idx][new_max_site_index] != 0:
                            change_val = min(left_max, ter_arr[time][c_idx][new_max_site_index], new_need_val)
                            ter_arr[time][c_idx][new_max_site_index] -= change_val
                            left_max -= change_val
                            ter_arr[time][c_idx][site_index] += change_val
                            new_include_val += change_val
                            new_need_val -= change_val
                            if left_max == 0 or new_need_val == 0:
                                break
                    if new_need_val != 0:
                        changed_list.append(new_max_site_index)
                    if new_include_val != 0 and False:
                        all_can_add_to = new_include_val
                        sum_power = 0
                        for i in site_arr[new_max_site_index].sons_index:
                            sum_power += times_client_request[time][i]
                        for i in site_arr[new_max_site_index].sons_index:
                            # 先求出每一行（每一个client）可以在当前site下增加多少；this_client_add
                            # sum_i_rest_site 是当前比重
                            sum_i_rest_site = times_client_request[time][i]
                            if sum_i_rest_site == 0 or sum_power == 0:
                                continue
                            if sum_power != 0:
                                this_client_add = sum_i_rest_site * all_can_add_to // sum_power
                                sum_power -= sum_i_rest_site
                                all_can_add_to -= this_client_add
                            else:
                                this_client_add = 0
                            ter_arr[time][i][new_max_site_index] += this_client_add
                            times_client_request[time][i] -= this_client_add

                            # 非site_index依次减少
                            # 加权平分 this_client_add
                            if this_client_add == 0:
                                continue
                            for j in client_arr[i].fathers_index:
                                if j == new_max_site_index:
                                    continue
                                if sum_i_rest_site != 0:
                                    tmp_del = origin_time_client_site[time][i][j] * this_client_add // sum_i_rest_site
                                    sum_i_rest_site -= origin_time_client_site[time][i][j]
                                    origin_time_client_site[time][i][j] -= tmp_del
                                    this_client_add -= tmp_del
                                else:
                                    tmp_del = 0
                                history_time_site[time][j] -= tmp_del

                while len(changed_list) != 0:
                    over_max_site_time_arr[time].append(changed_list.pop())

            already += 1
            continue

        over_max_site_time_arr[time].append(site_index)
        # print('here', 'time = ', time, 'site_index = ', site_index)

        # 按比例分配, 当前的不变，剩余的按比例分配
        # sum_power是权重，是 每一个client 根据他们 剩余的需求 和 在当前site之下的差 、的和
        sum_power = 0
        site_max = site_arr[site_index].max_q
        for i in site_arr[site_index].sons_index:
            sum_power += times_client_request[time][i] - origin_time_client_site[time][i][site_index]


        all_can_add_to = site_arr[site_index].max_q - history_time_site[time][site_index]
        for i in site_arr[site_index].sons_index:
            # 先求出每一行（每一个client）可以在当前site下增加多少；this_client_add
            if len(client_arr[i].fathers_index) <= 1:
                ter_arr[time][i][site_index] = origin_time_client_site[time][i][site_index]
                origin_time_client_site[time][i][site_index] = 0
                times_client_request[time][i] -= ter_arr[time][i][site_index]
                if times_client_request[time][i] < 0:
                    print('error -here 115')
                    return
                continue
            # sum_i_rest_site 是当前比重
            sum_i_rest_site = times_client_request[time][i] - origin_time_client_site[time][i][site_index]
            if sum_i_rest_site == 0:
                ter_arr[time][i][site_index] = origin_time_client_site[time][i][site_index]
                origin_time_client_site[time][i][site_index] = 0
                times_client_request[time][i] -= ter_arr[time][i][site_index]
                if times_client_request[time][i] < 0:
                    print('error -here 114')
                    return
                continue
            if sum_i_rest_site < 0:
                print('error !-- req < real')
                print(times_client_request[time])
                print(origin_time_client_site[time][i])
                print('i = ', i, 'site_index = ', site_index)
                bb = 0
                aa = 1 // bb
                exit()
            if sum_power != 0:
                this_client_add = sum_i_rest_site * all_can_add_to // sum_power
                sum_power -= sum_i_rest_site
                all_can_add_to -= this_client_add
            else:
                this_client_add = all_can_add_to
            ter_arr[time][i][site_index] = origin_time_client_site[time][i][site_index] + this_client_add
            origin_time_client_site[time][i][site_index] = 0
            times_client_request[time][i] -= ter_arr[time][i][site_index]
            if times_client_request[time][i] < 0:
                print('error -here 113')
                print(times_client_request[time][i],ter_arr[time][i][site_index])
                print(time, i, site_index)
                print(origin_time_client_site[time])
                print('this_client_add = ', this_client_add)
                return


            # 非site_index依次减少
            # 加权平分 this_client_add
            if this_client_add == 0:
                continue
            if this_client_add < 0:
                print('error --33')
                return
            for j in client_arr[i].fathers_index:
                if j == site_index:
                    continue
                if sum_i_rest_site != 0:
                    tmp_del = origin_time_client_site[time][i][j] * this_client_add // sum_i_rest_site
                    sum_i_rest_site -= origin_time_client_site[time][i][j]
                    origin_time_client_site[time][i][j] -= tmp_del
                    this_client_add -= tmp_del
                    if origin_time_client_site[time][i][j] < 0:
                        print('here-- 112')
                        return
                else:
                    tmp_del = 0
                history_time_site[time][j] -= tmp_del
                if history_time_site[time][j] < 0:
                    print('here -- 116')
            # if True:
            #     return # --v7 -运行失败
        #
        # if True:
        #     return
        #  -- v6 -运行失败
        already += 1
    # if True:
    #     return
    #  -- v5 -运行失败



    for t in range(input_data.all_times):
        for i in range(input_data.client_cnt):
            for j in range(input_data.site_cnt):
                origin_time_client_site[t][i][j] += ter_arr[t][i][j]


    step = 0
    while t_time.time() - start_time < 240:
        step += 1
        res = False
        # 清除历史：history
        for s in range(input_data.site_cnt):
            site_arr[s].history_max = site_arr[s].sub_his_max = 0

        if step != 1:
            for t in range(input_data.all_times):
                for j in range(input_data.site_cnt):
                    n_q = 0
                    for i in range(input_data.client_cnt):
                        n_q += origin_time_client_site[t][i][j]

                    if n_q == site_arr[j].history_max:
                        continue

                    if n_q >= site_arr[j].history_max:
                        site_arr[j].sub_his_max = site_arr[j].history_max
                        site_arr[j].history_max = n_q
                    elif n_q > site_arr[j].sub_his_max:
                        site_arr[j].sub_his_max = n_q


        for s in range(input_data.site_cnt):
            site_arr[s].history_max = site_arr[s].sub_his_max

        for t in range(input_data.all_times):
            for j in range(input_data.site_cnt):
                n_q = 0
                for i in range(input_data.client_cnt):
                    n_q += origin_time_client_site[t][i][j]
                site_arr[j].now_q = n_q
            if adjust_mix_all(input_data, origin_time_client_site[t], max_site_times_arr[t], site_arr):
                res = True

        print('step = ', step, 'res = ', res)
        if not res:
            break






    for t in range(input_data.all_times):
        for i in range(input_data.client_cnt):
            output_buffer = client_arr[i].name
            output_buffer += ':'
            temp_arr = []
            for j in range(input_data.site_cnt):
                val = origin_time_client_site[t][i][j]
                if val < 0:
                    print("error !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
                    print(val)
                if val != 0:
                    temp_arr.append(f'<{site_arr[j].name},{str(val)}>')
            # print(output_buffer + ','.join(temp_arr))
            if i == input_data.client_cnt - 1 and t == input_data.all_times - 1:
                file_handle.write(output_buffer + ','.join(temp_arr))
            else:
                file_handle.write(output_buffer + ','.join(temp_arr) + '\n')


    return




















