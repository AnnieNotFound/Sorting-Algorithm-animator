import matplotlib.pyplot as plt
import matplotlib.animation as animation
import random
import warnings
warnings.filterwarnings("ignore")  


def bubble_sort(arr):
    n = len(arr)
    for i in range(n):3
        for j in range(0, n - i - 1):
            # Highlight the two bars being compared
            color_positions = ["blue"] * n
            color_positions[j] = "red"
            color_positions[j+1] = "red"
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
            yield arr.copy(), color_positions
    # After sorting, all bars green
    yield arr.copy(), ["green"] * n

def insertion_sort(arr):
    n = len(arr)
    for i in range(1, n):
        key = arr[i]
        j = i - 1
        while j >= 0 and arr[j] > key:
            arr[j + 1] = arr[j]
            color_positions = ["blue"] * n
            color_positions[j] = "red"
            color_positions[j+1] = "red"
            j -= 1
            yield arr.copy(), color_positions
        arr[j + 1] = key
        color_positions = ["blue"] * n
        color_positions[j+1] = "red"
        yield arr.copy(), color_positions
    yield arr.copy(), ["green"] * n

def merge_sort(arr, l=0, r=None):
    if r is None:
        r = len(arr) - 1
    if l < r:
        m = (l + r) // 2
        yield from merge_sort(arr, l, m)
        yield from merge_sort(arr, m + 1, r)
        yield from merge(arr, l, m, r)
        yield arr.copy(), ["blue"] * len(arr)
    yield arr.copy(), ["green"] * len(arr)

def merge(arr, l, m, r):
    left = arr[l:m+1]
    right = arr[m+1:r+1]
    i = j = 0
    k = l
    while i < len(left) and j < len(right):
        color_positions = ["blue"] * len(arr)
        color_positions[k] = "red"
        if left[i] <= right[j]:
            arr[k] = left[i]
            i += 1
        else:
            arr[k] = right[j]
            j += 1
        k += 1
        yield arr.copy(), color_positions
    while i < len(left):
        color_positions = ["blue"] * len(arr)
        color_positions[k] = "red"
        arr[k] = left[i]
        i += 1
        k += 1
        yield arr.copy(), color_positions
    while j < len(right):
        color_positions = ["blue"] * len(arr)
        color_positions[k] = "red"
        arr[k] = right[j]
        j += 1
        k += 1
        yield arr.copy(), color_positions

def quick_sort(arr, low=0, high=None):
    if high is None:
        high = len(arr) - 1
    if low < high:
        pi, states = partition(arr, low, high)
        for s in states:
            yield s
        yield from quick_sort(arr, low, pi - 1)
        yield from quick_sort(arr, pi + 1, high)
    yield arr.copy(), ["green"] * len(arr)

def partition(arr, low, high):
    pivot = arr[high]
    i = low - 1
    states = []
    for j in range(low, high):
        color_positions = ["blue"] * len(arr)
        color_positions[j] = "red"
        color_positions[high] = "orange"  # pivot
        if arr[j] < pivot:
            i += 1
            arr[i], arr[j] = arr[j], arr[i]
        states.append((arr.copy(), color_positions))
    arr[i+1], arr[high] = arr[high], arr[i+1]
    states.append((arr.copy(), ["green"]*len(arr)))
    return i+1, states

# ---------- Algorithm Dictionary ----------
algorithms = {
    "Bubble Sort": bubble_sort,
    "Insertion Sort": insertion_sort,
    "Merge Sort": merge_sort,
    "Quick Sort": quick_sort
}

# ---------- Animator Function ----------
def animate_algorithm(algorithm_name, data, interval):
    generator = algorithms[algorithm_name](data.copy())
    fig, ax = plt.subplots()
    ax.set_title(f"{algorithm_name} Animation")
    bars = ax.bar(range(len(data)), data, align="edge")
    step_text = ax.text(0.02, 0.95, "", transform=ax.transAxes)

    def update(frame):
        arr, colors = frame
        for bar, val, color in zip(bars, arr, colors):
            bar.set_height(val)
            bar.set_color(color)
        step_text.set_text(f"Steps: {update.step}")
        update.step += 1
    update.step = 1

    anim = animation.FuncAnimation(
        fig, func=update, frames=generator,
        interval=interval, repeat=False
    )
    plt.show()


if __name__ == "__main__":
    size = int(input("Enter number of elements to sort (e.g., 20): "))
    data = [random.randint(1, 50) for _ in range(size)]
    
    print("Choose an algorithm:")
    for i, name in enumerate(algorithms.keys(), 1):
        print(f"{i}. {name}")
    choice = int(input("Enter choice (1-4): "))
    algorithm_name = list(algorithms.keys())[choice - 1]

    speed = int(input("Enter animation speed in ms per step (e.g., 200): "))

    animate_algorithm(algorithm_name, data, interval=speed)
710