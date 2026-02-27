import tkinter as tk

# 你的完整稀有模板数据
RAW_DATA = """
=======T1=======
100色无明显白斑断层：87
100色：41、93、205、326、341、348、403、468
99色无明显白斑断层：150、399、449
99色：34、84、105、107、147、201、256、345、375、396、422、428、494
98色无明显白斑断层：482
98色：11、29、46、80、136、137、224、229、278、358、395、401、447
97色无明显白斑断层：488
97色：181
96色：210、324
=======T2=======
99色无明显白斑断层：380
99色：486
98色无明显白斑断层：172、313、314、435、455
98色：43、64、141、173、236、249、308、462、465
97色无明显白斑断层：12、21、76、94、211、295、302、430
97色：6、30、73、89、103、130、145、168、223、260、282、283、377、440、458、466
96色无明显白斑断层：22、157、227、293、361、433、487
96色：33、37、109、154、155、161、191、212、276、285、336、392、424、429、442、446、481
95色无明显白斑断层：104、117、277、299、389
95色：18、79、111、176、179、187、273、289、312、376、382、416、421
95色以下：323、357、491
=======T3=======
96色：47
95色：23、57
95色以下无明显白斑断层：19、25、36、40、56、65、81、85、91、115、118、167、192、200、207、214、215、228、251、255、271、272、297、298、301、342、343、346、347、367、379、427、439、470
95色以下：2、10、26、38、50、51、52、53、61、63、67、69、78、82、95、97、114、139、163、175、240、257、267、270、291、294、300、318、319、322、327、363、365、390、414、431、437、453、475
"""


def parse_data(raw_text):
    database = {}
    current_tier = "Unknown"
    for line in raw_text.strip().split('\n'):
        line = line.strip()
        if not line: continue
        if line.startswith('=======') and line.endswith('======='):
            current_tier = line.strip('=')
        elif '：' in line:
            description, seeds_str = line.split('：')
            seeds = [int(s) for s in seeds_str.split('、') if s.isdigit()]
            for seed in seeds:
                database[seed] = {'tier': current_tier, 'description': description}
    return database


# 解析数据字典
seed_database = parse_data(RAW_DATA)


def check_seed(event=None):
    user_input = entry.get().strip()

    if not user_input:
        result_label.config(text="⚠️ 请输入编号！", fg="#d32f2f")
        return

    try:
        seed = int(user_input)
    except ValueError:
        result_label.config(text="❌ 格式错误：请输入纯数字！", fg="#d32f2f")
        return

    if seed in seed_database:
        info = seed_database[seed]
        tier = info['tier']
        desc = info['description']

        star = "⭐⭐⭐" if tier == "T1" else ("⭐⭐" if tier == "T2" else "⭐")
        color = "#c62828" if tier == "T1" else ("#f57f17" if tier == "T2" else "#2e7d32")

        result_text = f"🎉 恭喜！检测到稀有模板！\n\n👉 模板编号：{seed}\n🏆 稀有级别：{tier} {star}\n💎 模板特征：{desc}"
        result_label.config(text=result_text, fg=color)
        # 如果是稀有模板，保留输入框，不清除
    else:
        result_label.config(text=f"❌ 模板 {seed} 是普通模板。", fg="#616161")
        # 如果是普通模板，自动清空输入框方便下次输入
        entry.delete(0, tk.END)


# ================= 界面设计 =================
root = tk.Tk()
root.title("爪子刀多普勒 P4 稀有检测")
root.geometry("700x500")  # 加宽了窗口以容纳右侧排行
root.configure(bg="#f5f7fa")

# 居中显示窗口
root.eval('tk::PlaceWindow . center')

# ================= 左侧：检测功能区 =================
left_frame = tk.Frame(root, bg="#f5f7fa")
left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=20, pady=20)

title_label = tk.Label(left_frame, text="🔪 爪子刀 P4 稀有检测", font=("Microsoft YaHei", 18, "bold"), bg="#f5f7fa",
                       fg="#333")
title_label.pack(pady=35)

entry = tk.Entry(left_frame, font=("Arial", 16), justify="center", width=15, relief="solid", bd=1)
entry.pack(pady=10)
entry.bind('<Return>', check_seed)  # 绑定回车键

btn = tk.Button(left_frame, text="开 始 检测", font=("Microsoft YaHei", 12, "bold"), bg="#4caf50", fg="white",
                activebackground="#388e3c", activeforeground="white", command=check_seed, width=15, relief="flat",
                cursor="hand2")
btn.pack(pady=15)

result_label = tk.Label(left_frame, text="请输入模板编号进行检测", font=("Microsoft YaHei", 12), bg="#f5f7fa",
                        fg="#757575", justify="center")
result_label.pack(pady=15)

# ================= 右侧：排行图鉴区 =================
right_frame = tk.Frame(root, bg="white", relief="solid", bd=1)
right_frame.pack(side=tk.RIGHT, fill=tk.Y, padx=20, pady=20)

rank_title = tk.Label(right_frame, text="🏆 稀有模板排行", font=("Microsoft YaHei", 14, "bold"), bg="white", fg="#333")
rank_title.pack(pady=10)

# 创建带有滚动条的文本框
scrollbar = tk.Scrollbar(right_frame)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

rank_text = tk.Text(right_frame, width=30, font=("Microsoft YaHei", 10), yscrollcommand=scrollbar.set, bg="white", bd=0,
                    highlightthickness=0)
rank_text.pack(side=tk.LEFT, fill=tk.BOTH, padx=10, pady=5)
scrollbar.config(command=rank_text.yview)

# 设置颜色标签
rank_text.tag_config("t1", foreground="#c62828", font=("Microsoft YaHei", 11, "bold"))
rank_text.tag_config("t2", foreground="#f57f17", font=("Microsoft YaHei", 11, "bold"))
rank_text.tag_config("t3", foreground="#2e7d32", font=("Microsoft YaHei", 11, "bold"))
rank_text.tag_config("item", foreground="#555555", font=("Microsoft YaHei", 10))

# 自动解析提取并插入排行文字
is_first = True
for line in RAW_DATA.strip().split('\n'):
    line = line.strip()
    if not line: continue
    if line.startswith('======='):
        tier = line.strip('=')
        tag_name = tier.lower()  # 转小写，对应上面的 t1/t2/t3
        prefix = "" if is_first else "\n"
        rank_text.insert(tk.END, f"{prefix}【{tier} 级别】\n", tag_name)
        is_first = False
    elif '：' in line:
        # 只提取冒号前面的说明文字
        desc = line.split('：')[0]
        rank_text.insert(tk.END, f" • {desc}\n", "item")

# 设为只读状态，防止鼠标去修改列表
rank_text.config(state=tk.DISABLED)

root.mainloop()