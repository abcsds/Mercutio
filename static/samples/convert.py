import base64, os

path = './reggae'
f = open('samples.js', 'w')

f.write("var samples = {\n")
for filename in os.listdir(path):
    with open(path+'/'+filename) as fp:
        f.write('"'+filename[:-4]+'" : new Audio("data:audio/wav;base64,'+base64.b64encode(fp.read())+'"),\n')
with open('./key.wav') as fp:
    f.write('"key" : new Audio("data:audio/wav;base64,'+base64.b64encode(fp.read())+'")\n')
f.write("}\n")
f.close()
