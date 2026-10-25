from controller import display, wifi
from server.DispServer import DispServer

def main():
    net_stat = wifi.connect()
    info = display.Disp()

    info.show_time("waiting for input")
    print("Build Light ready at", net_stat.ifconfig()[0])
    server = DispServer(info)
    server.start()

if __name__ == "__main__":
    main()
