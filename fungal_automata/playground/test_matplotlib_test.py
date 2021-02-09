
import time
import matplotlib.pyplot as plt
from PIL import Image
import numpy as np
import matplotlib.image as mpimg


from PIL import Image
import numpy as np


test_img = []

# nice_img = Image.open('index.png')

image = np.array(mpimg.imread("test2.jpeg"))

print("image.shape: ", image.shape)

print("middle: ", image[300][300])

plt.imshow(image)
plt.show()


exit()
np_nice = np.array(nice_img)

for i in range(20):
    # plt.title("{0}".format(-1))
    # plt.imshow(img, origin='lower')
    test_img = []
    for i in range(20):
        test_img.append([(0,1*i,0, 1-i*0.1)])

# w, h = 512, 512
# data = np.zeros((h, w, 3), dtype=np.uint8)
# data[0:256, 0:256] = [255, 0, 0] # red patch in upper left

# print("data.shape: ", data.shape)
# test_np = np.array(test_img)
# print("test_np: ", test_np)
# img = Image.fromarray(test_np, 'RGB')

plt.imshow(np_nice)

# img.save('my.png')
plt.show()

print("check: ", np.array(test_img).shape)
plt.imshow(test_img)
plt.show()
# img.show()


"""
nice_img = Image.open('index.png')

test = np.array(nice_img)
print("test: ", test)
print("test.shape: ", test.shape)
plt.imshow(test)
plt.show()

# print("test.shape: ", test.shape)

# print("nice_img: ", np.array(nice_img))

a = np.diag(range(15))
for i in range(20):
    # plt.title("{0}".format(-1))
    # plt.imshow(img, origin='lower')
    test_img = []
    for i in range(20):
        test_img.append([(255, 255-i, 255)])

# test_arr = np.array([test_img]).reshape((1, 20, 3))
test_arr = np.array(test_img)
plt.plot(test_arr)
plt.show()
print("test_arr.shape: ", test_arr.shape)
# plt.imshow(test_img, aspect='auto')
# plt.show()
# plt.show()
# plt.imshow(test_arr)
# plt.show()

rgb_array = [[255.000, 56.026 + (255 - 56.026) * i / 400, 255 * i / 400] for i in range(400)]
rgb_array += [[255 - 255 * i / 600, 255 - 255 * i / 600, 255] for i in range(600)]
img = np.array(rgb_array, dtype=int).reshape((1, len(rgb_array), 3))

print("img: ", img)
print("img.shape: ", img.shape)
plt.imshow(test_arr, extent=[0, 16000, 0, 1], aspect='auto')
plt.show()
"""
