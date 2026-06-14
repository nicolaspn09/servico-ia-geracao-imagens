import cv2
import glob

# Carregar as imagens geradas
img_files = sorted(glob.glob(r"C:/Users/nicol/OneDrive/Cursos online/Youtube/Segredos e Sombras/4. Ilha de Sentinel/Imagens/Convertida/*.jpg"))

# Definir codec e criar o objeto VideoWriter
video = cv2.VideoWriter(r"C:\Users\nicol\OneDrive\Cursos online\Youtube\Segredos e Sombras\4. Ilha de Sentinel\Imagens\Convertida\video.mp4", cv2.VideoWriter_fourcc(*'mp4v'), 24, (1920, 1080))

# Definir o tempo em segundos para cada imagem (5 segundos)
display_time = 5  # Tempo em segundos
fps = 24  # Frames por segundo
frames_per_image = display_time * fps  # Número de quadros para cada imagem

for img_file in img_files:
    img = cv2.imread(img_file)
    if img is not None:
        # Redimensionar a imagem para garantir que ela se ajuste à resolução 1920x1080
        img_resized = cv2.resize(img, (1920, 1080))

        # Adicionar a imagem ao vídeo por 'frames_per_image' quadros
        for _ in range(frames_per_image):
            video.write(img_resized)  # Adiciona a imagem ao vídeo

    else:
        print(f"Erro ao carregar {img_file}")

# Finalizar o vídeo
video.release()
print("Vídeo criado com sucesso!")