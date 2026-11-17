from datetime import datetime


def validar_cadastro(setor: str, material: str, quantidade_str: str, prioridade: str) -> tuple[bool, str]:
    if not setor.strip() or not material.strip() or not prioridade.strip():
        return False, "Todos os campos devem ser preenchidos."
    try:
        qtd = int(quantidade_str)
        if qtd <= 0:
            return False, "A quantidade deve ser um número inteiro maior que zero."
    except ValueError:
        return False, "A quantidade deve ser um número inteiro válido."
    return True, "OK"

def obter_proximo_status(status_atual: str) -> str | None:
    fluxo = {
        "Pendente": "Em atendimento",
        "Em atendimento": "Atendida"
    }
    return fluxo.get(status_atual, None)

def obter_data_hora_atual() -> str:
    return datetime.now().strftime("%d/%m/%Y %H:%M:%S")