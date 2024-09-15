# coding: utf_8

# Usage
# [python rekoru_add.py 引数1 引数2 引数3 引数4 引数5 引数6 引数7("memo")] Enter

# 引数1:
# 休憩開始
# 12:00

# 引数2:
# 休憩終了
# 13:00

# 引数3:
# 勤務開始 starting
# 09:00

# 引数4:
# 勤務終了 ending
# 18:00

# 引数5:
# workingForm
# [01]:顧客業務(オンサイト)
# [34]:顧客業務(オフサイト)
# [35]:社内業務(オンサイト)
# [36]:社内業務(オフサイト)

# 以下の勤務区分は未実装
# [02]:欠勤
# [03]:有給休暇（全休）
# [04]:有給休暇（半休）
# [08]:代休
# [27]:夏季休暇
# [21]:慶弔休暇

# 引数6:
# [追加する日付]
# 2022/08/01

# 引数7:
# メモ
# [オフィス名]
# ※無記述の場合 → ””

# 要 初期設定
url = "https://app.recoru.in/ap/"
url_list = "https://app.recoru.in/ap/menuAttendance/?ui=1860&pp=0"  # 「勤務表の編集」ボタン押下後の遷移URL
contractID = "170096"
# authID = "20230915" 自動ログインのため現在不要
# loginPW = "hogehoge"　自動ログインのため現在不要

from cgi import print_arguments
from lib2to3.pgen2.driver import Driver
from select import select
from selenium import webdriver
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.by import By
from time import sleep
from webdriver_manager.chrome import ChromeDriverManager
import sys
import re
import codecs

# 標準入力-マイパターン確認 + myPattern1 + ', 2:' + myPattern2 + ', 3:' + myPattern3
val = input('[Attention]Recoru [01]:顧客業務(オンサイト)[34]:顧客業務(オフサイト)[35]:社内業務(オンサイト)[36]:社内業務(オフサイト)' + ', y or n ?')
if val == 'y':

    driver = webdriver.Chrome(ChromeDriverManager().install())
    driver.get('https://google.com')

    rest_starting = sys.argv[1]
    rest_ending = sys.argv[2]
    work_starting = sys.argv[3]
    work_ending = sys.argv[4]
    work_form = int(sys.argv[5])
    work_date = sys.argv[6]
    work_memo = sys.argv[7]

    day = str(int(work_date[8:]) -1)
    day_int = re.sub(r"\D", "", work_date)
    addDate = 'tr-'+ day_int + '-1'
    print(day_int)

    # Recoru
    driver.get(url)

    # 契約ID
    driver.find_element_by_name("contractId").send_keys(contractID)

    # ログインID
    # driver.find_element_by_name("authId").send_keys(authID)

    # パスワード
    # driver.find_element_by_name("password").send_keys(loginPW)

    # 「ログイン」押下
    driver.find_element_by_class_name("common-btn.submit").click()

    sleep(1)

    # 「勤務表の編集」押下
    driver.get(url_list)

    sleep(1)

    # 勤務区分
    if work_form == 1:
        print("[選択]顧客業務 オンサイト")
        Select(driver.find_element_by_class_name('ID-attendKbn-' + day_int +'-1')).select_by_visible_text("顧客業務(オンサイト)")

    elif work_form == 34:
        print("[選択]顧客業務 オフサイト")
        Select(driver.find_element_by_class_name('ID-attendKbn-' + day_int +'-1')).select_by_visible_text("顧客業務(オフサイト)")

    elif work_form == 35:
        print("[選択]社内業務 オンサイト")
        Select(driver.find_element_by_class_name('ID-attendKbn-' + day_int +'-1')).select_by_visible_text("社内業務(オンサイト)")

    elif work_form == 36:
        print("[選択]社内業務 オフサイト")
        Select(driver.find_element_by_class_name('ID-attendKbn-' + day_int +'-1')).select_by_visible_text("社内業務(オフサイト)")

    print("[選択完了]勤務区分")

    sleep(1)

    # 開始
    driver.find_element_by_class_name('ID-worktimeStart-'+ day_int +'-1').send_keys(work_starting)

    # 終了
    driver.find_element_by_class_name('ID-worktimeEnd-'+ day_int +'-1').send_keys(work_ending)
    print("[完了]勤務時間")

    # メモ
    print("[完了]メモ")

    sleep(3)

    # 休憩時間編集ボタン
    driver.find_element(By.XPATH, '//*[@id="' + addDate + '"]/td[5]/a/img').click()

    sleep(2)

    # ウィンドウハンドルを切替
    driver.switch_to.window(driver.window_handles[-1])

    sleep(1)

    # 休憩開始時間
    driver.find_element(By.XPATH, '//*[@id="breaktimeDtos[0].breaktimeStart"]').send_keys(rest_starting)

    # 休憩終了時間
    driver.find_element(By.XPATH, '//*[@id="breaktimeDtos[0].breaktimeEnd"]').send_keys(rest_ending)

    # 更新ボタン
    driver.find_element(By.XPATH, '/html/body/div[9]/div[2]/form/div/div[6]/a[1]/input').click()

    sleep(3)

    # ウィンドウハンドルを切替
    alert_window = driver.switch_to_alert()

    # アラートウィンドウ OK
    alert_window.accept()

    print("[完了]休憩時間更新")

    sleep(3)

    # ウィンドウハンドルを切替
    driver.switch_to.window(driver.window_handles[0])

    # 更新
    driver.find_element_by_id("UPDATE-BTN").click()

    sleep(3)

    # 更新OK

    alert = driver.switch_to_alert()
    alert.accept()
    print("[完了]更新処理")

    sleep(3)

    # ブラウザを閉じる
    driver.quit()

    print('[finished]')

if val == 'n':
    print('[cancel]')
