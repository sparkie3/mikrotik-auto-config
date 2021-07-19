from tkinter import *
import paramiko


def run_command(cmd_str, hostname, port, username, password, nbytes=4096):
    client = paramiko.Transport((hostname, port))
    client.connect(username=username, password=password)

    stdout_data = []
    stderr_data = []
    session = client.open_channel(kind='session')
    session.exec_command(cmd_str)

    while True:
        if session.recv_ready():
            stdout_data.append(session.recv(nbytes))
        if session.recv_stderr_ready():
            stderr_data.append(session.recv_stderr(nbytes))
        if session.exit_status_ready():
                         break

    print('exit status: ', session.recv_exit_status())
    print(''.join(stdout_data))
    print(''.join(stderr_data))

    session.close()
    client.close()

def gen_cmd_str_ip(ip, interface):
    return f"ip address add address={ip} interface={interface}"


def gen_cmd_str_gw(gateway):
    return f"ip route add dst-address=0.0.0.0/0 gateway={gateway}"


def gen_cmd_str_id(identity):
    return f"system identity set name={identity}"


def gen_cmd_str_wpa(wpa):
    return f"interface wireless security-profiles add name=WPA mode=dynamic-keys authentication-types=wpa2-psk wpa2-pre-shared-key={wpa}"


def gen_cmd_str_ssid1(ssid1):
    return f"interface wireless set ssid={ssid1} wlan1"


def gen_cmd_str_ssid2(ssid2):
    return f"interface wireless set ssid={ssid2} wlan2"


def init_tk(root):
    def clear_entries():
        for key, entry, in entries.items():
            entry.delete(0, 'end')
    def send_commands():
        all_commands = []
        cmd_str = gen_cmd_str_ip(entries['ip'].get(), interface_select.get())
        all_commands.append(cmd_str)
        cmd_str = gen_cmd_str_gw(entries['gateway'].get())
        all_commands.append(cmd_str)
        cmd_str = gen_cmd_str_id(entries['identity'].get())
        all_commands.append(cmd_str)
        cmd_str = gen_cmd_str_wpa(entries['wpa'].get())
        all_commands.append(cmd_str)
        cmd_str = gen_cmd_str_ssid1(entries['ssid1'].get())
        all_commands.append(cmd_str)
        cmd_str = gen_cmd_str_ssid2(entries['ssid2'].get())
        all_commands.append(cmd_str)
        formatted_commands = "\n".join(all_commands)
        run_command(formatted_commands, entries['mgmt_ip'].get(), int(entries['port'].get()), entries['user'].get(), entries['pass'].get())
        
    entries = {}
    mgmt_ip_label = Label(root, text='Management IP Address:', font=('calibre', 10, 'bold'))
    entries['mgmt_ip'] = Entry(root, justify='center', font=('calibre', 10))
    mgmt_ip_label.grid(row=0, column=0, sticky = W, pady=2, padx=5)
    entries['mgmt_ip'].grid(row=0, column=1, pady=2)
    port_label = Label(root, text='Management Port:', font=('calibre', 10, 'bold'))
    entries['port'] = Entry(root, justify='center', font=('calibre', 10))
    port_label.grid(row=0, column=2, sticky=W, pady=2, padx=5)
    entries['port'].grid(row=0, column=3, pady=2)
    user_label = Label(root, text='Username:', font=('calibre', 10, 'bold'))
    entries['user'] = Entry(root, justify='center', font=('calibre', 10))
    user_label.grid(row=1, column=0, sticky=W, pady=2, padx=5)
    entries['user'].grid(row=1, column=1, pady=2)
    pass_label = Label(root, text='Password:', font=('calibre', 10, 'bold'))
    entries['pass'] = Entry(root, justify='center', show='*', font=('calibre', 10))
    pass_label.grid(row = 1, column=2, sticky=W, pady=2, padx=5)
    entries['pass'].grid(row=1, column=3, pady=2)
    ip_label = Label(root, text='WAN IP Address:', font=('calibre', 10, 'bold'))
    entries['ip'] = Entry(root, justify='center', font=('calibre', 10))
    ip_label.grid(row=2, column=0, sticky=W, pady=2, padx=5)
    entries['ip'].grid(row= 2, column=1, pady=2)
    interface_list = ['ether1', 'ether2', 'ether3', 'ether4', 'ether5', 'ether6', 'ether7', 'ether8', 'ether9', 'ether10', 'wlan1', 'wlan2', 'sfp1', 'sfp+plus1']
    interface_select = StringVar(root)
    interface_select.set(interface_list[0])
    interface_label = Label(root, text = 'WAN Interface:', font=('calibre', 10, 'bold')) #this should be a drop down
    interface_drop = OptionMenu(root, interface_select, *interface_list)
    interface_label.grid(row=3, column=0, sticky=W, pady=2, padx=5)
    interface_drop.grid(row=3, column=1, pady=2)
    gateway_label = Label(root, text='Default Gateway:', font=('calibre', 10, 'bold'))
    entries['gateway']=Entry(root, justify='center', font=('calibre', 10))
    gateway_label.grid(row=4, column=0, sticky=W, pady=2, padx=5)
    entries['gateway'].grid(row=4, column=1, pady=2)
    identity_label = Label(root, text='Identity:', font=('calibre', 10, 'bold'))
    entries['identity'] = Entry(root, justify='center', font=('calibre', 10))
    identity_label.grid(row=5, column=0, sticky=W, pady=2, padx=5)
    entries['identity'].grid(row=5, column=1, pady=2)
    wpa_label = Label(root, text='WiFi Password:', font=('calibre', 10, 'bold'))
    entries['wpa'] = Entry(root, justify='center', show='*', font=('calibre', 10))
    wpa_label.grid(row = 6, column=0, sticky=W, pady=2, padx=5)
    entries['wpa'].grid(row=6, column=1, pady=2)
    ssid1_label = Label(root, text='2.4Ghz SSID:', font=('calibre', 10, 'bold')) #ssid for 2.4Ghz
    entries['ssid1'] = Entry(root, justify='center', font=('calibre', 10))
    ssid1_label.grid(row=7, column=0, sticky=W, pady=2, padx=5)
    entries['ssid1'].grid(row=7, column=1, pady=2)
    ssid2_label = Label(root, text='5Ghz SSID:', font=('calibre', 10, 'bold')) #ssid for 5Ghz
    entries['ssid2'] = Entry(root, justify='center', font=('calibre', 10))
    ssid2_label.grid(row=8, column=0, sticky=W, pady=2, padx=5)
    entries['ssid2'].grid(row=8, column=1, pady=2)
    submit_button = Button(root, text='Submit', command=send_commands)
    submit_button.grid(row=9, column=2, sticky=W, pady=10, padx=5)
    clear_button = Button(root, text='Clear', command=clear_entries)
    clear_button.grid(row=9, column=1, sticky=E, pady=10, padx=5)


def main():
    root = Tk()
    root.geometry("750x315")
    root.title("Lets get configuring!")
    root.eval('tk::PlaceWindow . center')
    init_tk(root)
    root.mainloop()


if __name__ == '__main__':
    main()

