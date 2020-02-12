import subprocess
import json
from string import ascii_lowercase,ascii_uppercase
short = ascii_lowercase+ascii_uppercase
index = 0
def recursive(voc,cmd,neested=0):
    global index
    for i in voc:
        command='#[align=left fg='
        if i['mountpoint'] == None:
            command+='gray'
            mount=""
            cc="mount"
        else:
            command+='green'
            mount=i['mountpoint']
            cc="unmount"
        if i['type'] == 'disk':
            icon = ' '
        elif i['type'] == 'crypt':
            icon = ''
        elif i['type'] == 'part':
            icon = '﫭'
        command+=']'
        prefix='  '*neested
        if i == voc[-1]:
            prefix += '└─'
        else:
            prefix += '├─'
        command+=prefix+i['name']+'('+i['size']+')#[align=right]'+mount
        cmd.append(command)
        if index < len(short):
            cmd.append(short[index])
            index+=1
        else:
            cmd.append("")
        cmd.append("run -b \"udisksctl "+cc+' -b /dev/'+i['name']+'\"')
        if 'children' in i:
            recursive(i['children'],cmd,neested+1)
def show_menu():
    short=ascii_lowercase
    datas=subprocess.check_output(["lsblk",'-J'])
    datas=datas.decode('ASCII')
    voc = json.loads(datas)
    index = 0
    cmd = ["tmux","display-menu","-T","#[align=centre]Mountable disk","-x","R","-y","P"]
    for i in voc['blockdevices']:
        command='#[align=left fg='
        if i['mountpoint'] == None:
            command+='gray'
        else:
            command+='green'
        if i['type'] == 'disk':
            icon = ' '
        elif i['type'] == 'crypt':
            icon = ' ' 
        elif i['type'] == 'part':
            icon = '﫭 '
        command+=']'+i['name']
        cmd.append(command)
        cmd.append("")
        cmd.append("")
        recursive(i['children'],cmd)
    subprocess.check_output(cmd)
if __name__ == "__main__":
    show_menu();
