import asyncio
from pyppeteer import launch
from twocaptcha import TwoCaptcha
from proxy import proxy
import random
import json

import sys

token = sys.argv[1]
cpf = sys.argv[2]
data_nascimento = sys.argv[3]
file_path = f"data/{token}.json"


async def save_text_as_txt(content):
    # os.makedirs(os.path.dirname("save_datas"), exist_ok=True)
    try:
        with open(file_path, "w") as f:
            json.dump(content, f)
        # with open(file_path, "w", encoding="utf-8") as file:
        #     file.write(content)
    except:
        pass


async def main():
    limit_count = 5
    count = 0
    browser = None
    while True:
        try:
            proxy_chosen = proxy[random.randint(0, len(proxy))]
            url = "https://servicos.receita.fazenda.gov.br/Servicos/CPF/ConsultaSituacao/ConsultaPublica.asp"
            browser = await launch(
                options={
                    "args": [
                        "--no-sandbox",
                        "--disable-setuid-sandbox",
                        f"--proxy-server=http://{proxy_chosen}",
                    ]
                }
            )
            page = await browser.newPage()
            await page.goto(url)
            element = await page.querySelector("#hcaptcha")
            website_key = await page.evaluate(
                '(element) => element.getAttribute("data-sitekey")', element
            )
            solver = TwoCaptcha("239ee10e602e2c0051cd467d094202f0")
            # config = {
            #     'server':           '2captcha.com',
            #     'apiKey':           'YOUR_API_KEY',
            #     'softId':            123,
            #     'callback':         'https://your.site/result-receiver',
            #     'defaultTimeout':    120,
            #     'recaptchaTimeout':  600,
            #     'pollingInterval':   10,
            # }
            # solver = TwoCaptcha(**config)
            solution = solver.hcaptcha(sitekey=website_key, url=url)
            
            if solution:
                captcha_key = solution["code"]

            txt_cpf_element = await page.querySelector('input[name="txtCPF"]')
            if txt_cpf_element:
                await txt_cpf_element.type(cpf)
            else:
                print("txtCPF element not found!")
            txt_data_nascimento_element = await page.querySelector(
                'input[name="txtDataNascimento"]'
            )
            if txt_data_nascimento_element:
                await txt_data_nascimento_element.type(data_nascimento)
            else:
                print("txtDataNascimento element not found!")
            await page.waitForSelector("iframe")
            await page.evaluate(
                "(element, captchaKey) => element.value = captchaKey",
                await page.querySelector('textarea[name="h-captcha-response"]'),
                captcha_key,
            )
            await page.waitFor(2000)
            btn = await page.querySelector('input[name="Enviar"]')
            await btn.click()
            await page.waitFor(5000)
            # titleSelector = "h1[class='documentFirstHeading']"
            # titleSelector = "h1"
            # title = await page.evaluate(
            #     "(selector) => document.querySelector(selector).textContent", titleSelector
            # )
            # # print(await page.evaluate('(btn) => btn.getAttribute("class")', await page.querySelector('h1')))
            # print(title)
            selector = "body"  # div[id='main']
            text = await page.evaluate(
                "(selector) => document.querySelector(selector).innerHTML", selector
            )
            savedTxt = text
            await save_text_as_txt({"type": "content", "data": savedTxt})
            print(text)
            return
        except Exception as e:
            count = count + 1
            if count < limit_count:
                await save_text_as_txt(
                    {"type": "error", "data": f"{str(e)} Try again {count} time(s)."}
                )
            else:
                await save_text_as_txt({"type": "error", "data": f"{str(e)}, Failed!"})
                return
        finally:
            await browser.close()


if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(main())
    # asyncio.get_event_loop().run_until_complete(save_text_as_txt(f'{token}.json',"HERE"))
