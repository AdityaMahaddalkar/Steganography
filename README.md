# Steganography

## Python code to hide textual data into images

### Required modules:
    1. OpenCV for python
    2. numpy

### Encoding
  The program uses LSB method of storing the bits into picture. Each image is divided into three planes: Red, Blue, Green; thus each
  pixel associated with row and column has 3 values (r, g, b) in accordance to three planes.
  
  Open CV uses (b, g, r) format for manipulating images. The program stores each character from the message into one pixel by the
  following method
  
  Consider ascii binary value of 'H': 1001000. We divide it into 3 parts 100, 10, 00. Consider pixel at (0, 0), 100 is stored as LSB
  of value of blue plane, 10 is stored as LSB of value of green plane, 00 is stored as LSB of value of red plane. The number of 
  characters that can be stored is constrained by the product of dimensions of image, e.g if we use an image of 2700x1800, we can 
  store 4860000 characters into it.
  
### Tailer
  Each message is associated with a tailer with ascii 1111111 i.e DEL character to mark the end of string in the image.
  
### Decoding
  For decoding, 3 bit LSB from blue plane, 2 bit LSB from green plane and 2 bit LSB from red plane are extracted. These bits are 
  concatenated to from 7 bit value and further get the character corresponding to 7 bit ascii value. Characters are appended to get
  the required message.
  
### Prefered file format
  Prefer a png file format as it stores (b, g, r) values accurately than jpg file format. 
