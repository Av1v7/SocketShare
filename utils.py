import datetime

class Utils:
    @staticmethod
    def center_screen(root, width, height):
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()

        x = (screen_width - width) // 2
        y = (screen_height - height) // 2

        root.geometry(f'{width}x{height}+{x}+{y}')
    
    @staticmethod
    def get_current_time(display_code=3) -> str:
        if display_code == 1:
            return f'{datetime.datetime.now().strftime("%H")}'
        elif display_code == 2:
            return f'{datetime.datetime.now().strftime("%H:%M")}'
        else:
            return f'{datetime.datetime.now().strftime("%H:%M:%S")}'