import threading
import json
import tkinter as tk #匯入tkinter，用來建立提醒視窗與按鈕
from tkinter import messagebox #匯入messagebox，用來跳出提示訊息框
from datetime import datetime, timedelta #datetime取得現在時間，timedelta用來計算延後時間
import time 
import smtplib
from email.mime.text import MIMEText
from email.header import Header
root = tk.Tk()
root.withdraw()

def send_email_notification():
    sender_email = email_config["sender_email"]
    receiver_email = email_config["sender_email"]  # 寄給自己
    app_password = email_config["app_password"]
    # 以下不變...
    # --- 設定區 ---
    smtp_server = "smtp.gmail.com"
    smtp_port = 587
    #sender_email = "你的Gmail@gmail.com"
    #receiver_email = "接收通知的Email@gmail.com" # 可以跟寄件者相同
    #app_password = "你的16位應用程式密碼" 
    # -------------

    msg = MIMEText("提醒：時間到了，記得處理電卡！\n換卡連結：https://dormtopup.prince.com.tw/User/D01", "plain", "utf-8")
    msg["Subject"] = Header("【電卡提醒】該換電卡囉！", "utf-8")
    msg["From"] = sender_email
    msg["To"] = receiver_email

    try:
        # 建立與 SMTP 伺服器的連線
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()  # 啟動加密傳輸
        server.login(sender_email, app_password)
        server.sendmail(sender_email, receiver_email, msg.as_string())
        server.quit()
        print(">>> Gmail 通知已成功發送")
    except Exception as e:
        print(f">>> 郵件發送失敗: {e}")

# 設定要提醒的時間，格式為"小時:分鐘"
# 用字串儲存，之後會拿來和目前時間比較
# 原本是單一提醒時間版本 reminder_time = "14:19"

# 設定一周每天的提醒時間
# Python中 weekday()的數字代表: 0=星期一、1=星期二、2=星期三、3=星期四、4=星期五、5=星期六、6=星期日
# =====原本固定的weekly_schedule版本=====
# weekly_schedule ={
   # 0: "17:40",
   # 1: "18:00",
   # 2: "18:00",
   # 3: "18:00",
   # 4: "18:00",
   # 5: "20:00",
   # 6: "20:00",
# }

# =====讓使用者輸入一周每天的提醒時間，且用JSON處存版本=====

# 設定json檔案名稱
schedule_file = "weekly_schedule.json"

# 用GUI視窗繞使用者輸入一周提醒時間
def create_schedule_with_gui():
    weekly_schedule = {}

    weekdays = {
        0: "星期一",
        1: "星期二",
        2: "星期三",
        3: "星期四",
        4: "星期五",
        5: "星期六",
        6: "星期日"
    }

    
    setting_window = tk.Toplevel(root)
    setting_window.lift()
    setting_window.focus_force()
    setting_window.attributes('-topmost', True)  # 確保視窗在最上面
    setting_window.title("設定每週提醒時間")
    setting_window.geometry("350x350")
    

    entries = {}

    title_label = tk.Label(setting_window, text="請設定每天的提醒時間", font=("Arial", 14))
    title_label.pack(pady=10)

    for day_number, day_name in weekdays.items():
        row = tk.Frame(setting_window)
        row.pack(pady=3)

        label = tk.Label(row, text=day_name, width=8)
        label.pack(side="left")

        entry = tk.Entry(row, width=10)
        entry.insert(0, "18:00")
        entry.pack(side="left")

        entries[day_number] = entry

    def save_schedule():
        for day_number, entry in entries.items():
            user_time = entry.get()

            try:
                datetime.strptime(user_time, "%H:%M")
            except ValueError:
                messagebox.showerror(
                    "格式錯誤",
                    f"{weekdays[day_number]} 的時間格式錯誤！\n請輸入例如 18:00"
                )
                return

            weekly_schedule[day_number] = user_time

        with open(schedule_file, "w", encoding="utf-8") as file:
            json.dump(
                weekly_schedule,
                file,
                ensure_ascii=False,
                indent=4
            )

        messagebox.showinfo("完成", "每週提醒時間已儲存！")
        setting_window.destroy()

    save_button = tk.Button(setting_window, text="儲存設定", command=save_schedule)
    save_button.pack(pady=15)

    #setting_window.mainloop()
    root.wait_window(setting_window)

    return weekly_schedule

try:
    # 嘗試從檔案讀取每週提醒時間
    with open(schedule_file, "r", encoding="utf-8") as file:
        # 將JSON內容轉成Python dict 
        weekly_schedule = json.load(file)
        # JSON 的 key 會變成字串，所以轉回 int
        weekly_schedule = {
            int(key): value
            for key, value in weekly_schedule.items()
        }
    print("已成功讀取 weekly_schedule.json")

#如果檔案不存在
except FileNotFoundError:
    print("找不到設定檔，開始建立新的 weekly_schedule")
    weekly_schedule = create_schedule_with_gui()

    # #建立空字典，用來儲存每周提醒時間
    # weekly_schedule = {}
    # #建立星期對照表
    # weekdays = {
    # 0: "星期一",
    # 1: "星期二",
    # 2: "星期三",
    # 3: "星期四",
    # 4: "星期五",
    # 5: "星期六",
    # 6: "星期日"
    # }
    # #讓使用者輸入每天的提醒時間
    # for day_number, day_name in weekdays.items():
    #     # input() 讓使用者輸入時間
    #     user_time = input(f"請輸入{day_name}的提醒時間，例如 18:00：")
    #     # 將輸入結果存進weekly_schedule字典
    #     weekly_schedule[day_number] = user_time
    
    # # 將設定儲存到JSON檔案
    # with open(schedule_file, "w", encoding="utf-8") as file:
    #     json.dump(
    #         weekly_schedule, 
    #         file,
    #         ensure_ascii=False, #確保中文能正常儲存
    #         indent=4 #讓JSON檔案有縮排，方便閱讀
    #     )

#建立email通知
email_config_file = "email_config.json"

def create_email_config_with_gui():
    config = {}

    config_window = tk.Toplevel(root)
    config_window.title("設定 Gmail 收信帳號")
    config_window.geometry("400x250")
    config_window.lift()
    config_window.focus_force()
    config_window.attributes('-topmost', True)

    tk.Label(config_window, text="請設定收信用的 Gmail 帳號", font=("Arial", 13)).pack(pady=10)

    # Gmail 帳號
    row1 = tk.Frame(config_window)
    row1.pack(pady=5)
    tk.Label(row1, text="Gmail 帳號", width=12).pack(side="left")
    email_entry = tk.Entry(row1, width=28)
    email_entry.pack(side="left")

    # 應用程式密碼
    row2 = tk.Frame(config_window)
    row2.pack(pady=5)
    tk.Label(row2, text="你的16位Google\n應用程式密碼", width=12).pack(side="left")
    password_entry = tk.Entry(row2, width=28, show="*")  # show="*" 讓密碼顯示成星號
    password_entry.pack(side="left")

    def save_config():
        config["sender_email"] = email_entry.get()
        config["app_password"] = password_entry.get()

        with open(email_config_file, "w", encoding="utf-8") as f:
            json.dump(config, f, ensure_ascii=False, indent=4)

        messagebox.showinfo("完成", "Gmail 設定已儲存！")
        config_window.destroy()

    tk.Button(config_window, text="儲存設定", command=save_config).pack(pady=15)
    # config_window.mainloop()
    root.wait_window(config_window)

    return config

try:
    with open(email_config_file, "r", encoding="utf-8") as f:
        email_config = json.load(f)
    print("已成功讀取 email_config.json")
except FileNotFoundError:
    print("找不到 Gmail 設定，開始建立新的設定")
    email_config = create_email_config_with_gui()


# 延後提醒時間，一開始還沒有延後所以設為None
#若使用者按下延後提醒，變數會改成新的datetime
delayed_time = None

# 紀錄今天是否完成提醒
# False 代表尚未完成，True代表已完成
reminder_finished_today = False

# 紀錄今天是否已顯示過原始提醒
# 用來避免同一分鐘內重複跳出提醒視窗
original_reminder_shown_today = False

# 紀錄今天是否已經印出提醒時間
schedule_printed_today = False

# 記錄程式啟動的日期
# 之後可以用來判斷是否已經換到新的一天
today_date = datetime.now().date()



# 定義:當使用者按下「已處理」按鈕的時候執行
def mark_done(window):
    # 修改外面的全域變數
    global reminder_finished_today
    # 將今天的提醒狀態改為已完成「之後不會再體醒」
    reminder_finished_today = True
    # 在終端機印出訊息
    print("你按了：已處理")
    # 跳出提醒視窗，告訴使用者已完成
    messagebox.showinfo("完成", "你已經處理完電卡提醒！")
    # 關閉目前的提醒視窗
    window.destroy()

# 當使用者按下「延後一小時」按鈕時執行
def delay_one_hour(window):
    # 使用global， 表示要修改外部的delayed_time變數
    global delayed_time
    # 取得目前的時間 (datetime 物件)
    now = datetime.now()
    
    # 設定新的提醒時間 = 現在時間 + 1小時
    # timedelta 用來作時間加法
    delayed_time = now + timedelta(hours=1)
    # 在終端機印出新的延後時間 
    print("你按了：延後一小時，新時間 =", delayed_time.strftime("%H:%M:%S"))
    # 跳出提醒視窗，顯示延後之後的提醒時間
    messagebox.showinfo("延後", f"提醒已延後到 {delayed_time.strftime('%H:%M:%S')}")
    # 關閉提醒視窗
    window.destroy()

# 重新開啟 weekly_schedule 設定視窗
# 因為原先設定完如果還是超過並不會再次跳出提醒視窗
def change_schedule(window):
    global weekly_schedule, original_reminder_shown_today, schedule_printed_today

    window.destroy()

    # 取得新的時間設定，並更新記憶體裡的 weekly_schedule
    new_schedule = create_schedule_with_gui()
    if new_schedule:
        weekly_schedule = new_schedule

    # 重設提醒狀態，讓新時間可以重新觸發
    original_reminder_shown_today = False
    schedule_printed_today = False

    messagebox.showinfo("完成", "新的提醒時間已更新！")

# 建立控制面板視窗
# 使用者可隨時修改提醒時間，不需手動修改 JSON 檔案
def open_control_panel():
    panel = tk.Toplevel(root)
    panel.title("電卡提醒系統")
    panel.geometry("300x180")

    title_label = tk.Label(panel, text="電卡提醒系統", font=("Arial", 14))
    title_label.pack(pady=10)

    today_weekday = datetime.now().weekday()
    today_time = weekly_schedule[today_weekday]

    time_label = tk.Label(panel, text=f"今天提醒時間：{today_time}", font=("Arial", 12))
    time_label.pack(pady=10)

    #當使用者按下「修改提醒時間」時執行
    def edit_time():
        global weekly_schedule, original_reminder_shown_today, schedule_printed_today
        # 開啟設定時間的視窗讓使用者重新設定時間
        new_schedule = create_schedule_with_gui()

        if new_schedule:
            weekly_schedule = new_schedule #將新的時間表更新到程式記憶體
            original_reminder_shown_today = False  #重新設置提醒狀態、避免今天已經顯示過提醒而無法套用新時間
            schedule_printed_today = False #系統重新顯示新的提醒時間

            today_weekday = datetime.now().weekday()
            # 更新控制面板上提醒時間的文字
            time_label.config(text=f"今天提醒時間：{weekly_schedule[today_weekday]}")
            #通知使用者新的提醒時間已生效
            messagebox.showinfo("完成", "提醒時間已更新，程式會立刻使用新時間！")

    edit_button = tk.Button(panel, text="修改提醒時間", command=edit_time)
    edit_button.pack(pady=5)

    close_button = tk.Button(panel, text="關閉面板", command=panel.destroy)
    close_button.pack(pady=5)

    #panel.mainloop()
#def change_schedule(window):

    # 關閉目前提醒視窗
    #window.destroy()

    # 開啟設定視窗
    #create_schedule_with_gui()

    # 提示使用者
    #messagebox.showinfo("完成", "新的提醒時間已更新！")

# 顯示提醒視窗
def show_reminder():
    # 印出訊息，確認程式有進入這個函式
    print(">>> 已進入 show_reminder()，準備跳出視窗並發送郵件")
    
    # 這裡加入發送郵件的功能
    send_email_notification()
    # 建立一個新的視窗
    window = tk.Toplevel(root)
    # 設定視窗的標題
    window.title("電卡提醒")
    # 設定視窗的大小
    window.geometry("300x180")
    window.lift()
    window.focus_force()
    window.attributes('-topmost', True)  # 確保視窗在最上面
    
    # 建立文字標籤(顯示提醒的內容)
    label = tk.Label(window, text="記得處理電卡！", font=("Arial", 14))
    # 標籤放到視窗上並設定間距
    label.pack(pady=20) # .pack 把元件放上畫面，沒有的話會看不到東西

    # 建立「已處理」的按鈕
    # command 表示按下按鈕時要執行的函式
    # lambda 是要等按下按鈕再執行 等於延遲執行(等按才做)
    done_button = tk.Button(window, text="已處理", command=lambda: mark_done(window)) # 呼叫mark_down並傳入視窗 
    # 將按鈕放到視窗上
    done_button.pack(pady=5)

    # 建立延後一小時的按鈕
    delay_button = tk.Button(window, text="延後一小時", command=lambda: delay_one_hour(window)) # 呼叫延後函式
    # 將按鈕放到視窗上
    delay_button.pack(pady=5)
    # 建立修改設定按鈕
    change_button = tk.Button(
        window,
        text="修改提醒時間",
        command=lambda: change_schedule(window)
    )

    #將按鈕放到視窗上
    change_button.pack(pady=5)

    # 將視窗持續運作 (等待使用者操作)
    #window.mainloop()

# 建立獨立執行緒執行控制面板
# threading.Thread(
#     target=open_control_panel,
#     daemon=True
# ).start()

# # 印出程式啟動提示
# print("程式已啟動")
# # 顯示目前設定的提醒時間
# # print("原始提醒時間 =", reminder_time)
# print("每週提醒時間表 =", weekly_schedule)

# # 迴圈，讓程式持續運行 (持續檢查時間))
# while True:
#     # 取得現在的時間
#     now = datetime.now()

#     # 換天重置 如果現在日期不適之前紀錄的日期(已換天)
#     if now.date() != today_date:
#         # 更新今天日期
#         today_date = now.date()
#         # 清除延後提醒時間
#         delayed_time = None
#         # 重設「是否完成」狀態
#         reminder_finished_today = False
#         # 重設「是否顯示過提醒」狀態
#         original_reminder_shown_today = False
#         # 印出提示訊息
#         schedule_printed_today = False
#         print("已換天，狀態重置")

#     # 每5秒印一次現在狀態
#     print(
#         "現在時間 =",
#         now.strftime("%H:%M:%S"),
#         # "| reminder_time =", 
#         # reminder_time, #原始提醒時間
#         "| delayed_time =",
#         delayed_time.strftime("%H:%M:%S") if delayed_time else None, #如果有延後時間就顯示，沒就顯示None
#         "| finished =",
#         reminder_finished_today, #是否已完成
#         "| shown_today =",
#         original_reminder_shown_today #是否已顯示提醒
#     )

#     # 如果今天已完成，就不再提醒
#     if reminder_finished_today:
#         time.sleep(5)
#         #跳過以下程式，直接回到while開頭重新檢查
#         continue

#     # current_time = now.strftime("%H:%M") 

#     # 優先判斷延後提醒
#     if delayed_time is not None:
#         #如果現在時間已超過或等於延後時間
#         if now >= delayed_time:
#             print(">>> 延後時間到了，準備提醒")
#             # 清除延後時間
#             delayed_time = None
#             #呼叫提醒視窗
#             show_reminder()
    
#     # 沒有延後提醒，才判斷原始提醒
#     # else:
#     # ===== 改良版：避免錯過提醒 =====

#     # 將設定時間轉成今天的 datetime
#     # reminder_datetime = datetime.combine(
#     #    now.date(),
#     #    datetime.strptime(reminder_time, "%H:%M").time())

#     # 判斷是否要觸發原始提醒（或補發）
#     #if not original_reminder_shown_today and now >= reminder_datetime:
#     #    print(">>> 原始提醒時間（或補發）到了，準備提醒")
#     #    original_reminder_shown_today = True
#     #    show_reminder()
    
#     # ===== 每週不同提醒時間版本 =====
#     else:

#         # 取得今天是星期幾
#         # weekday() 回傳 0~6，0代表星期一，6代表星期日
#         weekday = now.weekday()

#         # 根據今天星期幾，從 weekly_schedule 取得今天的提醒時間
#         reminder_time = weekly_schedule[weekday]
        
#         # print("今天的提醒時間 =", reminder_time)

#         #只在今天第一次讀取提醒時間時印出
#         if not schedule_printed_today:
#             print("今天的提醒時間 =", reminder_time)
#             schedule_printed_today = True
        
#         # 將今天的提醒時間轉換成 datetime 物件
#         reminder_datetime = datetime.combine(
#             now.date(),
#             datetime.strptime(reminder_time, "%H:%M").time()
#         )

#         # 判斷是否要觸發原始提醒或補發提醒
#         if not original_reminder_shown_today and now >= reminder_datetime:
#             print(">>> 今天的提醒時間到了，準備提醒")
#             original_reminder_shown_today = True
#             show_reminder()

#     time.sleep(5)

def timer_loop():
    global delayed_time, reminder_finished_today, original_reminder_shown_today
    global schedule_printed_today, today_date

    while True:
        now = datetime.now()

        if now.date() != today_date:
            today_date = now.date()
            delayed_time = None
            reminder_finished_today = False
            original_reminder_shown_today = False
            schedule_printed_today = False
            print("已換天，狀態重置")

        print(
            "現在時間 =", now.strftime("%H:%M:%S"),
            "| delayed_time =", delayed_time.strftime("%H:%M:%S") if delayed_time else None,
            "| finished =", reminder_finished_today,
            "| shown_today =", original_reminder_shown_today
        )

        if not reminder_finished_today:
            if delayed_time is not None:
                if now >= delayed_time:
                    print(">>> 延後時間到了，準備提醒")
                    delayed_time = None
                    root.after(0, show_reminder)  # ← 通知主執行緒開視窗
            else:
                weekday = now.weekday()
                reminder_time = weekly_schedule[weekday]

                if not schedule_printed_today:
                    print("今天的提醒時間 =", reminder_time)
                    schedule_printed_today = True

                reminder_datetime = datetime.combine(
                    now.date(),
                    datetime.strptime(reminder_time, "%H:%M").time()
                )

                if not original_reminder_shown_today and now >= reminder_datetime:
                    print(">>> 今天的提醒時間到了，準備提醒")
                    original_reminder_shown_today = True
                    root.after(0, show_reminder)  # ← 通知主執行緒開視窗

        time.sleep(5)


print("程式已啟動")
print("每週提醒時間表 =", weekly_schedule)

# 計時迴圈放背景執行緒
threading.Thread(target=timer_loop, daemon=True).start()

# 控制面板和 mainloop 在主執行緒
open_control_panel()
root.mainloop()