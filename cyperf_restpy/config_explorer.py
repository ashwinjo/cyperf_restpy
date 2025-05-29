from cyperf.configuration import Configuration
from cyperf.api_client import ApiClient
from cyperf.api.configurations_api import ConfigurationsApi


config = Configuration(host="https://3.141.193.119",
                       refresh_token="eyJhbGciOiJIUzI1NiIsInR5cCIgOiAiSldUIiwia2lkIiA6ICIzOTMyN2I4OC0xYzkyLTRlYjktYTI0My01MTE3NTczNTBlNjIifQ.eyJpYXQiOjE3NDg0NjAwMjgsImp0aSI6ImI2NjAwMzNlLTk1NjEtNDIwZC05NjdiLWU1ZmQ5MmY1MDljNyIsImlzcyI6Imh0dHBzOi8vMy4xNDEuMTkzLjExOS9hdXRoL3JlYWxtcy9rZXlzaWdodCIsImF1ZCI6Imh0dHBzOi8vMy4xNDEuMTkzLjExOS9hdXRoL3JlYWxtcy9rZXlzaWdodCIsInN1YiI6ImNjNGQwZjU5LTEwNDUtNGI0MS05YjhjLTUwN2JjMWE2MWM4NiIsInR5cCI6Ik9mZmxpbmUiLCJhenAiOiJjbHQtd2FwIiwibm9uY2UiOiJhMDlhMTI0My02OGVhLTRmZTMtOGY5My04YThmMmU2NjNkNmIiLCJzZXNzaW9uX3N0YXRlIjoiYWFjYTI5ZjgtMzA3Mi00YWM1LThmMjQtZTJlMzI1YWYwMDNmIiwic2NvcGUiOiJvcGVuaWQgZW1haWwgb2ZmbGluZV9hY2Nlc3MgcHJvZmlsZSIsInNpZCI6ImFhY2EyOWY4LTMwNzItNGFjNS04ZjI0LWUyZTMyNWFmMDAzZiJ9.9lZbFCkd1zX-JhTsYanx_MtoId9gY4rPKmBka6-g5Ks")
# if you don't have a valid HTTPS certificate for controller, uncomment this line
config.verify_ssl = False
CLIENT = ApiClient(config)


# We will crete and empty config url here

config_api = ConfigurationsApi(CLIENT)

a = config_api.get_configs(take=None, 
                           skip=0, 
                           search_col=None, 
                           search_val=None, 
                           filter_mode=None, 
                           sort=None)

print(len(a.data))
with open("config_list.txt", "w") as f:
    for val in a.data:
        f.writelines(val.display_name + " || " + val.config_url + "\n")
