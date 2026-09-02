import multiprocessing
from ui.interface import criar_interface

if __name__ == '__main__':
    # A TRAVA DE SEGURANÇA para o Modo Turbo (Multiprocessing)
    multiprocessing.freeze_support()
    
    # Inicia o Cockpit Visual
    criar_interface()