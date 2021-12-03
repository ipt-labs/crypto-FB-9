package main

import (
	"io/ioutil"
	"log"
	"math"
	"os"
	"regexp"
	"sort"
	"strconv"
	"strings"
)

var alphabet = []string{"а", "б", "в", "г", "д", "е", "ж", "з", "a", "и", "й", "к", "л", "м", "н", "о", "п", "р", "с", "т", "у", "ф", "х", "ц", "ч", "ш", "щ", "ы", "ь", "э", "ю", "я"}
var textLen int
var alphabetEntropy float64

func check(err error) {
	if err != nil {
		log.Fatal(err)
	}
}

func openReportFile() (f *os.File) {
	f, err := os.OpenFile("../docs/report.txt", os.O_RDWR|os.O_CREATE, 0666)
	check(err)
	return f
}

func writeMapToFile(text string, dict map[string]float64, f *os.File){

	_, err := f.WriteString(text)
	check(err)
	for key, val := range dict{
		_, err = f.WriteString(key + ": " + strconv.FormatFloat(val, 'f', 6, 64) + "\n")
	}
}

func writeArrayToFile(text string, arr[]string, f *os.File){

	_, err := f.WriteString(text)
	check(err)
	for i:=0; i < len(arr); i++{
		_, err = f.WriteString(arr[i] + "\n")
	}
}

func replaceLetters() (string, string) {
	textFile, err := ioutil.ReadFile("../docs/text.txt")
	check(err)

	clearText := string(textFile)

	regexp.MustCompile("\n").ReplaceAllString(clearText, ``)
	regexp.MustCompile(`ё`).ReplaceAllString(clearText, `е`)
	regexp.MustCompile(`ъ`).ReplaceAllString(clearText, `ь`)

	noSpace := regexp.MustCompile(` `).ReplaceAllString(clearText, ``)

	textLen = len(noSpace)

	return clearText, noSpace
}

//struct for sorting letters frequency

type Pair struct {
	Key   string
	Value float64
}

type PairList []Pair

func (p PairList) Len() int           { return len(p) }
func (p PairList) Swap(i, j int)      { p[i], p[j] = p[j], p[i] }
func (p PairList) Less(i, j int) bool { return p[i].Value < p[j].Value }

//counting letters count and frequency
func lettersCountFreq(text string) (map[string]float64, []string) {

	alphabetEntropy = 0

	lettersCount := map[string]float64{}
	lettersFreq := map[string]float64{}
	textArray := strings.Split(text, "")

	for i, _ := range textArray {
		for j, _ := range alphabet {
			if alphabet[j] == strings.ToLower(textArray[i]) {
				lettersCount[strings.ToLower(textArray[i])]++
			}
		}
	}

	var lettersInText float64

	for _, val := range lettersCount {
		lettersInText += val
	}

	for key, val := range lettersCount {
		lettersFreq[key] = val / lettersInText
	}

	for _, val := range lettersFreq {
		alphabetEntropy += -val * math.Log2(val)
	}

	p := make(PairList, len(lettersFreq))
	sortedLettersFreq := make([]string, len(lettersFreq))

	i := 0
	for k, v := range lettersFreq {
		p[i] = Pair{k, v}
		i++
	}
	sort.Sort(sort.Reverse(p))

	for _, k := range p {
		stringToArray := k.Key + ": " + strconv.FormatFloat(k.Value, 'f', 6, 64)
		sortedLettersFreq = append(sortedLettersFreq, stringToArray)
	}

	return lettersCount, sortedLettersFreq
}

func bgrammsCount(text string) (map[string]float64, map[string]float64) {

	crossedBgrammCount := map[string]float64{}
	unCrossedBgrammCount := map[string]float64{}
	textArray := strings.Split(text, "")

	if len(textArray)%2 != 0 {
		textArray = append(textArray, "ю")
	}

	for i := 0; i < len(textArray)-1; i++ {
		crossedBgrammCount[strings.ToLower(textArray[i])+strings.ToLower(textArray[i+1])]++
	}

	for i := 0; i < len(textArray)-1; i += 2 {
		unCrossedBgrammCount[strings.ToLower(textArray[i])+strings.ToLower(textArray[i+1])]++
	}

	return crossedBgrammCount, unCrossedBgrammCount
}

func bgrammsFreq(cross map[string]float64, unCross map[string]float64) (map[string]float64, map[string]float64) {

	crossFreq := map[string]float64{}
	unCrossFreq := map[string]float64{}

	var lenCross float64 = 0
	var lenUnCross float64 = 0

	for _, val := range cross{
		lenCross += val
	}

	for _, val := range unCross{
		lenUnCross += val
	}

	for key, val := range cross {
		crossFreq[key] = val / lenCross
	}

	for key, val := range unCross {
		//unCrossFreq[key] = val / 2
		unCrossFreq[key] = val / lenUnCross
	}

	return crossFreq, unCrossFreq
}

func entropy(freq map[string]float64) float64 {

	var entropy float64 = 0
	for _, val := range freq {
		entropy += -val * math.Log2(val)
	}
	return entropy
}

func main() {

	reportF := openReportFile()
	truncErr := reportF.Truncate(0)
	check(truncErr)

	textSpaces, textNoSpaces := replaceLetters()
	lettersCountSpace, lettersFreqSpace := lettersCountFreq(textSpaces)
	_, err := reportF.WriteString("Letters with spaces entropy: " + strconv.FormatFloat(alphabetEntropy, 'f', 6, 64) + "\n")
	check(err)

	lettersCountNoSpace, lettersFreqNoSpace := lettersCountFreq(textNoSpaces)
	_, err = reportF.WriteString("Letters without spaces entropy: " + strconv.FormatFloat(alphabetEntropy, 'f', 6, 64) + "\n")
	check(err)

	_, err = reportF.WriteString("\n")
	check(err)

	writeMapToFile("Letters with spaces count: \n", lettersCountSpace, reportF)
	_, err = reportF.WriteString("\n")
	check(err)

	writeMapToFile("Letters without spaces count: \n", lettersCountNoSpace, reportF)
	_, err = reportF.WriteString("\n")
	check(err)

	writeArrayToFile("Letters frequency with spaces: \n", lettersFreqSpace, reportF)
	_, err = reportF.WriteString("\n")
	check(err)

	writeArrayToFile("Letters frequency without spaces: \n", lettersFreqNoSpace, reportF)
	_, err = reportF.WriteString("\n")
	check(err)

	crossedBgramssSpaces, unCrossedBgramssSpaces := bgrammsCount(textSpaces)
	crossedBgramssNoSpaces, unCrossedBgramssNoSpaces := bgrammsCount(textNoSpaces)

	crossFreqSpace, uncrossFreqSpaces := bgrammsFreq(crossedBgramssSpaces, unCrossedBgramssSpaces)
	crossFreqNoSpace, uncrossFreqNoSpaces := bgrammsFreq(crossedBgramssNoSpaces, unCrossedBgramssNoSpaces)

	_, err = reportF.WriteString("Entropy for crossed bgramms with spaces: " + strconv.FormatFloat(entropy(crossFreqSpace) / 2, 'f', 6, 64))
	check(err)
	_, err = reportF.WriteString("\n")
	check(err)

	_, err = reportF.WriteString("Entropy for uncrossed bgramms with spaces: " + strconv.FormatFloat(entropy(uncrossFreqSpaces) / 2, 'f', 6, 64))
	check(err)
	_, err = reportF.WriteString("\n")
	check(err)

	_, err = reportF.WriteString("Entropy for crossed bgramms without spaces: " + strconv.FormatFloat(entropy(crossFreqNoSpace) / 2, 'f', 6, 64))
	check(err)
	_, err = reportF.WriteString("\n")
	check(err)

	_, err = reportF.WriteString("Entropy for uncrossed bgramms without spaces: " + strconv.FormatFloat(entropy(uncrossFreqNoSpaces) / 2, 'f', 6, 64))
	check(err)
	_, err = reportF.WriteString("\n")
	check(err)

	_, err = reportF.WriteString("\n")
	check(err)

	writeMapToFile("Crossed bgramms with spaces count: \n", crossedBgramssSpaces, reportF)
	_, err = reportF.WriteString("\n")
	check(err)

	writeMapToFile("Uncrossed bgramms with spaces count: \n", unCrossedBgramssSpaces, reportF)
	_, err = reportF.WriteString("\n")
	check(err)

	writeMapToFile("Crossed bgramms without spaces count: \n", crossedBgramssNoSpaces, reportF)
	_, err = reportF.WriteString("\n")
	check(err)

	writeMapToFile("Uncrossed bgramms without spaces count: \n", unCrossedBgramssNoSpaces, reportF)
	_, err = reportF.WriteString("\n")
	check(err)

	writeMapToFile("Crossed bgramms frequency with spaces count: \n", crossFreqSpace, reportF)
	_, err = reportF.WriteString("\n")
	check(err)

	writeMapToFile("Uncrossed bgramms frequency with spaces count: \n", uncrossFreqSpaces, reportF)
	_, err = reportF.WriteString("\n")
	check(err)

	writeMapToFile("Crossed bgramms frequency without spaces count: \n", crossFreqNoSpace, reportF)
	_, err = reportF.WriteString("\n")
	check(err)

	writeMapToFile("Uncrossed bgramms frequency without spaces count: \n", uncrossFreqNoSpaces, reportF)
	_, err = reportF.WriteString("\n")
	check(err)

	defer func(reportF *os.File) {
		err := reportF.Close()
		check(err)
	}(reportF)
}
