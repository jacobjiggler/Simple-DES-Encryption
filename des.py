import sys
#simple DES
#8-bit blocks and uses 10-bit key
# Only 2 rounds
#todo
#finish encryption
#start decryption


#example command
#python des.py enc input output 1010000010


def xor(str1,str2):
    answer = ''
    for x in range(0, len(str1)):
        a = int(str1[x])
        b = int(str2[x])
        if (a + b == 1):
            answer = answer + '1'
        else:
            answer = answer + '0'
    return answer

def int2bin(val):
    return {
        0: '00',
        1: '01',
        2: '10',
        3: '11'
    }[val]

def main():
    encrypt = False
    if (str(sys.argv[1]) == "enc"):
        encrypt = True
    input_path = str(sys.argv[2])
    with open (input_path, "r") as myfile:
        inputStr = myfile.read().replace('\n', '')
    output_path = str(sys.argv[3])
    text_file = open(output_path, "w")
    key_bin = str(sys.argv[4])
    p10 = key_bin[2] + key_bin[4] + key_bin[1] + key_bin[6] + key_bin[3] + key_bin[9] + key_bin[0] + key_bin[8] + key_bin[7] + key_bin[5]
    #key1
    pA1 = p10[1:5]
    pA1 = pA1 + p10[0]
    pB1 = p10[6:10]
    pB1 = pB1 + p10[5]
    #print pA1
    #print pB1
    p8_1 = pB1[0] + pA1[2] + pB1[1] + pA1[3] + pB1[2] + pA1[4] + pB1[4] + pB1[3]
    print 'key1 ' + p8_1

    #key2
    pA2 = pA1[2:5]
    pA2 = pA2 + pA1[0] + pA1[1]
    pB2 = pB1[2:5]
    pB2 = pB2 + pB1[0] + pB1[1]
    #print pA2
    #print pB2
    p8_2 = pB2[0] + pA2[2] + pB2[1] + pA2[3] + pB2[2] + pA2[4] + pB2[4] + pB2[3]
    print 'key2 ' + p8_2

    #for each char
    if (len(inputStr) % 8 != 0) :
        print 'error'
    if encrypt :

        print 'plaintext input ' + inputStr

        for x in range(0, len(inputStr)/8):
            inputBin = inputStr[(x * 8):(x*8 + 8)]
            #L
            IPA1 = inputBin[1] + inputBin[5] + inputBin[2] + inputBin[0]
            #R
            IPB1 = inputBin[3] + inputBin[7] + inputBin[4] + inputBin[6]
            #expand IPB1
            IPB1E = IPB1[3] + IPB1[0] + IPB1[1] + IPB1[2] + IPB1[1] + IPB1[2] + IPB1[3] + IPB1[0]
            #xor key1 and IPB1E
            IPB1XOR = xor(IPB1E,p8_1)
            #split into 2 for Sbox
            IPB1Left = IPB1XOR[0:4]
            IPB1Right = IPB1XOR[4:8]
            #get row collumn from input
            row1 = int(IPB1Left[0] + IPB1Left[3],2)
            collumn1 = int(IPB1Left[1] + IPB1Left[2],2)

            #substitution box
            s0 = [[0 for x in range(4)] for x in range(4)]
            s0[0] = [1, 0, 3, 2]
            s0[1] = [3, 2, 1, 0]
            s0[2] = [0, 2, 1, 3]
            s0[3] = [3, 1, 3, 2]
            s0Output = int2bin(s0[row1][collumn1])

            row2 = int(IPB1Right[0] + IPB1Right[3],2)
            collumn2 = int(IPB1Right[1] + IPB1Right[2],2)
            s1 = [[0 for x in range(4)] for x in range(4)]
            s1[0] = [0, 1, 2, 3]
            s1[1] = [2, 0, 1, 3]
            s1[2] = [3, 0, 1, 0]
            s1[3] = [2, 1, 0, 3]
            s1Output = int2bin(s1[row2][collumn2])

            #Sbox permutation
            sBox = s0Output[1] + s1Output[1] + s1Output[0] + s0Output[0]
            #xor IPA1
            IPA1XOR = xor(sBox,IPA1)




            #switch out
            #L
            IPA2 = IPB1
            #R
            IPB2 = IPA1XOR
            #expand IPB2 into IPB2E
            IPB2E = IPB2[3] + IPB2[0] + IPB2[1] + IPB2[2] + IPB2[1] + IPB2[2] + IPB2[3] + IPB2[0]
            #xor key2 and IPB2E
            IPB2XOR = xor(IPB2E,p8_2)

            #split into 2 for Sbox
            IPB2Left = IPB2XOR[0:4]
            IPB2Right = IPB2XOR[4:8]
            #get row collumn from input
            row1 = int(IPB2Left[0] + IPB2Left[3],2)
            collumn1 = int(IPB2Left[1] + IPB2Left[2],2)
            row2 = int(IPB2Right[0] + IPB2Right[3],2)
            collumn2 = int(IPB2Right[1] + IPB2Right[2],2)

            #substitution box
            s0Output = int2bin(s0[row1][collumn1])
            s1Output = int2bin(s1[row2][collumn2])

            #Sbox permutation
            sBox = s0Output[1] + s1Output[1] + s1Output[0] + s0Output[0]

            #xor IPA2
            IPA2XOR = xor(sBox,IPA2)
            #Combine
            combin = IPA2XOR + IPB2
            #IPINVERSE
            inverse = combin[3] + combin[0] + combin[2] + combin[4] + combin[6] + combin[1] + combin[7] + combin[5]
            print 'ciphertext output' + inverse
            #save to output file
            text_file.write(inverse)

    else :
        #Decryption
        print 'encrypted input ' + inputStr
        #same as permutation but round keys used in opposite order
        for x in range(0, len(inputStr)/8):
            inputBin = inputStr[(x * 8):(x*8 + 8)]
            #L
            IPA1 = inputBin[1] + inputBin[5] + inputBin[2] + inputBin[0]
            #R
            IPB1 = inputBin[3] + inputBin[7] + inputBin[4] + inputBin[6]
            #expand IPB1
            IPB1E = IPB1[3] + IPB1[0] + IPB1[1] + IPB1[2] + IPB1[1] + IPB1[2] + IPB1[3] + IPB1[0]
            #xor key1 and IPB1E
            IPB1XOR = xor(IPB1E,p8_2)
            #split into 2 for Sbox
            IPB1Left = IPB1XOR[0:4]
            IPB1Right = IPB1XOR[4:8]
            #get row collumn from input
            row1 = int(IPB1Left[0] + IPB1Left[3],2)
            collumn1 = int(IPB1Left[1] + IPB1Left[2],2)

            #substitution box
            s0 = [[0 for x in range(4)] for x in range(4)]
            s0[0] = [1, 0, 3, 2]
            s0[1] = [3, 2, 1, 0]
            s0[2] = [0, 2, 1, 3]
            s0[3] = [3, 1, 3, 2]
            s0Output = int2bin(s0[row1][collumn1])

            row2 = int(IPB1Right[0] + IPB1Right[3],2)
            collumn2 = int(IPB1Right[1] + IPB1Right[2],2)
            s1 = [[0 for x in range(4)] for x in range(4)]
            s1[0] = [0, 1, 2, 3]
            s1[1] = [2, 0, 1, 3]
            s1[2] = [3, 0, 1, 0]
            s1[3] = [2, 1, 0, 3]
            s1Output = int2bin(s1[row2][collumn2])

            #Sbox permutation
            sBox = s0Output[1] + s1Output[1] + s1Output[0] + s0Output[0]
            #xor IPA1
            IPA1XOR = xor(sBox,IPA1)




            #switch out
            #L
            IPA2 = IPB1
            #R
            IPB2 = IPA1XOR
            #expand IPB2 into IPB2E
            IPB2E = IPB2[3] + IPB2[0] + IPB2[1] + IPB2[2] + IPB2[1] + IPB2[2] + IPB2[3] + IPB2[0]
            #xor key2 and IPB2E
            IPB2XOR = xor(IPB2E,p8_1)

            #split into 2 for Sbox
            IPB2Left = IPB2XOR[0:4]
            IPB2Right = IPB2XOR[4:8]
            #get row collumn from input
            row1 = int(IPB2Left[0] + IPB2Left[3],2)
            collumn1 = int(IPB2Left[1] + IPB2Left[2],2)
            row2 = int(IPB2Right[0] + IPB2Right[3],2)
            collumn2 = int(IPB2Right[1] + IPB2Right[2],2)

            #substitution box
            s0Output = int2bin(s0[row1][collumn1])
            s1Output = int2bin(s1[row2][collumn2])

            #Sbox permutation
            sBox = s0Output[1] + s1Output[1] + s1Output[0] + s0Output[0]

            #xor IPA2
            IPA2XOR = xor(sBox,IPA2)
            #Combine
            combin = IPA2XOR + IPB2
            #IPINVERSE
            inverse = combin[3] + combin[0] + combin[2] + combin[4] + combin[6] + combin[1] + combin[7] + combin[5]
            print 'plaintext output' + inverse
            #save to output file
            text_file.write(inverse)

    text_file.close()

if __name__ == "__main__":
    main()
