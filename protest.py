obj = [
{
"p":2,
"q":5
},
{
"p":3,
"q":4
},
{
"p":2,
"q":10
},
{
"p":1,
"q":2
}
]
pro =[]
qty =[]
for o in obj:
    if o['p'] in pro:
        qty[pro.index(o['p'])]+=o['q']
    else:
        pro.append(o['p'])
        qty.append(o['q'])

print(pro)
print(qty)


