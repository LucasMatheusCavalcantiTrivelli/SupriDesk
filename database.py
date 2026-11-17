import sqlite3

DB_NAME = "solicitacoes.db"

class Database:
    def __init__(self, db_name=DB_NAME) -> None:
        self.conn = sqlite3.connect(db_name)
        self.conn.execute(
            """CREATE TABLE IF NOT EXISTS solicitacoes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                setor TEXT NOT NULL,
                material TEXT NOT NULL,
                quantidade INTEGER NOT NULL,
                prioridade TEXT NOT NULL,
                status TEXT NOT NULL,
                data_hora TEXT NOT NULL
            )"""
        )
        self.conn.commit()

    def inserir_solicitacao(self, setor: str, material: str, quantidade: int, prioridade: str, data_hora: str) -> None:
        self.conn.execute(
            "INSERT INTO solicitacoes (setor, material, quantidade, prioridade, status, data_hora) VALUES (?, ?, ?, ?, ?, ?)",
            (setor, material, quantidade, prioridade, "Pendente", data_hora),
        )
        self.conn.commit()

    def listar_solicitacoes(self, termo_busca: str = "", filtro_status: str = "") -> list:
        query = "SELECT * FROM solicitacoes WHERE (setor LIKE ? OR material LIKE ? COLLATE NOCASE) AND status LIKE ?"
        termo = f"%{termo_busca}%"
        if not filtro_status or filtro_status.lower() == "todos":
            status_filter = "%"
        else:
            status_filter = filtro_status
        cursor = self.conn.execute(query, (termo, termo, status_filter))
        return cursor.fetchall()

    def atualizar_status(self, solicitacao_id: int, novo_status: str) -> None:
        self.conn.execute(
            "UPDATE solicitacoes SET status = ? WHERE id = ?",
            (novo_status, solicitacao_id),
        )
        self.conn.commit()

    def deletar_solicitacao(self, solicitacao_id: int) -> None:
        self.conn.execute(
            "DELETE FROM solicitacoes WHERE id = ?",
            (solicitacao_id,),
        )
        self.conn.commit()

    def fechar(self) -> None:
        self.conn.close()