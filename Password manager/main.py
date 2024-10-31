from cryptography.fernet import Fernet

class PasswordManager:

    def __init__(self):
        self.key = None
        self.password_file = None
        self.password_dict = {}

    def create_key(self, path):
        self.key = Fernet.generate_key()
        with open(path, "wb") as file:
            file.write(self.key)

    def load_key(self, path):
        try:
            with open(path, "rb") as file:
                self.key = file.read()
        except FileNotFoundError:
            print("Key file not found.")
            raise

    def create_password_file(self, path, initial_values=None):
        self.password_file = path
        if initial_values is not None:
            for key, value in initial_values.items():
                self.add_password(key, value)

    def load_password_file(self, path):
        self.password_file = path
        try:
            with open(path, "r") as file:
                for line in file:
                    site, encrypted = line.strip().split(":")
                    self.password_dict[site] = self._decrypt_password(encrypted)
        except FileNotFoundError:
            print("Password file not found.")
            raise

    def _decrypt_password(self, encrypted_password):
        if self.key is None:
            raise ValueError("Key not loaded. Please load the key before decrypting.")
        return Fernet(self.key).decrypt(encrypted_password.encode()).decode()

    def add_password(self, site, password):
        if self.key is None:
            raise ValueError("Key not loaded. Please load the key before adding passwords.")

        self.password_dict[site] = password
        if self.password_file is not None:
            with open(self.password_file, "a+") as file:
                encrypted = Fernet(self.key).encrypt(password.encode())
                file.write(site + ":" + encrypted.decode() + "\n")

    def get_password(self, site):
        return self.password_dict.get(site, "Password not found.")

    def remove_password(self, site):
        if site in self.password_dict:
            del self.password_dict[site]
            self._rewrite_password_file()
        else:
            print("Site not found in password manager.")

    def _rewrite_password_file(self):
        with open(self.password_file, "w") as file:
            for site, password in self.password_dict.items():
                encrypted = Fernet(self.key).encrypt(password.encode())
                file.write(site + ":" + encrypted.decode() + "\n")


def main():

    password = {}

    pm = PasswordManager()

    print("""Make a choice.
    (1) Create a new key.
    (2) Load an existing key.
    (3) Create a new password file.
    (4) Load an existing password file.
    (5) Add a password.
    (6) Get a password.
    (q) Quit.
    """)

    done = False

    while not done:

        choice = input("Enter your choice: ")
        if choice == "1":
            path = input('Enter path: ')
            pm.create_key(path)
        elif choice == "2":
            path = input("Enter path: ")
            pm.load_key(path)
        elif choice == "3":
            path = input("Enter path: ")
            pm.create_password_file(path, password)
        elif choice == "4":
            path = input("Enter path: ")
            pm.load_password_file(path)
        elif choice == "5":
            site = input("Enter the site: ")
            password = input("Enter the password: ")
            pm.add_password(site, password)
        elif choice == "6":
            site = input("Enter the site: ")
            print(f"Password for {site} is {pm.get_password(site)}")
        elif choice == "q":
            done = True
        else:
            print("Invalid choice!")

if __name__ == "__main__":
    main()
