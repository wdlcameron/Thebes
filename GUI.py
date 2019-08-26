
import os, sys
import numpy as np
import pandas as pd
from functools import partial
from pathlib import Path

from bokeh.plotting import figure
from bokeh.io import output_notebook, output_file, show, curdoc, export_png
from bokeh.layouts import gridplot, row, column, WidgetBox, layout
from bokeh.models import ColumnDataSource, Select, Slider, TextInput, RangeSlider, Paragraph, TextInput, Button
from bokeh.palettes import Spectral6

from utils.summary import create_summary_columns, create_cell_comparisons


sys.path.append("..")

#------------User Input: Choose the 
input_filepath = r'examples/01 - Nuc Cyto Hyper [Nuc Cyto Whole Br]-Reduced.pkl'
input_filepath = r"examples\2019-04-30 - INS1E H2O2 and Glucose (Manual Analyzed)\02 - Mito-Cyto H2O2 [Mito Cyto Whole Br]-Reduced.pkl"
#input_filepath = r"D:\William\2019-04-30 - INS1E H2O2 and Glucose (Manual Analyzed)\02 - Mito-Cyto H2O2 [Mito Cyto Whole Br]-Reduced.pkl"
input_filepath = r"examples\FCCP\Attempt 2 (50uM Etomoxir) [Mito Br]-Reduced.pkl"
input_filepath = r"examples\Monomer Dimer\03 - Dimer [Whole Whole Whole Br]-Reduced.pkl"
input_filepath = r"examples\Monomer Dimer\Controls [Whole Whole Whole Br]-Reduced.pkl"


dataframe_filepath = Path(input_filepath)



def change_dataframe():
    import_string = txt_in.value
    #print (import_string)
    if os.path.isfile(import_string):
        dataframe = pd.read_pickle(txt_in.value)
    else:
        print ("No dataframe by that name")
        dataframe = pd.DataFrame()
    print (dataframe.columns)
    
def get_source_data(x, y, radius = None, color=None):
    x_length = len(x)
    x_max, x_min, y_max, y_min = x.max(), x.min(), y.max(), y.min()    
    radius = [min(x_max, y_max)/100]*x_length
    color = ['red']*x_length
    return dict(x=x, y=y, radius = radius, color = color)

def unpack_parameters(parameters, symbol = '$'):
    channel, parameter = parameters.split(symbol)
    channel = int(channel)
    return (channel, parameter)

def get_subdata(dataframe, time, channel, parameter):
    return dataframe.loc[:, pd.IndexSlice[time,channel,parameter]]


def get_plot_data(dataframe, channel, parameter):
    means = dataframe.describe().loc['mean', pd.IndexSlice[:,channel,parameter]].values
    data = dict(x = range(len(means)), top = means)
    return data
    



def filter_dataframe(dataframe, filters, return_rows = False):
    filtered_dataframe = dataframe
    rows = filtered_dataframe.index #This is important for export without any filters
    
    
    for f in filters:
        channel, parameter = unpack_parameters(f.title)
        lower, upper = f.value

    #Greater than lower bound
        if not lower == f.start:
            rows = (filtered_dataframe.loc[:, pd.IndexSlice[0:, channel, parameter]]
                    .apply(lambda x: np.greater_equal(x, lower))
                    .apply(np.all, axis = 1))

            filtered_dataframe = filtered_dataframe.loc[rows]

    #Lower than upper bound
        if not upper == f.end:
            rows = (filtered_dataframe.loc[:, pd.IndexSlice[0:, channel, parameter]]
            .apply(lambda x: np.less_equal(x, upper))
            .apply(np.all, axis = 1))

            filtered_dataframe = filtered_dataframe.loc[rows]


    if return_rows: return rows
    elif len(filtered_dataframe)>0: return filtered_dataframe
    else:
        debug_output("Error, you've filtered out all the data... defaulting to the original")
        return(dataframe)    




def initialize_graphs():
    pass
    


def update(Data, Graphs):



    dataframe = Data['Dataframe']
    timepoints = Data['Timepoints']
    filters = Data['Filters']

    scatter_source = Graphs['Scatter Sources']
    bar_source = Graphs['Bar Source']



    filtered_dataframe = filter_dataframe(dataframe, filters)

    update_graph(filtered_dataframe, timepoints, scatter_source)
    update_bar_graph(filtered_dataframe, bar_source)



def debug_output(text = "tester"):
    output_text.text = text

def update_slider(attr, old, new, Data, Graphs):
    output_text.text = str(new)
    #print (layout.children[1].children[1])
    #layout.children[1].children[1] = (update_graph(),0,1)
    update(Data, Graphs)
    
def update_selection(attr, old, new, Data, Graphs):
    output_text.text = str(unpack_parameters(new))
    #print (layout.children[1].children[1])
    #layout.children[1].children[1] = (update_graph(),0,1)
    update(Data, Graphs)
    
    
def update_graph(dataframe, timepoints, sources):
    #debug_output(str(dataframe.loc[0, pd.IndexSlice[0,-1, 'Segmented_Area']]))
    x_ch, x_param = unpack_parameters(x_select.value)
    y_ch, y_param = unpack_parameters(y_select.value)
    
    for t in range(timepoints):
        sources[t].data = get_source_data(x = get_subdata(dataframe, t,int(x_ch),x_param),
                                y = get_subdata(dataframe, t,int(y_ch),y_param))

def update_bar_graph(dataframe, source):
    #filtered_dataframe = filter_dataframe(dataframe, filters)
    bar_ch, bar_param = unpack_parameters(bar_select.value)
    source_dict = get_plot_data(dataframe, bar_ch, bar_param)
    source.data = source_dict


def update_dataframe(attr, old, new, Data, Graphs):
    #Clear Previous Data
    scatter_source = Graphs['Scatter Sources']
    timepoints = Data['Timepoints']
    clear_graph(timepoints, scatter_source)

    #Load the new dataframe and update
    filename = dataframe_select.value
    open_dataframe(Data['Root Folder']/filename, Data)
    update(Data, Graphs)



def clear_graph(timepoints, sources):
    for t in range(timepoints):
        sources[t].data = dict(x=[], y=[], radius = [], color = [])






def open_dataframe(filepath, Data ={}):
    
    root_folder = filepath.parent
    filename = filepath.name
    raw_dataframe = pd.read_pickle(root_folder/filename)
    dataframe = raw_dataframe.select_dtypes(include = ['float64', 'int32'])

    timepoints = max([i for (i,j,k) in raw_dataframe])
    parameters = [(j,x) for (i,j,x) in dataframe if i ==0]
    parameters = ['$'.join(list(map(str,x))) for x in parameters]

    Data['Filepath'] = filepath
    Data['Root Folder'] = root_folder
    Data['Timepoints'] = timepoints
    Data['Parameters'] = parameters
    Data['Dataframe'] = dataframe
    Data['Filtered Dataframe'] = dataframe

    #debug_output(f'loaded dataframe {Data["Filepath"]}')

    return Data








def create_graph(dataframe, timepoints):
    
    p = figure(plot_width = 1000, plot_height = 1000, tools = "pan, wheel_zoom,box_zoom,reset, hover, lasso_select")

    x_ch, x_param = unpack_parameters(x_select.value)
    y_ch, y_param = unpack_parameters(y_select.value)
    
    sources = []
    plots = [None]*timepoints
    
    for t in range(timepoints):
        source_dict = get_source_data(x = get_subdata(dataframe, t,int(x_ch),x_param),
                                y = get_subdata(dataframe, t,int(y_ch),y_param))  
        
        source = ColumnDataSource(data = source_dict)
        
        plots[t] = p.circle(x = 'x', y = 'y',  color = Spectral6[t], source = source, alpha = 0.4)
        sources.append(source)
        
    return(p, plots, sources)



def create_bar_plot(dataframe):
    bar_ch, bar_param = unpack_parameters(bar_select.value)
    source_dict = get_plot_data(dataframe, bar_ch, bar_param)
    bar_source = ColumnDataSource(data = source_dict)
    p = figure(plot_width = 300, plot_height = 300, tools = 'hover')
    columns = p.vbar(x='x', top='top', width = 0.9, source = bar_source)
    
    return(p, columns, bar_source)


def create_filters(parameters, Data):
    filters = []
    dataframe = Data['Dataframe']
    for param in parameters:
        channel, parameter = unpack_parameters(param)
        max_value = np.max(dataframe.loc[:, pd.IndexSlice[:, channel, parameter]].apply(np.max))
        min_value = np.min(dataframe.loc[:, pd.IndexSlice[:, channel, parameter]].apply(np.min))
        
        step_size = (max_value-min_value)/100
        filters.append(RangeSlider(start = min_value, end = max_value, 
                                    value = (min_value,max_value), 
                                    step = step_size, title = str(param)))
        filters[-1].on_change('value', partial(update_slider, Data = Data, Graphs = Graphs))
        #print (parameter, channel, min_value, max_value, filters[-1].start)

    return filters


def export_graphs(folder, Graphs):
    #Export Scatter
    scatter_filename = f"{x_select.value} vs. {y_select.value}.png"
    export_png(Graphs['Scatter Graph'], folder/scatter_filename)
    

    #Export Bar Graph
    bar_filename = f'{bar_select.value}.png'
    export_png(Graphs['Bar Graph'], folder/bar_filename)

    debug_output(f'Export Successful of: {scatter_filename} and {bar_filename}!')


def output_filters(filters):
    df = pd.DataFrame(columns = ['Filter', 'Upper', 'Lower'])
    
    for f in filters:
        lower, upper = f.value

        new_row = {}

    #Greater than lower bound
        if not lower == f.start:
            new_row['Filter'] = f.title
            new_row['Lower'] = lower
    #Lower than upper bound
        if not upper == f.end:
            new_row['Filter'] = f.title  #This may be set twice on occasion...
            new_row['Upper'] = upper

        #print (new_row)

        if new_row: df = df.append(new_row, ignore_index = True)
    
    return df


def export_filtered_dataframe(Data):
    filepath = Data['Filepath']
    filters = Data['Filters']

    raw_dataframe = pd.read_pickle(filepath)


    export_dataframe = filter_dataframe(raw_dataframe, filters, return_rows = False)

    writer = pd.ExcelWriter(str(filepath.parent/"test.xlsx"), engine='xlsxwriter')

    export_dataframe.to_excel(writer, "Raw_Data")
    create_summary_columns(export_dataframe).to_excel(writer, "Summary")
    cell_cell_comparison = create_cell_comparisons(export_dataframe)
    for key in cell_cell_comparison:
        cell_cell_comparison[key].to_excel(writer, key)


    output_filters(filters).to_excel(writer, 'Filters')

    writer.save()

    

    debug_output('Export of Dataframe was successful')


    

"""
Import the default dataframe
"""
    #Put defaults in a text file to read in later...
#dataframe_filepath = Path(r'examples/01 - Nuc Cyto Hyper [Nuc Cyto Whole Br]-Reduced.pkl')
#root_folder = dataframe_filepath.parent
#filename = dataframe_filepath.name

Data = open_dataframe(dataframe_filepath)
Graphs = {}



"""


All the widgets and their callback behaviours



"""


txt_in = TextInput()
select_dataframe_btn = Button(label="Import Dataframe", button_type="success")
select_dataframe_btn.on_click(change_dataframe)


dataframes = []
#root_folder = current if current.is_dir() else current.parent
for file in Data['Root Folder'].iterdir():
    if file.name.endswith('Reduced.pkl'): dataframes.append(str(file.name))

dataframe_select = Select (title = "Dataframe Selector", value = None, options = dataframes)
dataframe_select.on_change('value', partial(update_dataframe, Data = Data, Graphs = Graphs))





parameters = Data['Parameters']

x_initial = parameters[0]
y_initial = parameters[1]

x_select = Select(title = 'X-Axis', value = x_initial, options = parameters)    
y_select = Select(title = 'Y-Axis', value = y_initial, options = parameters)
r_select = Select(title = 'Radius', value = 'None', options = parameters)
col_select = Select(title = 'Color', value = 'None', options = parameters)



bar_select = Select(title = 'BarGraph', value = x_initial, options = parameters)
bar_select.on_change('value', partial(update_selection, Data = Data, Graphs = Graphs))


for selection in [x_select, y_select, r_select, col_select]:
    selection.on_change('value', partial(update_selection, Data = Data, Graphs = Graphs))

output_text = Paragraph(text = 'Hello')

Data['Filters'] = create_filters(Data['Parameters'], Data)

graph_options = column([x_select, y_select, r_select, col_select]+Data['Filters'])








"""
Initialize the Plot

"""




Graphs['Scatter Graph'], Graphs['Scatter Plots'], Graphs['Scatter Sources'] = create_graph(Data['Dataframe'], Data['Timepoints'])
Graphs['Bar Graph'], Graphs['Bar Plot'], Graphs['Bar Source'] = create_bar_plot(Data['Dataframe'])


export_button = Button(label = 'Export Graphs', button_type = 'success')
export_button.on_click(partial(export_graphs, Data['Root Folder'], Graphs))


export_dataframe = Button (label = 'Export Filtered Data', button_type = 'success')
export_dataframe.on_click(partial(export_filtered_dataframe, Data)) 


bar_graph_column = column([bar_select, Graphs['Bar Graph'], export_button, export_dataframe])

        #dataframe, parameters = initialize()



import_row = row([txt_in, select_dataframe_btn, dataframe_select, output_text])
graph_row = row([graph_options, Graphs['Scatter Graph'], bar_graph_column])



#layout = gridplot([[txt_in, select_dataframe_btn, output_text],[graph_options,graph, bar_graph_column]], sizing_mode = 'scale_both')
#final_layout = column([import_row, graph_row])


final_layout = layout([import_row, graph_row])
curdoc().add_root(final_layout)