from pyfunc.gen_db import GenerateDB

def main():
	gdb = GenerateDB(GenerateDB.TYPE_FILE)
	gdb.gen_db()

if __name__ == '__main__':
	main()
