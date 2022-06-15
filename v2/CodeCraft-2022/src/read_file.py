#coding=utf-8
import csv
import configparser


class Input_datas():
    """11"""
    def __init__(self, input_path):

        self.read_print_flag = False

        self.client_names = []
        self.client_cnt = 0
        self.client_name_map = {}

        self.time_stream_name = []
        self.time_stream_cnt = []
        self.all_times = 0
        self.time_client_stream_req = []

        self.set_data_from_demand(input_path)


        self.site_cnt = 0
        self.site_names = []
        site_name_map = {}
        self.site_max = []
        self.all_site_max = 0
        with open(input_path + '/site_bandwidth.csv', 'r') as f:
            reader = csv.reader(f)
            idx = 0
            for row in reader:
                # print(row)
                j = 0
                for col in row:
                    # print(col, end = '  ')
                    if idx != 0:
                        if j == 0:
                            site_name_map[col] = len(self.site_names)
                            self.site_names.append(col)
                        else:
                            self.site_max.append(int(col))
                    j += 1
                idx += 1
            self.site_cnt = len(self.site_names)
        if self.read_print_flag:
            print('site_cnt is ', self.site_cnt)
            print('site_names is ', self.site_names)
            print('site_max is ', self.site_max)
            print(self.site_names[67])

        for val in self.site_max:
            if val > self.all_site_max:
                self.all_site_max = val

        # base_cost
        self.connect_thd = 0
        self.base_cost = 0
        conf = configparser.ConfigParser()
        conf.read(input_path + '/config.ini')
        for k,v in conf.items('config'):
            # print('k,v = ', k, v)
            if k == 'qos_constraint':
                self.connect_thd = int(v)
                # print("here")
            if k == 'base_cost':
                self.base_cost = int(v)
        if self.read_print_flag:
            print('self.connect_thd is ', self.connect_thd)
            print('self.base_cost is ', self.base_cost)


        if self.read_print_flag:
            print(self.client_name_map)
            print(site_name_map)


        self.bool_site_client = [[True for j in range(self.client_cnt)] for i in range(self.site_cnt)]
        with open(input_path + '/qos.csv', 'r') as f:
            reader = csv.reader(f)
            idx = 0
            tmp_client_index = []
            for row in reader:
                # print(row)
                j = 0
                site_idx = -1
                client_idx = -1
                for col in row:
                    # print(col, end = '  ')
                    if idx != 0:
                        if j != 0:
                            if int(col) >= self.connect_thd:
                                self.bool_site_client[site_idx][tmp_client_index[j - 1]] = False
                        else:
                            site_idx = site_name_map[col]
                    else:
                        # idx == 0
                        if j != 0:
                            client_idx = self.client_name_map[col]
                            tmp_client_index.append(client_idx)
                    j += 1
                idx += 1
        if self.read_print_flag:
            print(self.bool_site_client)

        return

    def set_data_from_demand(self, input_path):
        # read demand file
        demand_file = open(input_path + '/demand.csv', 'r')
        lines = demand_file.readlines()
        demand_file.close()
        demand_file_arr = []
        for line in lines:
            demand_file_arr.append(line.rstrip('\n').split(','))

        # set client name and cnt
        tmp_count = 0
        for c_name in demand_file_arr[0]:
            tmp_count += 1
            if tmp_count <= 2:
                continue
            if c_name not in self.client_names:
                self.client_name_map[c_name] = len(self.client_names)
                self.client_names.append(c_name)
        self.client_cnt = len(self.client_names)
        if self.read_print_flag:
            print(self.client_names)

        # set time_stream_name
        last_time = ''
        for i in range(1, len(demand_file_arr)):
            if last_time != demand_file_arr[i][0]:
                # new time
                last_time = demand_file_arr[i][0]
                if len(self.time_stream_name) != 0:
                    self.time_stream_cnt.append(len(self.time_stream_name[-1]))
                self.time_stream_name.append([])
                self.all_times += 1
                self.time_client_stream_req.append([[] for k in range(self.client_cnt)])
            self.time_stream_name[-1].append(demand_file_arr[i][1])
            for j in range(self.client_cnt):
                self.time_client_stream_req[-1][j].append(int(demand_file_arr[i][2 + j]))
        self.time_stream_cnt.append(len(self.time_stream_name[-1]))

        # if self.read_print_flag:
        #     print(self.time_stream_cnt)
        #
        #     print_cnt = 0
        #     max_print_cnt = 200
        #     for t in range(self.all_times):
        #         for c in range(self.client_cnt):
        #             for s in range(len(self.time_stream_name[t])):
        #                 print(t, self.client_names[c], self.time_stream_name[t][s], end = ':')
        #                 print(self.time_client_stream_req[t][c][s])
        #                 print_cnt += 1
        #                 if print_cnt == max_print_cnt:
        #                     break
        #             if print_cnt == max_print_cnt:
        #                 break
        #         if print_cnt == max_print_cnt:
        #             break
        return













