import pyecharts.options as opts
from pyecharts.charts import Bar, Line, Page
import random
import MySQLdb
from datetime import datetime
from datetime import timedelta


def taipei_page():
    try:
        db = MySQLdb.connect(host='127.0.0.1', user='dbuser', passwd='20200428', db='fruveg', port=3307, charset='utf8')
        cursor = db.cursor()

        Item_No = "A1"  # 香蕉
        market_list = [["109", "台北", "台北第一", "Taipei_Banana.html"],               
                       ["104", "台北", "台北第二", "Taipei_Banana.html"]]
    
        for market_index in range(0, len(market_list), 2):
            yesterday = (datetime.now() - timedelta(days=1)).strftime('%Y/%m/%d')
            # 取得2012~昨天所有西元日期放入List trade_date, 並設定為Line Chart及Bar Chart的X軸
            sql = """Select DATE_FORMAT(WDate, '%Y/%m/%d') as WDate 
                     From date_map 
                     Where wdate between '2012/01/01' and '""" + yesterday + """' 
                     Order by WDate;"""
            print("--------------------------------------4")
            cursor.execute(sql)
            datarows = cursor.fetchall()
            trade_date_1 = [row[0] for row in datarows]
            print("--------------------------------------5")

            # 依果菜市場代碼取得2012~昨天[每天]的交易平均單價及交易量
            # 並放入List avg_price trade_amount, 並加入Line Chart 及 Bar Chart Y軸系列
            sql = """Select a.trade_date, b.market_no, b.avg_price, b.trade_amount 
                     From 
                     (Select wDate as trade_date
                      From date_map 
                      Where wdate between '2012/01/01' and '%s') a 
                      Left Join 
                      (Select trade_date, market_no, avg_price, trade_amount  
                       From trade_raws 
                       Where item_no='%s' 
                       and market_no='%s'
                       and trade_date between '2012/01/01' and '%s') b
                       on a.trade_date=b.trade_date 
                       order by a.trade_date;""" % (yesterday, Item_No, market_list[market_index][0], yesterday)

            cursor.execute(sql)
            datarows = cursor.fetchall()
            avg_price_1 = [row[2] for row in datarows]
            trade_amount_1 = [row[3] for row in datarows]

            # 設定Line Chart屬性
            linechart_1 = (
                Line(
                    init_opts=opts.InitOpts(width="100%", height="400px")
                )
                    .add_xaxis(trade_date_1)
                    .add_yaxis(
                    "平均價格(NT$)",
                    avg_price_1,
                    is_connect_nones=True,
                    label_opts=opts.LabelOpts(is_show=False)
                )
                    # 因後續Line Chart要合併Bar Chart, 在此新增Line Chart右邊X軸的刻度
                    # 為了讓平均價格趨勢線及成交量合併後畫面的好看, 因此定義右邊X軸的最小及最大刻度
                    .extend_axis(
                    yaxis=opts.AxisOpts(
                        name="交易量(公斤)",
                        type_="value",
                        min_=0,
                        max_=80000,
                        interval=10000,
                        axislabel_opts=opts.LabelOpts(formatter="{value}"),
                    )
                )
                    .set_global_opts(
                    title_opts=opts.TitleOpts("%s果菜市場\n香蕉每日批發平均價格及交易量" % market_list[market_index][2], pos_left="center"),
                    datazoom_opts=opts.DataZoomOpts(type_="slider", range_start=97, range_end=100),
                    legend_opts=opts.LegendOpts(is_show=False),
                    tooltip_opts=opts.TooltipOpts(is_show=True, axis_pointer_type="cross"),
                    yaxis_opts=opts.AxisOpts(
                        name="新台幣(元)",
                        splitline_opts=opts.SplitLineOpts(is_show=True),
                    ),
                )
            )

            # 設定Bar Chart屬性
            barchart_1 = (
                Bar(init_opts=opts.InitOpts(width="100%", height="150px"))
                    .add_xaxis(trade_date_1)
                    .add_yaxis(
                    "成交量(公斤)",
                    trade_amount_1,
                    yaxis_index=1,
                    color="#00E3E3",
                    label_opts=opts.LabelOpts(is_show=False)
                )
                    .set_global_opts(
                    datazoom_opts=opts.DataZoomOpts(type_="slider", range_start=97, range_end=100),
                    legend_opts=opts.LegendOpts(is_show=False),
                    tooltip_opts=opts.TooltipOpts(is_show=True),
                    yaxis_opts=opts.AxisOpts(
                        name="公斤",
                        splitline_opts=opts.SplitLineOpts(is_show=True),
                    ),
                )
            )

            # 合併Line Chart及Bar Chart
            # linechart.overlap(barchart).render("Taipei_Banana.html")
            myoverlap_1 = linechart_1.overlap(barchart_1)

            today = datetime.now().strftime('%Y/%m/%d')
            t30 = (datetime.now() + timedelta(days=30)).strftime('%Y/%m/%d')
            # 產生今天起30天預測線Line Chart 並加入List pred_date
            sql = """Select Date_Format(WDate, '%Y/%m/%d') as WDate
                     From date_map
                     Where WDate Between '""" + today + """' and '""" + t30 + """'
                     Order by WDate;"""
            cursor.execute(sql)
            datarows = cursor.fetchall()
            pred_date_1 = [WDate[0] for WDate in datarows]

            # 產生30筆20~50之間的亂數做為虛擬的預測平均價格, 放入List pred_price
            pred_price_1 = [random.randrange(20, 50) for i in range(1, 31)]

            pred_linechart_1 = (
                Line(init_opts=opts.InitOpts(width="100%", height="250px"))
                    .add_xaxis(pred_date_1)
                    .add_yaxis(
                    "預測平均價格(NT$)",
                    pred_price_1,
                    is_connect_nones=True,
                    label_opts=opts.LabelOpts(is_show=False)
                )
                    .set_global_opts(
                    title_opts=opts.TitleOpts("[預測]%s果菜市場\n香蕉批發平均價格及交易量" % market_list[market_index][2], pos_left="center"),
                    # datazoom_opts=opts.DataZoomOpts(type_="slider", range_start=97, range_end=100),
                    legend_opts=opts.LegendOpts(is_show=False),
                    tooltip_opts=opts.TooltipOpts(is_show=True, axis_pointer_type="cross"),
                    yaxis_opts=opts.AxisOpts(
                        name="新台幣(元)",
                        splitline_opts=opts.SplitLineOpts(is_show=True),
                    ),
                )
            )

            # 以上完成區域第一個市場
            # -----------------------------------------------------------------------------------------------------------
            # 以下開始區域第二個市場
            trade_date_2 = trade_date_1

            # 依果菜市場代碼取得2012~昨天[每天]的交易平均單價及交易量
            # 並放入List avg_price trade_amount, 並加入Line Chart 及 Bar Chart Y軸系列
            sql = """Select a.trade_date, b.market_no, b.avg_price, b.trade_amount 
                     From 
                     (Select wDate as trade_date
                      From date_map 
                      Where wdate between '2012/01/01' and '%s') a 
                      Left Join 
                      (Select trade_date, market_no, avg_price, trade_amount  
                       From trade_raws 
                       Where item_no='%s' 
                       and market_no='%s'
                       and trade_date between '2012/01/01' and '%s') b
                       on a.trade_date=b.trade_date 
                       order by a.trade_date;""" % (yesterday, Item_No, market_list[market_index + 1][0], yesterday)

            cursor.execute(sql)
            datarows = cursor.fetchall()
            avg_price_2 = [row[2] for row in datarows]
            trade_amount_2 = [row[3] for row in datarows]

            # 設定Line Chart屬性
            linechart_2 = (
                Line(
                    init_opts=opts.InitOpts(width="100%", height="400px")
                )
                    .add_xaxis(trade_date_2)
                    .add_yaxis(
                    "平均價格(NT$)",
                    avg_price_2,
                    is_connect_nones=True,
                    label_opts=opts.LabelOpts(is_show=False)
                )
                    # 因後續Line Chart要合併Bar Chart, 在此新增Line Chart右邊X軸的刻度
                    # 為了讓平均價格趨勢線及成交量合併後畫面的好看, 因此定義右邊X軸的最小及最大刻度
                    .extend_axis(
                    yaxis=opts.AxisOpts(
                        name="交易量(公斤)",
                        type_="value",
                        min_=0,
                        max_=80000,
                        interval=10000,
                        axislabel_opts=opts.LabelOpts(formatter="{value}"),
                    )
                )
                    .set_global_opts(
                    title_opts=opts.TitleOpts("%s果菜市場\n香蕉每日批發平均價格及交易量" % market_list[market_index + 1][2],
                                              pos_left="center"),
                    datazoom_opts=opts.DataZoomOpts(type_="slider", range_start=97, range_end=100),
                    legend_opts=opts.LegendOpts(is_show=False),
                    tooltip_opts=opts.TooltipOpts(is_show=True, axis_pointer_type="cross"),
                    yaxis_opts=opts.AxisOpts(
                        name="新台幣(元)",
                        splitline_opts=opts.SplitLineOpts(is_show=True),
                    ),
                )
            )

            # 設定Bar Chart屬性
            barchart_2 = (
                Bar(init_opts=opts.InitOpts(width="100%", height="150px"))
                    .add_xaxis(trade_date_1)
                    .add_yaxis(
                    "成交量(公斤)",
                    trade_amount_2,
                    yaxis_index=1,
                    color="#00E3E3",
                    label_opts=opts.LabelOpts(is_show=False)
                )
                    .set_global_opts(
                    datazoom_opts=opts.DataZoomOpts(type_="slider", range_start=97, range_end=100),
                    legend_opts=opts.LegendOpts(is_show=False),
                    tooltip_opts=opts.TooltipOpts(is_show=True),
                    yaxis_opts=opts.AxisOpts(
                        name="公斤",
                        splitline_opts=opts.SplitLineOpts(is_show=True),
                    ),
                )
            )

            # 合併Line Chart及Bar Chart
            # linechart.overlap(barchart).render("Taipei_Banana.html")
            myoverlap_2 = linechart_2.overlap(barchart_2)

            # 產生預測線Line Chart
            pred_date_2 = pred_date_1

            # 產生30筆25~50之間的亂數做為虛擬的預測平均價格, 放入List pred_price
            pred_price_2 = [random.randrange(25, 50) for i in range(1, 31)]

            pred_linechart_2 = (
                Line(init_opts=opts.InitOpts(width="100%", height="250px"))
                    .add_xaxis(pred_date_2)
                    .add_yaxis(
                    "預測平均價格(NT$)",
                    pred_price_2,
                    is_connect_nones=True,
                    label_opts=opts.LabelOpts(is_show=False)
                )
                    .set_global_opts(
                    title_opts=opts.TitleOpts("[預測]%s果菜市場\n香蕉批發平均價格及交易量" % market_list[market_index + 1][2],
                                              pos_left="center"),
                    # datazoom_opts=opts.DataZoomOpts(type_="slider", range_start=97, range_end=100),
                    legend_opts=opts.LegendOpts(is_show=False),
                    tooltip_opts=opts.TooltipOpts(is_show=True, axis_pointer_type="cross"),
                    yaxis_opts=opts.AxisOpts(
                        name="新台幣(元)",
                        splitline_opts=opts.SplitLineOpts(is_show=True),
                    ),
                )
            )

            # 以上完成區域第二個市場
            # ----------------------------------------------------------------------------------------------------------
            # 以下將兩個市場的圖合併在一個網頁中
            mypage = (
                Page(page_title="%s" % market_list[market_index][1])
                    .add(myoverlap_1, pred_linechart_1)
                    .add(myoverlap_2, pred_linechart_2)
            )

            mypage.render(r"./static/%s" % market_list[market_index][3])

    except Exception as Err:
        print(Err)

    db.close()
