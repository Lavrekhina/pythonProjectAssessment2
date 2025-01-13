import tkinter as tk
from tkinter import messagebox
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('TkAgg') # to see the animation on iOS
from data_processor_my import DataProcessor
from matplotlib.animation import FuncAnimation

# Class for data visualisation
class Visualizer:
    @staticmethod
    def pie_chart(data, title):
        labels = data.keys()
        sizes = [float(value) for value in data.values()]
        plt.figure(figsize=(8, 6))
        plt.pie(sizes, labels=labels, autopct='%1.1f%%')
        plt.title(title)
        plt.show()

    @staticmethod
    def histogram(data, title):
        # Create a figure and axes for the plot
        fig, ax = plt.subplots(figsize=(10, 6))

        # Set the plot title
        ax.set_title(title)
        # Label the X-axis
        ax.set_xlabel('Transaction Value')
        # Label the Y-axis
        ax.set_ylabel('Frequency')

        # Create a histogram and get the bar heights
        n, bins, patches = ax.hist(data, bins=30, edgecolor='black', alpha=0.7)
        # Initialize bar heights to zero
        heights = [0] * len(n)  # heights will store current heights of bars

        # Define an update function for animation
        def update(frame):
            # Clear the previous histogram
            ax.clear()
            # Set plot title, labels, and adjust limits
            ax.set_title(title)
            ax.set_xlabel('Transaction Value')
            ax.set_ylabel('Frequency')

            # Gradually increase bar heights
            for i in range(len(heights)):
                # Increase height only if current height is less than target
                if heights[i] < n[i]:
                    heights[i] += n[i] / 30  # Gradually increasing the height
                    # Make sure we don't exceed the target height
                    if heights[i] > n[i]:
                        heights[i] = n[i]

            # Redraw the histogram with updated heights
            ax.bar(bins[:-1], heights, width=[bins[i + 1] - bins[i] for i in range(len(bins) - 1)],
                   edgecolor='black', alpha=0.7)

            # Set limits on the X axis
            ax.set_xlim(min(data), max(data))
            # Set limits on the Y axis
            ax.set_ylim(0, max(n) + 1)  # Increase the upper limit by a certain amount for better display

        # Increase the number of frames for smoother animation
        ani = FuncAnimation(fig, update, frames=30, interval= 200, repeat=False)
        plt.show()  # Displaying the graph

    @staticmethod
    def interactive_dashboard(processor):
        window = tk.Tk()
        create_window(window)
        add_components(window, processor)
        window.mainloop()


# Creating the main window for the interactive dashboard
def create_window(window):
    window.geometry("300x300")
    window.title("Interactive Dashboard")
    window.config(bg="#ddf", padx=10, pady=10)
    return window


# Adding components (buttons)
def add_components(window, processor):
    add_button_pie_chart(window, processor)
    add_button_hist(window, processor)
    add_button_rural(window, processor)
    add_button_suburban(window, processor)
    add_button_city_centre(window, processor)


# Adding button for the pie chart
def add_button_pie_chart(window, processor):
    pie_button = tk.Button(window, text="Pie Chart Three Shops Income %", bg="#ddf", font=("Arial", 12), width=30, height=2)
    pie_button.grid(row=0, column=0, columnspan=2, sticky="EW", pady=(0, 10))

    # Configuring button to an event handler
    pie_button.config(command=lambda: pie_button_clicked(processor))


def pie_button_clicked(processor):
    location_revenue = processor.group_by_location()
    Visualizer.pie_chart(location_revenue, "Revenue Contribution by Store Location")


# Adding button for the histogram
def add_button_hist(window, processor):
    hist_button = tk.Button(window, text="Histogram", bg="#ddf", font=("Arial", 12), width=30, height=2)
    hist_button.grid(row=1, column=0, columnspan=2, sticky="EW", pady=(0, 10))

    # Configuring button to an event handler
    hist_button.config(command=lambda: hist_button_clicked(processor))


def hist_button_clicked(processor):
    transaction_values = [float(transaction['TotalPrice'].replace(',', '.')) for transaction in processor.data if 'TotalPrice' in transaction]
    Visualizer.histogram(transaction_values, "Animated Histogram of Total Transaction Values")


# Adding button for the sales summary for Rural area
def add_button_rural(window, processor):
    rural_button = tk.Button(window, text="Sales Summary Rural Location", bg="#ddf", font=("Arial", 12), width=30, height=2)
    rural_button.grid(row=2, column=0, columnspan=2, sticky="EW", pady=(0, 10))

    # Configuring button to an event handler
    rural_button.config(command=lambda: rural_button_clicked(processor))


def rural_button_clicked(processor):
    summary = processor.sales_summary("Rural")
    messagebox.showinfo("Sales Summary", summary)


# Adding button for the sales summary for Suburban area
def add_button_suburban(window, processor):
    suburban_button = tk.Button(window, text="Sales Summary Suburban Location", bg="#ddf", font=("Arial", 12), width=30, height=2)
    suburban_button.grid(row=3, column=0, columnspan=2, sticky="EW", pady=(0, 10))

    # Configuring button to an event handler
    suburban_button.config(command=lambda: suburban_button_clicked(processor))


def suburban_button_clicked(processor):
    summary = processor.sales_summary("Suburban")
    messagebox.showinfo("Sales Summary", summary)


# Adding button for the sales summary for City Centre area
def add_button_city_centre(window, processor):
    city_centre_button = tk.Button(window, text="Sales Summary City Centre Location", bg="#ddf", font=("Arial", 12), width=30, height=2)
    city_centre_button.grid(row=4, column=0, columnspan=2, sticky="EW", pady=(0, 10))

    # Configuring button to an event handler
    city_centre_button.config(command=lambda: city_centre_button_clicked(processor))


def city_centre_button_clicked(processor):
    summary = processor.sales_summary("City Centre")
    messagebox.showinfo("Sales Summary", summary)


def run():
    processor = DataProcessor("retail_sales_data.csv")  # Initialize DataProcessor
    Visualizer.interactive_dashboard(processor)


if __name__ == "__main__":
    run()