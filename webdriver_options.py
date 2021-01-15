from selenium.webdriver.chrome.options import Options


def set_options():
    options = Options()
    options.add_argument("start-maximized")
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-gpu")
    options.add_argument("--disable-extensions")
    options.add_argument("--dns-prefetch-disable")
    # options.add_argument("--window-size=1366,768")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    return options
