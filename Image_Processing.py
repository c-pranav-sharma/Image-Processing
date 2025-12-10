import numpy as np
from PIL import Image

class NaryTreeNode:
    def __init__(self, name):
        self.name = name
        self.children = []

    def add_child(self, child_node):
        self.children.append(child_node)

class NaryTree:
    def __init__(self):
        self.root = NaryTreeNode("Filters")

    def add_filter(self, parent_name, filter_name):
        parent_node = self._find_node(self.root, parent_name)
        if parent_node:
            parent_node.add_child(NaryTreeNode(filter_name))

    def _find_node(self, node, name):
        if node.name == name:
            return node
        for child in node.children:
            found = self._find_node(child, name)
            if found:
                return found
        return None

class FilterHistory:
    def __init__(self):
        self.history = []

    def push(self, image):
        self.history.append(np.copy(image))

    def pop(self):
        if self.history:
            return self.history.pop()
        return None

class FilterRegistry:
    def __init__(self):
        self.filters = {}

    def register(self, name, func):
        self.filters[name] = func

    def get(self, name):
        return self.filters.get(name)

class ImageProcessor:
    def __init__(self, image_path):
        self.image = Image.open(image_path).convert("RGB")
        self.image_array = np.array(self.image)
        self.history = FilterHistory()
        self.registry = FilterRegistry()
        self.tree = NaryTree()
        self._register_filters()
        self._build_tree()

    def _register_filters(self):
        self.registry.register("grayscale", self.apply_grayscale)
        self.registry.register("inversion", self.apply_inversion)
        self.registry.register("blur", self.apply_blur)
        self.registry.register("crop", self.apply_crop)
        self.registry.register("rotate", self.apply_rotate)

    def _build_tree(self):
        self.tree.add_filter("Filters", "Color Filters")
        self.tree.add_filter("Color Filters", "Grayscale")
        self.tree.add_filter("Color Filters", "Inversion")
        self.tree.add_filter("Filters", "Effects")
        self.tree.add_filter("Effects", "Blur")
        self.tree.add_filter("Filters", "Transformations")
        self.tree.add_filter("Transformations", "Crop")
        self.tree.add_filter("Transformations", "Rotate")

    def apply_filter(self, kernel):
        kh, kw = kernel.shape
        ph, pw = kh // 2, kw // 2

        padded = np.pad(self.image_array, ((ph, ph), (pw, pw), (0, 0)), mode='edge')
        filtered = np.zeros_like(self.image_array)

        for i in range(self.image_array.shape[0]):
            for j in range(self.image_array.shape[1]):
                region = padded[i:i+kh, j:j+kw]
                pixel = np.sum(region * kernel[:, :, None], axis=(0, 1))
                filtered[i, j] = pixel

        self.history.push(self.image_array)
        self.image_array = filtered
        return Image.fromarray(filtered.astype('uint8'))

    def display_filters(self):
        print("\nAvailable Filters:")
        for i, child in enumerate(self.tree.root.children, start=1):
            print(f"{i}. {child.name}")
            for j, sub in enumerate(child.children, start=1):
                print(f"   {i}.{j} {sub.name}")

    def apply_inversion(self):
        result = 255 - self.image_array
        self.history.push(self.image_array)
        self.image_array = result
        return Image.fromarray(result.astype('uint8'))

    def apply_grayscale(self):
        gray = np.dot(self.image_array[..., :3], [0.2989, 0.5870, 0.1140])
        result = np.stack((gray,)*3, axis=-1)
        self.history.push(self.image_array)
        self.image_array = result
        return Image.fromarray(result.astype('uint8'))

    def apply_blur(self):
        kernel = np.ones((3, 3)) / 9
        return self.apply_filter(kernel)

    def apply_crop(self):
        left = int(input("Left: "))
        top = int(input("Top: "))
        right = int(input("Right: "))
        bottom = int(input("Bottom: "))

        if left < 0 or top < 0 or right > self.image_array.shape[1] or bottom > self.image_array.shape[0]:
            print("Invalid coordinates.")
            return Image.fromarray(self.image_array.astype('uint8'))

        if left >= right or top >= bottom:
            print("Invalid rectangle.")
            return Image.fromarray(self.image_array.astype('uint8'))

        result = self.image_array[top:bottom, left:right]
        self.history.push(self.image_array)
        self.image_array = result
        return Image.fromarray(result.astype('uint8'))

    def apply_rotate(self):
        angle = float(input("Angle: "))
        rotated = Image.fromarray(self.image_array).rotate(angle)
        self.history.push(self.image_array)
        self.image_array = np.array(rotated)
        return rotated

    def undo(self):
        prev = self.history.pop()
        if prev is not None:
            self.image_array = prev
            print("Undo successful.")
        else:
            print("Nothing to undo.")

    def show_image(self):
        Image.fromarray(self.image_array.astype('uint8')).show()

def main():
    path = input("Enter image path: ")
    processor = ImageProcessor(path)

    while True:
        processor.display_filters()
        choice = input("Choose (1.1, 1.2, 2.1, 3.1, 3.2) or Undo/Exit: ")

        if choice in ["1.1", "1.2", "2.1", "3.1", "3.2"]:
            mapping = {
                "1.1": processor.apply_grayscale,
                "1.2": processor.apply_inversion,
                "2.1": processor.apply_blur,
                "3.1": processor.apply_crop,
                "3.2": processor.apply_rotate
            }
            mapping[choice]()
            processor.show_image()

        elif choice.lower() == "undo":
            processor.undo()
            processor.show_image()

        elif choice.lower() == "exit":
            break

        else:
            print("Invalid input.")

if __name__ == "__main__":
    main()
