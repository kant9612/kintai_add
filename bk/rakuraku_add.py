# coding: utf_8

# Usage
# [python rakuraku_add.py 引数1 引数2 引数3] Enter

# 引数1:[追加する日付]　2022/08/01
# 引数2:[1]新規追加(月初)、[2]更新(一時保存有)
# 引数3:[1]マイパターン1、[2]:マイパターン2、[3]:マイパターン3

# 要 初期設定
url = "https://rsclef.rakurakuseisan.jp/CSR9KsE9qUa/"
url_list = "https://rsclef.rakurakuseisan.jp/CSR9KsE9qUa/sapKotsuhiKensaku/initializeView" #交通費精算_一覧
loginID = "20220801"
loginPW = "password"
reason = "通勤費(通常勤務地)"
myPattern1 = "在宅チャージ"
myPattern2 = "通勤ルート1"
myPattern3 = "通勤ルート2"
# DeveloperToolを用いて,楽楽精算上のマイパターンの[Xpath]を確認, 要修正箇所有

from selenium import webdriver
from selenium.webdriver.support.select import Select
from time import sleep
from webdriver_manager.chrome import ChromeDriverManager
import sys
import codecs

# 標準入力-マイパターン確認
val = input('[Attention]"マイパターン" 1:'+ myPattern1 + ', 2:' + myPattern2 + ', 3:' + myPattern3 + ', y or n ?')
if val == 'y':

    driver = webdriver.Chrome(ChromeDriverManager().install())
    driver.get('https://google.com')

    addDate = sys.argv[1]

    # 楽楽精算
    driver.get(url)

    # ログインID
    driver.find_element_by_name("loginId").send_keys(loginID)

    # パスワード
    driver.find_element_by_name("password").send_keys(loginPW)

    # 「ログイン」押下
    driver.find_element_by_class_name("common-btn.large.black").click()

    sleep(1)

    if sys.argv[2] == '1':

        # 入力画面に移動
        driver.get(url)

        sleep(1)

        # 「マイパターン」押下
        driver.find_element_by_xpath("//*[@id=\"denpyoFixedArea\"]/div[1]/div/button[4]").click()

        sleep(1)

        # ウィンドウ切り替え
        driver.switch_to.window(driver.window_handles[1])

        # マイパターンを選択
        driver.find_element_by_xpath("//*[@id=\"kakutei_0_3432\"]").click()   # DeveloperToolを用いてマイパターンのXpathを要確認

        # 次へ
        driver.find_element_by_xpath("//*[@id=\"d_footer\"]/div[1]/button").click()

        sleep(1)

        # 日付
        driver.find_element_by_xpath("//*[@id=\"meisai0\"]/tr[1]/td[2]/table/tbody/tr/td[1]/div/div/input[1]").send_keys(addDate)

        # 申請理由
        #Select(driver.find_element_by_xpath("//*[@id=\"meisai0\"]/tr[2]/td/table/tbody/tr/td[2]/div/div/select")).select_by_value(reason)

        # 「明細追加」押下
        driver.find_element_by_xpath("//*[@id=\"d_denpyo\"]/form/div/div[5]/div/button[3]").click()

        sleep(1)

        # 「一時保存」押下
        driver.find_element_by_xpath("//*[@id=\"d_denpyo\"]/form/div/div[5]/div/button[3]").click()



    elif sys.argv[2] == '2':

        # 交通費精算_一覧に移動
        driver.get(url_list)

        sleep(1)

        # 「一時保存」タブを選択
        driver.find_element_by_xpath("//*[@id=\"informationTab\"]/ul/li[2]/a").click()

        sleep(1)

        # 一時保存されている申請を選択
        links = driver.find_element_by_xpath("//*[@id=\"listTable\"]/tbody/tr[2]/td[2]/a")

        driver.get(links.get_attribute("href"))

        sleep(3)

        # 「マイパターン」押下
        driver.find_element_by_xpath("//*[@id=\"denpyoFixedArea\"]/div[1]/div/button[4]").click()

        sleep(1)

        # ウィンドウ切り替え
        driver.switch_to.window(driver.window_handles[1])

        # マイパターンを選択
        # DeveloperToolを用いてマイパターンの[Xpath]を確認後、要修正
        if sys.argv[3] == '1':
            driver.find_element_by_xpath("//*[@id=\"kakutei_0_3432\"]").click()  #在宅チャージ

        elif sys.argv[3] == '2':
            driver.find_element_by_xpath("//*[@id=\"kakutei_0_3674\"]").click()  #通勤路1

        elif sys.argv[3] == '3':
            driver.find_element_by_xpath("//*[@id=\"kakutei_0_3XXX\"]").click()  #通勤路2

        #else sys.argv[3] == '4':
            # other

        sleep(1)

        # 次へ
        driver.find_element_by_xpath("//*[@id=\"d_footer\"]/div[1]/button").click()

        sleep(1)

        # 日付
        driver.find_elements_by_name("meisaiDate")[1].send_keys(addDate)

        # 「明細追加」押下
        driver.find_element_by_xpath("//*[@id=\"d_denpyo\"]/form/div/div[5]/div/button[3]").click()

        sleep(1)

        # 「一時保存」押下
        driver.find_element_by_xpath("//*[@id=\"d_denpyo\"]/form/div/div[5]/div/button[3]").click()

    sleep(1)

    # ブラウザを閉じる
    driver.quit()

    # 最終確認
    if sys.argv[3] == '1':
        print('[Remind]”マイパターン” → ' + myPattern1)

    elif sys.argv[3] == '2':
        print('[Remind]”マイパターン” → ' + myPattern2)

    elif sys.argv[3] == '3':
        print('[Remind]”マイパターン” → ' + myPattern3)
    print('[finished]')

if val == 'n':
    print('[cancel]')
