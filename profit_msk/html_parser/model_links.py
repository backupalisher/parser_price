class ModelLinks(object):
    def __init__(self, driver, urls):
        self.driver = driver
        self.urls = urls

    def get_links_model(self):
        devices_list = []
        for url in self.urls:
            print(url[0])
            self.driver.get(url[1])
            td = self.driver.find_elements_by_xpath('//*[@id="zzzzzzzzzz"]/table/tbody/tr/td/div/div/a')
            for tableData in td:
                devices_list.append([url[0], tableData.get_attribute('href')])
        return devices_list
