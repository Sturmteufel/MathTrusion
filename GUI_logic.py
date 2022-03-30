import PySimpleGUI as sg
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.tri as mtri
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from GUI_visual import create_window, section_names
import examples
import base_shapes
from matplotlib.patches import Polygon


_VARS = {'window': False,
         'fig_agg': False,
         'plt_fig': False,
         'plt_ax': False,
         'data_size': 60}

SYMBOL_UP =    '▲'
SYMBOL_DOWN =  '▼'

_VARS['window'] = create_window()
_VARS['window'].maximize()


def get_plot_limits(data, pad=(0, 0)):
    ptp = np.ptp(data)
    left = min(data[:,0]) - pad[0] * ptp / 100
    right = max(data[:,0]) + pad[0] * ptp / 100
    top = min(data[:,0]) - pad[1] * ptp / 100
    bottom = max(data[:,0]) + pad[1] * ptp / 100
    print(ptp, (left, right), (top, bottom))
    return (left, right), (top, bottom)


def draw_figure(canvas, figure):
    figure_canvas_agg = FigureCanvasTkAgg(figure, canvas)
    figure_canvas_agg.draw()
    figure_canvas_agg.get_tk_widget().pack(side='top', fill='both', expand=1)
    return figure_canvas_agg


def draw_base_chart():
    _VARS['plt_fig_base'] = plt.figure(figsize=(5,5), dpi=50, facecolor='black')
    _VARS['ax_base'] = _VARS['plt_fig_base'].add_subplot(111)
    _VARS['ax_base'].plot([])
    _VARS['ax_base'].set_axis_off()
    _VARS['ax_base'].set_facecolor('black')
    _VARS['plt_fig_base'].tight_layout()
    _VARS['fig_agg_base'] = draw_figure(
        _VARS['window'][f'-CHOICES {section_names[0]} Plot-'].TKCanvas,\
        _VARS['plt_fig_base']
    )


def update_base_chart(base_shape):
    _VARS['fig_agg_base'].get_tk_widget().forget()
    _VARS['ax_base'].clear()

    polygon = Polygon(base_shape[:,:2], edgecolor='white', facecolor='black',\
                      linewidth=5)
    _VARS['ax_base'].add_patch(polygon)

    xlim, ylim = get_plot_limits(base_shape, (4, 4))
    _VARS['ax_base'].set_xlim(xlim)
    _VARS['ax_base'].set_ylim(ylim)
    _VARS['ax_base'].set_facecolor('black')
    _VARS['ax_base'].set_aspect('equal')
    _VARS['ax_base'].set_axis_off()
    _VARS['fig_agg_base'] = draw_figure(
        _VARS['window'][f'-CHOICES {section_names[0]} Plot-'].TKCanvas,\
        _VARS['plt_fig_base']
    )


def draw_3d_chart():
    _VARS['plt_fig'] = plt.figure(figsize=(8,8), dpi=120, facecolor='black')
    _VARS['ax'] = _VARS['plt_fig'].add_subplot(111, projection='3d')
    _VARS['ax'].plot([], [], [])
    _VARS['ax'].set_axis_off()
    _VARS['ax'].set_facecolor('black')
    _VARS['plt_fig'].subplots_adjust(left=0, right=1, top=1, bottom=0)
    _VARS['fig_agg'] = draw_figure(
        _VARS['window']['-PREVIEW Plot-'].TKCanvas, _VARS['plt_fig']
    )


def update_3d_chart(x, y, z, triangles):
    _VARS['fig_agg'].get_tk_widget().forget()
    _VARS['ax'].clear()
    _VARS['ax'].set_axis_off()
    _VARS['ax'].set_facecolor('black')
    _VARS['ax'].set_box_aspect((np.ptp(x), np.ptp(y), np.ptp(z)))
    triang = mtri.Triangulation(x, y, triangles=triangles)
    _VARS['ax'].plot_trisurf(triang, z, cmap=plt.cm.rainbow,\
                             edgecolors='grey', linewidths=0.1)
    _VARS['fig_agg'] = draw_figure(
        _VARS['window']['-PREVIEW Plot-'].TKCanvas, _VARS['plt_fig']
    )


sec_last_opened = None

def open_section(section):
    global sec_last_opened

    open = (
        sec_last_opened != section or\
        (sec_last_opened == section and\
        _VARS['window'][f'-SEC{section}-'].visible == False)
    )

    if sec_last_opened != None:
        _VARS['window'][f'-OPEN SEC{sec_last_opened}-'].update(SYMBOL_DOWN)
        _VARS['window'][f'-SEC{sec_last_opened}-'].update(visible=False)

    if open:
        _VARS['window'][f'-OPEN SEC{section}-'].update(SYMBOL_UP)
        _VARS['window'][f'-SEC{section}-'].update(visible=True)
    
    sec_last_opened = section


for s in section_names:
    _VARS['window'][f'-OPEN SEC{s}-'].update(SYMBOL_DOWN)
    _VARS['window'][f'-SEC{s}-'].update(visible=False)

draw_base_chart()
update_base_chart(base_shapes.n_gon(5))
draw_3d_chart()
update_3d_chart(*examples.star_helix())

while True:
    event, values = _VARS['window'].read()
    print(event)
    print(values)
    print()
    if event == sg.WIN_CLOSED or event == 'Exit':
        break
    
    if event.startswith(f'-OPEN SEC'):
        open_section(event[9:-1])

_VARS['window'].close()