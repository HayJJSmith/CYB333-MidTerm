#CYB333 Socket Connection Client.py

import socket

HOST = '127.0.0.1'
PORT = 65432
SOCKET_TIMEOUT = 200


def start_client():
	with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
		client_socket.settimeout(SOCKET_TIMEOUT)
		try:
			client_socket.connect((HOST, PORT))
			print(f"[+] Connected to server at {HOST}:{PORT}")

			while True:
				message = input("Enter message ('exit' to quit): ")
				if message.strip().lower() == 'exit':
					break

				client_socket.sendall(message.encode('utf-8'))
				data = client_socket.recv(1024)
				if not data:
					print("[-] Server disconnected")
					break

				print(f"[<] {data.decode('utf-8')}")

			print("[-] Closing connection")
		except ConnectionRefusedError:
			print("[!] Connection failed: server is not running or unreachable")
		except socket.timeout:
			print(f"[!] Socket operation timed out after {SOCKET_TIMEOUT} seconds")
		except OSError as e:
			print(f"[!] Client error: {e}")


if __name__ == "__main__":
	start_client()