
class SITE():
    def __init__(self):
        self.name = None
        self.max_q = 0
        self.now_q = 0 #
        self.sons_index = []
        self.sons_cnt = 0
        self.history_max = 1
        self.sub_his_max = 0
        self.last_power = 0

        self.history_req = []
        self.times = 0

        self.max_use_cnt = 0
        self.already_max = 0

        self.is_max_this_time = False
        return
    def show(self):
        print(self.name, self.a, self.b, self.max_q, self.now_q, self.press, self.sons_index, self.sons_cnt)

class MY_CLIENT():
    def __init__(self):
        self.name = None
        self.left_request = 0 #
        self.father_cnt = 0
        self.min_depart = 0 #
        self.fathers_index = []
        return
    def show(self):
        print(self.name, self.left_request, self.father_cnt, self.min_depart, self.fathers_index)
