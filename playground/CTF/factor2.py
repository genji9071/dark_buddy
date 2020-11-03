cipher = "oWdnreuf.lY uoc nar ae dht eemssga eaw yebttrew eh nht eelttre sra enic roertco drre . Ihtni koy uowlu dilekt  oes eoyrup sawsro don:wc arggnslsma.a"
answer = ""
i = 0
for char in cipher:
    if i == 1:
        answer = answer + char + temp
        i = 0
    else:
        i += 1
        temp = char
print(answer)