package main

import (
	"advent-of-code/commons/go/answers"
	"advent-of-code/commons/go/conversions"
	"advent-of-code/commons/go/files"
	"strings"
)

type Packet struct {
	version    int
	packetType int
	value      int
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
	switch packet.packetType {
	case 4:
		return packet.value
	case 0:
		return packet.math(func(acc int, curr int) int { return acc + curr })
	case 1:
		return packet.math(func(acc int, curr int) int { return acc * curr })
	case 2:
		return packet.absolute(func(result int, curr int) bool { return curr < result })
	case 3:
		return packet.absolute(func(result int, curr int) bool { return curr > result })
	case 5:
		return packet.eqaulity(func(v1 int, v2 int) bool { return v1 > v2 })
	case 6:
		return packet.eqaulity(func(v1 int, v2 int) bool { return v1 < v2 })
	case 7:
		return packet.eqaulity(func(v1 int, v2 int) bool { return v1 == v2 })
	default:
		panic("Unknown packet type")
	}
}

func (packet Packet) math(f func(int, int) int) int {
	result := packet.calculateSubPacket(0)
	for i := range packet.subPackets[1:] {
		result = f(result, packet.calculateSubPacket(i+1))
	}
	return result
}

func (packet Packet) absolute(f func(int, int) bool) int {
	result := packet.calculateSubPacket(0)
	for i := range packet.subPackets[1:] {
		value := packet.calculateSubPacket(i + 1)
		if f(result, value) {
			result = value
		}
	}
	return result
}

func (packet Packet) eqaulity(f func(int, int) bool) int {
	if f(packet.calculateSubPacket(0), packet.calculateSubPacket(1)) {
		return 1
	} else {
		return 0
	}
}

func (packet Packet) calculateSubPacket(index int) int {
	return packet.subPackets[index].calculate()
}

func main() {
	packets, _ := parsePackets(getData(), -1)
	packet := packets[0]

	answers.Part1(929, packet.versionSum())
	answers.Part2(911945136934, packet.calculate())
}

func parsePackets(packets string, max int) ([]Packet, int) {
	i := 0
	var result []Packet
	for (max < 0 && i < len(packets)-10) || (max > 0 && len(result) != max) {
		packet := getHeader(packets, i)
		i += 6
		if packet.packetType == 4 {
			value, newIndex := pullType4Number(packets, i)
			packet.value = value
			i = newIndex
		} else if packets[i] == '0' {
			length := conversions.BinaryToDecimal(packets[i+1 : i+16])
			i += 16
			subPackets, _ := parsePackets(packets[i:i+length], -1)
			packet.subPackets = subPackets
			i += length
		} else {
			length := conversions.BinaryToDecimal(packets[i+1 : i+12])
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
		version:    conversions.BinaryToDecimal(packets[i : i+3]),
		packetType: conversions.BinaryToDecimal(packets[i+3 : i+6]),
	}
}

func pullType4Number(packets string, i int) (int, int) {
	var number strings.Builder
	for packets[i] == '1' {
		number.WriteString(packets[i+1 : i+5])
		i += 5
	}
	number.WriteString(packets[i+1 : i+5])
	return conversions.BinaryToDecimal(number.String()), i + 5
}

func getData() string {
	var packets strings.Builder
	for _, hex := range files.Content() {
		hexadecimal := string(hex)
		decimal := conversions.HexToDecimal(hexadecimal)
		binary := conversions.DecimalToBinary(decimal)
		for i := 0; i < 4-len(binary); i++ {
			packets.WriteString("0")
		}
		packets.WriteString(binary)
	}
	return packets.String()
}
