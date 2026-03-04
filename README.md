# Aplicaci-n-de-Traductor-de-imagenes
Este programa es una herramienta de escritorio diseñada para la extracción, traducción y limpieza de texto en imágenes (especialmente cómics y mangas), con soporte para procesamiento automático y corrección manual.

1. Interfaz Principal (GUI)
   
La interfaz está construida sobre Tkinter y actúa como el centro de control.

Carga de Imagen: Permite importar archivos locales. Al cargar una imagen, el sistema limpia la memoria de traducción y el historial para evitar conflictos entre archivos.

Visualización Dinámica (Canvas): Muestra la imagen ajustada al tamaño de la ventana. Utiliza un sistema de coordenadas escalado para que los clics en pantalla coincidan exactamente con los píxeles de la imagen original.

Logs de Estado: Una consola inferior informa en tiempo real sobre el proceso (ej: "Procesando...", "Traducción finalizada").

2. Modos de Procesamiento
   
  A. Proceso Automático (Auto Run)
  Escanea la imagen completa utilizando el motor de OCR.
  
  Detección por Párrafos: Agrupa líneas de texto cercanas para mantener la coherencia de las frases.
  
  Filtrado de Contraste: Ignora áreas que no contienen texto (como texturas del dibujo) analizando la desviación estándar de los colores.
  
  Traducción en Bloque: Envía el texto detectado a la API de traducción y lo pega automáticamente sobre los globos de diálogo.

  B. Proceso Manual (Selección por Recuadro)
  Permite al usuario seleccionar un área específica arrastrando el ratón.
  
  Precisión Quirúrgica: Ideal para textos que el modo automático ignora o para áreas con mucho ruido visual.
  
  Ventana de Edición (Pop-up): Tras soltar el ratón, se abre una ventana que permite:
  
  Corregir errores de lectura del OCR (ej: cambiar _ por ...).
  
  Modificar la traducción sugerida antes de pegarla permanentemente.
  
  Confirmar el pegado en la imagen original.

3. Lógica de Mejora Visual (Logic B/N)
   
Un módulo especializado en pre-procesar la imagen antes de que el OCR la lea, vital para cómics en blanco y negro.

Umbral Adaptativo (Otsu): Analiza la iluminación local para separar las letras del fondo, incluso si hay sombras.

Filtro de Contornos: Elimina elementos que no son letras basándose en su forma (proporción entre ancho y alto). Por ejemplo, ignora las líneas verticales largas de una estantería de libros.

Limpieza de Ruido: Aplica desenfoque gaussiano y operaciones morfológicas para "engrosar" letras desgastadas y borrar motas de polvo digitales.

4. Motor de Traducción y Dibujo (TranslatorLogic)
   
Traducción Inteligente: Utiliza DeepL o Google Translate (vía deep_translator). Incluye una lógica que protege los signos de puntuación y puntos suspensivos para que no se pierdan en el proceso.

Incrustación de Texto: Calcula automáticamente el tamaño de la fuente para que el texto traducido encaje dentro del cuadro seleccionado.

Limpieza de Caracteres: Reemplaza secuencias de guiones bajos (____) por puntos suspensivos (...), corrigiendo un error común de los motores de OCR.

5. Gestión de Datos y Edición
   
Sistema de Historial (Deshacer/Undo)
Copia de Seguridad: Antes de cada pegado (manual o automático), el programa guarda una copia de la imagen en una "pila" de historial.

Reversión: El botón deshacer recupera el estado anterior píxel por píxel, permitiendo eliminar traducciones erróneas sin perder el progreso anterior.

Exportación de Texto (Exporter)
Genera un archivo .txt con todo lo trabajado en la sesión.

Formato Bilingüe: Guarda el texto original detectado y la traducción final lado a lado.

Persistencia: Incluye tanto las traducciones automáticas como las correcciones manuales hechas en la ventana de edición.

Sincronización: Si deshaces una acción en la imagen, el sistema también la elimina de la lista de exportación.

6. Requisitos Técnicos
   
OCR: EasyOCR (requiere modelos de lenguaje descargados).

Procesamiento de Imagen: OpenCV (cv2) y Pillow (PIL).

Traducción: API de Google/DeepL mediante conexión a internet.

7. Librerías y Dependencias Requeridas
   
Para ejecutar este proyecto, debes contar con las siguientes librerías instaladas en tu entorno de Python:

  A. Procesamiento de Imágenes y Visión Artificial
  opencv-python (cv2): Fundamental para la manipulación de imágenes en tiempo real, filtros de blanco y negro, detección de contornos y dibujo de geometrías.
  
  Pillow (PIL): Se encarga de la apertura de archivos de imagen, la conversión de formatos y el renderizado de texto con tipografías específicas sobre los globos de diálogo.
  
  numpy: Utilizada por OpenCV para manejar las imágenes como matrices numéricas de alta velocidad.
  
  B. Inteligencia Artificial y OCR
  easyocr: El motor de Reconocimiento Óptico de Caracteres. Es el encargado de "leer" las letras dentro del dibujo. Requiere la descarga automática de modelos (generalmente inglés y español) la primera vez que se usa.
  
  torch (PyTorch): Es la base sobre la que corre EasyOCR. Si tienes una tarjeta gráfica NVIDIA, se recomienda la versión con soporte CUDA para que el escaneo sea mucho más rápido.
  
  C. Traducción y Conectividad
  deep-translator: Una librería flexible que conecta el programa con servicios de traducción como Google Translate o DeepL sin necesidad de configurar claves API complejas.
  
  D. Interfaz y Sistema
  tkinter: (Viene incluida por defecto en la mayoría de instalaciones de Python). Proporciona las ventanas, botones y el canvas de dibujo.
  
  re (Regular Expressions): Librería nativa de Python utilizada para la limpieza de texto (corregir guiones bajos por puntos suspensivos).
  
  threading: Librería nativa que permite que el OCR trabaje en segundo plano para que la ventana del programa no se congele mientras procesa.

Puedes instalar todas las dependencias externas ejecutando el siguiente comando en tu terminal o consola (CMD):

pip install opencv-python pillow numpy easyocr deep-translator
