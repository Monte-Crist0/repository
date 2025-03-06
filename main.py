import random
import threading
import datetime
from time import sleep

from selenium import webdriver
import logging
from logging import *

from selenium.webdriver import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time

from selenium.webdriver.support.wait import WebDriverWait

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler('logs.log', mode='a', encoding='utf-8'),  # Scrie logurile în fișier
        logging.StreamHandler()  # Continuă să afișeze logurile și în terminal
    ]
)

logger = logging.getLogger(__name__)

def main(driver: webdriver.Firefox, url: str):

    # options.set_preference("dom.webdriver.enabled", False)
    # options.set_preference("useAutomationExtension", False)

    # Раскомментируйте следующие строки, если используете сервер без GUI и получаете ошибку “session not created: probably user data directory is already in use, please specify a unique value for --user-data-dir argument, or don't use --user-data-dir”
    # options.add_argument("--headless")
    # options.add_argument("--no-sandbox")
    # options.add_argument("--disable-dev-shm-usage")


    #driver.set_window_size(600, 600)
    # Открываем страницу
    wait = WebDriverWait(driver, 10)
    driver.execute_script(f"window.open('{url}')")

    title = driver.title
    logger.log(INFO, 'Video opened')

    driver.refresh()
    # cookieList = cookies.cook
    # for cookie in cookieList:
    #     driver.add_cookie({k: cookie[k] for k in {'name', 'value'}})
    #
    # logger.log(INFO, 'Cookies: True')
    # sleep(10)
    # logger.log(INFO, '1 refresh')
    # driver.refresh()

    # element_dot = wait.until(EC.element_to_be_clickable((By.XPATH, '/html/body/ytd-app/div[1]/ytd-page-manager/ytd-watch-flexy/div[5]/div[1]/div/div[2]/ytd-watch-metadata/div/div[2]/div[2]/div/div/ytd-menu-renderer/yt-button-shape/button/yt-touch-feedback-shape/div/div[2]')))
    logger.log(INFO, 'Go to click 3 dots')
    sleep(3)
    element_dot = driver.find_element(by=By.XPATH, value='/html/body/ytd-app/div[1]/ytd-page-manager/ytd-watch-flexy/div[5]/div[1]/div/div[2]/ytd-watch-metadata/div/div[2]/div[2]/div/div/ytd-menu-renderer/yt-button-shape/button/yt-touch-feedback-shape/div/div[2]')
    # element_dot.click()
    driver.execute_script("arguments[0].click();", element_dot)
    try:
        logger.log(INFO, 'Create Clip')
        element_clip = driver.find_element(By.XPATH, value='//*[@id="items"]/ytd-menu-service-item-renderer[1]/tp-yt-paper-item')
        text_clip = driver.find_element(By.XPATH, value='//*[@id="items"]/ytd-menu-service-item-renderer[1]/tp-yt-paper-item/yt-formatted-string')
        if text_clip.text == 'Создать клип':
            driver.execute_script("arguments[0].click();", element_clip)
        else:
            print(text_clip.text)
            sleep(30)
            driver.stop_client()
            driver.quit()
            logger.log(level=logging.ERROR, msg=f'Error: Cant Create Clip')
            return -1
    except Exception as e:
        driver.quit()
        logger.log(level=logging.ERROR, msg=f'Error: {e}')
        return -1

    current_timestamp = datetime.datetime.now().timestamp()
    try:
        clip_title = driver.find_element(by=By.XPATH, value='//*[@id="textarea"]')
        clip_title.send_keys(f'Clip{current_timestamp}')
        logger.log(INFO, 'set title for clip')
    except Exception as e:
        logger.log(ERROR, 'Error set title for clip.... retry.')
        driver.save_screenshot(f'screen{random.randint(0, 10000)}.png')
        sleep(5)
        clip_title = driver.find_element(by=By.XPATH, value='//*[@id="textarea"]')
        clip_title.send_keys(f'Clip{current_timestamp}')
        logger.log(INFO, 'set title for clip')

    script = """

const elements = document.querySelectorAll('#end');
if (elements.length > 0) {
    const endElement = elements[elements.length - 1];
    endElement.focus();
    const event = new Event('input', {
        bubbles: true
    });
    endElement.value = " "
    endElement.dispatchEvent(event);
    endElement.dispatchEvent(new Event('change'));
}
"""

    driver.execute_script(script)

    elements = driver.find_elements(By.ID, 'end')
    if elements:
        # Взятие последнего элемента
        last_element = elements[-1]
        last_element.send_keys('1:00.0')
        clip_title = driver.find_element(by=By.XPATH, value='//*[@id="textarea"]')
        clip_title.click()
    else:
        logger.log(ERROR, 'cant find end element to send keys')

    # is_acted = False
    # x_offset = 100
    #
    # while not is_acted:
    #     logger.log(INFO, f'starting clipping, video: {title}')
    #     end_time = driver.find_element(By.ID, "duration")
    #     if int(str(end_time.text.split(' ')[0].split('.')[0])) < 50:
    #         clip_holder_r = driver.find_element(by=By.ID, value='handle-right')
    #         actions = ActionChains(driver)
    #         # Перенос элемента вправо на 150 пикселей
    #         actions.click_and_hold(clip_holder_r).move_by_offset(x_offset, 0).release().perform()
    #         x_offset+=50
    #         sleep(3)
    #     else:
    #         break

    click_send = driver.find_element(by=By.XPATH, value='//*[@id="share"]/yt-button-renderer/yt-button-shape/button')
    driver.execute_script("arguments[0].click();", click_send)

    wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="share-url"]')))
    link_dv = driver.find_element(by=By.XPATH, value='//*[@id="share-url"]')
    lnk = link_dv.get_attribute('value')

    # Завершаем работу
    driver.close()
    return lnk

def thread_function(args, result_container, index):
    profile = webdriver.FirefoxProfile('./profile')
    options = webdriver.FirefoxOptions()
    options.profile = profile
    driver = webdriver.Firefox(options=options)
    driver.implicitly_wait(20)
    driver.get('https://google.com')

    links = ['https://www.youtube.com/watch?v=PF3wSHZ6wpw']

    for lnk in links:
        ss = main(driver=driver, url=lnk)
        print(ss)

# def main_thread_starter():
#     # Аргументы, с которыми мы будем вызывать функцию
#     args = ['https://www.youtube.com/watch?v=PF3wSHZ6wpw']
#
#     # Контейнер для результатов
#     results = [None] * len(args)
#
#     # Список потоков
#     threads = []
#
#     for i, arg in enumerate(args):
#         thread = threading.Thread(target=thread_function, args=(arg, results, i))
#         threads.append(thread)
#         thread.start()
#
#     for thread in threads:
#         thread.join()
#
#     for i, result in enumerate(results):
#         print(f'Result for argument {args[i]}: {result}')

if __name__ == '__main__':
    thread_function(0,0,0)