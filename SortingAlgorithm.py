# -*- coding: utf-8 -*-
""" Almost working fine GUI
Created on Thu Nov 16 23:11:25 2023

@author: Prerna Joshi
GUI Modifing COde- still modifications are needed.
"""
import tkinter as tk
from tkinter import ttk, messagebox
import random
import timeit
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib import cm
from matplotlib.colors import Normalize

class SortingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Sorting Algorithms & their Runtime Complexity")

        self.create_widgets()

    def create_widgets(self):
        # Option Selection
        self.option_label = ttk.Label(self.root, text="Select Input Option:")
        self.option_label.grid(row=0, column=0, pady=10, padx=10, sticky=tk.W)

        self.option_var = tk.StringVar(value="Manual Input")
        self.option_manual = ttk.Radiobutton(self.root, text="Manual Input", variable=self.option_var, value="Manual Input", command=self.show_input_widgets)
        self.option_manual.grid(row=0, column=1, pady=10, padx=10, sticky=tk.W)

        self.option_random = ttk.Radiobutton(self.root, text="Randomly Generate", variable=self.option_var, value="Randomly Generate", command=self.show_input_widgets)
        self.option_random.grid(row=0, column=2, pady=10, padx=10, sticky=tk.W)
        
        # Algorithm Runtime Check Radio Button
        self.option_algo_runtime = ttk.Radiobutton(self.root, text="Graphical Comparison", variable=self.option_var, value="Graphical Comparison", command=self.show_input_widgets)
        self.option_algo_runtime.grid(row=0, column=3, pady=10, padx=10, sticky=tk.W)
        
        # Input Widgets
        self.size_label = ttk.Label(self.root, text="Enter Size of Array:")
        self.size_label.grid(row=1, column=0, pady=10, padx=10, sticky=tk.W)

        self.size_entry = ttk.Entry(self.root)
        self.size_entry.grid(row=1, column=1, pady=10, padx=10)

        self.array_label = ttk.Label(self.root, text="Enter Array Elements (comma-separated):")
        self.array_label.grid(row=2, column=0, pady=10, padx=10, sticky=tk.W)

        self.array_entry = ttk.Entry(self.root)
        self.array_entry.grid(row=2, column=1, pady=10, padx=10)

        # Sorting Algorithm Checkboxes
        self.algo_label = ttk.Label(self.root, text="Select Sorting Algorithms:")
        self.algo_label.grid(row=3, column=0, pady=10, padx=10, sticky=tk.W)

        self.algo_vars = {
            "Insertion Sort": tk.BooleanVar(),
            "Selection Sort": tk.BooleanVar(),
            "Bubble Sort": tk.BooleanVar(),
            "Merge Sort": tk.BooleanVar(),
            "Heap Sort": tk.BooleanVar(),
            "Regular Quick Sort": tk.BooleanVar(),
            "3-Way Quick Sort": tk.BooleanVar(),
        }

        row_counter = 4
        for algo, var in self.algo_vars.items():
            checkbox = ttk.Checkbutton(self.root, text=algo, variable=var)
            checkbox.grid(row=row_counter, column=0, columnspan=2, pady=5, padx=10, sticky=tk.W)
            row_counter += 1

        # Run Button
        self.run_button = ttk.Button(self.root, text="Run Comparison", command=self.run_comparison)
        self.run_button.grid(row=row_counter, column=0, columnspan=2, pady=10)

        # Display Sorted Array Button
        self.display_sorted_button = ttk.Button(self.root, text="Display Sorted Array", command=self.display_sorted_array)
        self.display_sorted_button.grid(row=row_counter, column=1, columnspan=2, pady=10)

        # Display Input Array Button
        self.display_input_button = ttk.Button(self.root, text="Display Input Array", command=self.display_input_array)
        self.display_input_button.grid(row=row_counter, column=2, columnspan=2, pady=10)

        # Result Label
        self.result_label = ttk.Label(self.root, text="")
        self.result_label.grid(row=row_counter+7, column=0, columnspan=2, pady=10)
        
        # Clear Button
        #self.clear_button = ttk.Button(self.root, text="Clear", command=self.clear_results)
        #self.clear_button.grid(row=row_counter + 5, column=0, columnspan=2, pady=10)
        
        # initialized the Figure, Axes, and Canvas for the Matplotlib plot
        self.fig, self.ax = plt.subplots(figsize=(8, 4))
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.root)
        self.canvas.get_tk_widget().grid(row=1, column=4, rowspan=20, padx=10, pady=10)


        # Initially hide input widgets
        self.show_input_widgets()
        
        # Initially hide Matplotlib elements
        self.canvas.get_tk_widget().grid_remove()
        
    #def clear_results(self):
        # Clear the text in the result_label
        #self.result_label.config(text="")

    def show_input_widgets(self):
        # Clear the text in the result_label
        self.result_label.config(text="")
        
        # Uncheck all sorting algorithm checkboxes
        for var in self.algo_vars.values():
            var.set(False)
        
        # Hide Matplotlib elements by default
        self.canvas.get_tk_widget().grid_remove()
        
        # Show or hide input widgets based on the selected option
        if self.option_var.get() == "Manual Input":
            self.size_label.grid()
            self.size_entry.grid()
            self.array_label.grid()
            self.array_entry.grid()
            self.display_input_button.grid()  # Display the input button
            self.display_sorted_button.grid()  # Display the sorted button
        elif self.option_var.get() == "Randomly Generate":
            self.size_label.grid()
            self.size_entry.grid()
            self.array_label.grid_remove()
            self.array_entry.grid_remove()
            self.display_input_button.grid_remove()  # Hide the input button
            self.display_sorted_button.grid()  # UnHide the sorted button
        elif self.option_var.get() == "Graphical Comparison":
            self.size_label.grid()
            self.size_entry.grid()
            self.array_label.grid_remove()
            self.array_entry.grid_remove()
            self.display_input_button.grid_remove()   #Hide the input button
            self.display_sorted_button.grid_remove()  #Hide the sorted button
            # Display Matplotlib elements
            self.canvas.get_tk_widget().grid(row=1, column=3, rowspan=15, padx=10, pady=20)

    def bubble_sort(self, arr):
        n = len(arr)
        for i in range(n - 1):
            for j in range(0, n - i - 1):
                if arr[j] > arr[j + 1]:
                    arr[j], arr[j + 1] = arr[j + 1], arr[j]

    def selection_sort(self, arr):
        n = len(arr)
        for i in range(n):
            min_index = i
            for j in range(i + 1, n):
                if arr[j] < arr[min_index]:
                    min_index = j
                    arr[i], arr[min_index] = arr[min_index], arr[i]

    def insertion_sort(self, arr):
        n = len(arr)
        for i in range(1, n):
            key = arr[i]
            j = i - 1
            while j >= 0 and arr[j] > key:
                arr[j + 1] = arr[j]
                j -= 1
            arr[j + 1] = key
    
    def merge_sort(self, arr):
        if len(arr) > 1:
            mid = len(arr) // 2
            left_half = arr[:mid]
            right_half = arr[mid:]

            self.mergesort(left_half)
            self.mergesort(right_half)

            i = j = k = 0

            while i < len(left_half) and j < len(right_half):
                if left_half[i] < right_half[j]:
                    arr[k] = left_half[i]
                    i += 1
                else:
                    arr[k] = right_half[j]
                    j += 1
                k += 1

            while i < len(left_half):
                arr[k] = left_half[i]
                i += 1
                k += 1

            while j < len(right_half):
                arr[k] = right_half[j]
                j += 1
                k += 1    
     
    def regularquick_sort(self, arr):
        low = 0 
        high = len(arr) - 1
        self.quicksort(arr, low, high)

    def quicksort(self, arr, low, high):
        if low < high:
            p = self.partition(arr, low, high)
            self.quicksort(arr, low, p - 1)
            self.quicksort(arr, p + 1, high)

    def partition(self, arr, low, high):
        pivot = arr[low]
        i = low + 1
        j = high

        while True:
            while i <= j and arr[i] <= pivot:
                i += 1
            while i <= j and arr[j] >= pivot:
                j -= 1
            if i <= j:
                arr[i], arr[j] = arr[j], arr[i]
            else:
                break

        arr[low], arr[j] = arr[j], arr[low]
        return j  
    
    def heapify(self, arr, n, i):
        largest = i
        left_child = 2 * i + 1
        right_child = 2 * i + 2

        if left_child < n and arr[i] < arr[left_child]:
            largest = left_child

        if right_child < n and arr[largest] < arr[right_child]:
            largest = right_child

        if largest != i:
            arr[i], arr[largest] = arr[largest], arr[i]
            self.heapify(arr, n, largest)

    def heap_sort(self, arr):
        n = len(arr)

        for i in range(n // 2 - 1, -1, -1):
            self.heapify(arr, n, i)

        for i in range(n - 1, 0, -1):
            arr[i], arr[0] = arr[0], arr[i]
            self.heapify(arr, i, 0)

    def quick3way_sort(self, arr):
        first = 0
        last = len(arr) - 1
        self.quick3sort(arr, first, last)

    def partition_3quick(self, arr, first, last, start, mid):
        pivot = arr[last]
        end = last
        # Iterate while mid is not greater than end.
        while (mid[0] <= end):
         
            # Inter Change position of element at the starting if it's value is less than pivot.
            if (arr[mid[0]] < pivot):
                arr[mid[0]], arr[start[0]] = arr[start[0]], arr[mid[0]]
                mid[0] = mid[0] + 1
                start[0] = start[0] + 1
             # Inter Change position of element at the end if it's value is greater than pivot.
            elif (arr[mid[0]] > pivot):
                arr[mid[0]], arr[end] = arr[end], arr[mid[0]]
                end = end - 1
            else:
                mid[0] = mid[0] + 1        

    def quick3sort(self, arr, first, last):
        if first >= last:
            return
        if last == first + 1:
            if arr[first] > arr[last]:
                arr[first], arr[last] = arr[last], arr[first]
                return
        start = [first]
        mid = [first]
        self.partition_3quick(arr, first, last, start, mid)
        self.quick3sort(arr, first, start[0] - 1)
        self.quick3sort(arr, mid[0], last)
    
    def run_comparison(self):
        
        algorithm_list = [algo for algo, var in self.algo_vars.items() if var.get()]
        if not algorithm_list:
            messagebox.showwarning("Warning", "Please select at least one sorting algorithm.")
            return

        try:
            size = int(self.size_entry.get())
             # Check if the size is less than 1
            if size < 1:
                messagebox.showerror("Error", "Array size must be at least 1.")
                return
            
        except ValueError:
            messagebox.showerror("Error", "Invalid size. Please enter a valid integer.")
            return

        if self.option_var.get() == "Manual Input":
            try:
                input_array = [int(x) for x in self.array_entry.get().split(",")]
            except ValueError:
                messagebox.showerror("Error", "Invalid array elements. Please enter valid integers.")
                return
        else:  # Randomly Generate
            input_array = [random.randint(1, 100000) for _ in range(size)]


        # Measure runtime for each selected sorting algorithm
        runtimes = []
        #result_text = ""
        for algorithm in algorithm_list:
            data = input_array.copy()
            start_time = timeit.default_timer()

            if algorithm == "Bubble Sort":
                self.bubble_sort(data)
            elif algorithm == 'Mergesort':
                self.merge_sort(data)
            elif algorithm == 'Heapsort':
                self.heap_sort(data)
            elif algorithm == 'Insertion Sort':
                self.insertion_sort(data)
            elif algorithm == 'Selection Sort':
                self.selection_sort(data)
            elif algorithm == 'Regular Quick Sort':
                self.regularquick_sort(data)
            elif algorithm == '3-Way Quick Sort':
                self.quick3way_sort(data)

            end_time = timeit.default_timer()
            runtimes.append(end_time - start_time)
        result_text = "\n".join([f"Runtime of {algorithm} : {runtime} seconds \n" for algorithm, runtime in zip(algorithm_list, runtimes)])
        #result_text = "\n".join([f"{algorithm}: {runtime:.9f} nanoseconds" for algorithm, runtime in zip(selected_algorithms, runtimes)])
        self.result_label.config(text=result_text)
         
        # Create a color map based on the number of selected algorithms
        color_map = cm.get_cmap('viridis', len(algorithm_list))
        norm = Normalize(vmin=0, vmax=len(algorithm_list))

        # Display the sorting results in a bar graph with different colors
        self.ax.clear()
        bars = self.ax.bar(algorithm_list, runtimes, color=color_map(norm(range(len(algorithm_list)))))
        self.ax.set_ylabel("Runtime (seconds)")
        self.ax.set_title("Sorting Algorithm Runtimes")
        self.ax.tick_params(axis='x', rotation=10, labelsize=10)

        # Add a manual colorbar for reference
        #color_bar = plt.colorbar(plt.cm.ScalarMappable(norm=norm, cmap=color_map), ax=self.ax, orientation='vertical', pad=0.05)
        #color_bar.set_label('Algorithm Index')

        self.canvas.draw()
            
    def display_sorted_array(self):
        algorithm_list = [algo for algo, var in self.algo_vars.items() if var.get()]
        if not algorithm_list:
            messagebox.showwarning("Warning", "Please select at least one sorting algorithm.")
            return

        try:
            size = int(self.size_entry.get())
        except ValueError:
            messagebox.showerror("Error", "Invalid size. Please enter a valid integer.")
            return

        if self.option_var.get() == "Manual Input":
            try:
                input_array = [int(x) for x in self.array_entry.get().split(",")]
            except ValueError:
                messagebox.showerror("Error", "Invalid array elements. Please enter valid integers.")
                return
        else:  # Randomly Generate
            input_array = [random.randint(1, 1000000) for _ in range(size)]

        sorted_array = input_array.copy()
        self.bubble_sort(sorted_array)

        # Display the sorted array
        messagebox.showinfo("Sorted Array", f"Sorted Array: {sorted_array}")

    def display_input_array(self):
        if self.option_var.get() == "Manual Input":
            try:
                input_array = [int(x) for x in self.array_entry.get().split(",")]
                messagebox.showinfo("Input Array", f"Input Array: {input_array}")
            except ValueError:
                messagebox.showerror("Error", "Invalid array elements. Please enter valid integers.")
        else:  # Randomly Generate
            try:
                size = int(self.size_entry.get())
                input_array = [random.randint(1, 100000) for _ in range(size)]
                messagebox.showinfo("Input Array", f"Input Array: {input_array}")
            except ValueError:
                messagebox.showerror("Error", "Invalid size. Please enter a valid integer.")

if __name__ == "__main__":
    root = tk.Tk()
    app = SortingApp(root)
    root.mainloop()
