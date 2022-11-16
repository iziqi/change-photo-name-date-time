# before: wz=1,bcwyatt.com
# after:  wz,1=bcwyatt.com

f = open('new text.txt','a')
for line in open('old text.txt', 'rb'): 
    line = line.decode("utf-8")
    res = line.split('=', 1)
    input = res[0]
    res = res[1].split(',', 1)
    pos = res[0]
    text = res[1]
    new_text = input + ',' + pos + '=' + text
    print(input, pos, text)
    print(new_text)
    f.write(new_text)
f.close