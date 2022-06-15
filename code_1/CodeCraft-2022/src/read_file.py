import csv
import configparser


class Input_datas():
    """11"""
    def __init__(self, input_path):
        self.read_print_flag = False

        self.all_times = 0
        self.client_names = []
        self.client_cnt = 0
        self.time_client_request = []
        with open(input_path + '/demand.csv', 'r') as f:
            reader = csv.reader(f)

            idx = 0
            for row in reader:
                # print(row)
                if idx != 0:
                    self.time_client_request.append([])
                j = 0
                for col in row:
                    # print(col, end = '  ')
                    if idx != 0:
                        if j != 0:
                            self.time_client_request[-1].append(int(col))
                    else:
                        if col != 'mtime':
                            self.client_names.append(col)
                    j += 1

                # print('')
                if idx != 0:
                    self.all_times += 1
                idx += 1
            self.client_cnt = len(self.client_names)
        # if debug_print:
        #     self.all_times -= 4


        if self.read_print_flag:
            print('all times is ',self.all_times)
            print('all client name is ', self.client_names)
            print('all client cnt is ', self.client_cnt)
            print('request arr is', self.time_client_request)

        self.site_cnt = 0
        self.site_names = []
        self.site_max = []
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

        self.connect_thd = 0
        conf = configparser.ConfigParser()
        conf.read(input_path + '/config.ini')
        for k,v in conf.items('config'):
            # print('k,v = ', k, v)
            if k == 'qos_constraint':
                self.connect_thd = int(v)
                # print("here")
        if self.read_print_flag:
            print('self.connect_thd is ', self.connect_thd)

        self.bool_site_client = []
        with open(input_path + '/qos.csv', 'r') as f:
            reader = csv.reader(f)
            idx = 0
            for row in reader:
                # print(row)
                j = 0
                if idx != 0:
                    self.bool_site_client.append([])
                for col in row:
                    # print(col, end = '  ')
                    if idx != 0:
                        if j != 0:
                            if int(col) >= self.connect_thd:
                                self.bool_site_client[-1].append(False)
                            else:
                                self.bool_site_client[-1].append(True)
                    j += 1
                idx += 1
        if self.read_print_flag:
            print(self.bool_site_client)

        self.now_time = -1

        self.now_time_client_request = []#self.time_client_request[self.now_time][1:]

        return

    def get_next_time(self):
        if self.now_time == self.all_times - 1:
            return False
        self.now_time += 1
        self.now_time_client_request = self.time_client_request[self.now_time]
        return True

    def reset_time(self):
        self.now_time = -1
        return










