import numpy as np
from PIL import Image
from collections import deque

class FilterHistory:
    """A simple stack to maintain filter history for undo functionality."""
    def __init__(self):
        self.history = []

    def push(self, image):
        self.history.append(np.copy(image))  # Save a copy of the image state

    def pop(self):
        if self.history:
            return self.history.pop()
        return None

class FilterRegistry:
    """A hash map to register and retrieve filters by name."""
    def __init__(self):
        self.filters = {}

    def register(self, name, filter_function):
        self.filters[name] = filter_function

    def get_filter(self, name):
        return self.filters.get(name)

class ImageProcessor:
    def __init__(self, image_path):
        self.image = Image.open(image_path).convert('RGB')
        self.image_array = np.array(self.image)
        self.history = FilterHistory()  # Stack for history
        self.filter_registry = FilterRegistry()
        self._register_filters()

    def _register_filters(self):
        """Register available filters in the filter registry."""
        self.filter_registry.register("grayscale", self.apply_grayscale)
        self.filter_registry.register("inversion", self.apply_inversion)
        self.filter_registry.register("blur", self.apply_blur)

    def apply_grayscale(self):
        """Convert the image to grayscale."""
        gray = np.dot(self.image_array[..., :3], [0.2989, 0.5870, 0.1140])
        gray_image = np.stack((gray,) * 3, axis=-1)
        self.history.push(self.image_array)  # Save current state for undo
        self.image_array = gray_image
        return Image.fromarray(gray_image.astype('uint8'))

    def apply_inversion(self):
        """Invert the colors of the image."""
        inverted_image = 255 - self.image_array
        self.history.push(self.image_array)  # Save current state for undo
        self.image_array = inverted_image
        return Image.fromarray(inverted_image.astype('uint8'))

    def apply_blur(self):
        """Apply a simple blur filter using a kernel."""
        kernel = np.array([[1/16, 2/16, 1/16],
                           [2/16, 4/16, 2/16],
                           [1/16, 2/16, 1/16]])
        return self.apply_filter(kernel)

    def apply_filter(self, kernel):
        """Apply a convolutional filter to the image."""
        kernel_height, kernel_width = kernel.shape
        pad_height = kernel_height // 2
        pad_width = kernel_width // 2

        # Pad the image with zeros on the border
        padded_image = np.pad(self.image_array, ((pad_height, pad_height), (pad_width, pad_width), (0, 0)), mode='constant')

        filtered_image = np.zeros_like(self.image_array)

        # Convolve the kernel over the image
        for i in range(self.image_array.shape[0]):
            for j in range(self.image_array.shape[1]):
                filtered_image[i, j] = np.sum(
                    padded_image[i:i + kernel_height, j:j + kernel_width] * kernel[:, :, np.newaxis], axis=(0, 1)
                )

        self.history.push(self.image_array)  # Save current state for undo
        self.image_array = filtered_image
        return Image.fromarray(filtered_image.astype('uint8'))

    def undo(self):
        """Undo the last filter applied."""
        previous_image = self.history.pop()
        if previous_image is not None:
            self.image_array = previous_image
            print("Undo successful.")
        else:
            print("No more actions to undo.")

    def show_image(self):
        """Display the current image."""
        img = Image.fromarray(self.image_array.astype('uint8'))
        img.show()

def main():
    image_path = input("Enter the path to the image file: ")
    processor = ImageProcessor(image_path)

    while True:
        print("\nChoose a filter:")
        print("1. Grayscale")
        print("2. Inversion")
        print("3. Blur")
        print("4. Undo")
        print("5. Exit")
        choice = input("Enter your choice (1/2/3/4/5): ")

        if choice == '1':
            processed_image = processor.apply_grayscale()
            processor.show_image()
        elif choice == '2':
            processed_image = processor.apply_inversion()
            processor.show_image()
        elif choice == '3':
            processed_image = processor.apply_blur()
            processor.show_image()
        elif choice == '4':
            processor.undo()
            processor.show_image()
        elif choice == '5':
            break
        else:
            print("Invalid choice.")

if __name__ == "__main__":
    main()