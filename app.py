import time, os, sys, math, datetime, urllib, json
from PIL import Image
from flask import Flask
from flask import stream_with_context, request, Response

speed = 100
Char32 = bytearray([0,0,0,0,0,0,0,0])

def LoadFont():
	font = Image.open("font.png").load()
	index = 33
	skip = 0
	for i in range(0, 6):
		for j in range(0, 16):
			variableName = "Char" + str(index)
			
			index+=1
			if skip == 0 and index == 96:
				index -= 1
				skip = 1
			globals()[variableName] = bytearray([0,0,0,0,0,0,0,0])
			# read the sub image here
			for ii in range(0, 8):
				ix = i*8+ii
				for jj in range(0, 8):
					jx = j*8+jj
					if font[jx, ix][1] > 200 :
						globals()[variableName][ii] += int(math.pow(2, 7 - jj))

def GetChar(ch):
	varName = 'Char' + str(ord(ch));
	if varName in globals():
		return globals()[varName]
	else:
		return Char32

def ShowString(message):
	message = ' ' + message + ' '
	CharNew = bytearray([0,0,0,0,0,0,0,0])
	for i in range(0, len(message) - 1):
		currentChar = message[i]
		nextChar = message[i+1]
		for j in range(0, 8):
			CharCurrent = GetChar(currentChar)
			CharNext = GetChar(nextChar)
			for k in range(0, 8):
				cByte = CharCurrent[k]
				cByte = cByte << j
				nByte = CharNext[k]
				nByte = nByte >> 8 - j
				CharNew[k] = (cByte & 255) | nByte
			yield str(speed) + " "
			for c in CharNew:
				yield str(c) + " "

def ShowRandom(lenght):
	for i in range(0, lenght):
		rndVar = bytearray(os.urandom(8))
		yield "10 "
		for c in rndVar:
			yield str(c) + " "

def RenderChar(CharNew):
	result = ""
	for c in CharNew:
		result += str(c) + " "
	return result

def Love(lenght):
	for i in range(0, lenght):
		yield str(777) + " "
		yield RenderChar(Char32)

		yield str(777) + " "
		yield RenderChar(bytearray([0,0,0,0,24,24,0,0]))

		yield str(777) + " "
		yield RenderChar(bytearray([0,0,0,60,60,60,60,0]))

		yield str(777) + " "
		yield RenderChar(bytearray([0,0,102,255,255,126,60,24]))

		yield str(777) + " "
		yield RenderChar(bytearray([0,102,255,255,126,60,24,0]))

		yield str(777) + " "
		yield RenderChar(bytearray([102,255,255,126,60,24,0,0]))

		yield str(777) + " "
		yield RenderChar(bytearray([0,102,255,255,126,60,24,0]))

		yield str(777) + " "
		yield RenderChar(bytearray([0,0,102,255,255,126,60,24]))

		yield str(777) + " "
		yield RenderChar(bytearray([0,0,0,60,60,60,60,0]))

		yield str(777) + " "
		yield RenderChar(bytearray([0,0,0,0,24,24,0,0]))

app = Flask(__name__)
LoadFont()

@app.route("/list.json")
def list():
	return "{\"urls\":[\"/file0.bin\",\"/file1.bin\",\"/file2.bin\",\"/file3.bin\"]}"

@app.route("/file0.bin")
def file0():
	return Response(stream_with_context(ShowRandom(200)))

@app.route("/file1.bin")
def file1():
	return Response(stream_with_context(ShowString("Happy Holidays!")))

@app.route("/file2.bin")
def file2():
	return Response(stream_with_context(ShowRandom(200)))

@app.route("/file3.bin")
def file3():
	return Response(stream_with_context(ShowString(time.strftime("%d/%m/%Y - %I:%M:%S"))))

if __name__ == "__main__":
	app.run(debug=1,host='0.0.0.0')