# internet speed test
# packet loss

#pip install speedtest-cli
import speedtest

#pip install icmplib
from icmplib import ping

def check_speed():

    option = int(input('''What speed do you want to test:  
 

    1) Download Speed  

    2) Upload Speed  

    3) Ping 

    Your Choice: '''))

    st = speedtest.Speedtest()


    if option == 1:

        print(st.download())

    elif option == 2:

        print(st.upload())

    elif option == 3:

        servernames =[]
        st.get_servers(servernames)


    else:
        print("Please select a valid option")




    print(st.results.ping)


    host = ping("8.8.8.8", count = 10, interval = 0.1, privileged = False)

    print(f"packets found: {host.packets_found}")
    print(f"packets lost: {host.packets_lost * 100:.1f}%")

if __name__ == "__main__":
    check_speed()