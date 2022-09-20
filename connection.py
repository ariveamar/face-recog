from pymongo import MongoClient
import os
from dotenv import load_dotenv
load_dotenv()
client = MongoClient(os.getenv("IP_ADDR_SERVER_MONGO"), int(os.getenv("PORT_SERVER_MONGO")))

devdb_dpo = client.devdb_dpo
dpos = devdb_dpo.dpos

devdb_doh = client.devdb_doh
doh = devdb_doh.doh

devdb_hiltem = client.devdb_hiltem
hiltem = devdb_hiltem.hiltem