from playwright.sync_api import sync_playwright

import requests

import aria2p

aria2 = aria2p.API(
    aria2p.Client(
        host="http://localhost",
        port=16800,
        secret="191564",
    )
)

with sync_playwright() as p:
    b = p.chromium.launch(headless=False)
    page = b.new_page()
    page.goto('https://www.zxx.edu.cn/elecEdu')

    grade_list = [page.locator(
        '//*[@id="root"]/div/div/div[2]/div[2]/div[2]/div[1]/ul/li[5]')]
    for grade in grade_list[-1:]:
        grade.click()
        subject_list = page.query_selector_all(
            '//*[@id="root"]/div/div/div[2]/div[2]/div[2]/div[2]/div[1]/div[1]/div[2]/label')
        for i in range(len(subject_list)):
            subject_list[i].click()
            subject_list = page.query_selector_all(
                '//*[@id="root"]/div/div/div[2]/div[2]/div[2]/div[2]/div[1]/div[1]/div[2]/label')
            version_list = page.query_selector_all(
                '//*[@id="root"]/div/div/div[2]/div[2]/div[2]/div[2]/div[1]/div[2]/div[2]/label')
            for iv in range(len(version_list)):
                version_list[iv].click()
                version_list = page.query_selector_all(
                    '//*[@id="root"]/div/div/div[2]/div[2]/div[2]/div[2]/div[1]/div[2]/div[2]/label')
                level_list = page.query_selector_all(
                    '//*[@id="root"]/div/div/div[2]/div[2]/div[2]/div[2]/div[1]/div[3]/div[2]/label/span[2]')
                for il in range(len(level_list)):
                    level_list[il].click()
                    level_list = page.query_selector_all(
                        '//*[@id="root"]/div/div/div[2]/div[2]/div[2]/div[2]/div[1]/div[3]/div[2]/label/span[2]')
                    book_list = page.query_selector_all(
                        '//*[@id="root"]/div/div/div[2]/div[2]/div[2]/div[2]/div[2]/ul/li')
                    for book in book_list:
                        book.click()
                        with b.contexts[0].expect_page() as page_info:
                            url = [page_info.value.url]
                            page_info.value.close()
                            aria2.add_uris(url)
                        page.bring_to_front()
                        subject_list = page.query_selector_all(
                            '//*[@id="root"]/div/div/div[2]/div[2]/div[2]/div[2]/div[1]/div[1]/div[2]/label')
                        version_list = page.query_selector_all(
                            '//*[@id="root"]/div/div/div[2]/div[2]/div[2]/div[2]/div[1]/div[2]/div[2]/label')
                        
    page.close()
    b.close()
