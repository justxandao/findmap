import cv2

def encontrar_e_recortar_imagem_referencia(captura_path, referencia_path):
    imagem_captura = cv2.imread(captura_path)
    imagem_referencia = cv2.imread(referencia_path)
    
    if imagem_captura is None:
        print(f"Erro ao carregar a captura de tela: {captura_path}")
        return None
    
    if imagem_referencia is None:
        print(f"Erro ao carregar a imagem de referência: {referencia_path}")
        return None

    referencia_gray = cv2.cvtColor(imagem_referencia, cv2.COLOR_BGR2GRAY)
    w, h = referencia_gray.shape[::-1]

    resultado = cv2.matchTemplate(cv2.cvtColor(imagem_captura, cv2.COLOR_BGR2GRAY), referencia_gray, cv2.TM_CCOEFF_NORMED)

    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(resultado)

    threshold = 0.8
    if max_val >= threshold:
        top_left = max_loc
        bottom_right = (top_left[0] + w, top_left[1] + h)
        recorte = imagem_captura[top_left[1]:bottom_right[1], top_left[0]:bottom_right[0]]

        recorte_path = 'recorte.png'
        cv2.imwrite(recorte_path, recorte)
        return recorte_path
    else:
        print("A imagem de referência não foi encontrada na captura de tela.")
        return None
