import tkinter as tk #匯入tkinter，用來建立提醒視窗與按鈕
from tkinter import messagebox #匯入messagebox，用來跳出提示訊息框
from datetime import datetime, timedelta #datetime取得現在時間，timedelta用來計算延後時間
import time 

# 設定要提醒的時間，格式為"小時:分鐘"
# 用字串儲存，之後會拿來和目前時間比較
# 原本是單一提醒時間版本 reminder_time = "14:19"

# 設定一周每天的提醒時間
# Python中 weekday()的數字代表: 0=星期一、1=星期二、2=星期三、3=星期四、4=星期五、5=星期六、6=星期日
weekly_schedule ={
    0: "17:40", # 星期一
    1: "18:00", # 星期二
    2: "18:00", # 星期三
    3: "18:00", # 星期四
    4: "18:00", # 星期五
    5: "20:00", # 星期六
    6: "20:00", # 星期日
}

# 延後提醒時間，一開始還沒有延後所以設為None
#若使用者按下延後提醒，變數會改成新的datetime
delayed_time = None

# 紀錄今天是否完成提醒
# False 代表尚未完成，True代表已完成
reminder_finished_today = False

# 紀錄今天是否已顯示過原始提醒
# 用來避免同一分鐘內重複跳出提醒視窗
original_reminder_shown_today = False

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
def delay_one_minute(window):
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

# 顯示提醒視窗
def show_reminder():
    # 印出訊息，確認程式有進入這個函式
    print(">>> 已進入 show_reminder()，準備跳出視窗")
    # 建立一個新的視窗
    window = tk.Tk()
    # 設定視窗的標題
    window.title("電卡提醒")
    # 設定視窗的大小
    window.geometry("300x180")
    
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
    delay_button = tk.Button(window, text="延後一小時", command=lambda: delay_one_minute(window)) # 呼叫延後函式
    # 將按鈕放到視窗上
    delay_button.pack(pady=5)

    # 將視窗持續運作 (等待使用者操作)
    window.mainloop()

# 印出程式啟動提示
print("程式已啟動")
# 顯示目前設定的提醒時間
# print("原始提醒時間 =", reminder_time)
print("每週提醒時間表 =", weekly_schedule)

# 迴圈，讓程式持續運行 (持續檢查時間))
while True:
    # 取得現在的時間
    now = datetime.now()

    # 換天重置 如果現在日期不適之前紀錄的日期(已換天)
    if now.date() != today_date:
        # 更新今天日期
        today_date = now.date()
        # 清除延後提醒時間
        delayed_time = None
        # 重設「是否完成」狀態
        reminder_finished_today = False
        # 重設「是否顯示過提醒」狀態
        original_reminder_shown_today = False
        # 印出提示訊息
        print("已換天，狀態重置")

    # 每5秒印一次現在狀態
    print(
        "現在時間 =",
        now.strftime("%H:%M:%S"),
        # "| reminder_time =", 
        # reminder_time, #原始提醒時間
        "| delayed_time =",
        delayed_time.strftime("%H:%M:%S") if delayed_time else None, #如果有延後時間就顯示，沒就顯示None
        "| finished =",
        reminder_finished_today, #是否已完成
        "| shown_today =",
        original_reminder_shown_today #是否已顯示提醒
    )

    # 如果今天已完成，就不再提醒
    if reminder_finished_today:
        time.sleep(5)
        #跳過以下程式，直接回到while開頭重新檢查
        continue

    # current_time = now.strftime("%H:%M") 

    # 優先判斷延後提醒
    if delayed_time is not None:
        #如果現在時間已超過或等於延後時間
        if now >= delayed_time:
            print(">>> 延後時間到了，準備提醒")
            # 清除延後時間
            delayed_time = None
            #呼叫提醒視窗
            show_reminder()
    
    # 沒有延後提醒，才判斷原始提醒
    # else:
    # ===== 改良版：避免錯過提醒 =====

    # 將設定時間轉成今天的 datetime
    # reminder_datetime = datetime.combine(
    #    now.date(),
    #    datetime.strptime(reminder_time, "%H:%M").time())

    # 判斷是否要觸發原始提醒（或補發）
    #if not original_reminder_shown_today and now >= reminder_datetime:
    #    print(">>> 原始提醒時間（或補發）到了，準備提醒")
    #    original_reminder_shown_today = True
    #    show_reminder()
    
    # ===== 每週不同提醒時間版本 =====
    else:

        # 取得今天是星期幾
        # weekday() 回傳 0~6，0代表星期一，6代表星期日
        weekday = now.weekday()

        # 根據今天星期幾，從 weekly_schedule 取得今天的提醒時間
        reminder_time = weekly_schedule[weekday]

        # 將今天的提醒時間轉換成 datetime 物件
        reminder_datetime = datetime.combine(
            now.date(),
            datetime.strptime(reminder_time, "%H:%M").time()
        )

        # 判斷是否要觸發原始提醒或補發提醒
        if not original_reminder_shown_today and now >= reminder_datetime:
            print(">>> 今天的提醒時間到了，準備提醒")
            original_reminder_shown_today = True
            show_reminder()

    time.sleep(5)
