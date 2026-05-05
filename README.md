# ImageDecoder-SO18
My submission for the 18th Stack Overflow challenge, using steganography techniques to find data hidden in the least significant bit of an image's colour channels.

I had a lot of fun with this one. I don't do much bitwise/byte logic usually, so my mode of thinking with using lists was probably a little inefficient, but keeps debug readouts nice and easy to understand, and keeps codeflow beginner-friendly. Things could probably be improved by using bytearrays and getting pretty low level - but to my mind, if you wanted to be that close to the ground, I'm unsure if python would be the best choice to begin with...

Either way, using a main loop and mapping out first-element header values, I made things so you can whack all of the related images into a folder wherever you run the script, and it'll create text or image files for output as required.

Dependencies are Pillow and Numpy, as listed in requirements.txt, if you want to run it yourself!
