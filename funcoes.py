import time
def lento(texto):
    for letra in texto:
        print(letra, end ='',flush=True)
        time.sleep(0.03)
    print()

