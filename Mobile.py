class Mobile:
    def __init__(self, name):
        self.mobile_name = name

    def receive_message(self):
        print(f"Receive message using {self.mobile_name} Mobile")

    def send_message(self):
        print(f"Send message using {self.mobile_name} Mobile")

if __name__ == "__main__":
    main()
