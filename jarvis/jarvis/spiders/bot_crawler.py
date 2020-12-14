import scrapy
import json
import os
import errno

#crawled
# class ChototSpiders(scrapy.Spider):
#     name = "chotot"

#     file = open('/home/tien/projects/projectsyear4/datascience/jarvis/jarvis/chotot_crawl/data.txt',mode='a',encoding='utf-8')
#     urls = []
#     def start_requests(self):
#         for i in range(11001,11010):
#             api = 'https://gateway.chotot.com/v1/public/ad-listing?cg=1020&limit=20&o='+ str(i*20) +'&st=s,k&page=' + str(i+1)
#             self.urls.append(api)

#         for url in self.urls:
#             yield scrapy.Request(url=url, callback=self.parse)

#     def parse(self, response):

#         data = response.body.decode('utf-8')

#         data = json.loads(data)
#         for item in data['ads']:
#         #   self.file.write(str(item)+'\n')
#             print(str(item))



# class MuaBanNhaDatSpider(scrapy.Spider):
#     name = "muabannhadat"

#     file = open('/home/tien/projects/projectsyear4/datascience/jarvis/jarvis/muabannhadat_crawl/data_muabannhadat.txt',mode='a',encoding='utf-8')
#     list_keys = ['id','title','heading','price','currency_iso','data_properties','description','location']
#     urls = []
#     def start_requests(self):
#         for i in range(0,10877):
#             api = 'https://api.muabannhadat.vn/v1/listings?page='+str(i+1)+'&offer_type=sell&category_id=3&category_title=Nh%C3%A0'
#             self.urls.append(api)

#         for url in self.urls:
#             yield scrapy.Request(url=url, callback=self.parse)

#     def parse(self, response):

#         data = response.body.decode('utf-8')
#         data = json.loads(data)
        
#         for item in data['data']:
#             new_item = {key:val for key,val in item.items() if key in self.list_keys}
#             self.file.write(str(str(new_item)+'\n'))

class DistributePeople(scrapy.Spider):
    name = "distributepeople"
    filename = '/home/tien/projects/projectsyear4/datascience/spider/jarvis/jarvis/distribute_people/data_people2.json'
    if not os.path.exists(os.path.dirname(filename)):
        try:
            os.makedirs(os.path.dirname(filename))
        except OSError as exc: # Guard against race condition
            if exc.errno != errno.EEXIST:
                raise
    list_keys = ['id','title','heading','price','currency_iso','data_properties','description','location']
    urls = ['https://vi.wikipedia.org/wiki/Danh_s%C3%A1ch_%C4%91%C6%A1n_v%E1%BB%8B_h%C3%A0nh_ch%C3%ADnh_c%E1%BA%A5p_huy%E1%BB%87n_c%E1%BB%A7a_Vi%E1%BB%87t_Nam']
    
    unicode_list = {
        'a' : 'á à ả ã ạ ă ắ ẳ ẵ ặ ằ ấ ầ ẫ ậ ẩ â', 
        'e' : 'é è ẻ ẽ ẹ ế ề ể ễ ệ ê', 
        'i' : 'í ì ỉ ĩ ị', 
        'o' : 'ô ố ồ ổ ỗ ộ ơ ớ ờ ở ỡ ợ ó ò õ ỏ ọ',
        'u' : 'ú ù ủ ũ ụ ư ứ ừ ử ữ ự',
        'y' : 'ý ỳ ỷ ỹ ỵ',
        'd' : 'đ'
    }

    res = {}
    
    def start_requests(self):
        for url in self.urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):

        data = response.body.decode('utf-8')
        table = response.css('table.sortable')
        # print(len(tbody)
        list_tr = table.css('tr')
        #list_tr[0] == header
        list_tr = list_tr[1:]
        for tr in list_tr:
            list_td = tr.css('td')
            district = list_td[1].css('a::text').get()
            province = list_td[2].css('a::text').get()
            number_people = list_td[4].css('::text').get()
            area = list_td[5].css('::text').get()
            distribute = list_td[6].css('::text').get()
            distribute = distribute.replace("\n","")
            new_province = []
            for _char in province.lower():
                flag = False
                for _key in self.unicode_list.keys():
                    if _char in self.unicode_list[_key] and _char != ' ':
                        # print('uni', _char)
                        new_province.append(_key)
                        flag = True
                        break
                if not flag:
                    new_province.append(_char)                    
            new_province = ''.join(new_province)


            new_district = []
            for _char in district.lower():
                flag = False
                for _key in self.unicode_list.keys():
                    if _char in self.unicode_list[_key] and _char != ' ':
                        # print('uni', _char)
                        new_district.append(_key)
                        flag = True
                        break
                if not flag:
                    new_district.append(_char)                    
            district = ''.join(new_district)
            if new_province not in self.res:

                self.res[new_province] = {
                    district : {
                        'number_people':number_people.split(' ')[0],
                        'area': area.split('*')[0].strip(),
                        'distribute': distribute
                    }
                }
            else:
                self.res[new_province][district] = {
                    'number_people':number_people.split(' ')[0],
                    'area': area.split('*')[0].strip(),
                    'distribute': distribute
                }
        # Serializing json  
        json_object = json.dumps(self.res) 
        # print(len(self.res))
        # sum_district = 0
        # for key, value in self.res.items():
        #     # print(key,'\n')
        #     sum_district += len(value)
        # print(sum_district)
  
        # # Writing to sample.json 
        with open(self.filename, "w" ,encoding='utf-8') as outfile: 
            outfile.write(json_object) 
