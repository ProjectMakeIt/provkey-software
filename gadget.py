def disable():
    with open('/sys/kernel/config/usb_gadget/provkey/UDC','w') as f:
        f.write('')
        f.close()

def enable():
    with open('/sys/kernel/config/usb_gadget/provkey/UDC','w') as f:
        f.write('20980000.usb')
        f.close()
