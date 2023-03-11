import streamlit as st
import matplotlib.pyplot as plt
import imageio

from io import BytesIO
from tempfile import NamedTemporaryFile


x = [1, 2, 3, 4, 4, 4, 4, 3, 2, 1, 1, 1, 1]
y = [1, 1, 1, 1, 2, 3, 4, 4, 4, 4, 3, 2, 1]
time = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]

frames = []
for t in time:
    fig = plt.figure(figsize=(6, 6))
    plt.plot(x[:(t+1)], y[:(t+1)], color = 'grey' )
    plt.plot(x[t], y[t], color = 'black', marker = 'o' )
    plt.xlim([0,5])
    plt.xlabel('x', fontsize = 14)
    plt.ylim([0,5])
    plt.ylabel('y', fontsize = 14)
    plt.title(f'Relationship between x and y at step {t}',
              fontsize=14)
    with NamedTemporaryFile() as tmp:
        plt.savefig(tmp.name, 
                    transparent = False,  
                    facecolor = 'white'
                )
        plt.close()
        frames.append(imageio.v2.imread(tmp.name))

with NamedTemporaryFile() as tmp:
    imageio.mimsave(tmp.name, # output gif
                    frames,          # array of input frames
                    fps = 5)         # optional: frames per second
    st.image(tmp.name)
