import requests
from bs4 import BeautifulSoup


class R6Tracker:
    def __init__(self):
        self.r6tracker_url = "https://r6.tracker.network"
        self.platforms = ["pc", "psn", "xbox"]
        
        self.match_schema = {
            "fields": [
                { "name": "index", "type": "integer" },
                { "name": "year", "type": "integer" },
                { "name": "season", "type": "integer" },
                { "name": "rp", "type": "integer" },
                { "name": "map", "type": "string" },
                { "name": "mode", "type": "string" },
                { "name": "user_id", "type": "string" },
                { "name": "update", "type": "datetime" },
                { "name": "round_win", "type": "integer" },
                { "name": "round_lose", "type": "integer" },
                { "name": "kill", "type": "integer" },
                { "name": "death", "type": "integer" }
                
            ],
            "primaryKey": ["index"],
            "pandas_version": "1.4.0"
        }
    
    def get_url_by_name(self, name, platform): # 유저 이름으로 프로필 url 얻기
        return f"{self.r6tracker_url}/profile/{platform}/{name}"

    def get_url_by_id(self, id):  # 유저 id로 프로필 url 얻기
        return f"{self.r6tracker_url}/profile/id/{id}"
    
    def get_profile_url(self, id=None, name=None): # id 또는 name으로 유효한 url을 리턴, 유효한 url이 없다면 None을 리턴
        if id != None:
            url = self.get_url_by_id(id)
            response = requests.get(url)
            if response.status_code == 200:
                return url
        if name != None:
            for platform in self.platforms:
                url = self.get_url_by_name(name, platform)
                response = requests.get(url)
                if response.status_code == 200:
                    return url
        return None
        
    def getIDbyName(self, name):
        platform = self.getPlatformbyName(name)
        if platform == None:
            return None
        url = self.get_url_by_name(name, platform)
        response = requests.get(url)
        if response.status_code == 200:
            html = response.text
            soup = BeautifulSoup(html, "html.parser")
            selector = "#profile > div.trn-scont.trn-scont--swap > div.trn-scont__aside > div:nth-child(3) > div.trn-card__content.pt0.trn--mobile-hidden > input"
            url = soup.select_one(selector)["value"].strip()
            id = url[url.rfind("/")+1:]
            return id
    
    def getNamebyID(self, id):
        url = self.get_url_by_id(id)
        response = requests.get(url)
        if response.status_code == 200:
            html = response.text
            soup = BeautifulSoup(html, "html.parser")
            selector = "#profile > div.trn-profile-header > div > div.trn-profile-header__main > h1 > span.trn-profile-header__name"
            name = soup.select_one(selector).text.strip()
            return name
        
    def getPlatformbyName(self, name):
        for platform in self.platforms:
            url = self.get_url_by_name(name, platform)
            response = requests.get(url)
            if response.status_code == 200:
                return platform
    
    def get_profile_icon_url(self, id=None, name=None):
        profile_url = self.get_profile_url(id=id, name=name)
        response = requests.get(profile_url)
        if response.status_code == 200:
            html = response.text
            soup = BeautifulSoup(html, "html.parser")
            selector = "#profile > div.trn-profile-header > div > div.trn-profile-header__main > div > img"
            profile_icon_url = soup.select_one(selector)["src"].strip()
            return profile_icon_url
        
    def get_proper_name(self, name):
        profile_url = self.get_profile_url(name=name)
        response = requests.get(profile_url)
        if response.status_code == 200:
            html = response.text
            soup = BeautifulSoup(html, "html.parser")
            selector = "#profile > div.trn-profile-header > div > div.trn-profile-header__main > h1 > span.trn-profile-header__name"
            name = soup.select_one(selector).text.strip()
            return name
        
    def isOnline(self): # 유저 온/오프라인 확인
        pass
    
    def website_status(self): # 200: Success, 503: Service Unavailable, 404: Not Found
        response = requests.get(self.r6tracker_url)
        return response.status_code == 200

            
    def get_current_season(self, current_season):
        self.current_season = current_season



if __name__ == "__main__":
    print("---")
    name = "pale.32"
    R6Tracker = R6Tracker()
    R6Tracker .getProfile(name)
    print("---")
    p_id = "45f12102-07db-4351-a400-452e260ee659"
