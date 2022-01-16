from random import *
import requests
import json


def gcd(x, y):
	return x if y == 0 else gcd(y, x % y)


def EGCD(a, b):
	if a == 0:
		return b, 0, 1
	Gcd, x1, y1 = EGCD(b % a, a)
	x = y1 - (b // a) * x1
	y = x1
	return Gcd, x, y


def rev(x, m):
	Gcd, a, b = EGCD(x, m)
	if Gcd == 1:
		return (a % m + m) % m


class my_rsa:
	def __init__(self, m=4, length=256):
		# 27-41 инициализация класса, создание парі моих ключей, создание сессии, и запрос с сервере открітіх модуля и експоненты
		self.number = m
		self.length = 256
		self.my_primes = None
		self.A = None
		self.B = None
		self.A_key = None
		self.B_key = None
		self.data = None
		self.session = requests.Session()
		server_publik_key = json.loads(
			self.session.get("https://asym-crypt-study.herokuapp.com/rsa/serverKey?keySize=512").content)
		self.Exp = int(server_publik_key['publicExponent'], 16)
		self.Mod = int(server_publik_key['modulus'], 16)
		self.regenerate(m, length)

	# вернуть ключ
	def GetExampleCreds(self):
		return self.A_key

	# создать новую пару ключей
	def regenerate(self, m, length):
		self.number = m
		self.length = 256
		self.my_primes = self.genPrimes()
		self.A = [self.my_primes[0], self.my_primes[1]]
		self.B = [self.my_primes[2], self.my_primes[3]]
		self.A_key = self.get_key(self.A)
		self.B_key = self.get_key(self.B)
		self.data = 0xff # это даные сообщения
		self.check_all()

	def check_all(self):
		print("A")
		print(f"p {self.A[0]}")
		print(f"q {self.A[1]}")
		print("B")
		print(f"p {self.B[0]}")
		print(f"q {self.B[1]}")
		print("A_key")
		print(f"n {self.A_key[0]}")
		print(f"e {self.A_key[1]}")
		print(f"d {self.A_key[2]}")
		print("B_key")
		print(f"n {self.B_key[0]}")
		print(f"e {self.B_key[1]}")
		print(f"d {self.B_key[2]}")
		print("data")
		print(f"my message {self.data}")
		print("Message")
		# создает ключ 74-75
		Msg = self.get_message(self.data, self.A_key[2], self.B_key[1], self.A_key[0], self.B_key[0])
		print(Msg[0])
		print(Msg[1])
		# проверяет аутентичность
		print("Checking Auth")
		sign = self.get_sign(self.data, self.A_key[0], self.A_key[2])
		sign_checked = self.checkup_sigh(sign, self.A_key[0], self.A_key[1])
		print(sign_checked)
		# проверяет конфиденциальность
		print("Checking Conf")
		k = self.checkup_conf(Msg[0], self.B_key[0], self.B_key[2])
		print(k)

		...

	@staticmethod
	# 94-129 проверка на простое число тестом Миллера-Рабина
	def check_prime(p):
		for prime in [2, 3, 5, 7]:
			if p % prime == 0:
				return False
		d, z = p - 1, 0
		while True:
			if d % 2 == 0:
				d = d // 2
				z += 1
			else:
				break
		K = 20
		for iteration in range(K):
			# 1
			x = randint(2, p - 1)
			if gcd(x, p) == 1:
				# 2
				pw = pow(x, d, p)
				if pw == 1 or pw - p == -1:
					print("", end="")
				else:
					# 3
					flag = 0
					for r in range(1, z):
						xr = pow(x, d * (2 ** r), p)
						if xr - p == -1:
							flag = 1
							break
						elif xr == 1:
							return False
					if flag == 0:
						return False
			else:
				return False
		return True

	# создание 4 простіх чисел длинной в 256 байт
	def genPrimes(self):
		primes = []
		print(f"#{'-' * 75}#")
		while len(primes) < self.number:
			p = getrandbits(self.length)
			if self.check_prime(p):
				primes.append(p)
			else:
				print(p)
		print(f"#{'-' * 75}#\nКінець відкинутих простих чисел\n")
		return primes

	@staticmethod
	# создание ключа с пары  p & q
	def get_key(key):
		n = key[0] * key[1]  # modulus
		phi = (key[0] - 1) * (key[1] - 1)
		while True:
			e = randrange(2, phi - 1)
			if gcd(e, phi) == 1:
				d = rev(e, phi)
				if d is None:
					continue
				else:
					return n, e, d
			else:
				continue

	# 160-179 єто условніе операции по шифровке, дешифровке, подписи. Так как все они по-сути просто возведение в степень так проще с ними работать
	@staticmethod
	def encypher(m, n, e):
		return pow(m, e, n)

	@staticmethod
	def decypher(c, n, d):
		return pow(c, d, n)

	@staticmethod
	def get_sign(k, n, d):
		return pow(k, d, n)

	@staticmethod
	def checkup_conf(m, n, d):
		return pow(m, d, n)

	@staticmethod
	def checkup_sigh(s, n, e):
		return pow(s, e, n)

	# создание сообщения
	def get_message(self, k, d, e1, n, n1):
		k1 = self.encypher(k, n1, e1)
		s = self.get_sign(k, n, d)
		s1 = self.encypher(s, n1, e1)
		return [k1, s1]

	# обращение	к серверу: он дешифркует нами зашифрованое сообщение
	def Decrypt(self, K=None, Type='BYTES'):
		K = self.data if K is None else K
		print("input:", hex(K))
		Message = self.encypher(K, self.Mod, self.Exp)
		print("encrypted:", Message)
		print("response:", self.session.get(
			"https://asym-crypt-study.herokuapp.com/rsa/decrypt?cipherText=" + hex(Message)[
																			   2:] + "&type=" + Type).content)

	# обращение	к серверу за сообщением, мы дешифруем его сообщение
	def Encrypt(self, K=None, Type='BYTES'):
		K = self.data if K is None else K
		reply = json.loads(self.session.get(
			"https://asym-crypt-study.herokuapp.com/rsa/encrypt?modulus=" + hex(self.GetExampleCreds()[0])[2:] + "&publicExponent=" + hex(
				self.GetExampleCreds()[1])[2:] + "&message=" + hex(K)[2:] + "&type=" + Type).content)
		print(reply)
		result = self.checkup_conf(int('0x'+reply['cipherText'], 16), self.GetExampleCreds()[0], self.GetExampleCreds()[2])
		print(f"result {result}")

	# обращение	к серверу за верификацей
	def Verify(self, K = None):
		K = self.data if K is None else K
		Sign = self.get_sign(K, self.GetExampleCreds()[0], self.GetExampleCreds()[2])
		print(self.session.get("https://asym-crypt-study.herokuapp.com/rsa/verify?message=" + hex(K)[2:] + "&type=BYTES&signature=" + hex(Sign)[2:] + "&modulus=" + hex(self.GetExampleCreds()[0])[2:] + "&publicExponent=" + hex(self.GetExampleCreds()[1])[2:]).content)

	# обращение	к серверу за подписью
	def Sign(self, K=None):
		K = self.data if K is None else K
		print(self.session.get(
			"https://asym-crypt-study.herokuapp.com/rsa/sign?message=" + hex(K)[2:] + "&type=BYTES").content)

	# обращение	к серверу за ключем и верификацей
	def SendKey(self):
		print(self.session.get(
			"https://asym-crypt-study.herokuapp.com/rsa/sendKey?modulus=" + hex(self.GetExampleCreds()[0])[2:] + "&publicExponent=" + hex(
				self.GetExampleCreds()[1])[2:]).content)

	# обращение	к серверу за ключем и верификацей
	def ReceiveKey(self, K=None):
		K = self.data if K is None else K
		remote = self.get_message(K, self.GetExampleCreds()[2], self.Exp, self.GetExampleCreds()[0], self.Mod)
		print(self.session.get(
			"https://asym-crypt-study.herokuapp.com/rsa/receiveKey?key=" + hex(remote[0])[2:] + "&signature=" + hex(
				remote[1])[2:] + "&modulus=" + hex(self.GetExampleCreds()[0])[2:] + "&publicExponent=" + hex(self.GetExampleCreds()[1])[2:]).content)
