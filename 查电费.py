import core.net as net
import datetime
import matplotlib.pyplot as plt

# 获取电费使用情况
def get_electricity_use():
    today = datetime.datetime.today()
    data = net.post_json("https://api.baletu.com/App401/User/getElectricMeterMonthlyWattage", {
        "year": str(today.year),
        "month": str(today.month),
        "v": "6.0.7",
        "use_type": "0",
        "city_id": "1",
        "ut": "xxxx",
        "user_id": "1017963078",
    })
    # printLog("巴乐兔结果:", data)
    use = 0.0
    share = 0.0
    # 计算本月总用电量
    if "result" in data and "list" in data["result"]:
        for day in data["result"]["list"]:
            try:
                use += float(day["wattage"])
                share += float(day["shared_value"])
            except Exception as e:
                pass
        # 获取剩余用电和昨日用电
        remain = data["result"]["list"][-1]["read_value"]
        today = data["result"]["list"][-1]["wattage"]
        # 保存统计图片
        get_chart(data["result"]["list"])
        total = use+share
        return "总用电量:%.2f度 [电费:%.2f元]\n本月分摊电量:%.2f\n本月用电量:%.2f\n累计剩余电量:%s\n昨日用电量:%s" % (total, total*0.9, share, use, remain, today)
    else:
        return "获取结果失败"


# 绘制折线图
def get_chart(data):
    use = {"x": [], "y": []}
    share = {"x": [], "y": []}
    for item in data:
        # 图表中添加数字
        try:
            now = str(item["date"])
            now = now.split("-")[-1]
            use["y"].append(float(item["wattage"]))
            use["x"].append(now)
            share["y"].append(round(float(item["shared_value"]), 2))
            share["x"].append(now)
        except Exception as e:
            pass
    #  清空
    plt.close()
    # 添加字体
    plt.rcParams['font.sans-serif'] = ['SimHei']  # 用黑体显示中文
    # 设置两条直线
    l1 = plt.plot(use["x"], use["y"], label="个人")
    l2 = plt.plot(share["x"], share["y"], label="共享")
    # 设置线条颜色
    plt.setp(l1, color='r')
    plt.setp(l2, color='g')
    # 设置标题
    plt.title('使用情况')
    plt.xlabel("日期")
    plt.ylabel("电费(单位:度)")
    # 加上这个才会显示图例
    plt.legend()
    # 设置网格
    plt.grid()
    # 保存到本地
    plt.savefig("01.jpg", dpi=100)


if __name__ == '__main__':
    print(get_electricity_use())