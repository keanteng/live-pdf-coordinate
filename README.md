# Live PDF Coordinate Viewer


![Static Badge](https://img.shields.io/badge/license-MIT-blue)
![Static Badge](https://img.shields.io/badge/python-3.11-blue)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

An application for you to check the live coordinate of your cursor as you click around in a PDF document. This application is especially useful when you need to know the coordinate in order to put in text or images inside a PDF document. For example, you want to put text to fill up your personal information inside a PDF form, you want to put a logo in a specific position of a PDF document.

![Alt Text](demo.gif)

## Usage Tips
The application can be helpful for tools such as [PDF-Lib](https://pdf-lib.js.org/) a javascript program to create and modify PDF document. You can use it to get the coordinate that you want to put a text or image component.

You can use a package manager such as `npm` to install the program for web development:

```js
npm i --save pdf-lib
```

## Getting Started

Install the required packages:

```py
py -m pip install -r requirements.txt
```

To run the program, you will then be prompted to input the path of the PDF file:

```py
py pdf_coordinate.py
```

## Concepts

First of all, we will render a PDF document in a display window. As we move our cursor, information such as the cursor coordinate can then be mapped to the PDF coordinate. With this information, we can then convert this coordinate to a PDF coordinate. 

The crucial part is the conversion of canvas coordinates to PDF coordinates. For a canvas coordinate system the origin is at the top-left corner of the canvas. In contrast, the PDF coordinate system has the origin at the bottom-left corner of the PDF page. We can use this formula to convert between the two:

```py
pdf_x = (canvas_x / canvas_width) * page_width
pdf_y = (canvas_height - canvas_y) / canvas_height * page_height
```

## Explantion

Let $C$ be canvas and $P$ be PDF. We will denote height as $h$ and width as $w$. The $x$ and $y$ will represent a coordinate, $(x,y)$ in a cartesian plane for both the canvas and PDF system.

### X-Coordinate Mapping

$C_x / C_w$ normalizes x-coordinate relative to canvas where it converts the canvas x-coordinate into a value between 0 and 1 (fractional position along the canvas width)

$(C_x / C_w)*{page}_w$ scales the normalized x-coordinate to the actual width of the PDF page. 

### Y-Coordinate Mapping
$C_h - C_y$ adjusts for the difference in the origin between the two systems. 

$(C_h - C_y)/C_h$ normalizes the y-coordinate relative to the canvas and convert it into a fractional position along the canvas height. 

Finally, $(C_h - C_y)/C_h * {page}_h$ scales the normalized y-coordinate to the actual height of the PDF
