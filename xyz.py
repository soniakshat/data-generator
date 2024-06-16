import pandas as pd
import matplotlib.pyplot as plt
from tkinter import Tk, Label, Button, Text, Scrollbar, END, Frame, Canvas, VERTICAL, HORIZONTAL
from tkinter.messagebox import showerror
from tkcalendar import DateEntry
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


def load_data():
    # Read CSV file into DataFrame
    try:
        df = pd.read_csv('ad_revenue.csv', parse_dates=['Date'])
        return df
    except Exception as e:
        showerror("Error", f"Failed to load data: {e}")
        return None


def filter_data(df, start_date, end_date):
    # Convert DateEntry dates to datetime
    start_date = pd.to_datetime(start_date)
    end_date = pd.to_datetime(end_date)
    # Filter the DataFrame based on the provided date range
    mask = (df['Date'] >= start_date) & (df['Date'] <= end_date)
    return df.loc[mask]


def show_results(filtered_df):
    # Clear the text box
    text_box.delete(1.0, END)
    if filtered_df.empty:
        text_box.insert(END, "No records found for the given date range.")
    else:
        text_box.insert(END, filtered_df.to_string(index=False))


def plot_graph(filtered_df):
    # Clear previous plot
    for widget in graph_frame.winfo_children():
        widget.destroy()

    if not filtered_df.empty:
        fig, ax = plt.subplots()
        ax.plot(filtered_df['Date'], filtered_df['Revenue'], marker='o')
        ax.set_title('Revenue over Time')
        ax.set_xlabel('Date')
        ax.set_ylabel('Revenue')

        canvas = FigureCanvasTkAgg(fig, master=graph_frame)
        canvas.draw()
        canvas.get_tk_widget().pack()


def on_submit():
    try:
        start_date = start_date_entry.get_date()
        end_date = end_date_entry.get_date()
        if start_date > end_date:
            showerror("Invalid Range", "Start date must be before end date.")
            return
        filtered_df = filter_data(df, start_date, end_date)
        show_results(filtered_df)
        plot_graph(filtered_df)
    except Exception as e:
        showerror("Error", f"Failed to filter data: {e}")


# Load data from CSV
df = load_data()

# Initialize tkinter window
root = Tk()
root.title("Revenue Data Filter")

# Create a canvas and a frame to hold the widgets
main_frame = Frame(root)
main_frame.pack(fill='both', expand=True)

canvas = Canvas(main_frame)
canvas.pack(side='left', fill='both', expand=True)

scrollbar_y = Scrollbar(main_frame, orient=VERTICAL, command=canvas.yview)
scrollbar_y.pack(side='right', fill='y')

scrollbar_x = Scrollbar(main_frame, orient=HORIZONTAL, command=canvas.xview)
scrollbar_x.pack(side='bottom', fill='x')

canvas.configure(yscrollcommand=scrollbar_y.set)
canvas.configure(xscrollcommand=scrollbar_x.set)

second_frame = Frame(canvas)

# Bind the canvas to the frame
second_frame.bind(
    "<Configure>",
    lambda e: canvas.configure(
        scrollregion=canvas.bbox("all")
    )
)

canvas.create_window((0, 0), window=second_frame, anchor="nw")

# Create and place widgets in the second frame
Label(second_frame, text="Start Date:").grid(row=0, column=0, padx=10, pady=10)
start_date_entry = DateEntry(second_frame, width=12, background='darkblue', foreground='white', borderwidth=2)
start_date_entry.grid(row=0, column=1, padx=10, pady=10)

Label(second_frame, text="End Date:").grid(row=1, column=0, padx=10, pady=10)
end_date_entry = DateEntry(second_frame, width=12, background='darkblue', foreground='white', borderwidth=2)
end_date_entry.grid(row=1, column=1, padx=10, pady=10)

Button(second_frame, text="Submit", command=on_submit).grid(row=2, column=0, columnspan=2, pady=20)

# Text box to display results
text_box = Text(second_frame, wrap='none', width=80, height=20)
text_box.grid(row=3, column=0, columnspan=2, padx=10, pady=10)

# Add scrollbars to the text box
x_scrollbar = Scrollbar(second_frame, orient='horizontal', command=text_box.xview)
x_scrollbar.grid(row=4, column=0, columnspan=2, sticky='ew')
text_box['xscrollcommand'] = x_scrollbar.set

y_scrollbar = Scrollbar(second_frame, orient='vertical', command=text_box.yview)
y_scrollbar.grid(row=3, column=2, sticky='ns')
text_box['yscrollcommand'] = y_scrollbar.set

# Frame for the graph
graph_frame = Frame(second_frame)
graph_frame.grid(row=5, column=0, columnspan=3, pady=10)

# Create a canvas for the graph
graph_canvas = Canvas(graph_frame)
graph_canvas.pack(fill='both', expand=True)

# Create a sub-frame for the graph to ensure it doesn't disappear when scrolling
graph_subframe = Frame(graph_canvas)
graph_canvas.create_window((0, 0), window=graph_subframe, anchor='nw')

# Bind the canvas to the graph sub-frame
graph_subframe.bind(
    "<Configure>",
    lambda e: graph_canvas.configure(
        scrollregion=graph_canvas.bbox("all")
    )
)

# Start the tkinter main loop
root.mainloop()
