package main

import (
	"fmt"
	"bufio"
	"os"
)

var hadError = false

func main() {
	args := os.Args[1:]
	if len(args) > 1 {
		fmt.Println("Usage: golox [script]")
		os.Exit(64)
	} else if len(args) == 1 {
		runFile(args[0])
	} else {
		runPrompt()
	}
}

func runFile(path string) {
	contents, err := os.ReadFile(path)
	if err != nil {
		fmt.Println("Error reading file:", err)
		os.Exit(74)
	}
	run(string(contents))
	if hadError {
		os.Exit(65)
	}
}

func runPrompt() {
	reader := bufio.NewReader(os.Stdin)
	for {
		fmt.Print("> ")
		text, _ := reader.ReadString('\n')
		if text == "exit\n" {
			os.Exit(0)
		}
		run(text)
		hadError = false
	}
}

func run(source string) {
	scanner := Scanner{source: source, tokens: []Token{}, start: 0, current: 0, line: 1}
	scanner.scanTokens()
	
	for _, token := range scanner.tokens {
		fmt.Println(token)
	}
}

func error(line int, message string) {
	report(line, "", message)
}

func report(line int, where string, message string) {
	fmt.Printf("[line %d] Error %s: %s\n", line, where, message)
	hadError = true
}