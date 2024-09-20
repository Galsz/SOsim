import random
import time


class Processo:

    contador_pid = 0  
    
    def __init__(self, tempo_execucao, prioridade, memoria_necessaria):
        Processo.contador_pid += 1
        self.pid = Processo.contador_pid
        self.tempo_execucao = tempo_execucao
        self.prioridade = prioridade
        self.memoria_necessaria = memoria_necessaria
        self.estado = 'Pronto' 
        
    def __str__(self):
        return (f'PID: {self.pid}, Tempo Execução: {self.tempo_execucao}, '
                f'Prioridade: {self.prioridade}, Memória Necessária: {self.memoria_necessaria}, '
                f'Estado: {self.estado}')
    

class MemoriaRAM:

    def __init__(self, tamanho_total):
        self.tamanho_total = tamanho_total
        self.memoria_disponivel = tamanho_total
        self.alocacao = {} 
        
    def alocar_memoria(self, processo):
        if processo.memoria_necessaria <= self.memoria_disponivel:
            self.memoria_disponivel -= processo.memoria_necessaria
            self.alocacao[processo.pid] = processo.memoria_necessaria
            return True
        return False
    
    def liberar_memoria(self, processo):
        if processo.pid in self.alocacao:
            self.memoria_disponivel += self.alocacao.pop(processo.pid)

class GerenciadorProcessos:
    def __init__(self, memoria_ram, vazamento_memoria=False):
        self.processos = []  
        self.fila_prontos = []  
        self.memoria_ram = memoria_ram
        self.vazamento_memoria = vazamento_memoria
        
    def criar_processo(self, tempo_execucao, prioridade, memoria_necessaria):
        novo_processo = Processo(tempo_execucao, prioridade, memoria_necessaria)
        if self.memoria_ram.alocar_memoria(novo_processo):
            self.processos.append(novo_processo)
            self.fila_prontos.append(novo_processo)
            self.fila_prontos.sort(key=lambda p: p.prioridade)  
            print(f'[CRIADO] {novo_processo}')
        else:
            print(f'[FALHA] Falta de memória para criar o processo PID: {novo_processo.pid}')
    
    def executar_processos(self, ciclos_maximos=10, chance_novo_processo=0.1):
        ciclo = 0
        while self.fila_prontos and ciclo < ciclos_maximos:
            ciclo += 1
            print(f'--- Ciclo {ciclo} ---')
            
            processo_atual = self.fila_prontos.pop(0)
            processo_atual.estado = 'Executando'
            print(f'[EXECUTANDO] {processo_atual}')
            
           
            processo_atual.tempo_execucao -= 1
            time.sleep(1)  
            
            if processo_atual.tempo_execucao == 0:
                processo_atual.estado = 'Finalizado'
                if not self.vazamento_memoria:
                    self.memoria_ram.liberar_memoria(processo_atual)
                print(f'[FINALIZADO] {processo_atual}')
            else:
                processo_atual.estado = 'Pronto'
                self.fila_prontos.append(processo_atual)
                self.fila_prontos.sort(key=lambda p: p.prioridade)
            
            
            if random.random() < chance_novo_processo:
                tempo_exec = random.randint(1, 5)
                prioridade = random.randint(1, 3)
                memoria = random.randint(10, 50)
                self.criar_processo(tempo_execucao=tempo_exec, prioridade=prioridade, memoria_necessaria=memoria)
                
           
            self.exibir_estado_memoria()
            self.exibir_processos()
    
    def exibir_estado_memoria(self):
        print(f'Memória Disponível: {self.memoria_ram.memoria_disponivel} / {self.memoria_ram.tamanho_total}')
    
    def exibir_processos(self):
        for processo in self.processos:
            print(processo)


def cenario_1():
    ram = MemoriaRAM(100)  
    gerenciador = GerenciadorProcessos(ram)
    
    for _ in range(10):  
        gerenciador.criar_processo(tempo_execucao=random.randint(1, 5), prioridade=random.randint(1, 3), memoria_necessaria=random.randint(10, 50))
    
    gerenciador.executar_processos(ciclos_maximos=10)


def cenario_2():
    ram = MemoriaRAM(100)  
    gerenciador = GerenciadorProcessos(ram)
    
    for _ in range(5):
        gerenciador.criar_processo(tempo_execucao=random.randint(1, 5), prioridade=random.randint(1, 3), memoria_necessaria=random.randint(10, 50))
    
    gerenciador.executar_processos(ciclos_maximos=10, chance_novo_processo=0.2)

def cenario_3():
    ram = MemoriaRAM(100)  
    gerenciador = GerenciadorProcessos(ram, vazamento_memoria=True)  

    for _ in range(5):
        gerenciador.criar_processo(tempo_execucao=random.randint(1, 5), prioridade=random.randint(1, 3), memoria_necessaria=random.randint(10, 50))
    
    gerenciador.executar_processos(ciclos_maximos=10)


def selecionar_cenario():
    print("Selecione um cenário para executar:")
    print("1 - Cenário 1: Grande número de processos (Falta de Memória)")
    print("2 - Cenário 2: Criação Aleatória de Processos")
    print("3 - Cenário 3: Simulação de Vazamento de Memória")
    
    escolha = int(input("Digite o número do cenário: "))
    
    if escolha == 1:
        cenario_1()
    elif escolha == 2:
        cenario_2()
    elif escolha == 3:
        cenario_3()
    else:
        print("Escolha inválida!")

selecionar_cenario()
