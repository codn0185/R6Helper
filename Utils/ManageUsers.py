from Utils.Json import *


class Users:
    def __init__(self):
        self.filename = "users"
        self.columns = ["email", "password", "id", "name", "update"]
        self.schema = {
            "fields": [
                { "name": "index", "type": "integer" },
                { "name": "email", "type": "string" },
                { "name": "password", "type": "string" },
                { "name": "id", "type": "string" },
                { "name": "name", "type": "string" },
                { "name": "update", "type": "datetime" }
            ],
            "primaryKey": ["index"],
            "pandas_version": "1.4.0"
        }
        
    def load(self):
        if not is_json(self.filename):
            write_json({"schema": self.schema, "data": []}, self.filename)
        self.df = df_from_json(self.filename)

    def save(self):
        df_to_json(self.df, self.filename)

    def add(self, user: dict):
        user["update"] = pd.Timestamp.now()
        self.df = pd.concat([self.df, pd.DataFrame([user])], ignore_index=True)
            
    def modify(self, user: dict):
        user["update"] = pd.Timestamp.now()
        self.df.loc[self.df["id"] == user["id"], user.keys()] = user.values()

    def drop(self, user: dict):
        self.df = self.df[self.df["id"] != user["id"]]
        
    def update(self, user: dict):
        if self.isDuplicated(user):
            self.modify(user)
        else:
            self.add(user)

    def isDuplicated(self, user: dict):
        return user["id"] in self.df["id"].values
        
    
if __name__ == "__main__":
    pass