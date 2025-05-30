from cyperf import ApplicationProfile, NetworkProfile, IPNetwork, AgentAssignments, ConfigId
from cyperf.configuration import Configuration
from cyperf.api_client import ApiClient
from cyperf.api.application_resources_api import ApplicationResourcesApi


config = Configuration(host="https://3.141.193.119",
                       refresh_token="eyJhbGciOiJIUzI1NiIsInR5cCIgOiAiSldUIiwia2lkIiA6ICIzOTMyN2I4OC0xYzkyLTRlYjktYTI0My01MTE3NTczNTBlNjIifQ.eyJpYXQiOjE3NDgzODE4MzcsImp0aSI6ImM4YjcwMDRmLTIzNzctNDNjZC04YmIxLWJjMmI2MDI2ZDUxZCIsImlzcyI6Imh0dHBzOi8vMy4xNDEuMTkzLjExOS9hdXRoL3JlYWxtcy9rZXlzaWdodCIsImF1ZCI6Imh0dHBzOi8vMy4xNDEuMTkzLjExOS9hdXRoL3JlYWxtcy9rZXlzaWdodCIsInN1YiI6ImNjNGQwZjU5LTEwNDUtNGI0MS05YjhjLTUwN2JjMWE2MWM4NiIsInR5cCI6Ik9mZmxpbmUiLCJhenAiOiJjbHQtd2FwIiwibm9uY2UiOiIwMzdmOGVkNC0zMjMxLTQ2NmYtOGFhZi1mN2U0MTIyOWUwZmIiLCJzZXNzaW9uX3N0YXRlIjoiYWFjYTI5ZjgtMzA3Mi00YWM1LThmMjQtZTJlMzI1YWYwMDNmIiwic2NvcGUiOiJvcGVuaWQgZW1haWwgb2ZmbGluZV9hY2Nlc3MgcHJvZmlsZSIsInNpZCI6ImFhY2EyOWY4LTMwNzItNGFjNS04ZjI0LWUyZTMyNWFmMDAzZiJ9.uSszcj6bYW97eqWLBhcY5-1UerWaMqihJDITPTMgF8E")
# if you don't have a valid HTTPS certificate for controller, uncomment this line
config.verify_ssl = False
CLIENT = ApiClient(config)

application_resources_api = ApplicationResourcesApi(CLIENT)

# app_reources_types = application_resources_api.get_resources_application_types()

# for p in app_reources_types:
#         print(p.id)
    


# app_resources = application_resources_api.get_resources_apps()
# for p in app_resources:
#     print(p.id, p.name)


#Malware
# attack_resources = application_resources_api.get_resources_attacks()
# for p in attack_resources:
#     print(p.name)

#CVE
# resources_strikes = application_resources_api.get_resources_strikes()
# for p in resources_strikes:
#     print(p.id)

# Get's all the PCAPS that we can run on cyperf
captures = application_resources_api.get_resources_captures()
for a in captures:
    print(a.id, a.name)

# for a in app_resources:
#     print(a.id, a.name)


