import pandas as pd
import time
from function.get_label_name import GetLabelName


class GetResultCSV:
    """
    整理並儲存瑕疵檢測的CSV
    """

    def __init__(self, location: list, rate: list, lang: bool):
        self.LabelName = GetLabelName()
        self.location = location
        self.rate = rate
        self.lang = lang
        if self.lang:
            self.column_name = ["種類", "位置", "比例(%)"]
            data = {
                "種類": [], "位置": [], "比例(%)": []
            }
        else:
            self.column_name = ["Name", "Location", "Rate(%)"]
            data = {
                "Name": [], "Location": [], "Rate(%)": []
            }
        self.saved_folder = 'reports/'

        self.csv_df = pd.DataFrame(data)
        self.get_result_csv()

    def get_result_csv(self):
        """
        將瑕疵種類、位置、比例輸出成csv檔
        :return: 帶有時間資料的csv files
        """
        try:
            for defect, element in enumerate(self.location):
                save_dict = {}
                if self.lang:
                    direction = GetLabelName.label_defect_direction_zh
                    json_defect_str = ', '.join(direction[direct - 1] for direct in self.location[defect])
                    save_list = [self.LabelName.defect_name_zh[element], json_defect_str, self.rate[element]]
                else:
                    direction = GetLabelName.label_defect_direction_en
                    json_defect_str = ', '.join(direction[direct - 1] for direct in self.location[defect])
                    save_list = [self.LabelName.defect_name_en[element], json_defect_str, self.rate[element]]

                for index, name in enumerate(self.column_name):
                    save_dict[name] = save_list[index]

                self.csv_df = pd.concat([self.csv_df, pd.DataFrame([save_dict])], ignore_index=True)
        except Exception as e:
            print(repr(e))

        t = time.strftime('%m_%d_%H_%M_%S', time.localtime(time.time()))
        save_path = f"{self.saved_folder}/{t}.csv"
        self.csv_df.to_csv(save_path, encoding='utf-8', index=False)
        print(f"Export the Result to {save_path} successfully.")
