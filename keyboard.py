##
# 2/9 self.get_merge_csv / self.set_merge_csv need to be incorporated into main for set 1, 2, 3, for set 4.
# ?? Considering to change but a lot of effort. - g / digraph should be changed to ng.
# standardise naming convention?
##

import time
import csv
import pandas as pd
import os
from statistics import fmean, stdev, variance

class Keyboard():
    def __init__(self):
        self.name = None # name of person
        self.csv = None # saved data in csv
        self.csv_ext = ".csv"
        self.export_path = None
        self.pressed_flag = False
        self.hold_flag = False
        self.press_df = pd.DataFrame(columns=['key', 'press_time'])
        self.release_df = pd.DataFrame(columns=['key', 'release_time'])

    def reset(self):
        self.press_df = self.press_df[0:0]
        self.release_df = self.release_df[0:0]

    def set_name(self, name): self.name = name
    def get_name(self): return self.name
    def set_csv(self, csv): self.csv = csv
    def get_csv(self): return self.csv
    def set_export(self, export_path): self.export_path = export_path
    def get_export(self): return self.export_path
    
    def get_press_df(self): return self.press_df
    def get_release_df(self): return self.release_df
    def set_merge_csv(self, merge_csv): self.merge_csv = merge_csv
    def get_merge_csv(self): return self.merge_csv

    def set_csv_single(self, csv_single): self.csv_single = csv_single
    def get_csv_single(self): return self.csv_single
    def set_csv_semi(self, csv_semi): self.csv_semi = csv_semi
    def get_csv_semi(self): return self.csv_semi
    def set_csv_bare(self, csv_bare): self.csv_bare = csv_bare
    def get_csv_bare(self): return self.csv_bare

    def key_press(self, key):
        press_time = time.time()

        if press_time is None:
            print("The press time is null")
        elif self.pressed_flag is False:
            self.pressed_flag = True
            self.hold_flag = False
            self.add_to_dataset("press", str(key), press_time, "individual")
        elif self.pressed_flag is True:
            if str(self.prior_key) != str(key):
                self.hold_flag = False
                self.add_to_dataset("press", str(key), press_time, "hold detected")
            else:
                if self.hold_flag is False:
                    self.press_df = self.press_df[:-1]
                    self.hold_flag = True
                    self.add_to_dataset("press", str(key), press_time, "hold detected and deleted")
                elif self.hold_flag is True:
                    self.add_to_dataset("press", str(key), press_time, "hold detected and not recorded")
        self.prior_key = key

    def key_release(self, key):
        release_time = time.time()
        if str(key) == "Key.enter":
            pass
        else:
            if release_time is None:
                print("The release time is null")
            elif self.hold_flag is True:
                self.pressed_flag = False
                self.hold_flag = False
                self.add_to_dataset("release", str(key), release_time, "hold recorded but deleted.")
            else:
                self.pressed_flag = False
                self.hold_flag = False
                self.add_to_dataset("release", str(key), release_time, "individual")

    def convert_key_to_int(self, keys):
        if keys == "\'a\'":
            return str(1), "a"
        elif keys == "\'b\'":
            return str(2), "b"
        elif keys == "\'c\'":
            return str(3), "c"
        elif keys == "\'d\'":
            return str(4), "d"
        elif keys == "\'e\'":
            return str(5), "e"
        elif keys == "\'f\'":
            return str(6), "f"
        elif keys == "\'g\'":
            return str(7), "g"
        elif keys == "\'h\'":
            return str(8), "h"
        elif keys == "\'i\'":
            return str(9), "i"
        elif keys == "\'j\'":
            return str(10), "j"
        elif keys == "\'k\'":
            return str(11), "k"
        elif keys == "\'l\'":
            return str(12), "l"
        elif keys == "\'m\'":
            return str(13), "m"
        elif keys == "\'n\'":
            return str(14), "n"
        elif keys == "\'o\'":
            return str(15), "o"
        elif keys == "\'p\'":
            return str(16), "p"
        elif keys == "\'q\'":
            return str(17), "q"
        elif keys == "\'r\'":
            return str(18), "r"
        elif keys == "\'s\'":
            return str(19), "s"
        elif keys == "\'t\'":
            return str(20), "t"
        elif keys == "\'u\'":
            return str(21), "u"
        elif keys == "\'v\'":
            return str(22), "v"
        elif keys == "\'w\'":
            return str(23), "w"
        elif keys == "\'x\'":
            return str(24), "x"
        elif keys == "\'y\'":
            return str(25), "y"
        elif keys == "\'z\'":
            return str(26), "z"
        elif keys == "key.space":
            return str(0), "~"
        elif keys == "\'0\'":
            return str(90), "0"
        elif keys == "\'1\'":
            return str(91), "1"
        elif keys == "\'2\'":
            return str(92), "2"
        elif keys == "\'3\'":
            return str(93), "3"
        elif keys == "\'4\'":
            return str(94), "4"
        elif keys == "\'5\'":
            return str(95), "5"
        elif keys == "\'6\'":
            return str(96), "6"
        elif keys == "\'7\'":
            return str(97), "7"
        elif keys == "\'8\'":
            return str(98), "8"
        elif keys == "\'9\'":
            return str(99), "9"

    def export_to_csv_1(self, password):
        # time.sleep(0.5)
        seq_no = password.find(" ")

        self.press_df.reset_index(inplace=True, drop=True)
        self.release_df.reset_index(inplace=True, drop=True)

        self.press_df["count"] = self.press_df.groupby("key").cumcount()
        self.release_df["count"] = self.release_df.groupby("key").cumcount()
        
        merge_df = pd.merge(self.press_df, self.release_df, on=["key", "count"], how='inner')
        merge_df = merge_df.drop(columns=["count"])
        merge_df_path = os.path.join(self.get_export(), "df_" + self.get_name() + self.csv_ext) # to be deleted and migrate to keyboard.py due to self.setmergecsv
        merge_df.to_csv(merge_df_path, sep=',', mode='a', header=False)

        two_dwell_list, two_int_list, two_pf_list, two_rf_list, two_ng_list = ([] for i in range(5))
        three_int_list, three_pf_list, three_rf_list, three_ng_list = ([] for i in range(4))
        four_int_list, four_pf_list, four_rf_list, four_ng_list = ([] for i in range(4))
        five_int_list, five_pf_list, five_rf_list, five_ng_list = ([] for i in range(4))
        six_int_list, six_pf_list, six_rf_list, six_ng_list = ([] for i in range(4))
        seven_int_list, seven_pf_list, seven_rf_list, seven_ng_list = ([] for i in range(4))
        eight_int_list, eight_pf_list, eight_rf_list, eight_ng_list = ([] for i in range(4))
        nine_int_list, nine_pf_list, nine_rf_list, nine_ng_list = ([] for i in range(4))

        with open(self.get_csv(), 'a', newline='') as file:
            placeholder = [merge_df.iloc[0]["release_time"] - merge_df.iloc[0]["press_time"]]
            two_dwell_list.append(merge_df.iloc[0]["release_time"] - merge_df.iloc[0]["press_time"])
            for row in range(0, 9):
                interval_time = merge_df.iloc[row+1]["press_time"] - merge_df.iloc[row]["release_time"]
                press_flight_time = merge_df.iloc[row+1]["press_time"] - merge_df.iloc[row]["press_time"]
                release_flight_time = merge_df.iloc[row+1]["release_time"] - merge_df.iloc[row]["release_time"]
                digraph_time = merge_df.iloc[row+1]["release_time"] - merge_df.iloc[row]["press_time"]
                later_dwell_time = merge_df.iloc[row+1]["release_time"] - merge_df.iloc[row+1]["press_time"]
                two_dwell_list.append(later_dwell_time)
                two_int_list.append(interval_time)
                two_pf_list.append(press_flight_time)
                two_rf_list.append(release_flight_time)
                two_ng_list.append(digraph_time)

                placeholder.extend([str(interval_time), str(press_flight_time),str(release_flight_time), str(digraph_time),
                str(later_dwell_time)])

            placeholder.extend([str(sum(two_dwell_list)), str(sum(two_int_list)), str(sum(two_pf_list)), str(sum(two_rf_list)), str(sum(two_ng_list)),
                str(fmean(two_dwell_list)), str(fmean(two_int_list)), str(fmean(two_pf_list)), str(fmean(two_rf_list)), str(fmean(two_ng_list)),
                str(variance(two_dwell_list)), str(variance(two_int_list)), str(variance(two_pf_list)), str(variance(two_rf_list)), str(variance(two_ng_list)),
                str(stdev(two_dwell_list)), str(stdev(two_int_list)), str(stdev(two_pf_list)), str(stdev(two_rf_list)), str(stdev(two_ng_list))])

            for row in range(0,8):
                three_int_time = merge_df.iloc[row+2]["press_time"] - merge_df.iloc[row]["release_time"]
                three_pf_time = merge_df.iloc[row+2]["press_time"] - merge_df.iloc[row]["press_time"]
                three_rf_time = merge_df.iloc[row+2]["release_time"] - merge_df.iloc[row]["release_time"]
                three_graph_time = merge_df.iloc[row+2]["release_time"] - merge_df.iloc[row]["press_time"]
                placeholder.extend([str(three_int_time), str(three_pf_time), str(three_rf_time), str(three_graph_time)])
                three_int_list.append(three_int_time)
                three_pf_list.append(three_pf_time)
                three_rf_list.append(three_rf_time)
                three_ng_list.append(three_graph_time)
            
            placeholder.extend([str(sum(three_int_list)), str(sum(three_pf_list)), str(sum(three_rf_list)), str(sum(three_ng_list)),
                str(fmean(three_int_list)), str(fmean(three_pf_list)), str(fmean(three_rf_list)), str(fmean(three_ng_list)),
                str(variance(three_int_list)), str(variance(three_pf_list)), str(variance(three_rf_list)), str(variance(three_ng_list)),
                str(stdev(three_int_list)), str(stdev(three_pf_list)), str(stdev(three_rf_list)), str(stdev(three_ng_list))])

            for row in range(0,7):
                four_int_time = merge_df.iloc[row+3]["press_time"] - merge_df.iloc[row]["release_time"]
                four_pf_time = merge_df.iloc[row+3]["press_time"] - merge_df.iloc[row]["press_time"]
                four_rf_time = merge_df.iloc[row+3]["release_time"] - merge_df.iloc[row]["release_time"]
                four_graph_time = merge_df.iloc[row+3]["release_time"] - merge_df.iloc[row]["press_time"]
                placeholder.extend([str(four_int_time), str(four_pf_time), str(four_rf_time), str(four_graph_time)])
                four_int_list.append(four_int_time)
                four_pf_list.append(four_pf_time)
                four_rf_list.append(four_rf_time)
                four_ng_list.append(four_graph_time)
            
            placeholder.extend([str(sum(four_int_list)), str(sum(four_pf_list)), str(sum(four_rf_list)), str(sum(four_ng_list)),
                str(fmean(four_int_list)), str(fmean(four_pf_list)), str(fmean(four_rf_list)), str(fmean(four_ng_list)),
                str(variance(four_int_list)), str(variance(four_pf_list)), str(variance(four_rf_list)), str(variance(four_ng_list)),
                str(stdev(four_int_list)), str(stdev(four_pf_list)), str(stdev(four_rf_list)), str(stdev(four_ng_list))])

            for row in range(0,6):
                five_int_time = merge_df.iloc[row+4]["press_time"] - merge_df.iloc[row]["release_time"]
                five_pf_time = merge_df.iloc[row+4]["press_time"] - merge_df.iloc[row]["press_time"]
                five_rf_time = merge_df.iloc[row+4]["release_time"] - merge_df.iloc[row]["release_time"]
                five_graph_time = merge_df.iloc[row+4]["release_time"] - merge_df.iloc[row]["press_time"]
                placeholder.extend([str(five_int_time), str(five_pf_time), str(five_rf_time), str(five_graph_time)])
                five_int_list.append(five_int_time)
                five_pf_list.append(five_pf_time)
                five_rf_list.append(five_rf_time)
                five_ng_list.append(five_graph_time)
            
            placeholder.extend([str(sum(five_int_list)), str(sum(five_pf_list)), str(sum(five_rf_list)), str(sum(five_ng_list)),
                str(fmean(five_int_list)), str(fmean(five_pf_list)), str(fmean(five_rf_list)), str(fmean(five_ng_list)),
                str(variance(five_int_list)), str(variance(five_pf_list)), str(variance(five_rf_list)), str(variance(five_ng_list)),
                str(stdev(five_int_list)), str(stdev(five_pf_list)), str(stdev(five_rf_list)), str(stdev(five_ng_list))])

            for row in range(0,5):
                six_int_time = merge_df.iloc[row+5]["press_time"] - merge_df.iloc[row]["release_time"]
                six_pf_time = merge_df.iloc[row+5]["press_time"] - merge_df.iloc[row]["press_time"]
                six_rf_time = merge_df.iloc[row+5]["release_time"] - merge_df.iloc[row]["release_time"]
                six_graph_time = merge_df.iloc[row+5]["release_time"] - merge_df.iloc[row]["press_time"]
                placeholder.extend([str(six_int_time), str(six_pf_time), str(six_rf_time), str(six_graph_time)])
                six_int_list.append(six_int_time)
                six_pf_list.append(six_pf_time)
                six_rf_list.append(six_rf_time)
                six_ng_list.append(six_graph_time)
            
            placeholder.extend([str(sum(six_int_list)), str(sum(six_pf_list)), str(sum(six_rf_list)), str(sum(six_ng_list)),
                str(fmean(six_int_list)), str(fmean(six_pf_list)), str(fmean(six_rf_list)), str(fmean(six_ng_list)),
                str(variance(six_int_list)), str(variance(six_pf_list)), str(variance(six_rf_list)), str(variance(six_ng_list)),
                str(stdev(six_int_list)), str(stdev(six_pf_list)), str(stdev(six_rf_list)), str(stdev(six_ng_list))])

            for row in range(0,4):
                seven_int_time = merge_df.iloc[row+6]["press_time"] - merge_df.iloc[row]["release_time"]
                seven_pf_time = merge_df.iloc[row+6]["press_time"] - merge_df.iloc[row]["press_time"]
                seven_rf_time = merge_df.iloc[row+6]["release_time"] - merge_df.iloc[row]["release_time"]
                seven_graph_time = merge_df.iloc[row+6]["release_time"] - merge_df.iloc[row]["press_time"]
                placeholder.extend([str(seven_int_time), str(seven_pf_time), str(seven_rf_time), str(seven_graph_time)])
                seven_int_list.append(seven_int_time)
                seven_pf_list.append(seven_pf_time)
                seven_rf_list.append(seven_rf_time)
                seven_ng_list.append(seven_graph_time)
            
            placeholder.extend([str(sum(seven_int_list)), str(sum(seven_pf_list)), str(sum(seven_rf_list)), str(sum(seven_ng_list)),
                str(fmean(seven_int_list)), str(fmean(seven_pf_list)), str(fmean(seven_rf_list)), str(fmean(seven_ng_list)),
                str(variance(seven_int_list)), str(variance(seven_pf_list)), str(variance(seven_rf_list)), str(variance(seven_ng_list)),
                str(stdev(seven_int_list)), str(stdev(seven_pf_list)), str(stdev(seven_rf_list)), str(stdev(seven_ng_list))])

            for row in range(0,3):
                eight_int_time = merge_df.iloc[row+7]["press_time"] - merge_df.iloc[row]["release_time"]
                eight_pf_time = merge_df.iloc[row+7]["press_time"] - merge_df.iloc[row]["press_time"]
                eight_rf_time = merge_df.iloc[row+7]["release_time"] - merge_df.iloc[row]["release_time"]
                eight_graph_time = merge_df.iloc[row+7]["release_time"] - merge_df.iloc[row]["press_time"]
                placeholder.extend([str(eight_int_time), str(eight_pf_time), str(eight_rf_time), str(eight_graph_time)])
                eight_int_list.append(eight_int_time)
                eight_pf_list.append(eight_pf_time)
                eight_rf_list.append(eight_rf_time)
                eight_ng_list.append(eight_graph_time)
            
            placeholder.extend([str(sum(eight_int_list)), str(sum(eight_pf_list)), str(sum(eight_rf_list)), str(sum(eight_ng_list)),
                str(fmean(eight_int_list)), str(fmean(eight_pf_list)), str(fmean(eight_rf_list)), str(fmean(eight_ng_list)),
                str(variance(eight_int_list)), str(variance(eight_pf_list)), str(variance(eight_rf_list)), str(variance(eight_ng_list)),
                str(stdev(eight_int_list)), str(stdev(eight_pf_list)), str(stdev(eight_rf_list)), str(stdev(eight_ng_list))])

            for row in range(0,2):
                nine_int_time = merge_df.iloc[row+8]["press_time"] - merge_df.iloc[row]["release_time"]
                nine_pf_time = merge_df.iloc[row+8]["press_time"] - merge_df.iloc[row]["press_time"]
                nine_rf_time = merge_df.iloc[row+8]["release_time"] - merge_df.iloc[row]["release_time"]
                nine_graph_time = merge_df.iloc[row+8]["release_time"] - merge_df.iloc[row]["press_time"]
                placeholder.extend([str(nine_int_time), str(nine_pf_time), str(nine_rf_time), str(nine_graph_time)])
                nine_int_list.append(nine_int_time)
                nine_pf_list.append(nine_pf_time)
                nine_rf_list.append(nine_rf_time)
                nine_ng_list.append(nine_graph_time)
            
            placeholder.extend([str(sum(nine_int_list)), str(sum(nine_pf_list)), str(sum(nine_rf_list)), str(sum(nine_ng_list)),
                str(fmean(nine_int_list)), str(fmean(nine_pf_list)), str(fmean(nine_rf_list)), str(fmean(nine_ng_list)),
                str(variance(nine_int_list)), str(variance(nine_pf_list)), str(variance(nine_rf_list)), str(variance(nine_ng_list)),
                str(stdev(nine_int_list)), str(stdev(nine_pf_list)), str(stdev(nine_rf_list)), str(stdev(nine_ng_list))])

            for row in range(0,1):
                ten_int_time = merge_df.iloc[row+9]["press_time"] - merge_df.iloc[row]["release_time"]
                ten_pf_time = merge_df.iloc[row+9]["press_time"] - merge_df.iloc[row]["press_time"]
                ten_rf_time = merge_df.iloc[row+9]["release_time"] - merge_df.iloc[row]["release_time"]
                ten_graph_time = merge_df.iloc[row+9]["release_time"] - merge_df.iloc[row]["press_time"]
                placeholder.extend([str(ten_int_time), str(ten_pf_time), str(ten_rf_time), str(ten_graph_time)])
            
            writer = csv.writer(file)
            writer.writerow([self.get_name(), str(seq_no), password, *placeholder])
            placeholder.clear()

            two_dwell_list.clear()
            two_int_list.clear()
            two_pf_list.clear()
            two_rf_list.clear()
            two_ng_list.clear()

            three_int_list.clear()
            three_pf_list.clear()
            three_rf_list.clear()
            three_ng_list.clear()

            four_int_list.clear()
            four_pf_list.clear()
            four_rf_list.clear()
            four_ng_list.clear()

            five_int_list.clear()
            five_pf_list.clear()
            five_rf_list.clear()
            five_ng_list.clear()
            
            six_int_list.clear()
            six_pf_list.clear()
            six_rf_list.clear()
            six_ng_list.clear()

            seven_int_list.clear()
            seven_pf_list.clear()
            seven_rf_list.clear()
            seven_ng_list.clear()

            eight_int_list.clear()
            eight_pf_list.clear()
            eight_rf_list.clear()
            eight_ng_list.clear()

            nine_int_list.clear()
            nine_pf_list.clear()
            nine_rf_list.clear()
            nine_ng_list.clear()


    def export_to_csv_2(self, password):
        # time.sleep(0.5)
        seq_no = password.find(" ")

        self.press_df.reset_index(inplace=True, drop=True)
        self.release_df.reset_index(inplace=True, drop=True)

        self.press_df["count"] = self.press_df.groupby("key").cumcount()
        self.release_df["count"] = self.release_df.groupby("key").cumcount()
        
        merge_df = pd.merge(self.press_df, self.release_df, on=["key", "count"], how='inner')
        merge_df = merge_df.drop(columns=["count"])
        merge_df_path = os.path.join(self.get_export(), "df_" + self.get_name() + self.csv_ext) # to be deleted and migrate to keyboard.py due to self.setmergecsv
        merge_df.to_csv(merge_df_path, sep=',', mode='a', header=False)

        two_dwell_list = []
        two_int_list = []
        two_pf_list = []
        two_rf_list = []
        two_ng_list = []

        three_int_list = []
        three_pf_list = []
        three_rf_list = []
        three_ng_list = []

        four_int_list = []
        four_pf_list = []
        four_rf_list = []
        four_ng_list = []

        five_int_list = []
        five_pf_list = []
        five_rf_list = []
        five_ng_list = []

        six_int_list = []
        six_pf_list = []
        six_rf_list = []
        six_ng_list = []

        seven_int_list = []
        seven_pf_list = []
        seven_rf_list = []
        seven_ng_list = []

        eight_int_list = []
        eight_pf_list = []
        eight_rf_list = []
        eight_ng_list = []

        nine_int_list = []
        nine_pf_list = []
        nine_rf_list = []
        nine_ng_list = []

        with open(self.get_csv_single(), 'a', newline='') as file:
            for row in range(0, len(merge_df)-1):
                # str_keys = str(merge_df.iloc[row]["key"]) + "_" + str(merge_df.iloc[row+1]["key"])
                init_num_key, init_str_key = self.convert_key_to_int(str(merge_df.iloc[row]["key"]))
                end_num_key, end_str_key = self.convert_key_to_int(str(merge_df.iloc[row+1]["key"]))
                str_key = str(init_str_key) + "_" + str(end_str_key)
                int_key = str(init_num_key) + "_" + str(end_num_key)
                current_dwell_time = merge_df.iloc[row]["release_time"] - merge_df.iloc[row]["press_time"]
                interval_time = merge_df.iloc[row+1]["press_time"] - merge_df.iloc[row]["release_time"]
                press_flight_time = merge_df.iloc[row+1]["press_time"] - merge_df.iloc[row]["press_time"]
                release_flight_time = merge_df.iloc[row+1]["release_time"] - merge_df.iloc[row]["release_time"]
                digraph_time = merge_df.iloc[row+1]["release_time"] - merge_df.iloc[row]["press_time"]
                later_dwell_time = merge_df.iloc[row+1]["release_time"] - merge_df.iloc[row+1]["press_time"]
                writer = csv.writer(file)
                writer.writerow([self.get_name(), str_key, int_key, str(init_num_key), str(end_num_key), str(seq_no), str(current_dwell_time), str(interval_time),
                    str(press_flight_time), str(release_flight_time),str(digraph_time), str(later_dwell_time)])



        with open(self.get_csv(), 'a', newline='') as file:
            placeholder = [merge_df.iloc[0]["release_time"] - merge_df.iloc[0]["press_time"]]
            two_dwell_list.append(merge_df.iloc[0]["release_time"] - merge_df.iloc[0]["press_time"])
            for row in range(0, 9):
                interval_time = merge_df.iloc[row+1]["press_time"] - merge_df.iloc[row]["release_time"]
                press_flight_time = merge_df.iloc[row+1]["press_time"] - merge_df.iloc[row]["press_time"]
                release_flight_time = merge_df.iloc[row+1]["release_time"] - merge_df.iloc[row]["release_time"]
                digraph_time = merge_df.iloc[row+1]["release_time"] - merge_df.iloc[row]["press_time"]
                later_dwell_time = merge_df.iloc[row+1]["release_time"] - merge_df.iloc[row+1]["press_time"]
                two_dwell_list.append(later_dwell_time)
                two_int_list.append(interval_time)
                two_pf_list.append(press_flight_time)
                two_rf_list.append(release_flight_time)
                two_ng_list.append(digraph_time)

                placeholder.extend([str(interval_time), str(press_flight_time),str(release_flight_time), str(digraph_time),
                str(later_dwell_time)])

            placeholder.extend([str(sum(two_dwell_list)), str(sum(two_int_list)), str(sum(two_pf_list)), str(sum(two_rf_list)), str(sum(two_ng_list)),
                str(fmean(two_dwell_list)), str(fmean(two_int_list)), str(fmean(two_pf_list)), str(fmean(two_rf_list)), str(fmean(two_ng_list)),
                str(variance(two_dwell_list)), str(variance(two_int_list)), str(variance(two_pf_list)), str(variance(two_rf_list)), str(variance(two_ng_list)),
                str(stdev(two_dwell_list)), str(stdev(two_int_list)), str(stdev(two_pf_list)), str(stdev(two_rf_list)), str(stdev(two_ng_list))])

            for row in range(0,8):
                three_int_time = merge_df.iloc[row+2]["press_time"] - merge_df.iloc[row]["release_time"]
                three_pf_time = merge_df.iloc[row+2]["press_time"] - merge_df.iloc[row]["press_time"]
                three_rf_time = merge_df.iloc[row+2]["release_time"] - merge_df.iloc[row]["release_time"]
                three_graph_time = merge_df.iloc[row+2]["release_time"] - merge_df.iloc[row]["press_time"]
                placeholder.extend([str(three_int_time), str(three_pf_time), str(three_rf_time), str(three_graph_time)])
                three_int_list.append(three_int_time)
                three_pf_list.append(three_pf_time)
                three_rf_list.append(three_rf_time)
                three_ng_list.append(three_graph_time)
            
            placeholder.extend([str(sum(three_int_list)), str(sum(three_pf_list)), str(sum(three_rf_list)), str(sum(three_ng_list)),
                str(fmean(three_int_list)), str(fmean(three_pf_list)), str(fmean(three_rf_list)), str(fmean(three_ng_list)),
                str(variance(three_int_list)), str(variance(three_pf_list)), str(variance(three_rf_list)), str(variance(three_ng_list)),
                str(stdev(three_int_list)), str(stdev(three_pf_list)), str(stdev(three_rf_list)), str(stdev(three_ng_list))])

            for row in range(0,7):
                four_int_time = merge_df.iloc[row+3]["press_time"] - merge_df.iloc[row]["release_time"]
                four_pf_time = merge_df.iloc[row+3]["press_time"] - merge_df.iloc[row]["press_time"]
                four_rf_time = merge_df.iloc[row+3]["release_time"] - merge_df.iloc[row]["release_time"]
                four_graph_time = merge_df.iloc[row+3]["release_time"] - merge_df.iloc[row]["press_time"]
                placeholder.extend([str(four_int_time), str(four_pf_time), str(four_rf_time), str(four_graph_time)])
                four_int_list.append(four_int_time)
                four_pf_list.append(four_pf_time)
                four_rf_list.append(four_rf_time)
                four_ng_list.append(four_graph_time)
            
            placeholder.extend([str(sum(four_int_list)), str(sum(four_pf_list)), str(sum(four_rf_list)), str(sum(four_ng_list)),
                str(fmean(four_int_list)), str(fmean(four_pf_list)), str(fmean(four_rf_list)), str(fmean(four_ng_list)),
                str(variance(four_int_list)), str(variance(four_pf_list)), str(variance(four_rf_list)), str(variance(four_ng_list)),
                str(stdev(four_int_list)), str(stdev(four_pf_list)), str(stdev(four_rf_list)), str(stdev(four_ng_list))])

            for row in range(0,6):
                five_int_time = merge_df.iloc[row+4]["press_time"] - merge_df.iloc[row]["release_time"]
                five_pf_time = merge_df.iloc[row+4]["press_time"] - merge_df.iloc[row]["press_time"]
                five_rf_time = merge_df.iloc[row+4]["release_time"] - merge_df.iloc[row]["release_time"]
                five_graph_time = merge_df.iloc[row+4]["release_time"] - merge_df.iloc[row]["press_time"]
                placeholder.extend([str(five_int_time), str(five_pf_time), str(five_rf_time), str(five_graph_time)])
                five_int_list.append(five_int_time)
                five_pf_list.append(five_pf_time)
                five_rf_list.append(five_rf_time)
                five_ng_list.append(five_graph_time)
            
            placeholder.extend([str(sum(five_int_list)), str(sum(five_pf_list)), str(sum(five_rf_list)), str(sum(five_ng_list)),
                str(fmean(five_int_list)), str(fmean(five_pf_list)), str(fmean(five_rf_list)), str(fmean(five_ng_list)),
                str(variance(five_int_list)), str(variance(five_pf_list)), str(variance(five_rf_list)), str(variance(five_ng_list)),
                str(stdev(five_int_list)), str(stdev(five_pf_list)), str(stdev(five_rf_list)), str(stdev(five_ng_list))])

            for row in range(0,5):
                six_int_time = merge_df.iloc[row+5]["press_time"] - merge_df.iloc[row]["release_time"]
                six_pf_time = merge_df.iloc[row+5]["press_time"] - merge_df.iloc[row]["press_time"]
                six_rf_time = merge_df.iloc[row+5]["release_time"] - merge_df.iloc[row]["release_time"]
                six_graph_time = merge_df.iloc[row+5]["release_time"] - merge_df.iloc[row]["press_time"]
                placeholder.extend([str(six_int_time), str(six_pf_time), str(six_rf_time), str(six_graph_time)])
                six_int_list.append(six_int_time)
                six_pf_list.append(six_pf_time)
                six_rf_list.append(six_rf_time)
                six_ng_list.append(six_graph_time)
            
            placeholder.extend([str(sum(six_int_list)), str(sum(six_pf_list)), str(sum(six_rf_list)), str(sum(six_ng_list)),
                str(fmean(six_int_list)), str(fmean(six_pf_list)), str(fmean(six_rf_list)), str(fmean(six_ng_list)),
                str(variance(six_int_list)), str(variance(six_pf_list)), str(variance(six_rf_list)), str(variance(six_ng_list)),
                str(stdev(six_int_list)), str(stdev(six_pf_list)), str(stdev(six_rf_list)), str(stdev(six_ng_list))])

            for row in range(0,4):
                seven_int_time = merge_df.iloc[row+6]["press_time"] - merge_df.iloc[row]["release_time"]
                seven_pf_time = merge_df.iloc[row+6]["press_time"] - merge_df.iloc[row]["press_time"]
                seven_rf_time = merge_df.iloc[row+6]["release_time"] - merge_df.iloc[row]["release_time"]
                seven_graph_time = merge_df.iloc[row+6]["release_time"] - merge_df.iloc[row]["press_time"]
                placeholder.extend([str(seven_int_time), str(seven_pf_time), str(seven_rf_time), str(seven_graph_time)])
                seven_int_list.append(seven_int_time)
                seven_pf_list.append(seven_pf_time)
                seven_rf_list.append(seven_rf_time)
                seven_ng_list.append(seven_graph_time)
            
            placeholder.extend([str(sum(seven_int_list)), str(sum(seven_pf_list)), str(sum(seven_rf_list)), str(sum(seven_ng_list)),
                str(fmean(seven_int_list)), str(fmean(seven_pf_list)), str(fmean(seven_rf_list)), str(fmean(seven_ng_list)),
                str(variance(seven_int_list)), str(variance(seven_pf_list)), str(variance(seven_rf_list)), str(variance(seven_ng_list)),
                str(stdev(seven_int_list)), str(stdev(seven_pf_list)), str(stdev(seven_rf_list)), str(stdev(seven_ng_list))])

            for row in range(0,3):
                eight_int_time = merge_df.iloc[row+7]["press_time"] - merge_df.iloc[row]["release_time"]
                eight_pf_time = merge_df.iloc[row+7]["press_time"] - merge_df.iloc[row]["press_time"]
                eight_rf_time = merge_df.iloc[row+7]["release_time"] - merge_df.iloc[row]["release_time"]
                eight_graph_time = merge_df.iloc[row+7]["release_time"] - merge_df.iloc[row]["press_time"]
                placeholder.extend([str(eight_int_time), str(eight_pf_time), str(eight_rf_time), str(eight_graph_time)])
                eight_int_list.append(eight_int_time)
                eight_pf_list.append(eight_pf_time)
                eight_rf_list.append(eight_rf_time)
                eight_ng_list.append(eight_graph_time)
            
            placeholder.extend([str(sum(eight_int_list)), str(sum(eight_pf_list)), str(sum(eight_rf_list)), str(sum(eight_ng_list)),
                str(fmean(eight_int_list)), str(fmean(eight_pf_list)), str(fmean(eight_rf_list)), str(fmean(eight_ng_list)),
                str(variance(eight_int_list)), str(variance(eight_pf_list)), str(variance(eight_rf_list)), str(variance(eight_ng_list)),
                str(stdev(eight_int_list)), str(stdev(eight_pf_list)), str(stdev(eight_rf_list)), str(stdev(eight_ng_list))])

            for row in range(0,2):
                nine_int_time = merge_df.iloc[row+8]["press_time"] - merge_df.iloc[row]["release_time"]
                nine_pf_time = merge_df.iloc[row+8]["press_time"] - merge_df.iloc[row]["press_time"]
                nine_rf_time = merge_df.iloc[row+8]["release_time"] - merge_df.iloc[row]["release_time"]
                nine_graph_time = merge_df.iloc[row+8]["release_time"] - merge_df.iloc[row]["press_time"]
                placeholder.extend([str(nine_int_time), str(nine_pf_time), str(nine_rf_time), str(nine_graph_time)])
                nine_int_list.append(nine_int_time)
                nine_pf_list.append(nine_pf_time)
                nine_rf_list.append(nine_rf_time)
                nine_ng_list.append(nine_graph_time)
            
            placeholder.extend([str(sum(nine_int_list)), str(sum(nine_pf_list)), str(sum(nine_rf_list)), str(sum(nine_ng_list)),
                str(fmean(nine_int_list)), str(fmean(nine_pf_list)), str(fmean(nine_rf_list)), str(fmean(nine_ng_list)),
                str(variance(nine_int_list)), str(variance(nine_pf_list)), str(variance(nine_rf_list)), str(variance(nine_ng_list)),
                str(stdev(nine_int_list)), str(stdev(nine_pf_list)), str(stdev(nine_rf_list)), str(stdev(nine_ng_list))])

            for row in range(0,1):
                ten_int_time = merge_df.iloc[row+9]["press_time"] - merge_df.iloc[row]["release_time"]
                ten_pf_time = merge_df.iloc[row+9]["press_time"] - merge_df.iloc[row]["press_time"]
                ten_rf_time = merge_df.iloc[row+9]["release_time"] - merge_df.iloc[row]["release_time"]
                ten_graph_time = merge_df.iloc[row+9]["release_time"] - merge_df.iloc[row]["press_time"]
                placeholder.extend([str(ten_int_time), str(ten_pf_time), str(ten_rf_time), str(ten_graph_time)])
                
            writer = csv.writer(file)
            writer.writerow([self.get_name(), str(seq_no), password, *placeholder])
            placeholder.clear()

            two_dwell_list.clear()
            two_int_list.clear()
            two_pf_list.clear()
            two_rf_list.clear()
            two_ng_list.clear()

            three_int_list.clear()
            three_pf_list.clear()
            three_rf_list.clear()
            three_ng_list.clear()

            four_int_list.clear()
            four_pf_list.clear()
            four_rf_list.clear()
            four_ng_list.clear()

            five_int_list.clear()
            five_pf_list.clear()
            five_rf_list.clear()
            five_ng_list.clear()
            
            six_int_list.clear()
            six_pf_list.clear()
            six_rf_list.clear()
            six_ng_list.clear()

            seven_int_list.clear()
            seven_pf_list.clear()
            seven_rf_list.clear()
            seven_ng_list.clear()

            eight_int_list.clear()
            eight_pf_list.clear()
            eight_rf_list.clear()
            eight_ng_list.clear()

            nine_int_list.clear()
            nine_pf_list.clear()
            nine_rf_list.clear()
            nine_ng_list.clear()

    def export_to_csv_3(self, password):
        ### FIVE CHARACTERS
        # time.sleep(0.5)

        self.press_df.reset_index(inplace=True, drop=True)
        self.release_df.reset_index(inplace=True, drop=True)

        self.press_df["count"] = self.press_df.groupby("key").cumcount()
        self.release_df["count"] = self.release_df.groupby("key").cumcount()

        merge_df = pd.merge(self.press_df, self.release_df, on=["key", "count"], how='inner')
        merge_df = merge_df.drop(columns=["count"])
        merge_df_path = os.path.join(self.get_export(), "df_rand_" + self.get_name() + self.csv_ext) # to be deleted and migrate to keyboard.py due to self.setmergecsv
        merge_df.to_csv(merge_df_path, sep=',', mode='a', header=False)

        two_dwell_list, two_int_list, two_pf_list, two_rf_list, two_ng_list = ([] for i in range(5))
        three_int_list, three_pf_list, three_rf_list, three_ng_list = ([] for i in range(4))
        four_int_list, four_pf_list, four_rf_list, four_ng_list = ([] for i in range(4))
        five_int_list, five_pf_list, five_rf_list, five_ng_list = ([] for i in range(4))

        with open(self.get_csv_single(), 'a', newline='') as file:
            for row in range(0, len(merge_df)-1):
                # str_keys = str(merge_df.iloc[row]["key"]) + "_" + str(merge_df.iloc[row+1]["key"])
                init_num_key, init_str_key = self.convert_key_to_int(str(merge_df.iloc[row]["key"]))
                end_num_key, end_str_key = self.convert_key_to_int(str(merge_df.iloc[row+1]["key"]))
                str_key = str(init_str_key) + "_" + str(end_str_key)
                int_key = str(init_num_key) + "_" + str(end_num_key)
                current_dwell_time = merge_df.iloc[row]["release_time"] - merge_df.iloc[row]["press_time"]
                interval_time = merge_df.iloc[row+1]["press_time"] - merge_df.iloc[row]["release_time"]
                press_flight_time = merge_df.iloc[row+1]["press_time"] - merge_df.iloc[row]["press_time"]
                release_flight_time = merge_df.iloc[row+1]["release_time"] - merge_df.iloc[row]["release_time"]
                digraph_time = merge_df.iloc[row+1]["release_time"] - merge_df.iloc[row]["press_time"]
                later_dwell_time = merge_df.iloc[row+1]["release_time"] - merge_df.iloc[row+1]["press_time"]
                writer = csv.writer(file)
                writer.writerow([self.get_name(), str_key, int_key, str(init_num_key), str(end_num_key), str(current_dwell_time), str(interval_time),
                    str(press_flight_time), str(release_flight_time),str(digraph_time), str(later_dwell_time)])

        with open(self.get_csv(), 'a', newline='') as file:
            placeholder = [merge_df.iloc[0]["release_time"] - merge_df.iloc[0]["press_time"]]
            two_dwell_list.append(merge_df.iloc[0]["release_time"] - merge_df.iloc[0]["press_time"])
            for row in range(0, 4):
                interval_time = merge_df.iloc[row+1]["press_time"] - merge_df.iloc[row]["release_time"]
                press_flight_time = merge_df.iloc[row+1]["press_time"] - merge_df.iloc[row]["press_time"]
                release_flight_time = merge_df.iloc[row+1]["release_time"] - merge_df.iloc[row]["release_time"]
                digraph_time = merge_df.iloc[row+1]["release_time"] - merge_df.iloc[row]["press_time"]
                later_dwell_time = merge_df.iloc[row+1]["release_time"] - merge_df.iloc[row+1]["press_time"]
                two_dwell_list.append(later_dwell_time)
                two_int_list.append(interval_time)
                two_pf_list.append(press_flight_time)
                two_rf_list.append(release_flight_time)
                two_ng_list.append(digraph_time)

                placeholder.extend([str(interval_time), str(press_flight_time),str(release_flight_time), str(digraph_time),
                str(later_dwell_time)])

            placeholder.extend([str(sum(two_dwell_list)), str(sum(two_int_list)), str(sum(two_pf_list)), str(sum(two_rf_list)), str(sum(two_ng_list)),
                str(fmean(two_dwell_list)), str(fmean(two_int_list)), str(fmean(two_pf_list)), str(fmean(two_rf_list)), str(fmean(two_ng_list)),
                str(variance(two_dwell_list)), str(variance(two_int_list)), str(variance(two_pf_list)), str(variance(two_rf_list)), str(variance(two_ng_list)),
                str(stdev(two_dwell_list)), str(stdev(two_int_list)), str(stdev(two_pf_list)), str(stdev(two_rf_list)), str(stdev(two_ng_list))])

            for row in range(0,3):
                
                three_int_time = merge_df.iloc[row+2]["press_time"] - merge_df.iloc[row]["release_time"]
                three_pf_time = merge_df.iloc[row+2]["press_time"] - merge_df.iloc[row]["press_time"]
                three_rf_time = merge_df.iloc[row+2]["release_time"] - merge_df.iloc[row]["release_time"]
                three_graph_time = merge_df.iloc[row+2]["release_time"] - merge_df.iloc[row]["press_time"]
                placeholder.extend([str(three_int_time), str(three_pf_time), str(three_rf_time), str(three_graph_time)])
                three_int_list.append(three_int_time)
                three_pf_list.append(three_pf_time)
                three_rf_list.append(three_rf_time)
                three_ng_list.append(three_graph_time)
            
            placeholder.extend([str(sum(three_int_list)), str(sum(three_pf_list)), str(sum(three_rf_list)), str(sum(three_ng_list)),
                str(fmean(three_int_list)), str(fmean(three_pf_list)), str(fmean(three_rf_list)), str(fmean(three_ng_list)),
                str(variance(three_int_list)), str(variance(three_pf_list)), str(variance(three_rf_list)), str(variance(three_ng_list)),
                str(stdev(three_int_list)), str(stdev(three_pf_list)), str(stdev(three_rf_list)), str(stdev(three_ng_list))])


            for row in range(0,2):
                
                four_int_time = merge_df.iloc[row+3]["press_time"] - merge_df.iloc[row]["release_time"]
                four_pf_time = merge_df.iloc[row+3]["press_time"] - merge_df.iloc[row]["press_time"]
                four_rf_time = merge_df.iloc[row+3]["release_time"] - merge_df.iloc[row]["release_time"]
                four_graph_time = merge_df.iloc[row+3]["release_time"] - merge_df.iloc[row]["press_time"]
                placeholder.extend([str(four_int_time), str(four_pf_time), str(four_rf_time), str(four_graph_time)])
                four_int_list.append(four_int_time)
                four_pf_list.append(four_pf_time)
                four_rf_list.append(four_rf_time)
                four_ng_list.append(four_graph_time)
            
            placeholder.extend([str(sum(four_int_list)), str(sum(four_pf_list)), str(sum(four_rf_list)), str(sum(four_ng_list)),
                str(fmean(four_int_list)), str(fmean(four_pf_list)), str(fmean(four_rf_list)), str(fmean(four_ng_list)),
                str(variance(four_int_list)), str(variance(four_pf_list)), str(variance(four_rf_list)), str(variance(four_ng_list)),
                str(stdev(four_int_list)), str(stdev(four_pf_list)), str(stdev(four_rf_list)), str(stdev(four_ng_list))])

            for row in range(0,1):
                five_int_time = merge_df.iloc[row+4]["press_time"] - merge_df.iloc[row]["release_time"]
                five_pf_time = merge_df.iloc[row+4]["press_time"] - merge_df.iloc[row]["press_time"]
                five_rf_time = merge_df.iloc[row+4]["release_time"] - merge_df.iloc[row]["release_time"]
                five_graph_time = merge_df.iloc[row+4]["release_time"] - merge_df.iloc[row]["press_time"]
                placeholder.extend([str(five_int_time), str(five_pf_time), str(five_rf_time), str(five_graph_time)])

            
            writer = csv.writer(file)
            writer.writerow([self.get_name(), password, *placeholder])
            placeholder.clear()

            two_dwell_list.clear()
            two_int_list.clear()
            two_pf_list.clear()
            two_rf_list.clear()
            two_ng_list.clear()

            three_int_list.clear()
            three_pf_list.clear()
            three_rf_list.clear()
            three_ng_list.clear()

            four_int_list.clear()
            four_pf_list.clear()
            four_rf_list.clear()
            four_ng_list.clear()

            five_int_list.clear()
            five_pf_list.clear()
            five_rf_list.clear()
            five_ng_list.clear()
    
    def export_to_csv_4(self, password):
        ### EIGHT CHARACTERS
        # time.sleep(0.5)
        maxPwdLen = len(password)

        self.press_df.reset_index(inplace=True, drop=True)
        self.release_df.reset_index(inplace=True, drop=True)

        self.press_df["count"] = self.press_df.groupby("key").cumcount()
        self.release_df["count"] = self.release_df.groupby("key").cumcount()
        
        merge_df = pd.merge(self.press_df, self.release_df, on=["key", "count"], how='inner')
        merge_df = merge_df.drop(columns=["count"])
        merge_df.to_csv(self.get_merge_csv(), sep=',', mode='a', header=False)

        two_dwell_list, two_int_list, two_pf_list, two_rf_list, two_ng_list = ([] for i in range(5))
        three_int_list, three_pf_list, three_rf_list, three_ng_list = ([] for i in range(4))
        four_int_list, four_pf_list, four_rf_list, four_ng_list = ([] for i in range(4))
        five_int_list, five_pf_list, five_rf_list, five_ng_list = ([] for i in range(4))
        six_int_list, six_pf_list, six_rf_list, six_ng_list = ([] for i in range(4))
        seven_int_list, seven_pf_list, seven_rf_list, seven_ng_list = ([] for i in range(4))

        with open(self.get_csv_single(), 'a', newline='') as file:
            for row in range(0, len(merge_df)-1):
                # str_keys = str(merge_df.iloc[row]["key"]) + "_" + str(merge_df.iloc[row+1]["key"])
                init_num_key, init_str_key = self.convert_key_to_int(str(merge_df.iloc[row]["key"]))
                end_num_key, end_str_key = self.convert_key_to_int(str(merge_df.iloc[row+1]["key"]))
                str_key = str(init_str_key) + "_" + str(end_str_key)
                int_key = str(init_num_key) + "_" + str(end_num_key)
                current_dwell_time = merge_df.iloc[row]["release_time"] - merge_df.iloc[row]["press_time"]
                interval_time = merge_df.iloc[row+1]["press_time"] - merge_df.iloc[row]["release_time"]
                press_flight_time = merge_df.iloc[row+1]["press_time"] - merge_df.iloc[row]["press_time"]
                release_flight_time = merge_df.iloc[row+1]["release_time"] - merge_df.iloc[row]["release_time"]
                digraph_time = merge_df.iloc[row+1]["release_time"] - merge_df.iloc[row]["press_time"]
                later_dwell_time = merge_df.iloc[row+1]["release_time"] - merge_df.iloc[row+1]["press_time"]
                writer = csv.writer(file)
                writer.writerow([self.get_name(), str_key, int_key, str(init_num_key), str(end_num_key), str(current_dwell_time), str(interval_time),
                    str(press_flight_time), str(release_flight_time),str(digraph_time), str(later_dwell_time)])

        with open(self.get_csv(), 'a', newline='') as file:
            placeholder = [merge_df.iloc[0]["release_time"] - merge_df.iloc[0]["press_time"]]
            two_dwell_list.append(merge_df.iloc[0]["release_time"] - merge_df.iloc[0]["press_time"])
            for row in range(0, maxPwdLen-1):
                interval_time = merge_df.iloc[row+1]["press_time"] - merge_df.iloc[row]["release_time"]
                press_flight_time = merge_df.iloc[row+1]["press_time"] - merge_df.iloc[row]["press_time"]
                release_flight_time = merge_df.iloc[row+1]["release_time"] - merge_df.iloc[row]["release_time"]
                digraph_time = merge_df.iloc[row+1]["release_time"] - merge_df.iloc[row]["press_time"]
                later_dwell_time = merge_df.iloc[row+1]["release_time"] - merge_df.iloc[row+1]["press_time"]
                placeholder.extend([str(interval_time), str(press_flight_time),str(release_flight_time), str(digraph_time),
                str(later_dwell_time)])

                two_dwell_list.append(later_dwell_time)
                two_int_list.append(interval_time)
                two_pf_list.append(press_flight_time)
                two_rf_list.append(release_flight_time)
                two_ng_list.append(digraph_time)
            placeholder.extend([str(sum(two_dwell_list)), str(sum(two_int_list)), str(sum(two_pf_list)), str(sum(two_rf_list)), str(sum(two_ng_list)),
                str(fmean(two_dwell_list)), str(fmean(two_int_list)), str(fmean(two_pf_list)), str(fmean(two_rf_list)), str(fmean(two_ng_list)),
                str(variance(two_dwell_list)), str(variance(two_int_list)), str(variance(two_pf_list)), str(variance(two_rf_list)), str(variance(two_ng_list)),
                str(stdev(two_dwell_list)), str(stdev(two_int_list)), str(stdev(two_pf_list)), str(stdev(two_rf_list)), str(stdev(two_ng_list))])

            for row in range(0, maxPwdLen-2):
                three_int_time = merge_df.iloc[row+2]["press_time"] - merge_df.iloc[row]["release_time"]
                three_pf_time = merge_df.iloc[row+2]["press_time"] - merge_df.iloc[row]["press_time"]
                three_rf_time = merge_df.iloc[row+2]["release_time"] - merge_df.iloc[row]["release_time"]
                three_graph_time = merge_df.iloc[row+2]["release_time"] - merge_df.iloc[row]["press_time"]
                placeholder.extend([str(three_int_time), str(three_pf_time), str(three_rf_time), str(three_graph_time)])
                
                three_int_list.append(three_int_time)
                three_pf_list.append(three_pf_time)
                three_rf_list.append(three_rf_time)
                three_ng_list.append(three_graph_time)
            placeholder.extend([str(sum(three_int_list)), str(sum(three_pf_list)), str(sum(three_rf_list)), str(sum(three_ng_list)),
                str(fmean(three_int_list)), str(fmean(three_pf_list)), str(fmean(three_rf_list)), str(fmean(three_ng_list)),
                str(variance(three_int_list)), str(variance(three_pf_list)), str(variance(three_rf_list)), str(variance(three_ng_list)),
                str(stdev(three_int_list)), str(stdev(three_pf_list)), str(stdev(three_rf_list)), str(stdev(three_ng_list))])


            for row in range(0, maxPwdLen-3):
                four_int_time = merge_df.iloc[row+3]["press_time"] - merge_df.iloc[row]["release_time"]
                four_pf_time = merge_df.iloc[row+3]["press_time"] - merge_df.iloc[row]["press_time"]
                four_rf_time = merge_df.iloc[row+3]["release_time"] - merge_df.iloc[row]["release_time"]
                four_graph_time = merge_df.iloc[row+3]["release_time"] - merge_df.iloc[row]["press_time"]
                placeholder.extend([str(four_int_time), str(four_pf_time), str(four_rf_time), str(four_graph_time)])
                
                four_int_list.append(four_int_time)
                four_pf_list.append(four_pf_time)
                four_rf_list.append(four_rf_time)
                four_ng_list.append(four_graph_time)
            placeholder.extend([str(sum(four_int_list)), str(sum(four_pf_list)), str(sum(four_rf_list)), str(sum(four_ng_list)),
                str(fmean(four_int_list)), str(fmean(four_pf_list)), str(fmean(four_rf_list)), str(fmean(four_ng_list)),
                str(variance(four_int_list)), str(variance(four_pf_list)), str(variance(four_rf_list)), str(variance(four_ng_list)),
                str(stdev(four_int_list)), str(stdev(four_pf_list)), str(stdev(four_rf_list)), str(stdev(four_ng_list))])

  

            for row in range(0, maxPwdLen-4):
                five_int_time = merge_df.iloc[row+4]["press_time"] - merge_df.iloc[row]["release_time"]
                five_pf_time = merge_df.iloc[row+4]["press_time"] - merge_df.iloc[row]["press_time"]
                five_rf_time = merge_df.iloc[row+4]["release_time"] - merge_df.iloc[row]["release_time"]
                five_graph_time = merge_df.iloc[row+4]["release_time"] - merge_df.iloc[row]["press_time"]
                placeholder.extend([str(five_int_time), str(five_pf_time), str(five_rf_time), str(five_graph_time)])
                
                five_int_list.append(five_int_time)
                five_pf_list.append(five_pf_time)
                five_rf_list.append(five_rf_time)
                five_ng_list.append(five_graph_time)
            placeholder.extend([str(sum(five_int_list)), str(sum(five_pf_list)), str(sum(five_rf_list)), str(sum(five_ng_list)),
                str(fmean(five_int_list)), str(fmean(five_pf_list)), str(fmean(five_rf_list)), str(fmean(five_ng_list)),
                str(variance(five_int_list)), str(variance(five_pf_list)), str(variance(five_rf_list)), str(variance(five_ng_list)),
                str(stdev(five_int_list)), str(stdev(five_pf_list)), str(stdev(five_rf_list)), str(stdev(five_ng_list))])

            for row in range(0, maxPwdLen-5):
                six_int_time = merge_df.iloc[row+5]["press_time"] - merge_df.iloc[row]["release_time"]
                six_pf_time = merge_df.iloc[row+5]["press_time"] - merge_df.iloc[row]["press_time"]
                six_rf_time = merge_df.iloc[row+5]["release_time"] - merge_df.iloc[row]["release_time"]
                six_graph_time = merge_df.iloc[row+5]["release_time"] - merge_df.iloc[row]["press_time"]
                placeholder.extend([str(six_int_time), str(six_pf_time), str(six_rf_time), str(six_graph_time)])
                
                six_int_list.append(six_int_time)
                six_pf_list.append(six_pf_time)
                six_rf_list.append(six_rf_time)
                six_ng_list.append(six_graph_time)
            placeholder.extend([str(sum(six_int_list)), str(sum(six_pf_list)), str(sum(six_rf_list)), str(sum(six_ng_list)),
                str(fmean(six_int_list)), str(fmean(six_pf_list)), str(fmean(six_rf_list)), str(fmean(six_ng_list)),
                str(variance(six_int_list)), str(variance(six_pf_list)), str(variance(six_rf_list)), str(variance(six_ng_list)),
                str(stdev(six_int_list)), str(stdev(six_pf_list)), str(stdev(six_rf_list)), str(stdev(six_ng_list))])


            for row in range(0, maxPwdLen-6):
                seven_int_time = merge_df.iloc[row+6]["press_time"] - merge_df.iloc[row]["release_time"]
                seven_pf_time = merge_df.iloc[row+6]["press_time"] - merge_df.iloc[row]["press_time"]
                seven_rf_time = merge_df.iloc[row+6]["release_time"] - merge_df.iloc[row]["release_time"]
                seven_graph_time = merge_df.iloc[row+6]["release_time"] - merge_df.iloc[row]["press_time"]
                placeholder.extend([str(seven_int_time), str(seven_pf_time), str(seven_rf_time), str(seven_graph_time)])
                
                seven_int_list.append(seven_int_time)
                seven_pf_list.append(seven_pf_time)
                seven_rf_list.append(seven_rf_time)
                seven_ng_list.append(seven_graph_time)
            placeholder.extend([str(sum(seven_int_list)), str(sum(seven_pf_list)), str(sum(seven_rf_list)), str(sum(seven_ng_list)),
                str(fmean(seven_int_list)), str(fmean(seven_pf_list)), str(fmean(seven_rf_list)), str(fmean(seven_ng_list)),
                str(variance(seven_int_list)), str(variance(seven_pf_list)), str(variance(seven_rf_list)), str(variance(seven_ng_list)),
                str(stdev(seven_int_list)), str(stdev(seven_pf_list)), str(stdev(seven_rf_list)), str(stdev(seven_ng_list))])

            for row in range(0, maxPwdLen-7):
                eight_int_time = merge_df.iloc[row+7]["press_time"] - merge_df.iloc[row]["release_time"]
                eight_pf_time = merge_df.iloc[row+7]["press_time"] - merge_df.iloc[row]["press_time"]
                eight_rf_time = merge_df.iloc[row+7]["release_time"] - merge_df.iloc[row]["release_time"]
                eight_graph_time = merge_df.iloc[row+7]["release_time"] - merge_df.iloc[row]["press_time"]
                placeholder.extend([str(eight_int_time), str(eight_pf_time), str(eight_rf_time), str(eight_graph_time)])

            writer = csv.writer(file)
            writer.writerow([self.get_name(), password, *placeholder])
            placeholder.clear()

            two_dwell_list.clear()
            two_int_list.clear()
            two_pf_list.clear()
            two_rf_list.clear()
            two_ng_list.clear()

            three_int_list.clear()
            three_pf_list.clear()
            three_rf_list.clear()
            three_ng_list.clear()

            four_int_list.clear()
            four_pf_list.clear()
            four_rf_list.clear()
            four_ng_list.clear()

            five_int_list.clear()
            five_pf_list.clear()
            five_rf_list.clear()
            five_ng_list.clear()
            
            six_int_list.clear()
            six_pf_list.clear()
            six_rf_list.clear()
            six_ng_list.clear()

            seven_int_list.clear()
            seven_pf_list.clear()
            seven_rf_list.clear()
            seven_ng_list.clear()

        with open(self.get_csv_semi(), 'a', newline='') as file:
            placeholder = [merge_df.iloc[0]["release_time"] - merge_df.iloc[0]["press_time"]]
            
            for row in range(0, maxPwdLen-1):
                interval_time = merge_df.iloc[row+1]["press_time"] - merge_df.iloc[row]["release_time"]
                press_flight_time = merge_df.iloc[row+1]["press_time"] - merge_df.iloc[row]["press_time"]
                release_flight_time = merge_df.iloc[row+1]["release_time"] - merge_df.iloc[row]["release_time"]
                digraph_time = merge_df.iloc[row+1]["release_time"] - merge_df.iloc[row]["press_time"]
                later_dwell_time = merge_df.iloc[row+1]["release_time"] - merge_df.iloc[row+1]["press_time"]
                placeholder.extend([str(interval_time), str(press_flight_time),str(release_flight_time), str(digraph_time),
                str(later_dwell_time)])


            for row in range(0, maxPwdLen-2):
                three_int_time = merge_df.iloc[row+2]["press_time"] - merge_df.iloc[row]["release_time"]
                three_pf_time = merge_df.iloc[row+2]["press_time"] - merge_df.iloc[row]["press_time"]
                three_rf_time = merge_df.iloc[row+2]["release_time"] - merge_df.iloc[row]["release_time"]
                three_graph_time = merge_df.iloc[row+2]["release_time"] - merge_df.iloc[row]["press_time"]
                placeholder.extend([str(three_int_time), str(three_pf_time), str(three_rf_time), str(three_graph_time)])
                

            for row in range(0, maxPwdLen-3):
                four_int_time = merge_df.iloc[row+3]["press_time"] - merge_df.iloc[row]["release_time"]
                four_pf_time = merge_df.iloc[row+3]["press_time"] - merge_df.iloc[row]["press_time"]
                four_rf_time = merge_df.iloc[row+3]["release_time"] - merge_df.iloc[row]["release_time"]
                four_graph_time = merge_df.iloc[row+3]["release_time"] - merge_df.iloc[row]["press_time"]
                placeholder.extend([str(four_int_time), str(four_pf_time), str(four_rf_time), str(four_graph_time)])
                
            for row in range(0, maxPwdLen-4):
                five_int_time = merge_df.iloc[row+4]["press_time"] - merge_df.iloc[row]["release_time"]
                five_pf_time = merge_df.iloc[row+4]["press_time"] - merge_df.iloc[row]["press_time"]
                five_rf_time = merge_df.iloc[row+4]["release_time"] - merge_df.iloc[row]["release_time"]
                five_graph_time = merge_df.iloc[row+4]["release_time"] - merge_df.iloc[row]["press_time"]
                placeholder.extend([str(five_int_time), str(five_pf_time), str(five_rf_time), str(five_graph_time)])
                
            for row in range(0, maxPwdLen-5):
                six_int_time = merge_df.iloc[row+5]["press_time"] - merge_df.iloc[row]["release_time"]
                six_pf_time = merge_df.iloc[row+5]["press_time"] - merge_df.iloc[row]["press_time"]
                six_rf_time = merge_df.iloc[row+5]["release_time"] - merge_df.iloc[row]["release_time"]
                six_graph_time = merge_df.iloc[row+5]["release_time"] - merge_df.iloc[row]["press_time"]
                placeholder.extend([str(six_int_time), str(six_pf_time), str(six_rf_time), str(six_graph_time)])
                
            for row in range(0, maxPwdLen-6):
                seven_int_time = merge_df.iloc[row+6]["press_time"] - merge_df.iloc[row]["release_time"]
                seven_pf_time = merge_df.iloc[row+6]["press_time"] - merge_df.iloc[row]["press_time"]
                seven_rf_time = merge_df.iloc[row+6]["release_time"] - merge_df.iloc[row]["release_time"]
                seven_graph_time = merge_df.iloc[row+6]["release_time"] - merge_df.iloc[row]["press_time"]
                placeholder.extend([str(seven_int_time), str(seven_pf_time), str(seven_rf_time), str(seven_graph_time)])
                
            for row in range(0, maxPwdLen-7):
                eight_int_time = merge_df.iloc[row+7]["press_time"] - merge_df.iloc[row]["release_time"]
                eight_pf_time = merge_df.iloc[row+7]["press_time"] - merge_df.iloc[row]["press_time"]
                eight_rf_time = merge_df.iloc[row+7]["release_time"] - merge_df.iloc[row]["release_time"]
                eight_graph_time = merge_df.iloc[row+7]["release_time"] - merge_df.iloc[row]["press_time"]
                placeholder.extend([str(eight_int_time), str(eight_pf_time), str(eight_rf_time), str(eight_graph_time)])

            writer = csv.writer(file)
            writer.writerow([self.get_name(), password, *placeholder])
            placeholder.clear()

        with open(self.get_csv_bare(), 'a', newline='') as file:
            placeholder = [merge_df.iloc[0]["release_time"] - merge_df.iloc[0]["press_time"]]
            
            for row in range(0, maxPwdLen-1):
                interval_time = merge_df.iloc[row+1]["press_time"] - merge_df.iloc[row]["release_time"]
                press_flight_time = merge_df.iloc[row+1]["press_time"] - merge_df.iloc[row]["press_time"]
                release_flight_time = merge_df.iloc[row+1]["release_time"] - merge_df.iloc[row]["release_time"]
                digraph_time = merge_df.iloc[row+1]["release_time"] - merge_df.iloc[row]["press_time"]
                later_dwell_time = merge_df.iloc[row+1]["release_time"] - merge_df.iloc[row+1]["press_time"]
                placeholder.extend([str(interval_time), str(press_flight_time),str(release_flight_time), str(digraph_time),
                str(later_dwell_time)])

            writer = csv.writer(file)
            writer.writerow([self.get_name(), password, *placeholder])
            placeholder.clear()