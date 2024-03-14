import pandas as pd
import time
from function.get_label_name import GetLabelName


class GetResultCSV:
    """
    整理並儲存瑕疵檢測的CSV
    """

    def __init__(self, location: list, rate: list):
        self.LabelName = GetLabelName()
        self.location = location
        self.rate = rate
        self.column_name = ["種類","位置","比例"]
        self.savedir = 'reports/'
        data = {
            "種類": [], "位置": [], "比例": []
        }
        self.csv_df = pd.DataFrame(data)
        print(self.csv_df)
        self.get_result_csv()

    def get_result_csv(self):
        """
        將瑕疵種類、位置、比例輸出成csv檔
        :return: 帶有時間資料的csv files
        """
        try:
            for defect, element in enumerate(self.location):
                save_dict = {}
                json_defect_str = ', '.join(GetLabelName.label_defect_direction[direct]
                                            for direct, _ in enumerate(self.location[defect]))
                save_list = [self.LabelName.defect_name[element], json_defect_str, self.rate[element]]
                for index, name in enumerate(self.column_name):
                    save_dict[name] = save_list[index]
                print(save_dict)
                self.csv_df = pd.concat([self.csv_df, pd.DataFrame([save_dict])], ignore_index=True)
        except Exception as e:
            print(repr(e))

        print(self.csv_df)

        t1 = time.localtime(time.time())
        t2 = time.strftime('%m_%d_%H_%M_%S', t1)
        savepath = f"{self.savedir}/{t2}.csv"
        self.csv_df.to_csv(savepath, encoding='utf-8', index=False)