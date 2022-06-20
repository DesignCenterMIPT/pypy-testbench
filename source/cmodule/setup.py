from distutils.core import setup, Extension

def main():
    setup(name="SimpleSum",
          version="1.0.0",
          description="Python interface for the SimpleSum function",
          author="Alexander Gerasimov",
          author_email="samik.mechanic@gmail.com",
          ext_modules=[Extension("simplesum", ["simplesum.c"])])

if __name__ == "__main__":
    main()
