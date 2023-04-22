from io import StringIO

import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import numpy as np
import matplotlib
import mplfinance as mpf
import pandas as pd

my_color = mpf.make_marketcolors(
    up="red",  # 上涨K线的颜色
    down="green",  # 下跌K线的颜色
    edge="black",  # 蜡烛图箱体的颜色
    volume="purple",  # 成交量柱子的颜色
    wick="black"  # 蜡烛图影线的颜色
)

my_style = mpf.make_mpf_style(
    base_mpf_style='nightclouds',
    # base_mpl_style='seaborn',  # 也可以试试matplotlib的seaborn等风格。
    marketcolors=my_color,
    figcolor='(0, 0.8, 0.85)',
    gridcolor='(0.9, 0.9, 0.9)',
    rc={'font.family': 'SimHei', 'axes.unicode_minus': 'False'}
)


def showKGraph(data):
    datas = list(data.split('\n'))
    if '股票' in datas[1]:
        del datas[1]
    df = pd.read_csv(StringIO('\n'.join(datas)))
    df.rename(columns={
        'tdate': 'Date',
        'zrspj': 'Open',
        'zgj': 'High',
        'zdj': 'Low',
        'price': 'Close',
        'cjl': 'Volume'
    },
        inplace=True)
    df = df.iloc[1:, :]
    df['Date'] = pd.to_datetime(df['Date'])  # 转换日期列的格式，便于作图
    df.set_index(['Date'], inplace=True)  # 将日期列作为行索引
    df = df.sort_index()
    columns = ('Open', 'High', 'Low', 'Close', 'Volume')
    for col in columns:
        for v in df[col]:
            conv(v)

    mpf.plot(df,
             type='candle',
             ylabel="price",
             style='blueskies',
             title='PINGANBank from 2022-6-1 to 2022-8-31',
             mav=(5, 10),
             volume=True,
             figratio=(5, 3),
             ylabel_lower="Volume")
    # mpf.plot(df,
    #          type='candle',
    #          ylabel="price",
    #          style=my_style,
    #          title='平安银行6-8月 日线行情',
    #          mav=(5, 10),
    #          volume=True,
    #          figratio=(5, 3),
    #          ylabel_lower="Volume")

def conv(s):
    try:
        s = float(s)
    except ValueError:
        pass
    return s
