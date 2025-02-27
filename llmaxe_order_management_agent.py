from llm_axe.agents import FunctionCaller
from llm_axe import Agent, AgentType, make_prompt

def get_orders(username):
    """
    This function is used to read orders by username.

    Parameters:
    :param username: (str): required: The username you want to get the order history.
    """
    connection = sqlite3.connect("orders.db")
    cursor = connection.cursor()

    cursor.execute('SELECT * FROM orders WHERE username = ?', (username,))
    rows = cursor.fetchall()
    connection.close()
    return str(f"(username, product, amount, price_per_item, price_total)\n{rows}")

system_prompt_order_confirmation_agent = '''
You are a confirmation assistant tasked with reviewing database transaction results. Your goal is to confirm whether the user's order was successful. Provide the confirmation in a clear, professional, and consistent format. Ensure to include the following details in your response:

    Products: List all purchased items with their respective names.
    Amounts: Specify the quantity of each product purchased.
    Total Price: State the total cost of the transaction.

If the transaction was successful, output the confirmation in the following format:

Order Confirmation:
-------------------
Status: Successful

Products:
- [Product Name 1]: [Amount 1]
- [Product Name 2]: [Amount 2]
...

Total Price: $[Total Price]

Thank you for your purchase!

If the transaction was not successful, output the following message:

Order Confirmation:
-------------------
Status: Failed

We're sorry, but your order could not be processed. Please try again or contact support.

Ensure the output is always consistent and clear.
'''

llm = MyCustomLLM()
order_confirmation_agent = Agent(llm, agent_type=AgentType.GENERIC_RESPONDER, custom_system_prompt=system_prompt_order_confirmation_agent)

fc = FunctionCaller(llm, [create_order, get_orders, send_email])
