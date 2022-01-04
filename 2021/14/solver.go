package main

import (
	"advent-of-code/commons/go/answers"
	"advent-of-code/commons/go/files"
	"advent-of-code/commons/go/utils"
	"strings"
)

type Rules map[string]string

type Template struct {
	pairs     map[string]int
	firstChar string
}

func (template Template) apply(rules Rules) Template {
	newTemplate := make(map[string]int)
	for pair, count := range template.pairs {
		insert, exists := rules[pair]
		if exists {
			p1 := string(pair[0]) + insert
			newTemplate[p1] += count
			p2 := insert + string(pair[1])
			newTemplate[p2] += count
		} else {
			newTemplate[pair] += count
		}
	}
	return Template{newTemplate, template.firstChar}
}

type Frequencies map[string]int

func (frequencies Frequencies) diff() int {
	most, least := -1, -1
	for _, frequency := range frequencies {
		if most == -1 && least == -1 {
			most, least = frequency, frequency
		} else {
			most = utils.Max(most, frequency)
			least = utils.Min(least, frequency)
		}
	}
	return most - least
}

func (template Template) frequencies() Frequencies {
	result := make(Frequencies)
	result[template.firstChar]++
	for pair, frequency := range template.pairs {
		result[string(pair[1])] += frequency
	}
	return result
}

func main() {
	answers.Part1(2899, diffAfter(10))
	answers.Part2(3528317079545, diffAfter(40))
}

func diffAfter(n int) int {
	template, rules := getData()
	for i := 0; i < n; i++ {
		template = template.apply(rules)
	}
	return template.frequencies().diff()
}

func getData() (Template, Rules) {
	templateRules := files.ReadGroups()

	template := make(map[string]int)
	for i := 0; i < len(templateRules[0])-1; i++ {
		template[templateRules[0][i:i+2]]++
	}
	firstChar := string(templateRules[0][0])

	rules := make(Rules)
	for _, rule := range strings.Split(templateRules[1], "\r\n") {
		parts := strings.Split(rule, " -> ")
		rules[parts[0]] = parts[1]
	}

	return Template{template, firstChar}, rules
}
