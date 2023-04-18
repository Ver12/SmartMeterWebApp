import streamlit as st
import pandas as pd
import serial
import numpy as np
import threading
import plotly.express as px
import plotly.graph_objects as go
from streamlit_lottie import st_lottie
import requests
from PIL import Image

import warnings
warnings.filterwarnings("ignore")

totalLoad = pd.DataFrame(data=[],columns=['Time Interval','Total Load'])
wind = pd.DataFrame(data=[],columns=['Time Interval','Wind Capacity'])
pv = pd.DataFrame(data=[],columns=['Time Interval','PV Capacity'])

busbarVoltage = pd.DataFrame(data=[],columns=['Time Interval','Busbar Voltage'])
busbarCurrent = pd.DataFrame(data=[],columns=['Time Interval','Busbar Current'])
battery= pd.DataFrame(data=[],columns=['Time Interval','Battery'])

ser = serial.Serial(port='COM8', baudrate=9600, parity=serial.PARITY_NONE,stopbits=serial.STOPBITS_ONE,bytesize=serial.EIGHTBITS,timeout=1) #Change the COM port to whichever port your arduino is in
ser.reset_input_buffer()
i=0
j=0
k=0
l=0
m=0
n=0

def read_data():
    global i,j,k,l,m,n
    global record, battery,wind,pv,busbarCurrent,busbarVoltage,mainCap
    while True:
        line = ser.readline()
        if line:
            string = line.decode()
            #print("Opcode is " + string[0])
            try:
                num = int(string[1:-1])
                print("Opcode is " + string[0] +  "  "+ str(num))
                #print(num)

                # if opcode is 0 means total Load
                if string[0] == '0':
                    if (i < 24):
                        totalLoad.loc[i, 'Time Interval'] = i
                        totalLoad.loc[i, 'Total Load'] = num
                        i += 1

                # if opcode is 1 means battery
                elif string[0] == '1':
                    print(battery)
                    if (j < 24):
                        battery.loc[j, 'Time Interval'] = j
                        battery.loc[j, 'Battery'] = num
                        j += 1

                # if opcode is 2 means wind capacity
                elif string[0] == '2':

                    if (k < 24):
                        wind.loc[k, 'Time Interval'] = k
                        wind.loc[k, 'Wind Capacity'] = num
                        k += 1

                    # if opcode is 3 means PV capacity
                elif string[0] == '3':

                    if (l < 24):
                        pv.loc[l, 'Time Interval'] = l
                        pv.loc[l, 'PV Capacity'] = num
                        l += 1

                    # if opcode is 4 means busbarVoltage
                elif string[0] == '4':

                    if (m < 24):
                        busbarVoltage.loc[m, 'Time Interval'] = m
                        busbarVoltage.loc[m, 'Busbar Voltage'] = num
                        m += 1

                # if opcode is 5 means busbarCurrent
                elif string[0]=='5':
                    busbarC = (((num/1024)*3.3)*6.4272 - 11.2)
                    print(busbarC)
                    if (n < 24):
                        busbarCurrent.loc[n, 'Time Interval'] = n
                        busbarCurrent.loc[n, 'Busbar Current'] = busbarC
                        n += 1

                # if opcode is invalid do nothing
                else:
                    pass
            except:
                print(" hello")

st.set_page_config(
    page_title="Real-Time Dashboard",
    page_icon="✅",
    layout="wide",
)

def load_lottieurl(url:str):
    r=requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

#st.title("TEAM B Smart Meter Dashboard :chart:")
lottie_hello=load_lottieurl("https://assets2.lottiefiles.com/packages/lf20_3vbOcw.json")

image = Image.open('smartmeters.jpg')

st.markdown("""
<style>
.font {
    font-size:26px !important;
}
</style>
""", unsafe_allow_html=True)

text,animation=st.columns(2)
with text:
    st.title("TEAM B Smart Meter Dashboard :chart:")
    #st.image(image, caption='Smart meter')
    st.write('')
    st.write('')
    st.markdown('<p class="font">A smart meter  is an electronic device that records information such asconsumption of electric energy, voltage levels, current and power factor. Smart meters communicate the information to the consumer for greater clarity of consumption behavior, and electricity suppliers for system monitoring and customer billing. Smart meters  typically record energy near real-time, and report regularly, short intervals throughout the day.</p>', unsafe_allow_html=True)
    # st.write('''A smart meter  is an electronic device that records information such as
    #     consumption of :blue[electric energy], :green[voltage levels], :orange[current], and :red[power factor].
    #     Smart meters communicate the information to the consumer for greater clarity of consumption
    #     behavior, and electricity suppliers for system monitoring and customer billing. Smart meters
    #     typically record energy near real-time, and report regularly, short intervals throughout the day.'''
    #        )

with animation:
    st_lottie(lottie_hello,key="hello",height=400,width=400)

st.write(' ')
st.write(' ')

##################### Layout Application ##################

placeholder = st.empty()

#css injection
def _max_width_():
    max_width_str = "max-width: 1900px;"
    st.markdown(
        f"""
    <style>
    .block-container {{
        {max_width_str}
        }}
    .custom-widget {{
        display: grid;
        border: 1px solid black;
        padding: 12px;
        border-radius: 5%;
        color: #003366;
        margin-bottom: 5px;
        min-height: 251.56px;
        align-items: center;
    }}
    h6 {{
        display: block;
        font-size: 18px;
        margin-left: 0;
        margin-right: 0;
        font-weight: bold;
        color: #003366;
    }}
    h2 {{
        text-decoration: underline;
    }}
    h1 {{
        display: grid;
        justify-content: center;
        align-items: center;
    }}

    .css-1m8p54g{{
        justify-content: center;
    }}
    .css-1bt9eao {{
    }}
    .row-widget.stCheckbox {{
        display: grid;
        justify-content: center;
        align-items: center;
        border: solid 2px black;
        border-radius: 3%;
        height: 50px;
        background-color: #DF1B88;
        color: #FFFFFF;
    }}
    .css-1djdyxw {{
        color: #FFFFFF;
    }}
    .css-ps6290 {{
        color: black;
    }}
    .css-1cpxqw2 {{
        background-color: #00AB55;
        color: white;
        font-weight: 500;
        border: 1px solid #003366;
    }}
    <style>
    """,
        unsafe_allow_html=True,
    )


_max_width_()


def plot_graph():
    while True:
        with placeholder.container():
            totalLoadFig, batteryFig = st.columns(2)
            windFig,pvFig = st.columns(2)

             #Create traces
            with totalLoadFig:
               # st.markdown("### :purple[Total Load against Time Interval]")
                fig = go.Figure()
                fig.add_trace(go.Line(x=totalLoad['Time Interval'], y=totalLoad['Total Load'],
                                         mode='lines',
                                         name='lines'))
                fig.update_layout(
                title=dict(text="Total Load against Time Interval", font=dict(size=30), automargin=True,
                           yref='paper'),  title_font_color="purple",xaxis_title="Time Interval", yaxis_title="Total Load")
                fig.update_layout( xaxis_title="Time Interval", yaxis_title="Total Load")

                fig.update_xaxes(
                    mirror=True,
                    ticks='outside',
                    showline=True,
                    linecolor='black',
                    gridcolor='lightgrey'
                )
                fig.update_yaxes(
                    mirror=True,
                    ticks='outside',
                    showline=True,
                    linecolor='black',
                    gridcolor='lightgrey'
                )

                st.write(fig)

            with batteryFig:
               # st.markdown("### :yellow[ Battery Amount against Time Interval]")
                fig2=go.Figure()
                fig2.add_trace(go.Line(x=battery['Time Interval'], y=battery['Battery'],
                                      mode='lines',
                                      name='lines'))
                fig2.update_layout(
                    title=dict(text="Battery Amount against Time Interval", font=dict(size=30), automargin=True,
                               yref='paper'),title_font_color="brown",xaxis_title = "Time Interval", yaxis_title = "Battery Amount")
                fig2.update_layout(xaxis_title = "Time Interval", yaxis_title = "Battery Amount")

                fig2.update_xaxes(
                    mirror=True,
                    ticks='outside',
                    showline=True,
                    linecolor='black',
                    gridcolor='lightgrey'
                )
                fig2.update_yaxes(
                    mirror=True,
                    ticks='outside',
                    showline=True,
                    linecolor='black',
                    gridcolor='lightgrey'
                )

                st.write(fig2)

            with windFig:
                #st.markdown("### :green[Renewable Energy against Time Interval]")
                fig3 = go.Figure()
                fig3.add_trace(go.Line(x=wind['Time Interval'],y=wind['Wind Capacity'],
                                         mode='lines'))
                fig3.add_trace(go.Line(x=pv['Time Interval'],y=pv['PV Capacity'],
                                        mode='lines'))
                fig3.update_layout(
                title=dict(text="Renewable Energy against Time Interval", font=dict(size=30), automargin=True,
                           yref='paper'),title_font_color="green",xaxis_title = "Time Interval", yaxis_title = "Renewable Energy")

                fig3.update_layout(xaxis_title = "Time Interval", yaxis_title = "Renewable Energy")
                fig3.update_xaxes(
                    mirror=True,
                    ticks='outside',
                    showline=True,
                    linecolor='black',
                    gridcolor='lightgrey'
                )
                fig3.update_yaxes(
                    mirror=True,
                    ticks='outside',
                    showline=True,
                    linecolor='black',
                    gridcolor='lightgrey'
                )
                st.write(fig3)

            with pvFig:
                #st.markdown("### :blue[Busbar Voltage and Current against Time Interval]")
                fig4 = go.Figure()
                fig4.add_trace(go.Line(x=busbarVoltage['Time Interval'], y=busbarVoltage['Busbar Voltage'],
                                       mode='lines'))
                fig4.add_trace(go.Line(x=busbarCurrent['Time Interval'], y=busbarCurrent['Busbar Current'],
                                       mode='lines'))
                fig4.update_layout(
                    title=dict(text="Busbar Voltage and Current against Time Interval", font=dict(size=30), automargin=True, yref='paper'),
                    title_font_color="blue",xaxis_title = "Time Interval", yaxis_title = "BusbarCurrent and Voltage")
                fig4.update_layout(xaxis_title = "Time Interval", yaxis_title = "BusbarCurrent and Voltage")
                fig4.update_xaxes(
                    mirror=True,
                    ticks='outside',
                    showline=True,
                    linecolor='black',
                    gridcolor='lightgrey'
                )
                fig4.update_yaxes(
                    mirror=True,
                    ticks='outside',
                    showline=True,
                    linecolor='black',
                    gridcolor='lightgrey'
                )
                st.write(fig4)

                # # create two columns for charts
                # totalLoadFig, batteryFig = st.columns(2)
                # windFig,pvFig = st.columns(2)
                # voltageFig, currentFig = st.columns(2)
                #
                # with totalLoadFig:
                #     st.markdown("### Total Load against Time Interval")
                #     totalLoadFig= px.line(totalLoad, x="Time Interval", y="Total Load", title='Total Load vs. time')
                #     st.write(totalLoadFig)
                #
                # with batteryFig:
                #     st.markdown("### Battery Amount against Time Interval")
                #     batteryFig = px.line(battery, x="Time Interval", y="Battery", title='Battery vs. time',
                #          template='plotly_dark').update_layout(
                #                    {'plot_bgcolor': 'rgba(0, 0, 0, 0)',
                #                     'paper_bgcolor': 'rgba(0, 0, 0, 0)'})
                #     st.write(batteryFig)
                #
                # with windFig:
                #     st.markdown("### Wind Turbine Capacity against Time Interval")
                #     windFig = px.line(wind, x="Time Interval", y="Wind Capacity", title='Wind Capacity vs. time')
                #     st.write(windFig)
                #
                # with pvFig:
                #     st.markdown("### PV Capacity against Time Interval")
                #     pvFig = px.line(pv, x="Time Interval", y="PV Capacity", title='PV Capacity vs. time')
                #     st.write(pvFig)
                #
                # with voltageFig:
                #     st.markdown("### Busbar Voltage against Time Interval")
                #     voltageFig = px.line(busbarVoltage, x="Time Interval", y="Busbar Voltage", title='Busbar Voltage vs. time')
                #     st.write(voltageFig)
                #
                # with currentFig:
                #     st.markdown("### Busbar Current against Time Interval")
                #     currentFig = px.line(busbarCurrent, x="Time Interval", y="Busbar Current", title='Busbar Current vs. time')
                #     st.write(currentFig)

t1=threading.Thread(target=read_data)
t1.start()
plot_graph()
