# --*-- conding:utf-8 --*--
import asyncio
from playwright.async_api import async_playwright
import pandas as pd
import requests

# Step 1: 使用Playwright抓取中国招标网数据
async def fetch_tender_data(keyword):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()

        # 访问中国招标网并搜索关键词
        await page.goto('https://www.chinabidding.cn/')  # 替换为具体的招标信息页面URL
        await page.fill('input[name="search"]', keyword)
        await page.click('button[type="submit"]')
        await page.wait_for_timeout(3000)  # 等待页面加载

        # 抓取数据
        tenders = await page.query_selector_all('.tender-item')  # 修改为正确的选择器
        data_list = []
        for tender in tenders:
            title = await tender.query_selector_eval('.title', 'el => el.textContent')
            date = await tender.query_selector_eval('.date', 'el => el.textContent')
            link = await tender.query_selector_eval('a', 'el => el.href')
            data_list.append({'title': title.strip(), 'date': date.strip(), 'link': link.strip()})

        await browser.close()
        return pd.DataFrame(data_list)

# Step 2: 数据清洗
def clean_data(df):
    df.drop_duplicates(subset='title', inplace=True)
    df = df[df['title'].str.contains('半导体研磨设备', case=False)]
    return df

# Step 3: 推送至钉钉
def push_to_dingtalk(df, webhook_url):
    for _, row in df.iterrows():
        message = f"**招标信息**\n标题: {row['title']}\n日期: {row['date']}\n链接: {row['link']}"
        payload = {"msgtype": "markdown", "markdown": {"title": "招标信息更新", "text": message}}
        response = requests.post(webhook_url, json=payload)
        if response.status_code == 200:
            print(f"成功推送: {row['title']}")
        else:
            print(f"推送失败: {row['title']}")

# 主程序入口
if __name__ == "__main__":
    keyword = "半导体研磨设备"
    webhook_url = "your_dingtalk_webhook_url"  # 替换为你的钉钉Webhook链接

    tender_data = asyncio.run(fetch_tender_data(keyword))
    if not tender_data.empty:
        cleaned_data = clean_data(tender_data)
        push_to_dingtalk(cleaned_data, webhook_url)
    else:
        print("未找到相关招标信息。")
