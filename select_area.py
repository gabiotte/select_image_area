import cv2
import os
import csv

def selecionar_area(imagem, imagem_path):
    altura_max = 1000
    if imagem.shape[0] > altura_max:
        escala = altura_max / imagem.shape[0]
        imagem = cv2.resize(imagem, (int(imagem.shape[1] * escala), altura_max))

    while True:
        print(f"\n🔍 Selecionando área em: {imagem_path}")
        roi = cv2.selectROI("Selecionar Área", imagem, fromCenter=False, showCrosshair=True)
        cv2.destroyAllWindows()

        x, y, w, h = roi
        if w == 0 or h == 0:
            print("⚠️ Seleção cancelada.")
            return None

        print(f"📐 Tamanho selecionado: {w} x {h} = {w*h} pixels")
        print("Pressione 'R' para refazer ou 'C' para confirmar.")

        while True:
            tecla = input("Digite sua escolha (R/C): ").strip().upper()
            if tecla == "R":
                break  # repete seleção
            elif tecla == "C":
                return x, y, w, h
            else:
                print("Entrada inválida. Digite 'R' ou 'C'.")

def processar_pasta(pasta_imagens):
    extensoes_validas = (".jpg", ".jpeg", ".png", ".bmp", ".tif", ".tiff")
    imagens = [f for f in os.listdir(pasta_imagens) if f.lower().endswith(extensoes_validas)]
    imagens.sort()

    if not imagens:
        print("Nenhuma imagem válida encontrada na pasta.")
        return

    caminho_saida = os.path.join(pasta_imagens, "selecoes.csv")
    with open(caminho_saida, mode="w", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Imagem", "x", "y", "w", "h"])

        for nome_arquivo in imagens:
            caminho_completo = os.path.join(pasta_imagens, nome_arquivo)
            imagem = cv2.imread(caminho_completo)

            if imagem is None:
                print(f"Erro ao carregar {caminho_completo}. Pulando.")
                continue

            resultado = selecionar_area(imagem, nome_arquivo)
            if resultado:
                x, y, w, h = resultado
                writer.writerow([nome_arquivo, x, y, w, h])
                print(f"✅ Coordenadas salvas para {nome_arquivo}")

    print(f"\n📝 Todas as seleções foram salvas em: {caminho_saida}")

if __name__ == "__main__":
    pasta = input("Digite o caminho da pasta com as imagens: ").strip()
    if not os.path.isdir(pasta):
        print("Pasta inválida ou não encontrada.")
    else:
        processar_pasta(pasta)
