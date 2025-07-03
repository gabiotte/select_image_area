import cv2
import os
import csv
import argparse

extensoes_validas = (".jpg", ".jpeg", ".png", ".bmp", ".tif", ".tiff")

def selecionar_area(imagem, imagem_path):
    altura_max = 1000
    if imagem.shape[0] > altura_max:
        escala = altura_max / imagem.shape[0]
        imagem = cv2.resize(imagem, (int(imagem.shape[1] * escala), altura_max))

    while True:
        print(f"\n🔍 Selecionando área em: {imagem_path}")
        roi = cv2.selectROI("Selecionar Área", cv2.cvtColor(imagem, cv2.COLOR_BGR2GRAY), fromCenter=False, showCrosshair=True)
        cv2.destroyAllWindows()

        x, y, w, h = roi
        if w == 0 or h == 0:
            print("⚠️ Seleção cancelada.")
            return None

        print(f"📐 Tamanho selecionado: {w} x {h} = {w*h} pixels")
        print("Pressione 'R' para refazer, 'C' para confirmar ou 'A' para aplicar a todos.")

        while True:
            tecla = input("Digite sua escolha (R/C/A): ").strip().upper()
            if tecla == "R":
                break  # repete seleção
            elif tecla in ("C", "A"):
                aplicar_todos = (tecla == "A")
                return x, y, w, h, aplicar_todos
            else:
                print("Entrada inválida. Digite 'R', 'C' ou 'A'.")

def processar_imagens_em(dir):

    imagens = [f for f in os.listdir(dir) if f.lower().endswith(extensoes_validas)]
    imagens.sort()

    if not imagens:
        return False

    caminho_saida = os.path.join(dir, "selecoes.csv")
    with open(caminho_saida, mode="w", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Imagem", "x", "y", "w", "h"])

        coordenadas_fixas = None
        aplicar_para_todas = False

        for i, nome_arquivo in enumerate(imagens):
            caminho_completo = os.path.join(dir, nome_arquivo)
            imagem = cv2.imread(caminho_completo)

            if imagem is None:
                print(f"Erro ao carregar {caminho_completo}. Pulando.")
                continue

            if coordenadas_fixas and aplicar_para_todas:
                x, y, w, h = coordenadas_fixas
            else:
                resultado = selecionar_area(imagem, nome_arquivo)
                if resultado is None:
                    continue
                x, y, w, h, aplicar_para_todas = resultado
                if aplicar_para_todas:
                    coordenadas_fixas = (x, y, w, h)

            writer.writerow([nome_arquivo, x, y, w, h])
            print(f"✅ Coordenadas salvas para {nome_arquivo}")

    print(f"\n📝 Todas as seleções foram salvas em: {caminho_saida}")

def processar_dir(dir):
    
    # Primeiro, tenta processar o próprio diretório
    if processar_imagens_em(dir):
        return
    
    # Se não houver imagens, procura subdiretórios com imagens
    subdirs = [os.path.join(dir, d) for d in os.listdir(dir) if os.path.isdir(os.path.join(dir, d))]
    encontrou = False

    for subdir in subdirs:
        if processar_imagens_em(subdir):
            encontrou = True
    
    if not encontrou:
        print("❌ Nenhuma imagem válida encontrada no diretório ou em seus subdiretórios.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Processa um diretório contendo imagens"
    )
    parser.add_argument(
        "--diretorio", type=str, required=True,
        help="Caminho da diretório com as imagens"
    )

    args = parser.parse_args()

    if not os.path.isdir(args.diretorio):
        print("Diretório inválida ou não encontrada.")
    else:
        processar_dir(args.diretorio)
