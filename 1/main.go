package main

import (
	"bufio"
	"fmt"
	"os"
	"strconv"
)

func main() {
	f, _ := os.Open("input")
	defer f.Close()

	s := bufio.NewScanner(f)

	var (
		prev       = -1
		increasing = 0
	)

	for s.Scan() {
		n, _ := strconv.Atoi(s.Text())
		if prev != -1 && n > prev {
			increasing++
		}
		prev = n
	}

	fmt.Printf("increasing: %d\n", increasing)
}
