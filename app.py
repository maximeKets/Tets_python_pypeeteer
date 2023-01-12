import asyncio
import pytest
from pyppeteer import launch


async def main():
    page, browser = await connect()
    await page.goto('https://polr.stationmyr.net/')
    await fill_imput(page, 'http://www.tit.com', 'link-url')
    await push_input(page, 'shorten')
    shorted = await get_input_value(page)
    await go_url(page, shorted)
    await browser.close()


@pytest.mark.asyncio
async def test_title():
    page, browser = await connect()
    assert await page.title() == 'Shorturl'


@pytest.mark.asyncio
async def test_shorted():
    page, browser = await connect()
    await fill_imput(page, 'http://www.tit.com', 'link-url')
    await push_input(page, 'shorten')
    shorted = await get_input_value(page, 'link-url')
    await go_url(page, shorted)
    newurl = page.url
    await browser.close()
    assert newurl == 'http://www.tit.com/'


async def get_title(page):
    title = await page.title()
    return title


async def connect():
    browser = await launch()
    page = await browser.newPage()
    await page.goto('https://polr.stationmyr.net/')
    return page, browser


async def fill_imput(page, text, input_name):
    url_input = await page.xpath('//input[@name="' + input_name + '"]')
    await url_input[0].type(text)
    await page.screenshot({'path': input_name + '.png'})


async def push_input(page, submit_name):
    shorten_button = await page.xpath('//input[@id="' + submit_name + '"]')
    await shorten_button[0].click()
    await page.screenshot({'path': 'submit_' + submit_name +'".png'})


async def get_input_value(page, input_name ):
    short_url = await page.xpath('//input[@id="' + input_name + '"]')
    result_url = await short_url[0].getProperty('value')
    await page.screenshot({'path': input_name + '.png'})
    result_url_string = await result_url.jsonValue()
    return result_url_string


async def go_url(page, url):
    await page.goto(url)
    await page.screenshot({'path': url + '.png'})


asyncio.get_event_loop().run_until_complete(main())
