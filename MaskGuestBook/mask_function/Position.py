from MaskGuestBook.models import GuestBookModel


class position:
    def __init__(self):
        self.first_data = GuestBookModel.objects.first()
        self.position = self.first_data.id

    def up(self):
        self.position += 2

    def down(self):
        self.position -= 2

    def get_position(self):
        return self.position

    def next_page(self):
        if self.first_data.id >= self.position:
            return False
        else:
            return True

    def prev_page(self):
        last_data = GuestBookModel.objects.last()
        print(last_data.id)
        if last_data.id - self.position <= 1:
            return False
        else:
            return True
