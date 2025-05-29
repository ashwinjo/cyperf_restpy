from cyperf.api_client import ApiClient
from cyperf.api.agents_api import AgentsApi
from cyperf.configuration import Configuration
from cyperf.models.agent_assignment_details import AgentAssignmentDetails

from cyperf.models.agent_to_be_rebooted import AgentToBeRebooted
from cyperf.models.reboot_operation_input import RebootOperationInput
from cyperf.models.set_dpdk_mode_operation_input import SetDpdkModeOperationInput
from cyperf.models.reserve_operation_input import ReserveOperationInput
from cyperf.models.agent_reservation import AgentReservation    
from cyperf.models.release_operation_input import ReleaseOperationInput
from cyperf.models.agent_release import AgentRelease 

config = Configuration(host="https://3.141.193.119",
                       refresh_token="eyJhbGciOiJIUzI1NiIsInR5cCIgOiAiSldUIiwia2lkIiA6ICIzOTMyN2I4OC0xYzkyLTRlYjktYTI0My01MTE3NTczNTBlNjIifQ.eyJpYXQiOjE3NDgzODE4MzcsImp0aSI6ImM4YjcwMDRmLTIzNzctNDNjZC04YmIxLWJjMmI2MDI2ZDUxZCIsImlzcyI6Imh0dHBzOi8vMy4xNDEuMTkzLjExOS9hdXRoL3JlYWxtcy9rZXlzaWdodCIsImF1ZCI6Imh0dHBzOi8vMy4xNDEuMTkzLjExOS9hdXRoL3JlYWxtcy9rZXlzaWdodCIsInN1YiI6ImNjNGQwZjU5LTEwNDUtNGI0MS05YjhjLTUwN2JjMWE2MWM4NiIsInR5cCI6Ik9mZmxpbmUiLCJhenAiOiJjbHQtd2FwIiwibm9uY2UiOiIwMzdmOGVkNC0zMjMxLTQ2NmYtOGFhZi1mN2U0MTIyOWUwZmIiLCJzZXNzaW9uX3N0YXRlIjoiYWFjYTI5ZjgtMzA3Mi00YWM1LThmMjQtZTJlMzI1YWYwMDNmIiwic2NvcGUiOiJvcGVuaWQgZW1haWwgb2ZmbGluZV9hY2Nlc3MgcHJvZmlsZSIsInNpZCI6ImFhY2EyOWY4LTMwNzItNGFjNS04ZjI0LWUyZTMyNWFmMDAzZiJ9.uSszcj6bYW97eqWLBhcY5-1UerWaMqihJDITPTMgF8E")
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

# Get all available agents
#print(get_all_available_agents())

#print(agents_api.get_agent_by_id(agent_id="591d56b9-43b2-439a-8f9d-100774efd8d2"))
#print(agents_api.get_agents_tags())
for tag in agents_api.get_agents_tags():
    print(tag.name, tag.agents)

# Set DPDK mode and do async polling
# agents_api.start_agents_set_dpdk_mode(set_dpdk_mode_operation_input=SetDpdkModeOperationInput(agent_ids=['1234567890'], enabled=True))
# agents_api.poll_agents_set_dpdk_mode(id="12345")

# Reboot the agents and poll their progress
# agents_api.start_agents_reboot(reboot_operation_input=RebootOperationInput(agents=[AgentToBeRebooted(agent_id='1234567890')]))
# agents_api.poll_agents_reboot(id="12345")


# Reserve Agents
# agents_api.start_agents_reserve(reserve_operation_input=ReserveOperationInput(agents=[AgentReservation(agent_id='1234567890')]))
# agents_api.poll_agents_reserve(id="12345")

# Release Agents
# agents_api.start_agents_release(release_operation_input=ReleaseOperationInput(agents=[AgentRelease(agent_id='1234567890')]))
# agents_api.poll_agents_release(id="12345")

# Assign Agents to Network Profile
available_agents = agents_api.get_agents(exclude_offline='true')
for agent in available_agents:
    print(agent.ip, agent.status, agent.id)
    agent_assignment_details = AgentAssignmentDetails(agent_id=agent.id, interfaces=["eth0", "eth1"])
    agents_api.start_agents_assign(agent_assignment_details=agent_assignment_details)
    agents_api.poll_agents_assign(id="12345")



# agents = {
#     'PAN-FW-Client': ['10.38.68.151'],
#     'AWS-NW-FW-Client': ['10.38.68.185'],
#     'PAN-FW-Server': ['10.36.75.37'],
#     'AWS-NW-FW-Server': ['10.36.75.65']