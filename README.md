This project is a Python-based Image Processing Tool that allows users to apply multiple filters to an image through a simple command-line interface (CLI). It supports real-time image transformations such as grayscale conversion, color inversion, and blur filtering. The tool also includes an Undo functionality, enabling users to revert the image to any previous state.

Built using NumPy, Pillow (PIL), and custom data structures, the project demonstrates practical applications of:

Stacks (History Management)

Hash Maps (Filter Registry)

Image Processing Algorithms

Convolution Kernels (for blur effect)

⭐ Key Features
 1. Grayscale Filter

Converts the image to grayscale using weighted averages of RGB channels.

2. Color Inversion

Inverts all pixel values (255 – value) to create a negative-image effect.

3. Blur Filter

Applies a Gaussian-like blur using a 3×3 convolution kernel.

4. Undo Functionality (Stack)

Implements a custom FilterHistory stack to revert to previously applied states.

5. Filter Registry (Hash Map)

Uses a hash map-based registry to dynamically manage and retrieve filters by name.

6. Real-time Image Display

Displays the output image after applying each filter using Pillow.

7. Modular & Extensible Design

New filters can be added easily thanks to the registry and object-oriented structure.

🧠 Technical Concepts Used
📌 Data Structures

Stack → Maintaining history for Undo

Dictionary (Hash Map) → Storing filter functions

Numpy arrays → Representing and manipulating image pixel data

📌 Algorithms

Convolution operation for blur

Linear transformation for grayscale

Pixel-wise inversion

📌 Libraries

NumPy → Efficient matrix operations

Pillow (PIL) → Image input/output

Collections → (optional deque, shown in imports)

🏗️ Project Flow

User loads an image from local storage.

Program asks for a filter choice.

The corresponding filter is applied:

Image array is transformed

Current state is pushed into history stack

Image is displayed

User can undo previous modifications

User exits when done

📁 Use Cases

Basic image editing

Data structure demonstration (stack + hash map)

Digital image processing learning

Python OOP + NumPy practice
