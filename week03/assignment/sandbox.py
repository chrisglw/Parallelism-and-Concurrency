"""
------------------------------------------------------------------------------
Course: CSE 251
Lesson Week: 03
File: assignment.py
Author: Christian Landaverde

Purpose: Video Frame Processing

Instructions:

- Follow the instructions found in Canvas for this assignment
- No other packages or modules are allowed to be used in this assignment.
  Do not change any of the from and import statements.
- Only process the given MP4 files for this assignment

------------------------------------------------------------------------------
"""

from matplotlib.pylab import plt  # load plot library
from PIL import Image
import numpy as np
import timeit
import multiprocessing as mp

# Include cse 251 common Python files
from cse251 import *

# 4 more than the number of cpu's on your computer
CPU_COUNT = mp.cpu_count() + 4  

# TODO Your final video need to have 300 processed frames.  However, while you are 
# testing your code, set this much lower
FRAME_COUNT = 300

RED   = 0
GREEN = 1
BLUE  = 2


def create_new_frame(image_file, green_file, process_file):
    """ Creates a new image file from image_file and green_file """

    # this print() statement is there to help see which frame is being processed
    print(f'{process_file[-7:-4]}', end=',', flush=True)

    image_img = Image.open(image_file)
    green_img = Image.open(green_file)

    # Make Numpy array
    np_img = np.array(green_img)

    # Mask pixels 
    mask = (np_img[:, :, BLUE] < 120) & (np_img[:, :, GREEN] > 120) & (np_img[:, :, RED] < 120)

    # Create mask image
    mask_img = Image.fromarray((mask*255).astype(np.uint8))

    image_new = Image.composite(image_img, green_img, mask_img)
    image_new.save(process_file)


# TODO add any functions to need here
def create_frames(image_number):
    """ Creates a new image mixing two images from the elephan and green folders. """
    image_file = rf'elephant/image{image_number:03d}.png'
    green_file = rf'green/image{image_number:03d}.png'
    process_file = rf'processed/image{image_number:03d}.png'
    create_new_frame(image_file, green_file, process_file)


if __name__ == '__main__':
    # single_file_processing(300)
    # print('cpu_count() =', cpu_count())

    all_process_time = timeit.default_timer()
    log = Log(show_terminal=True)

    xaxis_cpus = []
    yaxis_times = []

    # TODO Process all frames trying 1 cpu, then 2, then 3, ... to CPU_COUNT
    #      add results to xaxis_cpus and yaxis_times

    # Iterate through processors.
    for processes in range(1, CPU_COUNT + 1):
      start_time = timeit.default_timer()
      with mp.Pool(processes) as p:
        p.map(create_frames, [x for x in range(1, FRAME_COUNT + 1)])   # Pass a list of all frames.
      end_time = timeit.default_timer() - start_time
      log.write(f'Time for {FRAME_COUNT} frames using {processes} processes: {end_time}')
      xaxis_cpus.append(processes)
      yaxis_times.append(end_time)

    # sample code: remove before submitting  >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
    # process one frame #10 (put it on a loop)
    # image_number = 10

    # image_file = rf'elephant/image{image_number:03d}.png'
    # green_file = rf'green/image{image_number:03d}.png'
    # process_file = rf'processed/image{image_number:03d}.png'

    # start_time = timeit.default_timer()
    # create_new_frame(image_file, green_file, process_file)
    # print(f'\nTime To Process all images = {timeit.default_timer() - start_time}')
    # <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<


    log.write(f'Total Time for ALL processing: {timeit.default_timer() - all_process_time}')

    # create plot of results and also save it to a PNG file
    plt.plot(xaxis_cpus, yaxis_times, label=f'{FRAME_COUNT}')
    
    plt.title('CPU Core yaxis_times VS CPUs')
    plt.xlabel('CPU Cores')
    plt.ylabel('Seconds')
    plt.legend(loc='best')

    plt.tight_layout()
    plt.savefig(f'Plot for {FRAME_COUNT} frames.png')
    plt.show()


# """
# ------------------------------------------------------------------------------
# Course: CSE 251
# Lesson Week: 03
# File: assignment.py
# Author: Christian Landaverde

# Purpose: Video Frame Processing

# Instructions:

# - Follow the instructions found in Canvas for this assignment
# - No other packages or modules are allowed to be used in this assignment.
#   Do not change any of the from and import statements.
# - Only process the given MP4 files for this assignment

# ------------------------------------------------------------------------------
# """

# from matplotlib.pylab import plt  # load plot library
# from PIL import Image
# import numpy as np
# import timeit
# import multiprocessing as mp

# # Include cse 251 common Python files
# from cse251 import *

# # 4 more than the number of cpu's on your computer
# CPU_COUNT = mp.cpu_count() + 4  

# # TODO Your final video need to have 300 processed frames.  However, while you are 
# # testing your code, set this much lower
# FRAME_COUNT = 20

# RED   = 0
# GREEN = 1
# BLUE  = 2


# def create_new_frame(image_file, green_file, process_file):
#     """ Creates a new image file from image_file and green_file """

#     # this print() statement is there to help see which frame is being processed
#     print(f'{process_file[-7:-4]}', end=',', flush=True)

#     image_img = Image.open(image_file)
#     green_img = Image.open(green_file)

#     # Make Numpy array
#     np_img = np.array(green_img)

#     # Mask pixels 
#     mask = (np_img[:, :, BLUE] < 120) & (np_img[:, :, GREEN] > 120) & (np_img[:, :, RED] < 120)

#     # Create mask image
#     mask_img = Image.fromarray((mask*255).astype(np.uint8))

#     image_new = Image.composite(image_img, green_img, mask_img)
#     image_new.save(process_file)


# # TODO add any functions to need here

# def process_frames_on_cpu_count(cpu_count):
#     """ Process all frames using the given CPU count and record the time """

#     all_process_time = timeit.default_timer()
#     log = Log(show_terminal=True)

#     xaxis_cpus = []
#     yaxis_times = []

#     # Process all frames using the given CPU count
#     pool = mp.Pool(cpu_count)

#     for i in range(1, FRAME_COUNT+1):
#         image_file = f'elephant/image{i:03d}.png'
#         green_file = f'green/image{i:03d}.png'
#         process_file = f'processed/image{i:03d}.png'
#         pool.apply_async(create_new_frame, args=(image_file, green_file, process_file))

#     pool.close()
#     pool.join()

#     log.write(f'Total Time for processing {FRAME_COUNT} frames with {cpu_count} CPUs: {timeit.default_timer() - all_process_time}')

#     return timeit.default_timer() - all_process_time


# if __name__ == '__main__':
#     # single_file_processing(300)
#     # print('cpu_count() =', cpu_count())

#     all_process_time = timeit.default_timer()
#     log = Log(show_terminal=True)

#     xaxis_cpus = []
#     yaxis_times = []

#     # TODO Process all frames trying 1 cpu, then 2, then 3, ... to CPU_COUNT
#     #      add results to xaxis_cpus and yaxis_times
#     for cpu in range(1, CPU_COUNT + 1):
#         pool = mp.Pool(cpu)
#         start_time = timeit.default_timer()

#         # use pool.map() to process all frames using the create_new_frame() function
#         # the inputs for the create_new_frame() function will be a tuple of the 3 file names

#         file_names = [(f'elephant/image{i:03d}.png', f'green/image{i:03d}.png', f'processed/image{i:03d}.png') for i in range(1, FRAME_COUNT + 1)]
#         pool.map(create_new_frame, file_names)
        
#         pool.close()
#         pool.join()

#         elapsed_time = timeit.default_timer() - start_time
#         xaxis_cpus.append(cpu)
#         yaxis_times.append(elapsed_time)
#         log.write(f'Total Time for ALL processing ({cpu} CPU core): {elapsed_time}')

#     # create plot of results and also save it to a PNG file
#     plt.plot(xaxis_cpus, yaxis_times, label=f'{FRAME_COUNT}')

#     # sample code: remove before submitting  >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
#     # process one frame #10 (put it on a loop)
#     # image_number = 10

#     # image_file = rf'elephant/image{image_number:03d}.png'
#     # green_file = rf'green/image{image_number:03d}.png'
#     # process_file = rf'processed/image{image_number:03d}.png'

#     # start_time = timeit.default_timer()
#     # create_new_frame(image_file, green_file, process_file)
#     # print(f'\nTime To Process all images = {timeit.default_timer() - start_time}')
#     # <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<


#     log.write(f'Total Time for ALL processing: {timeit.default_timer() - all_process_time}')

#     # create plot of results and also save it to a PNG file
#     plt.plot(xaxis_cpus, yaxis_times, label=f'{FRAME_COUNT}')
    
#     plt.title('CPU Core yaxis_times VS CPUs')
#     plt.xlabel('CPU Cores')
#     plt.ylabel('Seconds')
#     plt.legend(loc='best')

#     plt.tight_layout()
#     plt.savefig(f'Plot for {FRAME_COUNT} frames.png')
#     plt.show()
