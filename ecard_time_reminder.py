import tkinter as tk
from tkinter import messagebox
from datetime import datetime, timedelta
import time

# 把提醒時間改成現在往後兩分鐘，例如 "21:20"
reminder_time = "14:19"

# 延後提醒時間（一開始沒有）
delayed_time = None

# 今天是否完成提醒
reminder_finished_today = False

# 今天是否已顯示過原始提醒
original_reminder_shown_today = False

# 記錄今天日期
today_date = datetime.now().date()


def mark_done(window):
    global reminder_finished_today
    reminder_finished_today = True
    print("你按了：已處理")
    messagebox.showinfo("完成", "你已經處理完電卡提醒！")
    window.destroy()


def delay_one_minute(window):
    global delayed_time
    now = datetime.now()
    delayed_time = now + timedelta(minutes=1)
    print("你按了：延後一分鐘，新時間 =", delayed_time.strftime("%H:%M:%S"))
    messagebox.showinfo("延後", f"提醒已延後到 {delayed_time.strftime('%H:%M:%S')}")
    window.destroy()


def show_reminder():
    print(">>> 已進入 show_reminder()，準備跳出視窗")
    window = tk.Tk()
    window.title("電卡提醒")
    window.geometry("300x180")

    label = tk.Label(window, text="記得處理電卡！", font=("Arial", 14))
    label.pack(pady=20)

    done_button = tk.Button(window, text="已處理", command=lambda: mark_done(window))
    done_button.pack(pady=5)

    delay_button = tk.Button(window, text="延後一分鐘", command=lambda: delay_one_minute(window))
    delay_button.pack(pady=5)

    window.mainloop()


print("程式已啟動")
print("原始提醒時間 =", reminder_time)

while True:
    now = datetime.now()

    # 換天重置
    if now.date() != today_date:
        today_date = now.date()
        delayed_time = None
        reminder_finished_today = False
        original_reminder_shown_today = False
        print("已換天，狀態重置")

    # 每5秒印一次現在狀態
    print(
        "現在時間 =",
        now.strftime("%H:%M:%S"),
        "| reminder_time =",
        reminder_time,
        "| delayed_time =",
        delayed_time.strftime("%H:%M:%S") if delayed_time else None,
        "| finished =",
        reminder_finished_today,
        "| shown_today =",
        original_reminder_shown_today
    )

    # 如果今天已完成，就不再提醒
    if reminder_finished_today:
        time.sleep(5)
        continue

    current_time = now.strftime("%H:%M")

    # 優先判斷延後提醒
    if delayed_time is not None:
        if now >= delayed_time:
            print(">>> 延後時間到了，準備提醒")
            delayed_time = None
            show_reminder()

    # 再判斷原本提醒
    elif not original_reminder_shown_today and current_time == reminder_time:
        print(">>> 原始提醒時間到了，準備提醒")
        original_reminder_shown_today = True
        show_reminder()

    time.sleep(5)