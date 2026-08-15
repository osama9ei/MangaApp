import os
import flet as ft
from PIL import Image

def main(page: ft.Page):
    page.title = "Manga Binder Pro"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.scroll = ft.ScrollMode.AUTO
    
    status_text = ft.Text("Choose directory and start processing", size=14, color=ft.colors.BLUE_400)
    
    def run_processing(e):
        try:
            status_text.value = "Processing and resizing images..."
            page.update()
            
            source_directory = '/sdcard/Download/Manga/Downloaded_Mangas'
            sized_directory = '/sdcard/Download/Manga/Sized_Mangas'
            final_directory = '/sdcard/Download/Manga/Final_Result'
            
            os.makedirs(sized_directory, exist_ok=True)
            os.makedirs(final_directory, exist_ok=True)
            
            target_width = 1240
            target_height = 1754
            gutter_padding = 120
            available_width = target_width - gutter_padding
            
            image_files = []
            for filename in os.listdir(source_directory):
                if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.webp')):
                    file_path = os.path.join(source_directory, filename)
                    image_files.append((os.path.getmtime(file_path), file_path))
            
            image_files.sort(key=lambda x: x[0])
            
            counter = 1
            for _, file_path in image_files:
                with Image.open(file_path) as img:
                    img = img.convert('RGB')
                    resized_img = img.resize((available_width, target_height), Image.Resampling.LANCZOS)
                    canvas = Image.new('RGB', (target_width, target_height), (255, 255, 255))
                    canvas.paste(resized_img, (0, 0))
                    
                    new_filename = f"{counter:03d}.jpg"
                    canvas.save(os.path.join(sized_directory, new_filename), 'JPEG', quality=95)
                    counter += 1

            status_text.value = "Converting to Grayscale and generating PDF..."
            page.update()
            
            processed_images = []
            sized_files = sorted(os.listdir(sized_directory))
            for filename in sized_files:
                if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.webp')):
                    f_path = os.path.join(sized_directory, filename)
                    if os.path.isfile(f_path):
                        with Image.open(f_path) as img:
                            gray_img = img.convert('L').convert('RGB')
                            processed_images.append(gray_img)
            
            if processed_images:
                output_pdf_path = os.path.join(final_directory, 'manga_book.pdf')
                first_image = processed_images[0]
                remaining_images = processed_images[1:]
                
                first_image.save(
                    output_pdf_path,
                    "PDF",
                    save_all=True,
                    append_images=remaining_images,
                    resolution=100.0,
                    quality=95
                )
                status_text.value = "Completed successfully! PDF ready in Final_Result"
            else:
                status_text.value = "No valid images found for processing!"
                
            page.update()
            
        except Exception as ex:
            status_text.value = f"Error: {str(ex)}"
            page.update()

    start_btn = ft.ElevatedButton(
        text="Start Manga Processing",
        icon=ft.icons.PLAY_ARROW,
        on_click=run_processing,
        color=ft.colors.WHITE,
        bgcolor=ft.colors.GREEN_700
    )

    page.add(
        ft.Column([
            ft.Text("Manga Print Preparation Tool", size=20, weight=ft.FontWeight.BOLD),
            ft.Divider(),
            ft.Text("Click the button below to process, resize, and compile PDF automatically:", size=13),
            ft.Container(height=20),
            start_btn,
            ft.Container(height=20),
            status_text
        ], alignment=ft.MainAxisAlignment.CENTER)
    )

ft.app(target=main)
