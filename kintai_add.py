# coding: utf_8

# Usage
# [python ファイル名.py 引数1 引数2 引数3 引数4] Enter
# [python ファイル名.py 引数1] Enter # 勤務開始時間と休憩時間の変動がないため勤務終了時間のみ引数とする　2024/09/15

# 引数1:
# 休憩開始
# 12:00

# 引数2:
# 休憩終了
# 13:00

# 引数3:
# 勤務開始 starting
# 09:00

# 引数4: # 引数1とする 2024/09/15
# 勤務終了 ending
# 18:00

# 要 初期設定
url = "https://xxx"  # ログインのURL
url_list = "https://xxx//社員番号"  # 「勤務表の編集」ボタン押下後の遷移URL
contractID = "契約ID"
authID = "ログインID"
loginPW = "パスワード"

from cgi import print_arguments
from lib2to3.pgen2.driver import Driver
from select import select
from selenium import webdriver
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.by import By
from time import sleep
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from datetime import datetime
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import sys
import re
import codecs

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
driver.get('https://google.com')

# 休憩時間や勤務開始時間が変動する場合は引数を利用できるようにここを修正
# work_start = sys.argv[1] # 勤務開始時間
work_ending = sys.argv[1] # 勤務終了時間
work_date = datetime.now().strftime("%Y%m%d")

# 日付の「日」の部分を取得して、1日減算
day = str(int(work_date[6:8]) - 1)

day_int = re.sub(r"\D", "", work_date)
addDate = 'tr-'+ day_int + '-1'
print(day_int)

wait = WebDriverWait(driver, 10)
submit_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".common-btn.submit")))

driver.get(url)

# 契約ID
driver.find_element(By.NAME, "contractId").send_keys(contractID)

# ログインID
driver.find_element(By.NAME, "authId").send_keys(authID)

# パスワード
driver.find_element(By.NAME, "password").send_keys(loginPW)

# 「ログイン」押下
submit_button.click()

# 「勤務表の編集」押下
driver.get(url_list)

sleep(1)

# 勤務区分
# if work_form == 1:
# print("[選択]顧客業務 オンサイト")
wait = WebDriverWait(driver, 10)
select_element = wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'ID-attendKbn-' + day_int + '-1')))
Select(select_element).select_by_visible_text("顧客業務(オンサイト)")

# elif work_form == 34:
#     print("[選択]顧客業務 オフサイト")
#     Select(driver.find_element_by_class_name('ID-attendKbn-' + day_int +'-1')).select_by_visible_text("顧客業務(オフサイト)")

# elif work_form == 35:
#     print("[選択]社内業務 オンサイト")
#     Select(driver.find_element_by_class_name('ID-attendKbn-' + day_int +'-1')).select_by_visible_text("社内業務(オンサイト)")

# elif work_form == 36:
#     print("[選択]社内業務 オフサイト")
#     Select(driver.find_element_by_class_name('ID-attendKbn-' + day_int +'-1')).select_by_visible_text("社内業務(オフサイト)")

# print("[選択完了]勤務区分")

sleep(1)

# 開始
driver.find_element(By.CLASS_NAME, 'ID-worktimeStart-' + day_int + '-1').send_keys("09:00")

# 終了
driver.find_element(By.CLASS_NAME, 'ID-worktimeEnd-' + day_int + '-1').send_keys(work_ending)
print("[完了]勤務時間")

sleep(3)

# 休憩時間編集ボタン
driver.find_element(By.XPATH, '//*[@id="' + addDate + '"]/td[5]/a/img').click()

sleep(2)

# ウィンドウハンドルを切り替え
driver.switch_to.window(driver.window_handles[-1])

sleep(1)

# 休憩開始時間
driver.find_element(By.XPATH, '//*[@id="breaktimeDtos[0].breaktimeStart"]').send_keys("12:00")

# 休憩終了時間（定時とそれ以外で休憩時間を分岐）
if work_ending == "1730":
    driver.find_element(By.XPATH, '//*[@id="breaktimeDtos[0].breaktimeEnd"]').send_keys("12:45")
    
else :
    driver.find_element(By.XPATH, '//*[@id="breaktimeDtos[0].breaktimeEnd"]').send_keys("13:00")

# 更新ボタン
driver.find_element(By.XPATH, '/html/body/div[9]/div[2]/form/div/div[6]/a[1]/input').click()

sleep(3)

# アラートのウィンドウハンドルを切り替え
alert_window = driver.switch_to.alert

# アラートウィンドウ OK
alert_window.accept()

print("[完了]休憩時間更新")

sleep(3)

# 元のウィンドウに戻る
driver.switch_to.window(driver.window_handles[0])

# 更新ボタンのクリック
driver.find_element(By.ID, "UPDATE-BTN").click()

sleep(3)

# 更新OK
alert = driver.switch_to.alert

# アラートを受け入れる
alert.accept()
print("[完了]更新処理")

sleep(3)

# ブラウザを閉じる
driver.quit()

print('[finished]')