from pyodide.ffi import create_proxy
from pyscript import document

# Define the core logic (Same as C++)
class SimpleInfluencerNetwork:
    def __init__(self):
        self.max_influencers = 10
        self.influencers = []
        self.collaborations = [[False for _ in range(10)] for _ in range(10)]

    def get_index(self, name):
        try:
            return self.influencers.index(name)
        except ValueError:
            return -1

# Global state variables
network = SimpleInfluencerNetwork()
state = 'MENU'
temp_name = ''

# Function to write messages to the HTML console
def log(message, msg_type='system'):
    output_div = document.querySelector("#consoleOutput")
    new_line = document.createElement("div")
    new_line.className = f"log-line c-{msg_type}"
    new_line.innerText = message
    output_div.appendChild(new_line)
    output_div.scrollTop = output_div.scrollHeight

# Let the user know Python is ready


# Function triggered when the user clicks 'Enter'
def submit_command(event=None):
    global state, temp_name
    
    input_el = document.querySelector("#commandInput")
    val = input_el.value.strip()
    
    if not val:
        return
    input_el.value = ""
    log(f"> {val}", "user")

    if state == 'MENU':
        if val == '1':
            state = 'ADD_INFLUENCER'
            log("Enter influencer's name:", 'system')
        elif val == '2':
            state = 'ADD_COLLAB_1'
            log("Enter first influencer's name:", 'system')
        elif val == '3':
            if not network.influencers:
                log("The network is empty.", 'error')
            else:
                log("--- Current Collaborations ---", 'title')
                for i, name in enumerate(network.influencers):
                    friends = [network.influencers[j] for j in range(len(network.influencers)) if network.collaborations[i][j]]
                    friends_str = ", ".join(friends) if friends else "Nobody yet."
                    log(f"👤 {name} works with: {friends_str}", 'info')
        elif val == '4':
            if not network.influencers:
                log("The network is empty.", 'error')
            else:
                max_conns = -1
                popular = ""
                for i in range(len(network.influencers)):
                    conns = sum(network.collaborations[i][:len(network.influencers)])
                    if conns > max_conns:
                        max_conns = conns
                        popular = network.influencers[i]
                log(f"👑 Most Popular Influencer is: {popular} with {max_conns} collaborations!", 'success')
        elif val == '5':
            log("Exiting... Goodbye! 👋", 'title')
            document.querySelector("#commandInput").disabled = True
            document.querySelector("#submitBtn").disabled = True
        else:
            log("Invalid choice! Try again (1-5).", 'error')

    elif state == 'ADD_INFLUENCER':
        if val in network.influencers:
            log("Influencer already exists!", 'error')
        elif len(network.influencers) >= network.max_influencers:
            log("Network is full! (Max 10)", 'error')
        else:
            network.influencers.append(val)
            log(f"✔️ {val} has been added to the network.", 'success')
        state = 'MENU'

    elif state == 'ADD_COLLAB_1':
        temp_name = val
        state = 'ADD_COLLAB_2'
        log("Enter second influencer's name:", 'system')

    elif state == 'ADD_COLLAB_2':
        idx1 = network.get_index(temp_name)
        idx2 = network.get_index(val)
        
        if idx1 == -1 or idx2 == -1:
            log("❌ Error: One or both influencers not found. Add them first!", 'error')
        elif idx1 == idx2:
            log("❌ Error: An influencer cannot collaborate with themselves.", 'error')
        else:
            network.collaborations[idx1][idx2] = True
            network.collaborations[idx2][idx1] = True
            log(f"🤝 {temp_name} and {val} are now collaborating!", 'success')
        state = 'MENU'

# Function to handle pressing the "Enter" key on the keyboard
def handle_keypress(event):
    if event.key == "Enter":
        event.preventDefault()
        submit_command()

# Bind the Enter key using Python
document.querySelector("#commandInput").addEventListener("keypress", create_proxy(handle_keypress))