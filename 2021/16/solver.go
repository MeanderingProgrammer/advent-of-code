package main

import (
	"fmt"
	"io/ioutil"
	"strconv"
    "strings"
)

type Packet struct {
    version int
    packetType int
    value int
    subPackets []Packet
}

func (packet Packet) versionSum() int {
    result := packet.version
    for _, subPacket := range packet.subPackets {
        result += subPacket.versionSum()
    }
    return result
}

func (packet Packet) calculate() int {
    if packet.packetType == 4 {
        return packet.value
    } else if packet.packetType == 0 {
        return packet.math(func(acc int, curr int)int {return acc + curr})
    } else if packet.packetType == 1 {
        return packet.math(func(acc int, curr int)int {return acc * curr})
    } else if packet.packetType == 2 {
        return packet.absolute(func(result int, curr int)bool {return curr < result})
    } else if packet.packetType == 3 {
        return packet.absolute(func(result int, curr int)bool {return curr > result})
    } else if packet.packetType == 5 {
        return packet.eqaulity(func(v1 int, v2 int)bool {return v1 > v2})
    } else if packet.packetType == 6 {
        return packet.eqaulity(func(v1 int, v2 int)bool {return v1 < v2})
    } else if packet.packetType == 7 {
        return packet.eqaulity(func(v1 int, v2 int)bool {return v1 == v2})
    } else {
        return 0
    }
}

func (packet Packet) math(f func(int, int)int) int {
    result := packet.subPackets[0].calculate()
    for _, subPacket := range packet.subPackets[1:] {
        result = f(result, subPacket.calculate())
    }
    return result
}

func (packet Packet) absolute(f func(int, int)bool) int {
    result := packet.subPackets[0].calculate()
    for _, subPacket := range packet.subPackets[1:] {
        subPacketValue := subPacket.calculate()
        if f(result, subPacketValue) {
            result = subPacketValue
        }
    }
    return result
}

func (packet Packet) eqaulity(f func(int, int)bool) int {
    if f(packet.subPackets[0].calculate(), packet.subPackets[1].calculate()) {
        return 1
    } else {
        return 0
    }
}

func main() {
    packets, _ := parsePackets(getData(), -1)
    packet := packets[0]

    // Part 1: 929
    fmt.Printf("Part 1: %d \n", packet.versionSum())
    // Part 2: 911945136934
    fmt.Printf("Part 2: %d \n", packet.calculate())
}

func parsePackets(packets string, max int) ([]Packet, int) {
    i := 0
    var result []Packet
    for (max < 0 && i < len(packets) - 10) || (max > 0 && len(result) != max) {
        packet := getHeader(packets, i)
        i += 6
        if packet.packetType == 4 {
            value, newIndex := pullType4Number(packets, i)
            packet.value = value
            i = newIndex
        } else if packets[i] == '0' {
            length := binaryToDecimal(packets[i+1:i+16])
            i += 16
            subPackets, _ := parsePackets(packets[i:i+length], -1)
            packet.subPackets = subPackets
            i += length
        } else {
            length := binaryToDecimal(packets[i+1:i+12])
            i += 12
            subPackets, bitsParsed := parsePackets(packets[i:], length)
            packet.subPackets = subPackets
            i += bitsParsed
        }
        result = append(result, packet)
    }
    return result, i
}

func getHeader(packets string, i int) Packet {
    return Packet{
        version: binaryToDecimal(packets[i:i+3]), 
        packetType: binaryToDecimal(packets[i+3:i+6]),
    }
}

func pullType4Number(packets string, i int) (int, int) {
    var number strings.Builder
    for packets[i] == '1' {
        number.WriteString(packets[i+1:i+5])
        i += 5
    }
    number.WriteString(packets[i+1:i+5])
    return binaryToDecimal(number.String()), i+5
}

func getData() string {
    data, _ := ioutil.ReadFile("data.txt")
    var packets strings.Builder
    for _, hex := range string(data) {
        hexadecimal := string(hex)
        decimal := hexToDecimal(string(hexadecimal))
        binary := decimalToBinary(decimal)
        for i := 0; i < 4 - len(binary); i++ {
            packets.WriteString("0")
        }
        packets.WriteString(binary)
    }
    return packets.String()
}

func hexToDecimal(hexadecimal string) int {
    result, _ := strconv.ParseInt(hexadecimal, 16, 64)
    return int(result)
}

func decimalToBinary(decimal int) string {
    return strconv.FormatInt(int64(decimal), 2)
}

func binaryToDecimal(binary string) int {
    result, _ := strconv.ParseInt(binary, 2, 64)
    return int(result)
}
