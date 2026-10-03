#CYB333 Socket Connection Server

import socket

HOST = '127.0.0.1'
PORT = 65432


def start_server():
	# Create TCP socket
	with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
		server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		server_socket.settimeout(200)
		try:
			server_socket.bind((HOST, PORT))
			server_socket.listen(1)
			print(f"[*] Server listening on {HOST}:{PORT}")

			conn, addr = server_socket.accept()
			with conn:
				conn.settimeout(200)
				print(f"[+] Connected by {addr}")
				while True:
					data = conn.recv(1024)
					if not data:
						break
					message = data.decode('utf-8')
					print(f"[>] Received: {message}")
					response = f"Server received: {message}"
					conn.sendall(response.encode('utf-8'))
				print("[-] Client disconnected")
		except OSError as e:
			print(f"[!] Server error: {e}")


if __name__ == "__main__":
	start_server()

