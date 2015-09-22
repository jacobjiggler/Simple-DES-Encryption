import sys

#8-bit blocks and uses 10-bit key
# Only 2 rounds

#Plaintext: 02468aceeca86420
#Key: 0f1571c947d9e859
#Ciphertext: da02ce3a89ecac3b

# to ascii ->  chr(int('01110111', 2))



encrypt = False
if (str(sys.argv[1]) == "enc"):
    encrypt = True
input_path = str(sys.argv[2])
with open (input_path, "r") as myfile:
    inputStr = myfile.read().replace('\n', '')
output_path = str(sys.argv[3])
with open (input_path, "r") as myfile:
    outputStr = myfile.read().replace('\n', '')
key_bin = str(sys.argv[4])
outputStr = 'a'
if encrypt :

    print 'plaintext input ' + [ bin(ord(ch))[2:].zfill(8) for ch in inputStr ][0]
    p10 = key_bin[2] + key_bin[4] + key_bin[1] + key_bin[6] + key_bin[3] + key_bin[9] + key_bin[0] + key_bin[8] + key_bin[7] + key_bin[5]
    #key1
    pA1 = p10[1:5]
    pA1 = pA1 + p10[0]
    pB1 = p10[6:10]
    pB1 = pB1 + p10[5]
    print pA1
    print pB1
    p8_1 = pB1[0] + pA1[2] + pB1[1] + pA1[3] + pB1[2] + pA1[4] + pB1[4] + pB1[3]
    print p8_1

    #key2
    pA2 = pA1[1:5]
    pA2 = pA2 + pA1[0]
    pB2 = pB1[1:5]
    pB2 = pB2 + pB1[0]
    print pA2
    print pB2
    p8_2 = pB2[0] + pA2[2] + pB2[1] + pA2[3] + pB2[2] + pA2[4] + pB2[4] + pB2[3]
    print p8_2

    for x in range(0, len(inputStr)):
        inputBin = [ bin(ord(ch))[2:].zfill(8) for ch in inputStr ][x]
        IPA1 = inputBin[1] + inputBin[5] + inputBin[2] + inputBin[0]
        IPB1 = inputBin[3] + inputBin[7] + inputBin[4] + inputBin[6]
        #expand IPB1
        IPB1E = IPB1[3] + IPB1[0] + IPB1[1] + IPB1[2] + IPB1[1] + IPB1[2] + IPB1[3] + IPB1[0]

        #IPINVERSE =

#round keys generated using permutations and left shifts
#encryption
    #initial permutation -> round function -> switch halves
    #ciphertext = IP-1 (fK2(SW (fK1(IP(plaintext)))))
#    where
#    K1 = P8(Shift(P10(key)))
#   K2 = P8(Shift(Shift(P10(key))))


#int key =
    print 'encrypted output ' + [ bin(ord(ch))[2:].zfill(8) for ch in outputStr ][0]

else :
    print 'encrypted input ' + [ bin(ord(ch))[2:].zfill(8) for ch in inputStr ][0]
#Decryption
    #same as permutation but round keys used in opposite order
    print 'plaintext output ' + [ bin(ord(ch))[2:].zfill(8) for ch in outputStr ][0]
