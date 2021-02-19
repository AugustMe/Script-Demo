#-*- encoding: utf-8 -*-
import argparse
import os 
import shutil
import pandas as pd


def generate_excel(time_dir):
    """
    time_dir: 时间命名的文件夹，eg:2020-02-09
    生成统计缺陷的excel表格
    """
    type_dict = {}
    data_list = []
    type_list = [str(type) for type in os.listdir(time_dir)] 

    for type in type_list:
        result = {}
        # Get number list
        type_dict[type] = [file[1:7] for file in os.listdir(os.path.join(time_dir, type))]
        
        # Accumulate every number counts
        for number in set(type_dict[type]):
            result[number] = type_dict[type].count(number)
            data_list.append([number, type, result[number]])
    # print(data_list) 
    # Save data_list to excel 
    df = pd.DataFrame(columns=['流水号', '类型', '数量'], data=data_list)
    if os.path.exists(f'{time_dir}.xlsx'):
        os.remove(f'{time_dir}.xlsx')
    df.to_excel(f"{time_dir}.xlsx", index=False)
    print("Finish!!!")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--dir", '-d', type=str, required=True, help='The directory of picture named by time')
    args = vars(ap.parse_args())
    time_dir = args['dir']
    generate_excel(time_dir)