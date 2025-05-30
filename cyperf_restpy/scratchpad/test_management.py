from cyperf.api_client import ApiClient
from cyperf.api.agents_api import AgentsApi
from cyperf.configuration import Configuration

from cyperf.models.agent_to_be_rebooted import AgentToBeRebooted
from cyperf.models.reboot_operation_input import RebootOperationInput
from cyperf.models.set_dpdk_mode_operation_input import SetDpdkModeOperationInput

config = Configuration(host="https://3.141.193.119",
                       refresh_token="eyJhbGciOiJIUzI1NiIsInR5cCIgOiAiSldUIiwia2lkIiA6ICIzOTMyN2I4OC0xYzkyLTRlYjktYTI0My01MTE3NTczNTBlNjIifQ.eyJpYXQiOjE3NDgzMTkxMzksImp0aSI6IjEyZGExMWJlLTIwOGQtNGNmOC1hMDY3LTUyYzU4MTQ1MzE4OCIsImlzcyI6Imh0dHBzOi8vMy4xNDEuMTkzLjExOS9hdXRoL3JlYWxtcy9rZXlzaWdodCIsImF1ZCI6Imh0dHBzOi8vMy4xNDEuMTkzLjExOS9hdXRoL3JlYWxtcy9rZXlzaWdodCIsInN1YiI6ImNjNGQwZjU5LTEwNDUtNGI0MS05YjhjLTUwN2JjMWE2MWM4NiIsInR5cCI6Ik9mZmxpbmUiLCJhenAiOiJjbHQtd2FwIiwibm9uY2UiOiI3ZDMxMDFlNi00YWEyLTQyNjctOWYyZC04YWM3ZmYzMGIzMzYiLCJzZXNzaW9uX3N0YXRlIjoiNTE3NzBlMTQtZThhMS00M2Y0LWI5YzItMjIzMzNkMzY1M2ZkIiwic2NvcGUiOiJvcGVuaWQgZW1haWwgb2ZmbGluZV9hY2Nlc3MgcHJvZmlsZSIsInNpZCI6IjUxNzcwZTE0LWU4YTEtNDNmNC1iOWMyLTIyMzMzZDM2NTNmZCJ9.FQZCwtCEMqam14_eThKhLfGImyHiB1Awo5UXcQ1YW7c")
# if you don't have a valid HTTPS certificate for controller, uncomment this line
config.verify_ssl = False
CLIENT = ApiClient(config)

agents_api  = AgentsApi(CLIENT)

def get_all_available_agents():
    available_agents = agents_api.get_agents(exclude_offline='true')
    for agent in available_agents:
        print(agent.id)
        print(agent.ip)
        print(agent.hostname)
        print(agent.mgmt_interface)
        print(agent.status)


get_all_available_agents()

# Set DPDK mode and do async polling
agents_api.start_agents_set_dpdk_mode(set_dpdk_mode_operation_input=SetDpdkModeOperationInput(agent_ids=['1234567890'], enabled=True))
agents_api.poll_agents_set_dpdk_mode(id="12345")

# Reboot the agents and poll their progress
agents_api.start_agents_reboot(reboot_operation_input=RebootOperationInput(agents=[AgentToBeRebooted(agent_id='1234567890')]))
agents_api.poll_agents_reboot(id="12345")


# Reserve Agents


# Release Agentss
